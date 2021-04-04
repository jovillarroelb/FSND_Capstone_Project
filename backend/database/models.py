import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# Environment variable method to connect to the database
DB_HOST = os.getenv("DB_HOST", "127.0.0.1:5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "fsnd-jvb")
DB_PATH = "postgresql+psycopg2://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Comment the lines below if the migrations are intended.

    # db.app = app
    # db.init_app(app)
    # db.create_all()

    return app
    
"""
Managers
"""


class Manager(db.Model):
    __tablename__ = "managers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)

    # # Relationships:
    # projects = db.relationship("Project", backref=("managers"))

    def __init__(self, name, lastname, phone, email):
        self.name = name
        self.lastname = lastname
        self.phone = phone
        self.email = email

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.city,
            "phone": self.state,
            "email": self.phone,
            # "projects": self.projects,  # convert string to list
        }

    # def __repr__(self):
    #     return f"<Manager {self.id} {self.name}>"


"""
Project

"""


class Project(db.Model):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    # manager_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey("managers.id"),
    #     nullable=False,
    # )  # Child
    manager_id = Column(Integer)
    name = Column(String)
    country = Column(String)
    city = Column(String)
    address = Column(String)
    category = Column(Integer)
    description = Column(String)

    def __init__(
        self,
        manager_id,
        name,
        country,
        city,
        address,
        category,
        description,
    ):
        self.name = name
        self.country = country
        self.manager_id = manager_id
        self.city = city
        self.address = address
        self.category = category
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "manager_id": self.manager_id,
            "name": self.question,
            "country": self.answer,
            "city": self.category,
            "address": self.difficulty,
            "description": self.description,
        }


"""
Category: List of categories of projects (1: Residential, 2: Retail, 
3: Industrial)

"""


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            "id": self.id,
            "type": self.type,
        }
