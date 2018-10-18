from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Report(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    html_path = db.Column(db.String(64))

    def __repr__(self):
        return '<Report {}>'.format(self.timestamp)