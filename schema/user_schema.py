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