from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('home.view_events'))
            return redirect(nextp)
        else:
            flash(error, 'danger')
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    error = None
    if register_form.validate_on_submit():
        user_name = register_form.user_name.data
        contact_number = register_form.contact_number.data
        street_address = register_form.street_address.data
        email = register_form.email.data
        password = register_form.password.data
        existing_user = db.session.scalar(db.select(User).where(User.email==email)) 
        if existing_user:
            error = 'Email already registered'
        else:
            password_hash = generate_password_hash(password)
            new_user = User (name=user_name, contact_number=contact_number, street_address=street_address, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
        flash(error, 'danger')
    return render_template ('user.html', form=register_form, heading='Register')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home.view_events'))
