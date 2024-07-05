from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, Regexp, And
from marshmallow.exceptions import ValidationError
from models.campaigns import Campaign
from main import ma


VALID_PRIORITIES = ('Urgent', 'High', 'Low', 'Medium')
VALID_STATUSES = ('To Do', 'Done', 'Ongoing', 'Testing', 'Deployed')

#create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class CampaignSchema(ma.Schema):
    class Meta:
        ordered = True
        # Fields to expose
        fields = ("id", "name", "date", "user", "characters")
    user = fields.Nested("UserSchema", only=("email",))
    characters = fields.List(fields.Nested("CharacterSchema"))
    # # title = fields.String(required=True, validate=Length(min=1, error='Title cannot be blank'))
    # title = fields.String(required=True, validate=And(Length(min=1), Regexp('^[a-zA-Z0-9 ]+$')))
    # status = fields.String(required=True, validate=And(OneOf(VALID_STATUSES, error='You suck'), ))
    # # priority = fields.String(required=True, validate=OneOf(VALID_PRIORITIES))
    # priority = fields.String(load_default='Medium', validate=OneOf(VALID_PRIORITIES))

    # @validates('status')
    # def validate_status(self, value):
    #     # Only apply this validator if the attempted status is 'Ongoing'
    #     if value == 'Ongoing':
    #         # Get a count of cards that already have the 'Ongoing' status
    #         count = Campaign.query.filter_by(status='Ongoing').count()
    #         if count > 1:
    #             raise ValidationError('You already have an ongoing card')


#single card schema, when one card needs to be retrieved
campaign_schema = CampaignSchema()
#multiple card schema, when many cards need to be retrieved
campaigns_schema = CampaignSchema(many=True)