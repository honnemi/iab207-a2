from flask import Blueprint, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from .forms import CheckoutForm
from . models import Event, Comment

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods = ['GET'])
def show_tickets():
    return render_template('tickets.html')

@tickets_bp.route('/tickets/checkout', methods = ['GET', 'POST'])
def show_checkout():
    form = CheckoutForm()

    if form.validate_on_submit():
        card_number = form.card_number.data
        expiry = form.expiry.data
        cvv = form.cvv.data

        return redirect(url_for('tickets.show_confirmation'))

    return render_template('checkout.html', form=form)

@tickets_bp.route('/tickets/confirmation', methods = ['GET'])
def show_confirmation():
    return render_template('order_confirmation.html')