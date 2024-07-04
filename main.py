from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
# db = SQLALchemy(model_class=Base)
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    
    # Flask app object 
    app = Flask(__name__)

    # app configuration
    app.config.from_object("config.app_config")
    app.json.sort_keys = False

    # Database object that allows use of SQLAlchemy ORM
    db.init_app(app)

    # Marshmallow object that allow use of schemas
    ma.init_app(app)

    # Jwt and bcrypt objects that allow for authentication process
    bcrypt.init_app(app)
    jwt.init_app(app)

    # commands
    from commands import db_commands
    app.register_blueprint(db_commands)

    # import the controllers and activate blueprints
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
