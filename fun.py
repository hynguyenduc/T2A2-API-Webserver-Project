from controllers.campaign_controller import campaigns
# from controllers.character_controller import characters
from controllers.auth_controller import auth

registerable_controllers = [
    auth,
    campaigns,
    # character
]

from datetime import timedelta
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token
from main import db, bcrypt
from schema.user_schema import user_schema, users_schema
from models.users import User

auth = Blueprint('auth', __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def auth_register():
    # The request data will be loaded in a user_schema converted to JSON. request needs to be imported from
    user_fields = user_schema.load(request.json)
    # find the user
    stmt = db.select(User).filter_by(email=user_fields["email"])
    user = db.session.scalar(stmt)

    if user:
        # return an abort message to inform the user. That will end the request
        return abort(400, description="Email already registered")
    # Create the user object
    user = User()
    #Add the email attribute
    user.email = user_fields["email"]
    #Add the password attribute hashed by bcrypt
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    #set the admin attribute to false
    user.admin = False
    #Add it to the database and commit the changes
    db.session.add(user)
    db.session.commit()
    #create a variable that sets an expiry date
    expiry = timedelta(days=1)
    #create the access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # return the user email and the access token
    return jsonify({"user":user.email, "token": access_token })
    #return "User registered"


@auth.route("/login", methods=["POST"])
def auth_login():
    #get the user data from the request
    user_fields = user_schema.load(request.json)
    #find the user in the database by email
    stmt = db.select(User).filter_by(email=user_fields["email"])
    user = db.session.scalar(stmt)
    # there is not a user with that email or if the password is not correct send an error
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")

    #create a variable that sets an expiry date
    expiry = timedelta(days=1)
    #create the access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # return the user email and the access token
    return jsonify({"user":user.email, "token": access_token })
    #return "user logged in"

from datetime import date
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from main import db
from models.campaigns import Campaign
from models.users import User
from models.characters import Character
from schema.campaign_schema import campaign_schema, campaigns_schema
from schema.user_schema import users_schema
from schema.character_schema import character_schema, characters_schema

campaigns = Blueprint('campaigns', __name__, url_prefix="/campaigns")

# Error handling 
# @campaigns.errorhandler(KeyError)
# def key_error(e):
#     return jsonify({'error': f'The field {e} is required'}), 400

# @campaigns.errorhandler(BadRequest)
# def default_error(e):
#     return jsonify({'error': e.description}), 400

# @campaigns.errorhandler(ValidationError)
# def validation_error(e):
#     return jsonify(e.messages), 400

# The GET route endpoints

#GET one campaign
@campaigns.route("/<int:id>/", methods=["GET"])
def get_campaign(id):
    stmt = db.select(Campaign).filter_by(id=id)
    campaign = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not campaign:
        return abort(400, description= "Campaign does not exist")
    # Convert the campaigns from the database into a JSON format and store them in result
    result = campaign_schema.dump(campaign)
    # return the data in JSON format
    return jsonify(result)

#GET all campaigns
@campaigns.route("/", methods=["GET"])
def get_campaigns():
    # get all the campaigns from the database table
    stmt = db.select(Card)
    campaigns_list = db.session.scalars(stmt)
    # Convert the campaigns from the database into a JSON format and store them in result
    result = campaigns_schema.dump(campaigns_list)
    # return the data in JSON format
    return jsonify(result)
    #return "List of campaigns retrieved"

# @campaigns.route("/search", methods=["GET"])
# def search_campaigns():
#     # return the content of the query string
#     return request.query_string

# @campaigns.route("/search", methods=["GET"])
# def search_campaigns():
#     # return the content of the query string
#     return request.args.get('priority')

@campaigns.route("/search", methods=["GET"])
def search_campaigns():
    # create an empty list in case the query string is not valid
    campaigns_list = []

    if request.args.get('priority'):
        stmt = db.select(Card).filter_by(priority= request.args.get('priority'))
        campaigns_list = db.session.scalars(stmt)
    elif request.args.get('status'):
        stmt = db.select(Card).filter_by(status= request.args.get('status'))
        campaigns_list = db.session.scalars(stmt)

    result = campaigns_schema.dump(campaigns_list)
    # return the data in JSON format
    return jsonify(result)

@campaigns.route("/users", methods=["GET"])
def get_users():
    # get all the users from the database table
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    # Convert the users from the database into a JSON format and store them in result
    result = users_schema.dump(users_list)
    # return the data in JSON format
    return jsonify(result)

# The POST route endpoint
@campaigns.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_card(id):
    # #Create a new card
    card_fields = card_schema.load(request.json)

    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the card
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Card does not exist")
    #update the car details with the given values
    card.title = card_fields["title"]
    card.description = card_fields["description"]
    card.status = card_fields["status"]
    card.priority = card_fields["priority"]
    # not taken from the request, generated by the server
    card.date = date.today()
    # add to the database and commit
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(card))

