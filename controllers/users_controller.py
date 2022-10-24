from datetime import timedelta
from flask import Blueprint, abort, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from db import db, bcrypt, jwt
from models.user import User, UserSchema

users_bp = Blueprint('users', __name__, url_prefix='/users')



@users_bp.route('/')
def get_users():
    #query database for all users to display
    stmt = db.select(User).order_by(User.name, User.is_admin)
    users = db.session.scalars(stmt)
    #display error message if the database is empty
    if not users:
        abort(404, description='The databaes is empty')
    
    #return the users in the database
    return UserSchema(many=True, exclude=['password']).dump(users)

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    #search the database for the user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    #error message if user is not found
    if not user:
        abort(400, description=f'User {user_id} does not exist')

    #delete the user from the database and commit changes
    db.session.delete(user)
    db.session.commit()

    return{'Msg': f'User named {user.name} successfully deleted from the database'}




@users_bp.route('/signup/', methods=['POST'])
def signup():
    #create a User object to store the user information from the json request
    user = User (
        name = request.json['name'],
        email = request.json['email'],
        password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
        is_admin = request.json['is_admin']
    )

    #check to see if email already exists
    stmt = db.select(User).filter_by(email=user.email)
    result = db.session.scalar(stmt)

    #if the email already exists display error message
    if result:
        abort(409, description=f'The email address {user.email} already exists')

    #add the email to the database and commit changes
    db.session.add(user)
    db.session.commit()

    #user has been successfully add to the database
    #create a token for them hashed with their id
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))


    #return successfully entered user information message
    return {'Msg': f'Successfully created user {user.name}', 'Token': token}