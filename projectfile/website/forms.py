from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
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
    card_number = StringField('Card Number', render_kw={"placeholder": "Enter 16-digit card number"}, validators=[InputRequired(), Length(min=16, max=16)])
    expiry = StringField('Expiry', render_kw={"placeholder": "MM/YY"}, validators=[InputRequired(), Length(min=5, max=5)])
    cvv = StringField('CVV', render_kw={"placeholder": "Enter 3 or 4-digit security code"}, validators=[InputRequired(), Length(min=3, max=4)])
    submit = SubmitField('Complete Payment')
    # Still need to add proper validation for all fields