# Create a new card
@campaigns.route("/", methods=["POST"])
@jwt_required()
def create_card():
    #Create a new card
    card_fields = card_schema.load(request.json)
    # if 'title' not in card_fields or card_fields['title'] == '':
    #     return jsonify({'error': 'The \'title\' field is required'}), 400

    # get the id from jwt
    user_id = get_jwt_identity()
    new_card = Card()
    new_card.title = card_fields["title"]
    new_card.description = card_fields["description"]
    new_card.status = card_fields["status"]
    new_card.priority = card_fields["priority"]
    # not taken from the request, generated by the server
    new_card.date = date.today()
    # Use that id to set the ownership of the card
    new_card.user_id = user_id
    # add to the database and commit
    db.session.add(new_card)
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(new_card))
    #return "Card created"

#POST a new comment
@campaigns.route("/<int:id>/comments", methods=["POST"])
# logged in user required
@jwt_required()
# Card id required to assign the comment to a car
def post_comment(id):
    # #Create a new comment
    comment_fields = comment_schema.load(request.json)

    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")

    # find the card
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Card does not exist")
    #create the comment with the given values
    new_comment = Comment()
    new_comment.message = comment_fields["message"]
    # Use the card gotten by the id of the route
    new_comment.card = card
    # Use that id to set the ownership of the card
    new_comment.user_id = user_id
    # add to the database and commit
    db.session.add(new_comment)
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(card))


# Finally, we round out our CRUD resource with a DELETE method
@campaigns.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_card(id):
    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the card
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Card doesn't exist")
    #Delete the card from the database and commit
    db.session.delete(card)
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(card))
    #return "Card Deleted"


from main import db

class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date())
    description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship(
        "User", 
        back_populates="campaigns"
    )
    characters = db.relationship(
        "Character", 
        back_populates="campaign", 
        cascade="all, delete"
    )


from main import db

class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    race = db.Column(db.String(), nullable=False)
    char_class = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date())
    str_stat = db.Column(db.Integer(), nullable=False)
    dex_stat = db.Column(db.Integer(), nullable=False)
    con_stat = db.Column(db.Integer(), nullable=False)
    int_stat = db.Column(db.Integer(), nullable=False)
    wis_stat = db.Column(db.Integer(), nullable=False)
    cha_stat = db.Column(db.Integer(), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship(
        "User",
        back_populates="characters"
    )
    
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    campaign = db.relationship(
        "Campaign", 
        back_populates="characters"
    )


from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    # username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    characters = db.relationship(
        "Character", 
        backref="user", 
        cascade="all, delete"
        )
    campaigns = db.relationship(
        "Campaign",
        back_populates="user", 
        cascade="all, delete"
    )


from marshmallow import fields
from marshmallow.validate import Length
from main import ma

class CampaignSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'date_created', 'description', 'user', 'characters']
    user = fields.Nested("UserSchema", only=("email",))
    characters = fields.List(fields.Nested("CharacterSchema", only=("name",)))

    name = fields.String(required=True)
    
campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)


from marshmallow import fields
from marshmallow.validate import Length, Regexp, And, OneOf
from main import ma

VALID_RACES = ('half orc', 'elf', 'human', 'gnome', 'halfling', 'dragon born', 'dwarf')
VALID_CLASSES = ('barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin', 'ranger', 'rogue', 'sorcerer', 'warlock', 'wizard')
VALID_STATS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)

