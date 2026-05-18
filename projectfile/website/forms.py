from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DecimalField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp, Optional, NumberRange
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

GENRE_CHOICES = [
    ('', 'Select genre'),
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Fantasy', 'Fantasy'),
    ('Romance', 'Romance'),
    ('Thriller', 'Thriller'),
    ('Animated', 'Animated'),
]
 
RATING_CHOICES = [
    ('', 'Select rating'),
    ('G', 'G'),
    ('PG', 'PG'),
    ('M', 'M'),
    ('MA15+', 'MA15+'),
    ('R18+', 'R18+'),
]
 
class EventForm(FlaskForm):
    title = StringField(
        "Event Title",
        validators=[InputRequired(), Length(min=2, max=150)]
    )
    description = TextAreaField(
        "Description",
        validators=[InputRequired()]
    )
    genre = SelectField(
        "Genre",
        choices=GENRE_CHOICES,
        validators=[InputRequired(message="Please select a genre")]
    )
    rating = SelectField(
        "Rating",
        choices=RATING_CHOICES,
        validators=[InputRequired(message="Please select a rating")]
    )
    ticket_price = DecimalField(
        "Ticket Price (AUD)",
        validators=[Optional(), NumberRange(min=0, message="Price must be 0 or more")],
        places=2
    )
    tickets_available = IntegerField(
        "Tickets Available",
        validators=[Optional(), NumberRange(min=1, message="Must have at least 1 ticket")]
    )
    location = StringField(
        "Location",
        validators=[InputRequired()]
    )
    date = StringField(
        "Date & Time",
        validators=[InputRequired()],
        render_kw={"type": "datetime-local"}
    )
    image = StringField(
        "Movie Poster URL",
        validators=[Optional(), Length(max=255)]
    )
    submit = SubmitField("Create Event")
 
class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField("Post comment")