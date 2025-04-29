from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Import and register blueprints here (inside the function)
    from app.routes.auth import bp as auth_bp
    from app.routes.speakers import bp as speakers_bp
    from app.routes.users import bp as users_bp
    from app.routes.bookings import bp as bookings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(speakers_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(bookings_bp)

    return app
