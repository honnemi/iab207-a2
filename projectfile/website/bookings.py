from flask import Blueprint, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from . models import Booking, User, Event

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods = ['GET'])
def show_bookings():
    bookings = Booking.query.all()
    return render_template('booking_history.html', bookings=bookings)

@bookings_bp.route('/order_confirmation/<int:booking_id>', methods = ['GET'])
def show_order_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('order_confirmation.html', booking=booking)
