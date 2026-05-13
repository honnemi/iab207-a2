from flask import Blueprint, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods = ['GET'])
def show_bookings():
    return render_template('booking_history.html')
