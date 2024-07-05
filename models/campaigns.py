from main import db

class Campaign(db.Model):
    # define the table name for the db
    __tablename__= "campaigns"
    # Set the primary key
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
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