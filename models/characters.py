from main import db

class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    race = db.Column(db.String(), nullable=False)
    char_class = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date())
    str_stat = db.Column(db.Integer(), nullable=False)
    dex_stat = db.Column(db.Integer(), nullable=False)
    con_stat = db.Column(db.Integer(), nullable=False)
    int_stat = db.Column(db.Integer(), nullable=False)
    wis_stat = db.Column(db.Integer(), nullable=False)
    cha_stat = db.Column(db.Integer(), nullable=False)


