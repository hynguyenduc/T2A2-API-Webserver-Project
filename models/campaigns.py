from main import db

class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date())
    description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship(
        "User", 
        back_populates="campaigns"
    )
    characters = db.relationship(
        "Character", 
        back_populates="campaign", 
        cascade="all, delete"
    )