from flask import Blueprint, abort, request
from datetime import date
from init import db
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

# ====================================Get all cards===================================
@users_bp.route('/')
@jwt_required()
def get_all_users():

    #create statement to query the database
    #sort users by name descending
    stmt = db.select(User).order_by(User.name.desc())
    users = db.session.scalars(stmt)

    #return all the cards in the database
    return UserSchema(many=True, ).dump(users)