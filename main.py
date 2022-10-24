from flask import Flask
from db import db, ma, bcrypt, jwt
from controllers.cards_controller import cards_bp
from controllers.users_controller import users_bp
import os



def create_app():
    app = Flask(__name__)

    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = '?CodaCatIsACat!'

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(cards_bp)
    app.register_blueprint(users_bp)

    return app
