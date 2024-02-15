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
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager



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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#a partir de aquí ENDPOINTS##########################

#todos los usuarios
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

#todas las personas
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
    
#todos los planetas
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
      
#todos los vehiculos
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


#persona por su id
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
    
#planeta por su id
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

#vehículo por su id
@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicle(id):
    
    vehicle_query = Vehicle.query.filter_by(id = id).first() # estamos haciendo una consulta a la tabla User para que traiga a todos
    vehicle_data = vehicle_query.serialize()#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
    print(vehicle_data)
    print(vehicle_query)

    response_body = {
        "msg": "ok ",
        "vehicle" : vehicle_data
    }

    return jsonify(response_body), 200    

#mostramos todos los favoritos de un usuario     
#@app.route('/users/<int:user_id>/favourites', methods=['GET'])
#def get_all_favourites(user_id):
    
 #   favourite_query = Favourite.query.filter_by(user_id = user_id).all() # estamos haciendo una consulta a la tabla User para que traiga a todos
  #  favourite_data = list(map(lambda item: item.serialize(),favourite_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
   

   # response_body = {
    #    "msg": "ok ",
     #   "favourite" +str(user_id): favourite_data
    #}

    #return jsonify(response_body), 200


#POST para crear un nuevo planeta favorito
#@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
#def add_planet_favorite(planet_id):
    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
    #body = request.json
    #user_id = body.get("user_id")

    #if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y la persona específicos.
     #   delete_favorite = Favourite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

      #  if delete_favorite:
            # Si se encuentra un registro existente, elimínalo.
       #     db.session.delete(delete_favorite)
        #    db.session.commit()

        # Crear un nuevo favorito para la persona.
        #new_planet_favorite = Favourite(user_id=user_id, planet_id=planet_id)
        #db.session.add(new_planet_favorite)
        #db.session.commit()

       #return jsonify({"msg": "Planet favorite added successfully"}), 200
    #else:
     #   return jsonify({"error": "user_id not provided in the request body"}), 400

#POST para crear una nueva persona favorita
#@app.route('/favorite/people/<int:person_id>', methods=['POST'])
#def add_person_favorite(person_id):
    # Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
 #   body = request.json
  #  user_id = body.get("user_id")

   # if user_id is not None:
        # Intenta obtener una instancia existente de Favourite para el usuario y la persona específicos.
    #    existing_favorite = Favourite.query.filter_by(user_id=user_id, person_id=person_id).first()

     #   if existing_favorite:
            # Si se encuentra un registro existente, elimínalo.
      #      db.session.delete(existing_favorite)
       #     db.session.commit()

        # Crear un nuevo favorito para la persona.
        #new_person_favorite = Favourite(user_id=user_id, person_id=person_id)
        #db.session.add(new_person_favorite)
        #db.session.commit()

        #return jsonify({"msg": "Person favorite added successfully"}), 200
    #else:
     #   return jsonify({"error": "user_id not provided in the request body"}), 400
    
# POST para crear un nuevo vehiculo favorito
#  @app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
#  def add_vehicle_favorite(vehicle_id):
#      Asegúrate de tener el user_id disponible en el cuerpo de la solicitud.
#     body = request.json
#     user_id = body.get("user_id")

#     if user_id is not None:
#          Intenta obtener una instancia existente de Favourite para el usuario y el vehículo específico.
#         existing_favorite = Favourite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

#         if existing_favorite:
#              Si se encuentra un registro existente, elimínalo.
#             db.session.delete(existing_favorite)
#             db.session.commit()

#          Crear un nuevo cvehículo favorito
#          new_vehicle_favorite = Favourite(user_id=user_id, vehicle_id=vehicle_id)
#          db.session.add(new_vehicle_favorite)
#          db.session.commit()

#          return jsonify({"msg": "Vehicle favorite added successfully"}), 200
#      else:
#         return jsonify({"error": "user_id not provided in the request body"}), 400

    
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


#LOGIN
@app.route("/login", methods=["POST"])
def login():
    # body = request.json
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user_query = User.query.filter_by(email=email).first()

    #print(user_query.email)



    if email != user_query.email or password != user_query.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

