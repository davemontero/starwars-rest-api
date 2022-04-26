import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Users, Favorites, Planets, People

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dbname = 'app.db'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASEDIR, dbname)}"
Migrate(app, db, render_as_batch=True)
db.init_app(app)
CORS(app)

@app.route("/users", methods=["POST", "GET"])
def users():
    user = Users()
    if request.method == 'POST':
        dbuser = user.query.filter_by(user_name=request.json.get("user")).first()
        if dbuser:
            return jsonify({
                "message": "Usuario ya existe"
            })
        user.user_name = request.json.get("user")
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "Usuario agregado con exito"
        })

    if request.method == 'GET':
        result = user.query.all()
        users = [user.serialize() for user in result]
        return jsonify(users)

@app.route("/users/favorites")
def user_favorites():
    favorites = Favorites()
    result = favorites.query.all()
    favorite_rs = [favorites.serialize() for favorites in result]
    return jsonify(favorite_rs)

@app.route("/people", methods=["GET", "POST"])
def people():
    people = People()
    if request.method == 'POST':
        dbperson = people.query.filter_by(person_name=request.json.get("name")).first()
        if dbperson:
            return jsonify({
                "message": "Personaje ya existe"
            })
        people.person_name = request.json.get("name")
        db.session.add(people)
        db.session.commit()
        return jsonify({
            "message": "Personaje agregado con exito"
        })
    if request.method == 'GET':
        result = people.query.all()
        people_rs = [people.serialize() for people in result]
        return jsonify(people_rs)

@app.route("/people/<int:people_id>")
def person_info(people_id):
    people = People()
    result = people.query.filter_by(person_id=people_id)
    toReturn = [people.serialize() for people in result]
    return jsonify(toReturn)


@app.route("/favorite/people/<int:people_id>", methods=["POST", "DELETE"])
def set_favoritePerson(people_id):
    favorites = Favorites()
    people = People()

    if request.method == 'POST':
        query_rs = people.query.filter_by(person_id=people_id).first()
        
        favorites.favorite_item = query_rs.person_name
        favorites.favorite_type = "people"
        favorites.ext_id = query_rs.person_id

        db.session.add(favorites)
        db.session.commit()

        return jsonify({
            "message": "Favorito registrado"
        })

    if request.method == 'DELETE':
        query_rs = favorites.query.filter_by(ext_id=people_id).delete()
        db.session.commit()
        return jsonify({
            "message": "Favorito eliminado"
        })

@app.route("/planets", methods=["GET", "POST"])
def planets():
    planets = Planets()
    if request.method == 'POST':
        dbplanet = planets.query.filter_by(planet_name=request.json.get("name")).first()
        if dbplanet:
            return jsonify({
                "message": "Planeta ya existe"
            })
        planets.planet_name = request.json.get("name")
        db.session.add(planets)
        db.session.commit()
        return jsonify({
            "message": "Planeta agregado con exito"
        })
    if request.method == 'GET':
        result = planets.query.all()
        planets_rs = [planets.serialize() for planets in result]
        return jsonify(planets_rs)

@app.route("/planets/<int:planet_id>")
def planet_info(planet_id):
    planets = Planets()
    result = planets.query.filter_by(planet_id=planet_id)
    toReturn = [planets.serialize() for planets in result]
    return jsonify(toReturn)

@app.route("/favorite/planets/<int:planet_id>", methods=["POST", "DELETE"])
def set_favoritePlanets(planet_id):
    favorites = Favorites()
    planets = Planets()
    if request.method == 'POST':
        query_rs = planets.query.filter_by(planet_id=planet_id).first()
        
        favorites.favorite_item = query_rs.planet_name
        favorites.favorite_type = "planets"
        favorites.ext_id = query_rs.planet_id

        db.session.add(favorites)
        db.session.commit()
        return jsonify({
            "message": "Favorito registrado"
        })

    if request.method == 'DELETE':
        query_rs = favorites.query.filter_by(ext_id=planet_id).delete()
        db.session.commit()
        return jsonify({
            "message": "Favorito eliminado"
        })



if __name__ == "__main__":
    app.run("localhost")