from flask import Blueprint, abort, request
from datetime import date
from controllers.auth_controller import authorize
from controllers.auth_controller import authorize
from init import db
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

# ====================================Get all users===================================
@users_bp.route('/')
@jwt_required()
def get_all_users():

    #create statement to query the database
    #sort users by name descending
    stmt = db.select(User).order_by(User.name.desc())
    users = db.session.scalars(stmt)

    #return all the cards in the database
    return UserSchema(many=True, exclude=['password']).dump(users)

# ===================================Get a single User===================================
@users_bp.route('/<int:user_id>')
@jwt_required()
def get_one_user(user_id):

    #create statement to query the database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    #if the user id is not found abort with error message
    if not user:
        abort(401, description={'Error': f'User id: {user_id} not found'})
    #user found return user details
    return UserSchema(exclude=['password']).dump(user)


# ====================================Update a single User===================================
@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_user(user_id):

    #create a statement to search for the user_id in database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    #if the user is found update the details with request body or leave the details unchanged
    if user:
        user.name = request.json.get('name') or user.name
        user.email = request.json.get('email') or user.email
        user.password = request.json.get('password') or user.password
        user.is_admin = request.json.get('is_admin') or user.is_admin
        
        print(user.name)
        #commit the changes to the user
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user)
    else:
        abort(401, description={'Error': f'User id: {user_id} not found'})

    

# ===================================Delete a single User===================================
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    #check to see if user is an admin
    authorize()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {'Msg': f'User {user.name} deleted successfully'}, 200
    else:
        abort(404, description=f'User {user_id} does not exist')
