from flask import Blueprint, render_template, url_for, redirect, flash
from .forms import ContactForm

about_bp = Blueprint('about', __name__)

@about_bp.route('/about_us', methods=['GET', 'POST'])
def show_about():
    contact_form = ContactForm()

    if contact_form.validate_on_submit():
        flash('Thanks for your submission!', 'success')
        return redirect(url_for('about.show_about'))

    return render_template('about_us.html', form=contact_form)