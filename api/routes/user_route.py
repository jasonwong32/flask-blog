from datetime import datetime
from flask import Blueprint, request, jsonify, abort, render_template
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from api.user import utility
from api.user.model import User
from api import db, redis_queue

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/api/v1/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        abort(400)
    if not data['email']:
        return jsonify({'message': 'empty email is not allowed'}), 400
    if not data['password']:
        return jsonify({'message': 'empty password is not allowed'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'email address has been used'}), 400
    user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        confirmed=False,
        registered_on=datetime.now()
    )

    if data['firstName']:
        user.first_name = data['firstName']
    if data['lastName']:
        user.last_name = data['lastName']
    if data['birthDate']:
        user.birthdate = datetime.strptime(data['birthDate'], 'yyyy/mm/dd')

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'status': 'failed',
                        'message': 'That email already exists, please use another one.'}), 400

    token = utility.generate_confirmation_token(user.email)
    confirm_url = utility.generate_url('user.confirm_email', token)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = 'Please confirm your email'
    # utility.send_mail(data['email'], subject, html)
    redis_queue.enqueue(utility.send_mail, data['email'], subject, html)

    return {'message': 'email sent'}, 200


@user_blueprint.route('/api/v1/user/signup/confirm/<token>')
def confirm_email(token):
    email = None
    try:
        email = utility.confirm_token(token)
    except:
        return jsonify({'status': 'danger',
                        'message': 'The confirmation link is invalid or has expired.'}), 400
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify({'status': 'success',
                        'message': 'Account already confirmed. Please login'}), 200
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()

    return jsonify({'status': 'confirmed',
                    'message': 'You have confirmed your account. Thanks!'}), 200


@user_blueprint.route('/api/v1/user/login', methods=['POST'])
def user_login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Invalid user'}), 400
    if not user.confirmed:
        return jsonify({'message': 'Your email has not been confirmed',
                        'status': 'denied'}), 401
    if check_password_hash(user.password, data['password']):
        jwt_token = create_access_token(identity=user.email)
        return jsonify({'access_token': jwt_token})
    else:
        return jsonify({'message': 'Invalid email or password'}), 400


@user_blueprint.route('/api/v1/user/logout')
def user_logout():
    logout_user()
    return jsonify({
        'status': 'success',
        'message': 'You were logged out.'
    })


@user_blueprint.route('/api/v1/user/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return jsonify({'status': 'confirmed'})
    return jsonify({'status': 'unconfirmed',
                    'message': 'Please confirm your account!'}), 401


@user_blueprint.route('/api/v1/user/confirm/resend')
def resend_confirmation():
    token = utility.generate_confirmation_token(current_user.email)
    confirm_url = utility.generate_url('user.confirm_email', token=token)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"

    redis_queue.enqueue(utility.send_mail, current_user.email, subject, html)

    return jsonify({'status': 'unconfirmed',
                    'message': 'A new confirmation email has been sent.'}), 200

# @user_blueprint.route('/user/forgot', methods=['GET', 'POST'])
# def forgot():
#     form = ForgotForm(request.form)
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         token = generate_confirmation_token(user.email)
#
#         user.password_reset_token = token
#         db.session.commit()
#
#         reset_url = url_for('user.forgot_new', token=token, _external=True)
#         html = render_template('user/reset.html',
#                                username=user.email,
#                                reset_url=reset_url)
#         subject = "Reset your password"
#         send_email(user.email, subject, html)
#
#         flash('A password reset email has been sent via email.', 'success')
#         return redirect(url_for("main.home"))
#
#     return render_template('user/forgot.html', form=form)
#
#
# @user_blueprint.route('/user/forgot/new/<token>', methods=['GET', 'POST'])
# def forgot_new(token):
#     email = confirm_token(token)
#     user = User.query.filter_by(email=email).first_or_404()
#
#     if user.password_reset_token is not None:
#         form = ChangePasswordForm(request.form)
#         if form.validate_on_submit():
#             user = User.query.filter_by(email=email).first()
#             if user:
#                 user.password = bcrypt.generate_password_hash(form.password.data)
#                 user.password_reset_token = None
#                 db.session.commit()
#
#                 login_user(user)
#
#                 flash('Password successfully changed.', 'success')
#                 return redirect(url_for('user.profile'))
#
#             else:
#                 flash('Password change was unsuccessful.', 'danger')
#                 return redirect(url_for('user.profile'))
#         else:
#             flash('You can now change your password.', 'success')
#             return render_template('user/forgot_new.html', form=form)
#     else:
#         flash('Can not reset the password, try again.', 'danger')
#
#     return redirect(url_for('main.home'))
