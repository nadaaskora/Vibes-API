# coding: utf-8
from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, Table, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from vibesapp import ma, db, secret_key
from passlib.apps import custom_app_context as pwd_context


# Assistant
class Assistant(db.Model):
    __tablename__ = 'assistant'
    assistant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text(11), nullable=False)
    region = db.Column(db.Text, nullable=False)
    photo = db.Column(db.LargeBinary)
    email = db.Column('email', db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Boolean, server_default=db.FetchedValue())
    current_location = db.Column(db.Text)
    number_of_trips = db.Column(db.Integer, server_default=db.FetchedValue())

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        self.password = pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        assistant_id = data['id']
        return assistant_id


class AssistantSchema(ma.Schema):
    class Meta:
        fields = ('assistant_id', 'name', 'phone', 'region', 'photo', 'email', 'password',
                  'availability', 'current_location', 'number_of_trips')


# AssistantNationalId
class AssistantNationalId(db.Model):
    __tablename__ = 'assistant_national_id'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    assistant_id = db.Column(db.ForeignKey('assistant.assistant_id'))
    assistant = db.relationship('Assistant', primaryjoin='AssistantNationalId.assistant_id == Assistant.assistant_id', backref='assistant_national_ids')


class AssistantNationalIdSchema(ma.Schema):
    class Meta:
        fields = ('id', 'photo', 'assistant_id', 'assistant')


# Blind
class Blind(db.Model):
    __tablename__ = 'blind'
    blind_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text(11), nullable=False)
    region = db.Column(db.Text, nullable=False)
    email = db.Column('email', db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    number_of_trips = db.Column(db.Integer)


class BlindSchema(ma.Schema):
    class Meta:
        fields = ('blind_id', 'name', 'phone', 'region', 'email', 'password', 'number_of_trips')


# BlindNationalId
class BlindNationalId(db.Model):
    __tablename__ = 'blind_national_id'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    blind_id = db.Column(db.ForeignKey('blind.blind_id'), nullable=False)

    blind = db.relationship('Blind', primaryjoin='BlindNationalId.blind_id == Blind.blind_id', backref='blind_national_ids')


class BlindNationalIdSchema(ma.Schema):
    class Meta:
        fields = ('id', 'photo', 'blind_id', 'blind')


# CarLicence
class CarLicence(db.Model):
    __tablename__ = 'car_licence'
    licence_id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    assistant_id = db.Column(db.ForeignKey('assistant.assistant_id'))
    assistant = db.relationship('Assistant', primaryjoin='CarLicence.assistant_id == Assistant.assistant_id', backref='car_licences')
#
#
# t_sqlite_sequence = db.Table(
#     'sqlite_sequence',
#     db.Column('name', db.NullType),
#     db.Column('seq', db.NullType)
# )


class CarLicenceSchema(ma.Schema):
    class Meta:
        fields = ('licence_id', 'photo', 'assistant_id', 'assistant')


# TrustedNationalId
class TrustedNationalId(db.Model):
    __tablename__ = 'trusted_national_id'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    trusted_id = db.Column(db.ForeignKey('trusted_person.trusted_id'), nullable=False)
    trusted = db.relationship('TrustedPerson', primaryjoin='TrustedNationalId.trusted_id == TrustedPerson.trusted_id', backref='trusted_national_ids')


class TrustedNationalIdSchema(ma.Schema):
    class Meta:
        fields = ('id', 'photo', 'trusted_id', 'trusted')


# TrustedPerson
class TrustedPerson(db.Model):
    __tablename__ = 'trusted_person'
    trusted_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text(11), nullable=False)
    relation = db.Column(db.Text, nullable=False)
    blind_id = db.Column(db.ForeignKey('blind.blind_id'), nullable=False)
    blind = db.relationship('Blind', primaryjoin='TrustedPerson.blind_id == Blind.blind_id', backref='trusted_people')


class TrustedPersonSchema(ma.Schema):
    class Meta:
        fields = ('trusted_id', 'name', 'phone', 'relation', 'blind_id', 'blind')


# Schemas

assistant_schema = AssistantSchema()
assistants_schema = AssistantSchema(many=True)

assistant_national_id_Schema = AssistantNationalIdSchema()
assistants_national_id_Schema = AssistantNationalIdSchema(many=True)

blind_schema = BlindSchema()
blinds_schema = BlindSchema(many=True)

blind_national_id_schema = BlindNationalIdSchema()
blinds_national_id_schema = BlindNationalIdSchema(many=True)

car_licence_schema = CarLicenceSchema()
cars_licence_schema = CarLicenceSchema(many=True)


trusted_national_id_schema = TrustedNationalIdSchema()
trusted_nationals_id_schema = TrustedNationalIdSchema(many=True)

trusted_person_schema = TrustedPersonSchema()
trusted_persons_Schema = TrustedPersonSchema(many=True)
