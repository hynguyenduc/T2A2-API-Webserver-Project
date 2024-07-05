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
from schema.character_schema import character_schema


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


# !!!!!!!!!!!!!!!!!!!!
# The GET routes endpoint
@campaigns.route("/<int:id>/", methods=["GET"])
def get_campaign(id):
    stmt = db.select(Campaign).filter_by(id=id)
    campaign = db.session.scalar(stmt)
    #return an error if the campaign doesn't exist
    if not campaign:
        return abort(400, description= "Campaign does not exist")
    # Convert the campaigns from the database into a JSON format and store them in result
    result = campaign_schema.dump(campaign)
    # return the data in JSON format
    return jsonify(result)

# !!!!!!!!!!!!!!!!!!!!
@campaigns.route("/", methods=["GET"])
def get_campaigns():
    # get all the campaigns from the database table
    stmt = db.select(Campaign)
    campaigns_list = db.session.scalars(stmt)
    # Convert the campaigns from the database into a JSON format and store them in result
    result = campaigns_schema.dump(campaigns_list)
    # return the data in JSON format
    return jsonify(result)
    #return "List of campaigns retrieved"

# !!!!!!!!!!!!!!!!!
@campaigns.route("/search", methods=["GET"])
def search_campaigns():
    # create an empty list in case the query string is not valid
    campaigns_list = []

    if request.args.get('name'):
        stmt = db.select(Campaign).filter_by(name= request.args.get('name'))
        campaigns_list = db.session.scalars(stmt)
    elif request.args.get('description'):
        stmt = db.select(Campaign).filter_by(description= request.args.get('description'))
        campaigns_list = db.session.scalars(stmt)

    result = campaigns_schema.dump(campaigns_list)
    # return the data in JSON format
    return jsonify(result)

# !!!!!!!!!!!!!!!!!!
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
#!!!!!!!!!!!!!!!!!!!!!
@campaigns.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_campaign(id):
    # #Create a new campaign
    campaign_fields = campaign_schema.load(request.json)

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
    # find the campaign
    stmt = db.select(Campaign).filter_by(id=id)
    campaign = db.session.scalar(stmt)
    #return an error if the campaign doesn't exist
    if not campaign:
        return abort(400, description= "Campaign does not exist")
    #update the car details with the given values
    campaign.name = campaign_fields["name"]
    campaign.description = campaign_fields["description"]
    # not taken from the request, generated by the server
    campaign.date = date.today()
    # add to the database and commit
    db.session.commit()
    #return the campaign in the response
    return jsonify(campaign_schema.dump(campaign))

# Create a new campaign !!!!!!!!!!!!!!!!!!!!!!
@campaigns.route("/", methods=["POST"])
@jwt_required()
def create_campaign():
    #Create a new campaign
    campaign_fields = campaign_schema.load(request.json)

    # get the id from jwt
    user_id = get_jwt_identity()
    new_campaign = Campaign()
    new_campaign.name = campaign_fields["name"]
    new_campaign.description = campaign_fields["description"]
    # not taken from the request, generated by the server
    new_campaign.date = date.today()
    # Use that id to set the ownership of the campaign
    new_campaign.user_id = user_id
    # add to the database and commit
    db.session.add(new_campaign)
    db.session.commit()
    #return the campaign in the response
    return jsonify(campaign_schema.dump(new_campaign))
    #return "Campaign created"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!
#POST a new character
@campaigns.route("/<int:id>/characters", methods=["POST"])
# logged in user required
@jwt_required()
# Campaign id required to assign the character to a car
def post_character(id):
    # #Create a new character
    character_fields = character_schema.load(request.json)

    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")

    # find the campaign
    stmt = db.select(Campaign).filter_by(id=id)
    campaign = db.session.scalar(stmt)
    #return an error if the campaign doesn't exist
    if not campaign:
        return abort(400, description= "Campaign does not exist")
    #create the character with the given values
    new_character = Character()
    new_character.name = character_fields["name"]
    new_character.race = character_fields["race"]
    new_character.char_class = character_fields["char_class"]
    new_character.str_stat = character_fields["str_stat"]
    new_character.dex_stat = character_fields["dex_stat"]
    new_character.con_stat = character_fields["con_stat"]
    new_character.int_stat = character_fields["int_stat"]
    new_character.wis_stat = character_fields["wis_stat"]
    new_character.cha_stat = character_fields["cha_stat"]
    # Use the campaign gotten by the id of the route
    new_character.campaign = campaign
    # Use that id to set the ownership of the campaign
    new_character.user_id = user_id
    # add to the database and commit
    db.session.add(new_character)
    db.session.commit()
    #return the campaign in the response
    return jsonify(campaign_schema.dump(campaign))

# !!!!!!!!!
# Finally, we round out our CRUD resource with a DELETE method
@campaigns.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_campaign(id):
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
    # find the campaign
    stmt = db.select(Campaign).filter_by(id=id)
    campaign = db.session.scalar(stmt)
    #return an error if the campaign doesn't exist
    if not campaign:
        return abort(400, description= "Campaign doesn't exist")
    #Delete the campaign from the database and commit
    db.session.delete(campaign)
    db.session.commit()
    #return the campaign in the response
    return "Campaign Deleted"