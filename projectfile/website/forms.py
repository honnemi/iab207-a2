from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
from wtforms.widgets import EmailInput

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class CheckoutForm(FlaskForm):
    card_number = StringField('Card Number', render_kw={"placeholder": "Enter 16-digit card number"}, validators=[InputRequired(), Regexp(r'^\d{16}$', message="Card number must be 16 digits")])
    expiry = StringField('Expiry', render_kw={"placeholder": "MM/YY"}, validators=[InputRequired(), Regexp(r'^(0[1-9]|1[0-2])\/\d{2}$', message="Format must be MM/YY")])
    cvv = StringField('CVV', render_kw={"placeholder": "Enter 3 or 4-digit security code"}, validators=[InputRequired(), Regexp(r'^\d{3,4}$', message="CVV must be 3 or 4 digits")])
    submit = SubmitField('Complete Payment')

class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[InputRequired(), Length(min=2, max=150)])
    descripttion = TextAreaField("Description", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    submit = SubmitField("Create Event")