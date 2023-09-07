from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from populate_database import populate_database

from werkzeug.security import generate_password_hash

def initialize_database():
    if not User.query.filter_by(name='admin').first():
        new_user = User(name='admin', password=generate_password_hash('admin', method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        initial_defaults = Defaults(
            view_sensor='SA_TEMP',
            user_id=1) 
        db.session.add(initial_defaults)
        db.session.commit()

        populate_database()



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'id: {self.id}, data: {self.data}, date: {self.date}, user_id: {self.user_id}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
    defaults = db.relationship('Defaults')

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, password: {self.password}'

class Defaults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    view_sensor = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'id: {self.id}, view_sensor: {self.view_sensor}'




# class equipment(db.Model):
#     equip_id = db.Column(db.Integer, primary_key=True)
#     equip_type = db.Column(db.String(10000))