from main import db

class Campaign(db.Model):
    # define the table name for the db
    __tablename__= "campaigns"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    date = db.Column(db.Date())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "User", 
        back_populates="campaigns"
    )
    characters = db.relationship(
        "Character",
        back_populates="campaign",
        cascade="all, delete"
    )