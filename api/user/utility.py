from flask import url_for, g
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from api import mail, conf_obj, db
from api.user.model import User


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(conf_obj.SECRET_KEY)
    return serializer.dumps(email, salt=conf_obj.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(conf_obj.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=conf_obj.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return ''
    return email


def generate_url(endpoint, token):
    return url_for(endpoint, token=token, _external=True)


def send_mail(to, subject, template):
    message = Message(
        subject=subject,
        recipients=[to],
        html=template
    )

    mail.send(message)

    user = User.query.filter_by(email=to).first()
    user.email_sent = True
    db.session.commit()

    return True
