from marshmallow import fields
from marshmallow.validate import Length
from main import ma

class UserSchema(ma.Schema):
    class Meta:
        #model = User
        fields = ['id', 'email', 'password', 'admin', 'campaigns']
        load_only = ['password', 'admin']
    #set the password's length to a minimum of 6 characters
    email = fields.Email(required=True)
    password = fields.String(validate=Length(min=6, error='Password must be at least 6 characters long'), required=True)
    campaigns = fields.List(fields.Nested("CampaignSchema", exclude=("user",)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)