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
from models import db, User, Person, Planet, Vehicle, Favourite
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
   # print(persons_query)

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
    #print(persons_data)
    #print(vehicles_query)

    response_body = {
        "msg": "ok ",
        "vehicles" : vehicles_data
    }

    return jsonify(response_body), 200    



@app.route('/persons/<int:id>', methods=['GET'])
def person(id):
    
    person_query = Person.query.filter_by(id = id).first() # estamos haciendo una consulta a la tabla User para que traiga a todos
    person_data = person_query.serialize()#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    #print(person_data)
    #print(person_query)
    if person_query:
        response_body = {
            "msg": "ok ",
            "person" : person_data
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "Persona no encontrada en la base de datos",
            
        }
        return jsonify(response_body), 404

@app.route('/planets/<int:id>', methods=['GET'])
def planet(id):
    
    planet_query = Planet.query.filter_by(id = id).first() # estamos haciendo una consulta a la tabla User para que traiga a todos
    planet_data = planet_query.serialize()#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    #print(planet_data)
    #print(planet_query)

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

#mostramos todos los favoritos de un usuario     
@app.route('/users/<int:user_id>/favourites', methods=['GET'])
def get_all_favourites(user_id):
    
    favourite_query = Favourite.query.filter_by(user_id = user_id).all() # estamos haciendo una consulta a la tabla User para que traiga a todos
    favourite_data = list(map(lambda item: item.serialize(),favourite_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
   

    response_body = {
        "msg": "ok ",
        "favourite" +str(user_id): favourite_data
    }

    return jsonify(response_body), 200


#POST para crear un nuevo planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    body = request.json
    user_id = body.get("user_id")

    if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y la persona específicos.
        delete_favorite = Favourite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if delete_favorite:
            # Si se encuentra un registro existente, elimínalo.
            db.session.delete(delete_favorite)
            db.session.commit()

        # Crear un nuevo favorito para la persona.
        new_planet_favorite = Favourite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_planet_favorite)
        db.session.commit()

        return jsonify({"msg": "Planet favorite added successfully"}), 200
    else:
        return jsonify({"error": "user_id not provided in the request body"}), 400

#POST para crear una nueva persona favorita
@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_person_favorite(person_id):
    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    body = request.json
    user_id = body.get("user_id")

    if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y la persona específicos.
        existing_favorite = Favourite.query.filter_by(user_id=user_id, person_id=person_id).first()

        if existing_favorite:
            # Si se encuentra un registro existente, elimínalo.
            db.session.delete(existing_favorite)
            db.session.commit()

        # Crear un nuevo favorito para la persona.
        new_person_favorite = Favourite(user_id=user_id, person_id=person_id)
        db.session.add(new_person_favorite)
        db.session.commit()

        return jsonify({"msg": "Person favorite added successfully"}), 200
    else:
        return jsonify({"error": "user_id not provided in the request body"}), 400
    
#POST para crear un nuevo vehiculo favorito
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_vehicle_favorite(vehicle_id):
    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    body = request.json
    user_id = body.get("user_id")

    if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y el vehículo específico.
        existing_favorite = Favourite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

        if existing_favorite:
            # Si se encuentra un registro existente, elimínalo.
            db.session.delete(existing_favorite)
            db.session.commit()

        # Crear un nuevo cvehículo favorito
        new_vehicle_favorite = Favourite(user_id=user_id, vehicle_id=vehicle_id)
        db.session.add(new_vehicle_favorite)
        db.session.commit()

        return jsonify({"msg": "Vehicle favorite added successfully"}), 200
    else:
        return jsonify({"error": "user_id not provided in the request body"}), 400

    
#eliminar planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    body = request.json

    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    user_id = body.get("user_id")

    if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y el planeta específicos.
        existing_favorite = Favourite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if existing_favorite:
            # Si se encuentra un registro existente, elimínalo.
            db.session.delete(existing_favorite)
            db.session.commit()
            return jsonify({"msg": "Planet favorite deleted successfully"}), 200
        else:
            return jsonify({"error": "Planet favorite not found"}), 404
    else:
        return jsonify({"error": "Missing user_id in the request body"}), 400
#eliminar persona favorita
@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_person_favorite(person_id):
    body = request.json

    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    user_id = body.get("user_id")

    if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y el planeta específicos.
        existing_favorite = Favourite.query.filter_by(user_id=user_id, person_id=person_id).first()

        if existing_favorite:
            # Si se encuentra un registro existente, elimínalo.
            db.session.delete(existing_favorite)
            db.session.commit()
            return jsonify({"msg": "Person favorite deleted successfully"}), 200
        else:
            return jsonify({"error": "Person favorite not found"}), 404
    else:
        return jsonify({"error": "Missing user_id in the request body"}), 400
    
#eliminar vehicle favorito
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_favorite(vehicle_id):
    body = request.json

    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    user_id = body.get("user_id")

    if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y el planeta específicos.
        existing_favorite = Favourite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

        if existing_favorite:
            # Si se encuentra un registro existente, elimínalo.
            db.session.delete(existing_favorite)
            db.session.commit()
            return jsonify({"msg": "Vehicle favorite deleted successfully"}), 200
        else:
            return jsonify({"error": "Vehicle favorite not found"}), 404
    else:
        return jsonify({"error": "Missing user_id in the request body"}), 400    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

