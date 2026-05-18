from flask import Blueprint, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods = ['GET'])
def show_bookings():
    return render_template('booking_history.html')

@bookings_bp.route('/order_confirmation/<int:booking_id>', methods = ['GET'])
def show_order_confirmation(booking_id):
    return render_template('order_confirmation.html')
