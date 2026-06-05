from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
from flask_login import current_user
from .forms import EventForm, CommentForm
from .models import Event, Booking, Comment
from . import db
from datetime import datetime 
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def view_events():
    bleh1 = Event.query.filter(Event.title.contains("2026")).first()

    if bleh1:
        db.session.delete(bleh1)
        db.session.commit()



    genre_filter = request.args.get('genre')
    search_query = request.args.get('q', '').strip()
    query = Event.query
    if genre_filter:
        query = query.filter_by(genre=genre_filter)
    if search_query:
        like = f'%{search_query}%'
        query = query.filter(
            db.or_(
                Event.title.ilike(like),
                Event.description.ilike(like),
                Event.location.ilike(like),
            )
        )
    events = query.all()
    all_genres = [r[0] for r in db.session.query(Event.genre).distinct() if r[0]]

    return render_template('view_events.html', events=events, search_query=search_query, 
                           all_genres=all_genres, selected_genre=genre_filter or '')


@home_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
 
    if form.validate_on_submit():
        
        date_str = form.date.data
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            event_date = None

        if (form.acknowledgement_type.data == 'enhanced'
            and not (form.acknowledgement_text.data or '').strip()):
            flash ('Please enter your custom Acknowledgment text for the Enhanced option.', 'warning')
            return render_template('create_events.html', form = form)

        image_filename = None
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            # Save into website/static/event_images/
            upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'images')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            image_filename = filename 

        event = Event(
            title=form.title.data,
            description=form.description.data,
            genre=form.genre.data,
            rating=form.rating.data,
            ticket_price=float(form.ticket_price.data) if form.ticket_price.data else None,
            tickets_available=form.tickets_available.data,
            location=form.location.data,
            date=event_date,
            image=image_filename,
            owner_id =current_user.id,
            acknowledgement_type=form.acknowledgement_type.data,
            acknowledgement_text=form.acknowledgement_text.data or None

        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('home.event_detail', event_id=event.id))
 
    return render_template('create_events.html', form=form)

@home_bp.route('/events/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comment_form = CommentForm()
    comments = Comment.query.filter_by(event_id = event_id)\
                            .order_by(Comment.created_at.desc()).all()
    
    return render_template('event_detail.html', event=event, comment_form=comment_form, comments=comments)

@home_bp.route('/events/<int:event_id>/tickets', methods=['GET', 'POST'])
@login_required
def buy_tickets(event_id):
    event = Event.query.get_or_404(event_id)

    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    key = str(event_id)
    cart.setdefault(key, 1)

    if request.method == "POST":
        action = request.form.get("action")
        qty = cart[key]
        if action == "increase":
            if qty < event.tickets_available:
                qty += 1
                if qty == event.tickets_available:
                    flash("Maximum available tickets selected.")
            else:
                flash("No more tickets are available.")
        elif action == "decrease":
            if qty > 1:
                qty -= 1
        elif action == "checkout":
            if not current_user.is_authenticated:
                flash("You must be logged in to buy tickets", "warning")
                return redirect(request.url)
        
            else:
                booking = Booking(
                    created_at=datetime.now(),
                    user_id=current_user.id, 
                    event_id=event.id,
                    quantity=qty
                )
                db.session.add(booking)

                event.tickets_available -= qty # update tickets available for event
                db.session.commit()

                session.pop("cart", None)

                return redirect(url_for("bookings.show_order_confirmation", booking_id=booking.id))

        cart[key] = qty
        session["cart"] = cart
        return redirect(url_for("home.buy_tickets", event_id=event_id))

    quantity = cart[key]
    
    return render_template('tickets.html', event=event, quantity=quantity)

@home_bp.route('/events/<int:event_id>/comment', methods=['POST'])
def add_comment(event_id):
    if not current_user.is_authenticated:
        flash("You must be logged in to buy tickets", "warning")
        return redirect(request.url)
    else:
        event = Event.query.get_or_404(event_id)
        text = request.form.get('text', '').strip()
        if text:
            new_comment = Comment(text=text, 
                                user_id=current_user.id if current_user.is_authenticated else None, 
                                event_id=event.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment posted!', 'success')
        else:
            flash('Comment cannot be empty.', 'warning')
    return redirect(url_for('home.event_detail', event_id=event_id))

@home_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.owner_id != current_user.id:
        abort(403)
    if event.is_cancelled:
        flash('Cancelled events cannot be edited.', 'warning')
        return redirect(url_for('home.event_detail', event_id=event_id))

    form = EventForm(obj=event)  # pre-fills the form with existing data

    if form.validate_on_submit():
        date_str = form.date.data
        try:
            event.date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            event.date = None

        event.title = form.title.data
        event.description = form.description.data
        event.genre = form.genre.data
        event.rating = form.rating.data or None
        event.ticket_price = float(form.ticket_price.data) if form.ticket_price.data else None
        event.tickets_available = form.tickets_available.data
        event.location = form.location.data
        event.image = form.image.data or event.image  # keep old image if nothing entered
        event.acknowledgement_type = form.acknowledgement_type.data
        event.acknowledgement_text = form.acknowledgement_text.data or None

        db.session.commit()
        flash('Event updated!')
        return redirect(url_for('home.event_detail', event_id=event_id))

    return render_template('create_events.html', form=form, event=event)  # reuse same template


@home_bp.route('/events/<int:event_id>/cancel', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        abort(403)
    event.is_cancelled = True
    db.session.commit()
    flash(f'"{event.title}" has been cancelled.', 'success')
    return redirect(url_for('home.my_events'))  

@home_bp.route('/my-events')
@login_required
def my_events():
    events = Event.query.filter_by(owner_id=current_user.id)\
                        .order_by(Event.date.asc()).all()
    return render_template('my_events.html', events=events)

@home_bp.route('/events/<int:event_id>/cancel-confirm')
@login_required
def cancel_confirm(event_id):
    event = Event.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        abort(403)
    if event.is_cancelled:
        flash('This event is already cancelled.', 'info')
        return redirect(url_for('home.event_detail', event_id=event_id))
    return render_template('cancel_confirm.html', event=event)