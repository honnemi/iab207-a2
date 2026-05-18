from flask import Flask 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    Bootstrap5(app)

    from . import models

    """
    # initialise the login manager
    login_manager = LoginManager()
    
    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return db.session.scalar(db.select(User).where(User.id==user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import event
    app.register_blueprint(events.events_bp)
    from . import auth
    app.register_blueprint(auth.auth_bp)
    """

    from . import views, bookings
    app.register_blueprint(views.main_bp)
   #  app.register_blueprint(tickets.tickets_bp)
    app.register_blueprint(bookings.bookings_bp)

    return app

