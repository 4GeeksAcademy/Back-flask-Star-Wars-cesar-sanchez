from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favourites =db.relationship('Favourite', backref= 'user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password" : self.password
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    person = db.relationship('Person', backref= 'planet', lazy =True)
    favourites =db.relationship('Favourite', backref= 'planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter" :self.diameter,
            "climate": self.climate,
            "population": self.population,


            # do not serialize the password, its a security breach
        }


class Person(db.Model):
    
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer , nullable=False)
    eye_color = db.Column(db.String(250) , nullable=False)
    hair_color = db.Column(db.String(250) , nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id') ,nullable=True)
    vehicles =db.relationship('Vehicle', backref= 'person', lazy=True)
    favourites =db.relationship('Favourite', backref= 'person', lazy=True)

    

    def __repr__(self):
        return '<Person %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height" :self.height,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,


            # do not serialize the password, its a security breach
        }



class Vehicle(db.Model):
    
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    lenght = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    favourites =db.relationship('Favourite', backref= 'vehicle', lazy=True)



    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model" :self.model,
            "lenght": self.lenght,
            "manufacturer": self.manufacturer,


            # do not serialize the password, its a security breach
        }      
class Favourite(db.Model):
    
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    planet_id= db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)     


    def __repr__(self):
        return '<Favourite %r>' % self.id

    def serialize(self):
        person = Person.query.filter_by(id = self.person_id).first()
        planet = Planet.query.filter_by(id = self.planet_id).first()
        vehicle = Vehicle.query.filter_by(id = self.vehicle_id).first()
        if self.person_id is not None:
             return {
            "id": self.id,
            "user_id": self.user_id,
            "info": person.serialize(),               

        }
        elif self.planet_id is not None:
             return {
            "id": self.id,
            "user_id": self.user_id,
            "info": planet.serialize(),               

        }
        elif self.vehicle_id is not None:

            return {
            "id": self.id,
            "user_id": self.user_id,
            "info": vehicle.serialize(),
             # do not serialize the password, its a security breach
        }      
    
        user= User.query.filter_by(id = self.user_id).first()
        return{
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,

        }
        