#ver los favoritos de todos los usuarios
@app.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_all_favourites():

    current_user = get_jwt_identity()
    
    user_query = User.query.filter_by(email = current_user).first()
    
    
    favourite_query = Favourite.query.filter_by(user_id = user_query.id).all() # estamos haciendo una consulta a la tabla User para que traiga a todos
    
    favourite_data = list(map(lambda item: item.serialize(),favourite_query))#PROCESAMOS LA INFO CONSULTADA Y LA VOLVEMOS UN ARRAY DE OBJETOS
   

    response_body = {
        "msg": "ok ",
        "favourite" : favourite_data
    }

    return jsonify(response_body), 200


#añadir un nuevo planeta favorito
@app.route('/favorite/planet', methods=['POST'])
@jwt_required()
def add_planet_favorite():
    current_user_email = get_jwt_identity()

    # Validación adicional si es necesario
    if not current_user_email:
        response_body = {
            "error": "El email de usuario no está presente en el token",
        }
        return jsonify(response_body), 400

    user_query = User.query.filter_by(email=current_user_email).first()

    if user_query is None:
        response_body = {
            "error": "Usuario no encontrado",
        }
        return jsonify(response_body), 404

    # Obtén los datos del planeta
    planet_data = request.json.get('planet_data')

    # Verifica si el planeta ya existe
    existing_planet = Planet.query.filter_by(name=planet_data['name']).first()

    if existing_planet is None:
        # Si el planeta no existe, muestro un mensaje de error
       
        response_body = {
            "error": "Planeta no encontrado",
        }
        return jsonify(response_body), 404

    # Crea un nuevo objeto Favourite para el usuario actual y el planeta existente
    new_favorite = Favourite(user_id=user_query.id, planet_id=existing_planet.id)

    # Agrega el nuevo favorito a la base de datos
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Planeta añadido como favorito correctamente",
        "favourite": new_favorite.serialize()
    }

    return jsonify(response_body), 200

#añadir una nueva persona favorita
@app.route('/favorite/person', methods=['POST'])
@jwt_required()
def add_person_favorite():
    current_user_email = get_jwt_identity()

    # Validación adicional si es necesario
    if not current_user_email:
        response_body = {
            "error": "El email de usuario no está presente en el token",
        }
        return jsonify(response_body), 400

    user_query = User.query.filter_by(email=current_user_email).first()

    if user_query is None:
        response_body = {
            "error": "Usuario no encontrado",
        }
        return jsonify(response_body), 404

    # Obtén los datos de la persona
    person_data = request.json.get('person_data')

    # Verifica si la persona existe
    existing_person = Person.query.filter_by(name=person_data['name']).first()

    if existing_person is None:
        # Si la persona no existe, muestro un mensaje de error
       
        response_body = {
            "error": "Persona no encontrada",
        }
        return jsonify(response_body), 404

    # Crea un nuevo objeto Favourite para el usuario actual y el planeta existente
    new_favorite = Favourite(user_id=user_query.id, person_id=existing_person.id)

    # Agrega el nuevo favorito
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Persona añadida como favorito correctamente",
        "favourite": new_favorite.serialize()
    }

    return jsonify(response_body), 200

#añadir un nuevo vehículo favorito
@app.route('/favorite/vehicle', methods=['POST'])
@jwt_required()
def add_vehicle_favorite():
    current_user_email = get_jwt_identity()

    # Validación adicional si es necesario
    if not current_user_email:
        response_body = {
            "error": "El email de usuario no está en el token",
        }
        return jsonify(response_body), 400

    user_query = User.query.filter_by(email=current_user_email).first()

    if user_query is None:
        response_body = {
            "error": "Usuario no encontrado",
        }
        return jsonify(response_body), 404

    # Obtén los datos del vehiculo
    vehicle_data = request.json.get('vehicle_data')

    # Verifica si el vehículo ya existe
    existing_vehicle = Vehicle.query.filter_by(name=vehicle_data['name']).first()

    if existing_vehicle is None:
        # Si el vehiculo no existe, muestro un mensaje de error
       
        response_body = {
            "error": "Planeta no encontrado",
        }
        return jsonify(response_body), 404

    # Crea un nuevo objeto Favourite para el usuario actual y el vehículo existente
    new_favorite = Favourite(user_id=user_query.id, vehicle_id=existing_vehicle.id)

    # Agrega el nuevo favorito a la base de datos
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Vehiculo añadido como favorito correctamente",
        "favourite": new_favorite.serialize()
    }

    return jsonify(response_body), 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    info_profile = User.query.filter_by(email=current_user).first()

    return jsonify({"user":info_profile.serialize()}), 200

# this only runs if `$ python src/app.py` is executed





if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

