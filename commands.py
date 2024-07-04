from main import db
from flask import Blueprint
from main import bcrypt
from models.campaigns import Campaign
from models.characters import Character
from models.users import User
from datetime import date

db_commands = Blueprint("db", __name__)

# create app's cli command named create, then run it in the terminal as "flask db create", 
# it will invoke create_db function
@db_commands.cli.command("autofill")
def auto_generate():
    db.drop_all()
    db.create_all()
    print ("Created tables")

    # create admin user and user1    
    admin_user = User(
        email = "admin@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8"),
        admin = True
    )
    db.session.add(admin_user)

    user1 = User(
        email = "user1@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8")
    )
    db.session.add(user1)
    # This extra commit will end the transaction and generate the ids for the user
    db.session.commit()

    # create the card object
    campaign1 = Campaign(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "sample campaign 1",
        description = "",
        date_created = date.today(),
        # user_id = user1.id

    )
    # Add the object as a new row to the table
    db.session.add(campaign1)
    # commit the changes
    db.session.commit()

    character1 = Character(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "Ogmire",
        race = "half-orc",
        char_class = "barbarian",
        str_stat = 10,
        dex_stat = 14,
        con_stat = 12,
        int_stat = 16,
        wis_stat = 8,
        cha_stat = 10,
        date = date.today(),
        # user = user1
 
    )
    # Add the object as a new row to the table
    db.session.add(character1)

    # commit the changes
    db.session.commit()

    print("Users, Campaigns and Characters added") 

@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands .cli.command("seed")
def seed_db():
    # create admin user and user1    
    admin_user = User(
        email = "admin@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8"),
        admin = True
    )
    db.session.add(admin_user)

    user1 = User(
        email = "user1@email.com",
        password = bcrypt.generate_password_hash("11223344").decode("utf-8")
    )
    db.session.add(user1)
    # This extra commit will end the transaction and generate the ids for the user
    db.session.commit()

    # create the card object
    campaign1 = Campaign(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "sample campaign 1",
        description = "",
        date_created = date.today(),
        # user_id = user1.id

    )
    # Add the object as a new row to the table
    db.session.add(campaign1)
    # commit the changes
    db.session.commit()

    character1 = Character(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name = "Ogmire",
        race = "half-orc",
        char_class = "barbarian",
        str_stat = 10,
        dex_stat = 14,
        con_stat = 12,
        int_stat = 16,
        wis_stat = 8,
        cha_stat = 10,
        date = date.today(),
        # user = user1
 
    )
    # Add the object as a new row to the table
    db.session.add(character1)

    # commit the changes
    db.session.commit()

    print("Table seeded") 

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")