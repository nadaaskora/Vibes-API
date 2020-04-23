# coding: utf-8
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, LargeBinary, String, Table, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Assistant(db.Model):
    __tablename__ = 'assistant'

    assistant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text(11), nullable=False)
    region = db.Column(db.Text, nullable=False)
    photo = db.Column(db.LargeBinary)
    e_mail = db.Column('e-mail', db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Boolean, server_default=db.FetchedValue())
    current_location = db.Column(db.Text)
    number_of_trips = db.Column(db.Integer, server_default=db.FetchedValue())


class AssistantNationalId(db.Model):
    __tablename__ = 'assistant_national_id'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    assistant_id = db.Column(db.ForeignKey('assistant.assistant_id'))

    assistant = db.relationship('Assistant', primaryjoin='AssistantNationalId.assistant_id == Assistant.assistant_id', backref='assistant_national_ids')


class Blind(db.Model):
    __tablename__ = 'blind'

    blind_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text(11), nullable=False)
    region = db.Column(db.Text, nullable=False)
    e_mail = db.Column('e-mail', db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    number_of_trips = db.Column(db.Integer)


class BlindNationalId(db.Model):
    __tablename__ = 'blind_national_id'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    blind_id = db.Column(db.ForeignKey('blind.blind_id'), nullable=False)

    blind = db.relationship('Blind', primaryjoin='BlindNationalId.blind_id == Blind.blind_id', backref='blind_national_ids')


class CarLicence(db.Model):
    __tablename__ = 'car_licence'

    licence_id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    assistant_id = db.Column(db.ForeignKey('assistant.assistant_id'))

    assistant = db.relationship('Assistant', primaryjoin='CarLicence.assistant_id == Assistant.assistant_id', backref='car_licences')


class Request(db.Model):
    __tablename__ = 'request'

    request_id = db.Column(db.Integer, primary_key=True)
    type_of_service = db.Column(db.String, nullable=False)
    current_location = db.Column(db.Text, nullable=False)
    accepted = db.Column(db.Boolean, nullable=False)
    distenation_ = db.Column('distenation ', db.Text, nullable=False)
    time_needed = db.Column(db.Integer, nullable=False)
    blind_id = db.Column(db.ForeignKey('blind.blind_id'))
    assistant_id = db.Column(db.ForeignKey('assistant.assistant_id'))

    assistant = db.relationship('Assistant', primaryjoin='Request.assistant_id == Assistant.assistant_id', backref='requests')
    blind = db.relationship('Blind', primaryjoin='Request.blind_id == Blind.blind_id', backref='requests')


t_sqlite_sequence = db.Table(
    'sqlite_sequence',
    db.Column('name', db.NullType),
    db.Column('seq', db.NullType)
)


class Trip(db.Model):
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, primary_key=True)
    complete = db.Column(db.Boolean, nullable=False)
    state = db.Column(db.Boolean, nullable=False)
    total_distance = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Integer, nullable=False)
    payment = db.Column(db.Float(2), nullable=False)
    request_id = db.Column(db.ForeignKey('request.request_id'))

    request = db.relationship('Request', primaryjoin='Trip.request_id == Request.request_id', backref='trips')


class TrustedNationalId(db.Model):
    __tablename__ = 'trusted_national_id'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    trusted_id = db.Column(db.ForeignKey('trusted_person.trusted_id'), nullable=False)

    trusted = db.relationship('TrustedPerson', primaryjoin='TrustedNationalId.trusted_id == TrustedPerson.trusted_id', backref='trusted_national_ids')


class TrustedPerson(db.Model):
    __tablename__ = 'trusted_person'

    trusted_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text(11), nullable=False)
    relation = db.Column(db.Text, nullable=False)
    blind_id = db.Column(db.ForeignKey('blind.blind_id'), nullable=False)

    blind = db.relationship('Blind', primaryjoin='TrustedPerson.blind_id == Blind.blind_id', backref='trusted_people')
