from flask import Blueprint, render_template
from . forms import LoginForm, RegisterForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return '<h1>Starter code for assignment 3<h1>'

@main_bp.route('/login_testing')
def login_testing():
    form = LoginForm()
    return render_template('user.html', form = form, heading = 'Login')

@main_bp.route('/register_testing')
def register_testing():
    form = RegisterForm()
    return render_template('user.html', form = form, heading = 'Register')