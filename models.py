from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    # favorites = db.relationship('Favorites', backref="user", lazy=True)
    
    def __repr__(self):
        return f"<User {self.user_id}>"

    def serialize(self):
        return {
            "id": self.user_id,
            "name": self.user_name
        }

class Favorites(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    favorite_item = db.Column(db.String(150), nullable=False)
    favorite_type = db.Column(db.String(10), nullable=False)
    ext_id = db.Column(db.Integer, nullable=False)
    # uid = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    def __repr__(self):
        return f"<Favorites {self.favorite_id}>"

    def serialize(self):
        return {
            "id": self.favorite_id,
            "favorite": self.favorite_item,
            "type": self.favorite_type
        }


class Planets(db.Model):
    planet_id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"<Planets {self.planet_id}>"

    def serialize(self):
        return {
            "id": self.planet_id,
            "name": self.planet_name
        }


class People(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<People {self.person_id}>"

    def serialize(self):
        return {
            "id": self.person_id,
            "name": self.person_name
        }