from marshmallow import fields
from marshmallow.validate import Length
from main import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'email', 'password', 'admin']
        load_only = ['password', 'admin']
    password = ma.String(validate=Length(min=8, error='Password must be at least 8 characters long', required=True))
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)