from datetime import datetime
import redis
from rq import Queue
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from rq import Worker, Connection
from config import DevConfig

conf_obj = DevConfig()

mail = Mail()
db = SQLAlchemy()

redis_conn = redis.from_url(conf_obj.REDIS_URI)
redis_queue = Queue(connection=redis_conn)


def create_app():
    app = Flask(__name__,
                template_folder='/home/jason/Projects/PycharmProjects/flask-blog/templates',
                static_folder='/home/jason/Projects/PycharmProjects/flask-blog/static')

    app.config.from_object(conf_obj)

    from api.routes import user_route, blog_route
    app.register_blueprint(user_route.user_blueprint)
    app.register_blueprint(blog_route.blog_blueprint)

    from api import errors
    app.register_error_handler(400, errors.handle_bad_request)
    app.register_error_handler(404, errors.handle_page_not_found)
    app.register_error_handler(500, errors.handle_internal_server_error)

    mail.init_app(app)
    db.init_app(app)

    Migrate(app, db)
    CORS(app)
    JWTManager(app)

    @app.cli.command(name='create_superuser')
    @with_appcontext
    def create_superuser():
        from api.user.model import User
        superuser = User(
            email='example@outlook.com',
            password='2C80fa42',
            admin=True,
            confirmed=True,
            confirmed_on=datetime.now(),
            email_sent=True
        )
        superuser.password = generate_password_hash(superuser.password)
        db.session.add(superuser)
        db.session.commit()

    app.cli.add_command(create_superuser)

    @app.cli.command(name='run_rq_worker')
    @with_appcontext
    def run_rq_worker():
        with Connection(redis_conn):
            worker = Worker(queues=app.config['QUEUES'])
            worker.work()

    app.cli.add_command(run_rq_worker)

    return app
