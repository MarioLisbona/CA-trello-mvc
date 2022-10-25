from flask import Blueprint, abort, request
from datetime import date
from init import db
from models.card import Card, CardSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')


# ====================================Get all cards===================================
@cards_bp.route('/')
@jwt_required()
def get_all_cards():

    #create statement to query the database
    #sort cards by priority, descending and title
    stmt = db.select(Card).order_by(Card.date.desc())
    cards = db.session.scalars(stmt)

    #return all the cards in the database
    return CardSchema(many=True).dump(cards)


# ===================================Get a single card===================================
@cards_bp.route('/<int:card_id>')
@jwt_required()
def get_card(card_id):

    #create a statement to query the database for the id passed in
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)

    #if card doesnt exists then provide error messasge
    if not card:
        abort(404, description=f'Card {card_id} does not exist')

    #return card and display
    return CardSchema().dump(card)

# ====================================Update a single card===================================
@cards_bp.route('/<int:card_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_card(card_id):

    #create a statement to query the database for the id passed in
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)

    #if the card exists update the card with new inputs, or leave if no input entered
    if card:
        card.title = request.json.get('title') or card.title
        card.description = request.json.get('description') or card.description
        card.status = request.json.get('status') or card.status
        card.priority = request.json.get('priority') or card.priority

        #commit changes
        db.session.commit()

        # return updated card or show error message
        return CardSchema().dump(card)
    else:
        abort(404, description=f'Card {card_id} does not exist')


# ====================================create a single card===================================
@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
    # Create a new Card model instance from the user_info passed in the JSON post request
    card = Card(
        title = request.json['title'],
        description = request.json['description'],
        date = date.today(),
        status = request.json['status'],
        priority = request.json['priority']
    )

    # Add and commit card to DB
    db.session.add(card)
    db.session.commit()

    # Respond to client
    return CardSchema().dump(card), 201

# ===================================Delete a single card===================================
@cards_bp.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
def delete_one_card(card_id):
    authorize()

    #create a statement to query the database for the id passed in
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)

    #if card doesnt exists then provide error messasge
    if card:
        db.session.delete(card)
        db.session.commit()
        return {'Msg': f'Card {card.title} deleted successfully'}, 200
    else:
        abort(404, description=f'Card {card_id} does not exist')

    
    
