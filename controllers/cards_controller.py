from flask import Blueprint
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
    return CardSchema().dump(card)
