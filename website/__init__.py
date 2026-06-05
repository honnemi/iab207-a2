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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))

    from . import home, bookings, auth, about
    app.register_blueprint(home.home_bp)
    app.register_blueprint(bookings.bookings_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(about.about_bp)

    @app.errorhandler(404)
    def not_found(error):
        return "Page not found", 404

    @app.errorhandler(500)
    def server_error(error):
        return "Internal Server Error", 404

    return app
