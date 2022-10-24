from flask import Blueprint, abort, request
from db import db
from models.card import Card, CardSchema

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
# @jwt_required()
def all_cards():
    # return 'all cards route'
    # if not authorize():
    #     return {'Error': 'You must be an admin'}, 401

    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)
    return CardSchema(many=True).dump(cards)


@cards_bp.route('/<int:card_id>')
def get_card(card_id):

    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)

    if not card:
        abort(400, description=f'Card {card_id} does not exist')

    return CardSchema().dump(card)


@cards_bp.route('/', methods=['POST'])
def add_card():
    #create a card object to contain the card infomration sent in the JSON request body
    card = Card(
        title = request.json['title'],
        description = request.json['description'],
        date = request.json['date'],
        status = request.json['status'],
        priority = request.json['priority'],
    )

    #serch to see if a cardf with the same title aleady exists
    stmt = db.select(Card).filter_by(title=card.title)
    result = db.session.scalar(stmt)

    if result:
        abort(409, description=f'The card titled {card.title} already exists')

    #teh card doesnt exist, add the card to the database and commit changes
    db.session.add(card)
    db.session.commit()

    return {'msg': f'Card titled {card.title} successfully added to database'}


@cards_bp.route('/<int:card_id>', methods=['DELETE'])
def remove_card(card_id):

    #Search the database for the card entered by the user
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)

    #display error message if card is not found in the database
    if not card:
        abort(400, description=f'Card {card_id} does not exist')

    #delete the card and commit chages to the database
    db.session.delete(card)
    db.session.commit()

    #return message with card that was deleted from the database
    return{'Msg': f'Card titled {card.title} successfully deleted from the database'}

