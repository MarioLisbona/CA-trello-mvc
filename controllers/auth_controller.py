from doctest import debug_script
from flask import Blueprint, abort, request, jsonify
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ====================================Register a new user===================================
@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        # Create a new User model instance from the user_info
        user = User(
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            name = request.json.get('name')
        )

        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409



# ====================================Login a user===================================
@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    #find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    #If the user exists and the password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user), 200
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {"email": user.email, "token": token, 'is_admin': user.is_admin}
    else:
        return {'Error': 'Invalid email or password'}, 401


# ====================================function to return admin true/false===================================
def authorize():
    #get idendtity from JWT token 
    user_id = get_jwt_identity()

    #create a statement to query the database for the id retrieved from JWT token
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    #used here for a token frmo a delete used
    if not user:
        abort(401, description='Invalid Authorization token')
    if not user.is_admin:
        abort(401)