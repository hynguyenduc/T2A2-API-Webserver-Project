from main import db

class Character(db.Model):
    # define the table name for the db
    __tablename__= "characters"

    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    name = db.Column(db.String(), nullable=False)
    race = db.Column(db.String(), nullable=False)
    char_class = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date())
    str_stat = db.Column(db.Integer(), nullable=False)
    dex_stat = db.Column(db.Integer(), nullable=False)
    con_stat = db.Column(db.Integer(), nullable=False)
    int_stat = db.Column(db.Integer(), nullable=False)
    wis_stat = db.Column(db.Integer(), nullable=False)
    cha_stat = db.Column(db.Integer(), nullable=False)
    # two foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable=False)
    user = db.relationship(
        "User",
        back_populates="characters"
    )
    campaign = db.relationship(
        "Campaign",
        back_populates="characters"
    )