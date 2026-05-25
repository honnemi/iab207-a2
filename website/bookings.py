from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . models import Booking

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods = ['GET'])
@login_required
def show_bookings():
    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()
    return render_template('booking_history.html', bookings=bookings)

@bookings_bp.route('/order_confirmation/<int:booking_id>', methods = ['GET'])
@login_required
def show_order_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('order_confirmation.html', booking=booking)
