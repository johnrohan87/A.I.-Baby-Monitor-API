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

@app.route('/getuser/<string:user_email>/', methods=['GET'])
@jwt_required
def getuser(user_email):
    # Access the identity of the current user with get_jwt_identity

    # get only the ones named "Joe"
    user_query = User.query.filter_by(email=user_email).first()
    #print(user_query)
    #print(user_email)
    all_user_info = (user_query.serialize())
    return jsonify(all_user_info), 200

@app.route('/babies', methods=['POST','GET'])
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
