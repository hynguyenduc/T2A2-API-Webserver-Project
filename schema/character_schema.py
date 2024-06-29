from marshmallow import fields
from marshmallow.validate import Length
from main import ma

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'date_created', 'description', 'str_stat', 'dex_stat', 'con_stat', 'int_stat', 'wis_stat', 'cha_stat']
    str_stat =    


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)