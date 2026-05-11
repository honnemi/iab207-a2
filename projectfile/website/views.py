from flask import Blueprint, render_template, redirect, url_for, request, flash
from . forms import LoginForm, RegisterForm, EventForm, CommentForm
from . models import Event
from . import db
from datetime import datetime 

main_bp = Blueprint('main', __name__)

@main_bp.route('/index')
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
        # Parse the datetime-local string into a Python datetime
        date_str = form.date.data
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            event_date = None
 
        event = Event(
            title=form.title.data,
            description=form.description.data,
            genre=form.genre.data,
            rating=form.rating.data,
            ticket_price=float(form.ticket_price.data) if form.ticket_price.data else None,
            tickets_available=form.tickets_available.data,
            location=form.location.data,
            date=event_date,
            image=form.image.data or None,
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('main.view_events'))
 
    return render_template('events.html', form=form)

@main_bp.route('/')
def view_events():
    genre_filter = request.args.get('genre')
 
    if genre_filter:
        events = Event.query.filter_by(genre=genre_filter).all()
    else:
        events = Event.query.all()
 
    return render_template('view_events.html', events=events)

@main_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comment_form = CommentForm()
    return render_template('event_detail.html', event=event, comment_form=comment_form)

@main_bp.route('/events/<int:event_id>/comment', methods=['POST'])
def add_comment(event_id):
    event = Event.query.get_or_404(event_id)
    text = request.form.get('text', '').strip()
    if text:
        comment = comment(text=text, event_id=event.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!')
    else:
        flash('Comment cannot be empty.')
    return redirect(url_for('main.event_detail', event_id=event_id))