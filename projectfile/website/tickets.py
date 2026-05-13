from flask import Blueprint, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods = ['GET'])
def show_tickets():
    return render_template('tickets.html')

@tickets_bp.route('/tickets/confirmation', methods = ['GET'])
def show_confirmation():
    return render_template('order_confirmation.html')