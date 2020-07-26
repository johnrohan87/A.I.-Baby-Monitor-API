"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, request
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Baby,Alarm,Status
#from models import Person
from flask_jwt_simple import ( JWTManager, jwt_required, create_jwt, get_jwt_identity)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_user_info():

    #only for dev!!!
    user_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), user_query))

    return jsonify(all_users), 200

@app.route('/process-new-user/<string:user_email>/<string:user_pass>', methods=['POST'])
def handle_new_user(user_email,user_pass):

    exists = db.session.query(User.id).filter_by(email=user_email).scalar() is not None
    if exists == False:
        #response_body = {
        #    "msg": "Hello, this is your GET /user response - email = " + user_email + " pass = " + user_pass,
        #    "exists": str(exists),
        #    'jwt': create_jwt(identity=str(user_email))
        #}

        #add user info to db
        data = User(email=user_email,password=user_pass,is_active=True)

        db.session.add(data)
        db.session.flush()
        db.session.commit()

        
        ret = {'jwt': create_jwt(identity=user.id),
        "data-processed":data
        }
        return jsonify(ret), 200

    else:
        response_body = {
            "msg": "Hello, this is your POST /process-new-user/ response - email = " + user_email + " pass = " + user_pass,
            "exists": str(exists) + " this email is already in use"
        }
        return jsonify(response_body), 200
   

# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = User.query.filter_by(email = username,password = password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=user.id)}
    return jsonify(ret), 200

# Protect a view with jwt_required, which requires a valid jwt
# to be present in the headers.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify({'hello_from': get_jwt_identity()}), 200

@app.route('/user', methods=['GET','POST'])
@jwt_required
def getuser():
    if request.method == "GET":
        # Access the identity of the current user with get_jwt_identity
        user_id = get_jwt_identity()
        # get user by id
        user_query = User.query.get(user_id)

        #get user db info and return
        all_user_info = (user_query.serialize())
        return jsonify(all_user_info), 200
    #if request.method == "POST"


@app.route('/babies', methods=['POST','GET','DELETE'])
@jwt_required
def addbaby():

    #/<string:user_id>/<string:babyFirstName>/<string:babyLastName>/<string:dob>/<string:timeZone>/<string:gender>
    #user_id,babyFirstName,babyLastName,dob,timeZone,gender
    if request.method == "GET":
        return jsonify("not implemented"),501
    elif request.method == 'POST':
        params = request.get_json()
        user_id = get_jwt_identity()
        new_baby = Baby(
            parent_id=user_id,
            first_name=params["first_name"],
            last_name=params["last_name"],
            dob_baby=params["dob_baby"],
            time_zone=params["time_zone"],
            baby_gender=params["baby_gender"]
        )
        db.session.add(new_baby)
        try:
            db.session.commit()
            return jsonify(new_baby.serialize()),201
        except Exception as error:
            db.session.rollback()
            print(error)
            return jsonify(error), 500

    elif request.method == "DELETE":
        params = request.get_json()
        user_id = get_jwt_identity()
        babyID = params["baby_id"]


        #baby1 = db.session.query(Baby.id).filter_by(id=babyID)
        baby1 = Baby.query.get(babyID)
        if baby1 is None:
            raise APIException('baby not found = '+str(babyID), status_code=404)
        db.session.delete(baby1)
        db.session.commit()
        return jsonify(str(baby1)), 200

@app.route('/alarm', methods=['POST','GET','DELETE'])
#@jwt_required
def alarm():
    params = request.get_json()
    user_id = get_jwt_identity()
    if request.method == "GET":
        return jsonify("not implemented"),501

    elif request.method == "DELETE":
        return jsonify("not implemented"),501

    elif request.method == "POST":
        if params is None:
            print(str(params))
            raise APIException('params empty', status_code=404)
        new_alarm = Alarm(
            baby_id =params["baby_id"],
            crying = params["crying"],
            decibel_level = params["decibel_level"],
            overheated = params["overheated"],
            breathing = params["breathing"],
            face_down = params["face_down"],
            out_of_crib = params["out_of_crib"],
            is_active = params["is_active"]
        )
        print(str(new_alarm))
        db.session.add(new_alarm)
        try:
            db.session.commit()
            return jsonify(new_alarm.serialize()),201
        except Exception as error:
            db.session.rollback()
            print(str(error))
            return jsonify(str(error)), 500


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
