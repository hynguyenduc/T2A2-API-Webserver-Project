from marshmallow import fields
from main import ma


# Marshmallow Campaign Schema, it will provide the serialization needed for converting the data into JSON
class CampaignSchema(ma.Schema):
    class Meta:
        ordered = True
        # Fields to expose
        fields = ("id", "name", "description", "date", "user", "characters")
    user = fields.Nested("UserSchema", only=("email",))
    characters = fields.List(fields.Nested("CharacterSchema"))


#single campaign schema, when one campaign needs to be retrieved
campaign_schema = CampaignSchema()
#multiple campaign schema, when many campaigns need to be retrieved
campaigns_schema = CampaignSchema(many=True)