class CharacterSchema(ma.Schema):
    class Meta:
        
        fields = ['id', 'Creator', 'name', 'race', 'char_class', 'date_created', 'str_stat', 'dex_stat', 'con_stat', 'int_stat', 'wis_stat', 'cha_stat']
    
    Creator = fields.Nested('UserSchema',  only=('email',))

    race = fields.String(required=True, validate=OneOf(VALID_RACES))
    char_class = fields.String(required=True, validate=OneOf(VALID_CLASSES))
    
    str_stat = fields.Integer(required=True, validate=And(
        Regexp('^[0-9]+$', error='Only numbers between 1-20'), 
        Length(min=1, max=2, error="Only numbers between 1-20")
        ))   
    dex_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    con_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    int_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    wis_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    cha_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))


# single character schema, when one profile needs to be retrieved
character_schema = CharacterSchema()
# multiple character schema, when many profiles need to be retrieved
characters_schema = CharacterSchema(many=True)

from marshmallow import fields
from marshmallow.validate import Length
from main import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'email', 'password', 'admin', 'campaign', 'character']
        load_only = ['password', 'admin']
    password = fields.String(validate=Length(min=8, error='Password must be at least 8 characters long'), required=True)
    # characters = fields.List(fields.Nested("CharacterSchema", exclude=("user",))) 
    campaigns = fields.List(fields.Nested("CampaignSchema", exclude=("user",)))
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)


from main import db
from flask import Blueprint
from main import bcrypt
from models.campaigns import Campaign
from models.characters import Character
from models.users import User
from datetime import date

db_commands = Blueprint("db", __name__)

# create app's cli command named create, then run it in the terminal as "flask db create", 
# it will invoke create_db function
@db_commands.cli.command("autofill")
def auto_generate():
    db.drop_all()
    db.create_all()
    print ("Created tables")

    # create admin user and user1    
    admin_user = User(
        email = "admin@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8"),
        admin = True
    )
    db.session.add(admin_user)

    user1 = User(
        email = "user1@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8")
    )
    db.session.add(user1)
    # This extra commit will end the transaction and generate the ids for the user
    db.session.commit()

    # create the card object
    campaign1 = Campaign(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "sample campaign 1",
        description = "",
        date_created = date.today(),
        user_id = user1.id

    )
    # Add the object as a new row to the table
    db.session.add(campaign1)
    # commit the changes
    db.session.commit()

    character1 = Character(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "Ogmire",
        race = "half-orc",
        char_class = "barbarian",
        str_stat = 10,
        dex_stat = 14,
        con_stat = 12,
        int_stat = 16,
        wis_stat = 8,
        cha_stat = 10,
        date = date.today(),
        user_id = user1.id,
        campaign = campaign1
 
    )
    # Add the object as a new row to the table
    db.session.add(character1)

    # commit the changes
    db.session.commit()

    print("Users, Campaigns and Characters added") 

@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands .cli.command("seed")
def seed_db():
    # create admin user and user1    
    admin_user = User(
        email = "admin@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8"),
        admin = True
    )
    db.session.add(admin_user)

    user1 = User(
        email = "user1@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8")
    )
    db.session.add(user1)
    # This extra commit will end the transaction and generate the ids for the user
    db.session.commit()

    # create the card object
    campaign1 = Campaign(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "sample campaign 1",
        description = "",
        date_created = date.today(),
        user_id = user1.id

    )
    # Add the object as a new row to the table
    db.session.add(campaign1)
    # commit the changes
    db.session.commit()

    character1 = Character(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "Ogmire",
        race = "half-orc",
        char_class = "barbarian",
        str_stat = 10,
        dex_stat = 14,
        con_stat = 12,
        int_stat = 16,
        wis_stat = 8,
        cha_stat = 10,
        date = date.today(),
        # user = user1
        user_id = user1.id
 
    )
    # Add the object as a new row to the table
    db.session.add(character1)

    # commit the changes
    db.session.commit()

    print("Table seeded") 

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")