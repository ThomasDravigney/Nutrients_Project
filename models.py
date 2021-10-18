from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


def clear_database(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


class UserAteFood(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    food_id = db.Column(db.ForeignKey('food.id'), primary_key=True)
    quantity = db.Column(db.Float)
    date = db.Column(db.DateTime, index=True)
    meal = db.Column(db.String, index=True)
    user = db.relationship("User", back_populates="eaten_food")
    food = db.relationship("Food", back_populates="eaten_by")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    register_date = db.Column(db.DateTime, default=datetime.utcnow)
    eaten_food = db.relationship("UserAteFood", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(13), index=True, unique=True)
    eaten_by = db.relationship("UserAteFood", back_populates="food")


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
