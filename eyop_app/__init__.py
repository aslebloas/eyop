#!/usr/bin/env python3
"""App package and initialization of the flask app & db object"""
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create Flask app
app = Flask(__name__)

# Get configuration
app.config.from_object(Config)

# Create db object
db = SQLAlchemy(app)
db.create_all()

# Set up migration engine
migrate = Migrate(app, db)

from eyop_app import routes, models
