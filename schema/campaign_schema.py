from marshmallow import fields
from marshmallow.validate import Length
from main import ma

class CampaignSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'date_created', 'description']
    name = fields.String(required=True)
    
campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)