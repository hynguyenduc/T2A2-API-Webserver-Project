from marshmallow import fields
from marshmallow.validate import Length, Regexp, And, OneOf
from main import ma

VALID_RACES = ('half-orc', 'elf', 'human', 'gnome', 'halfling', 'dragon-born', 'dwarf')
VALID_CLASSES = ('barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin', 'ranger', 'rogue', 'sorcerer', 'warlock', 'wizard')
VALID_STATS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)

class CharacterSchema(ma.Schema):
    class Meta:
        ordered = True
        # Fields to expose
        fields = ("id", 'user', 'name', 'race', 'char_class', 'date', 'str_stat', 'dex_stat', 'con_stat', 'int_stat', 'wis_stat', 'cha_stat')
    user =  fields.Nested("UserSchema", only=("email",)) 
    race = fields.String(required=True, validate=OneOf(VALID_RACES))
    char_class = fields.String(required=True, validate=OneOf(VALID_CLASSES))
     
    str_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    dex_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    con_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    int_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    wis_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20')))
    cha_stat = fields.Integer(required=True, validate=And(OneOf(VALID_STATS, error='Only numbers between 1-20'))) 
      
character_schema = CharacterSchema()

characters_schema = CharacterSchema(many=True)