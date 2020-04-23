from flask import jsonify, request, g, abort
from vibesapp import app, db, auth
from vibesapp.models import Assistant, AssistantNationalId, Blind, BlindNationalId, CarLicence, TrustedNationalId, TrustedPerson, AssistantSchema
from flask_jwt_extended import create_access_token
import re

# @app.cli.command('db_create')
# def db_create():
#     db.create_all()
#     print('Database created!')
#
#
# @app.cli.command('db_drop')
# def db_drop():
#     db.drop_all()
#     print('Database dropped!')
#
#
# @app.cli.command('db_seed')
# def db_seed():
#     test_user = User(first_name='William',
#                      last_name='Herschel',
#                      email='test@test.com',
#                      password='P@ssw0rd')
#
#     db.session.add(test_user)
#     db.session.commit()
#     print('Database seeded!')
#

#
# @auth.verify_password
# def verify_password(email, password):
#     user = Assistant.query.filter_by(email=email).first()
#     if not user or not user.verify_password(password):
#         return False
#     g.user = user
#     return True


@app.route('/')
def vibes():
    return 'Vibes '


@app.route('/assistant/register', methods=['POST'])
def assistant_register():
    email = request.json['email']
    phone = request.json['phone']
    test_email = Assistant.query.filter_by(email=email).first()
    test_phone = Assistant.query.filter_by(phone=phone).first()
    if test_email:
        return jsonify(message='That user already exists.'), 409
    elif test_phone:
        return jsonify(message='This Phone number already exists.'), 409
    else:
        name = request.json['name']
        phone = request.json['phone']
        region = request.json['region']
        #photo = request.json['photo']
        email = request.json['email']
        password = request.json['password']
    if name is "" or phone is "" or region is "" or email is "" or password is "":
        return jsonify(message="missing argument"), 400
    if len(phone) < 11:
        return jsonify(message='Phone number should be 11 numbers.'), 400

    if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
        return jsonify(massage="Invalid Email address"), 401

    assistant = Assistant(name=name,
                          phone=phone,
                          region=region,
                          #photo=photo,
                          password=password,
                          email=email)
    #assistant.hash_password(password)
    db.session.add(assistant)
    db.session.commit()
    return jsonify(message="Assistant created successfully."), 201

# @auth.verify_password
# def verify_password(username_or_token, password):
#     #Try to see if it's a token first
#     user_id = Assistant.verify_auth_token(username_or_token)
#     if user_id:
#         user = Assistant.query.filter_by(id = user_id).one()
#     else:
#         user = Assistant.query.filter_by(username = username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True


@app.route('/assistant/login', methods=['POST'])
#@auth.login_required
def assistant_login():
    email = request.json['email']
    password = request.json['password']
    user = Assistant.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        # token = g.user.generate_auth_token()
        # return jsonify({'token': token.decode('ascii')})
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/blind/register', methods=['POST'])
def blind_register():
    email = request.json['email']
    phone = request.json['phone']
    test_email = Assistant.query.filter_by(email=email).first()
    test_phone = Assistant.query.filter_by(phone=phone).first()
    if test_email:
        return jsonify(message='This email already exists.'), 409
    elif test_phone:
        return jsonify(message='This Phone number already exists.'), 409
    else:
        name = request.json['name']
        phone = request.json['phone']
        region = request.json['region']
        email = request.json['email']
        password = request.json['password']

        if len(phone) < 11:
            return jsonify(message='Phone number should be 11 numbers.'), 411

        if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
            return jsonify(massage="Invalid Email address"), 401
        blind = Blind(name=name,
                      phone=phone,
                      region=region,
                      email=email,
                      password=password)

        db.session.add(blind)
        db.session.commit()

        return jsonify(message="Blind user created successfully."), 201


@app.route('/blind/login', methods=['POST'])
def blind_login():
    email = request.json['email']
    password = request.json['password']
    test = Blind.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401

