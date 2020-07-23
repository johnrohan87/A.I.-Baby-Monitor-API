import datetime
from flask_sqlalchemy import SQLAlchemy




db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    babies = db.relationship('Baby',backref='parent', lazy=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "babies": list(map(lambda x: x.serialize(), self.babies))
            # do not serialize the password, its a security breach
        }

class Baby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    alarms = db.relationship('Alarm',backref='subjectBaby', lazy=True)

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dob_baby = db.Column(db.String(10), nullable=False)
    time_zone = db.Column(db.String(10), nullable=False)
    baby_gender = db.Column(db.String(10), nullable=False)

    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    def __init__(self,parent_id,first_name,last_name,dob_baby,time_zone,baby_gender):
        self.parent_id = parent_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob_baby = dob_baby
        self.time_zone = time_zone
        self.baby_gender = baby_gender


    def __repr__(self):
        return f'<Baby {self.id}>' 

    def serialize(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "alarms": list(map(lambda x: x.serialize(), self.alarms)),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob_baby": self.dob_baby,
            "time_zone": self.time_zone,
            "baby_gender": self.baby_gender,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey("baby.id"))

    crying = db.Column(db.String(80), unique=False, nullable=False)
    overheated = db.Column(db.Boolean(), unique=False, nullable=False)
    breathing = db.Column(db.Boolean(), unique=False, nullable=False)
    face_down = db.Column(db.Boolean(), unique=False, nullable=False)
    out_of_crib = db.Column(db.Boolean(), unique=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Alarm %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "baby_id": self.baby_id,
            "crying": self.crying,
            "overheated": self.overheated,
            "breathing": self.breathing,
            "face_down": self.face_down,
            "out_of_crib": self.out_of_crib,
            "created_date": self.created_date,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baby_id = db.Column(db.Integer, db.ForeignKey("baby.id"))

    face_direction = db.Column(db.String(10), nullable=False)
    breathing = db.Column(db.String(10), unique=False, nullable=False)
    last_movement = db.Column(db.String(10), nullable=False)
    time_stamp = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Status %r>' % self.baby_id

    def serialize(self):
        return {
            "id": self.id,
            "baby_id": self.baby_id,
            "face_direction": self.face_direction,
            "breathing": self.breathing,
            "last_movement": self.last_movement,
            "time_stamp": self.time_stamp,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

