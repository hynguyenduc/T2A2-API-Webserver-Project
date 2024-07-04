from marshmallow import fields
from marshmallow.validate import Length, Regexp
from main import ma

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'date_created', 'description', 'str_stat', 'dex_stat', 'con_stat', 'int_stat', 'wis_stat', 'cha_stat']
    str_stat = fields.Integer(required=True, validate=And(
        Regexp('^[0-9]+$', error='Only numbers between 1-20'), 
        Length(min=1, max=2, error="Only numbers between 1-20")
        ))   


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)