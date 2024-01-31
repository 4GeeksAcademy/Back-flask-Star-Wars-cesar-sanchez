"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Vehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#a partir de aquí ENDPOINTS##########################
@app.route('/users', methods=['GET'])
def handle_hello():
    
    users_query = User.query.all() # estamos haciendo una consulta a la tabla User para que traiga a todos
    users_data = list(map(lambda item: item.serialize(),users_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    print(users_data)
    print(users_query)

    response_body = {
        "msg": "ok ",
        "users" : users_data
    }

    return jsonify(response_body), 200

@app.route('/persons', methods=['GET'])
def get_all_persons():
    
    persons_query = Person.query.all() # estamos haciendo una consulta a la tabla User para que traiga a todos
    persons_data = list(map(lambda item: item.serialize(),persons_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
   # print(persons_data)
    print(persons_query)

    response_body = {
        "msg": "ok ",
        "persons": persons_data
    }

    return jsonify(response_body), 200    

@app.route('/planets', methods=['GET'])
def get_all_planets():
    
    planets_query = Planet.query.all() # estamos haciendo una consulta a la tabla User para que traiga a todos
    planets_data = list(map(lambda item: item.serialize(),planets_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
   # print(persons_data)
    print(planets_query)

    response_body = {
        "msg": "ok ",
        "planets" : planets_data
    }

    return jsonify(response_body), 200      

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    
    vehicles_query = Vehicle.query.all() # estamos haciendo una consulta a la tabla User para que traiga a todos
    vehicles_data = list(map(lambda item: item.serialize(),vehicles_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
   # print(persons_data)
    print(vehicles_query)

    response_body = {
        "msg": "ok ",
        "vehicles" : vehicles_data
    }

    return jsonify(response_body), 200    



@app.route('/persons/<int:id>', methods=['GET'])
def person(id):
    
    person_query = Person.query.filter_by(id = id).first() # estamos haciendo una consulta a la tabla User para que traiga a todos
    person_data = person_query.serialize()#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    print(person_data)
    print(person_query)

    response_body = {
        "msg": "ok ",
        "person" : person_data
    }

    return jsonify(response_body), 200  

@app.route('/planets/<int:id>', methods=['GET'])
def planet(id):
    
    planet_query = Planet.query.filter_by(id = id).first() # estamos haciendo una consulta a la tabla User para que traiga a todos
    planet_data = planet_query.serialize()#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    print(planet_data)
    print(planet_query)

    response_body = {
        "msg": "ok ",
        "planet" : planet_data
    }

    return jsonify(response_body), 200      

@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicle(id):
    
    vehicle_query = Vehicle.query.filter_by(id = id).first() # estamos haciendo una consulta a la tabla User para que traiga a todos
    vehicle_data = vehicle_query.serialize()#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    print(vehicle_data)
    print(vehicle_query)

    response_body = {
        "msg": "ok ",
        "planet" : vehicle_data
    }

    return jsonify(response_body), 200          



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

