from flask import flash, redirect, render_template, request, url_for

from .. import db
from ..email import send_email
from ..main import main
from ..models import User
from . import auth
from .forms import RegistrationForm


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        username = email.split('@')[0]
        preferred_time = request.form.get('time')
        corona_update = True if request.form.get('category_extra') else False
        categories = request.form.getlist('category')
        user = User(email=email, preferred_time=preferred_time,
                    corona_update=corona_update)
        for category in categories:
            user.add_subscription(category)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your subscription',
                   '/auth/email/confirm', username=username, token=token)
        flash('A confirmation link has been sent to via email.')
    return render_template('auth/register.html')


@auth.route('/confirm/<token>')
def confirm(token):
    if User.confirm(token):
        db.session.commit()
        return redirect(url_for('auth.success'))
    else:
        flash('The confirmation link is invalid or has expired!')
    return redirect('auth.register')


@auth.route('/success')
def success():
    return render_template('auth/success.html')
