from flask import Blueprint, render_template

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets')
def show_tickets():
    return render_template('tickets.html')

@tickets_bp.route('/tickets/checkout')
def show_checkout():
    return render_template('checkout.html')