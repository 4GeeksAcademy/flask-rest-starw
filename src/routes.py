
from flask import Blueprint, request, jsonify
from models import db, User, People, Planet, Favorite

api_bp = Blueprint('api', __name__)


# USERS
@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


# PEOPLE
@api_bp.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200


@api_bp.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    person = People.query.get(id)
    if person is None:
     return jsonify({"msg": "Not found"}), 404
    return jsonify(person.serialize()), 200


# PLANETS
@api_bp.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@api_bp.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({"msg": "Not found"}), 404
    return jsonify(planet.serialize()), 200


# FAVORITES
@api_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


@api_bp.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorite(user_id):
    body = request.get_json()
    # Suponiendo que body contiene los campos necesarios para Favorite
    new = Favorite(user_id=user_id, **body)
    db.session.add(new)
    db.session.commit()
    return jsonify(new.serialize()), 201


@api_bp.route('/users/<int:user_id>/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(user_id, favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite is None:
        return jsonify({"msg": "Not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200
