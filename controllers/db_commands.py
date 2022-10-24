from flask import Blueprint
from db import db, jwt, bcrypt
from models.card import Card, CardSchema
from models.user import User, UserSchema
from datetime import date

db_commands = Blueprint('db_commands', __name__)

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='Coda Lisbona',
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='someone@spam.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8')
        ),
        User(
            name='Mario Lisbona',
            email='mario.lisbona@gmail.com',
            password=bcrypt.generate_password_hash('Muzza1234').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='Ali Taubner',
            email='amtaubner@gmail.com',
            password=bcrypt.generate_password_hash('aliT123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='Coda Cat',
            email='coda@cat.com',
            password=bcrypt.generate_password_hash('CodaCatttt!').decode('utf-8')
        )
    ]

    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today()
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        )
    ]

    db.session.add_all(cards)
    db.session.add_all(users)
    db.session.commit()
    print('Tables seeded')