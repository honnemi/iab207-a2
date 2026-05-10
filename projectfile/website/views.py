from flask import Blueprint, render_template, redirect, url_for, request
from . forms import LoginForm, RegisterForm, EventForm
from . models import Event
from . import db

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

@main_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()

    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('main.view_events'))

    return render_template('events.html', form=form)

@main_bp.route('/events')
def view_events():
    events = Event.query.all()
    return render_template('view_events.html', events=events)

@main_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)