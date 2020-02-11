from faker import Faker
import random

from graphql_python_example.models import Role, Event, User
from graphql_python_example.app import db


# Load dummy roles
def load_roles():
    # First clear all the existing roles
    roles = Role.query.all()
    for role in roles:
        role.permissions.clear()
        db.session.delete(role)
        db.session.commit()

    fake = Faker()
    for i in range(10):
        role = Role(
            name=fake.word(ext_word_list=None)
        )
        db.session.add(role)
        db.session.commit()

# Load dummy events
def load_events():
    # First clear all the existing roles
    events = Event.query.all()
    for event in events:
        event.permissions.clear()
        db.session.delete(event)
        db.session.commit()

    fake = Faker()
    for i in range(150):
        event = Event(
            name=fake.word(ext_word_list=None),
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None),
        )
        db.session.add(event)
        db.session.commit()

def load_users():
    # First delete all users
    users = User.query.all()
    for user in users:
        user.roles.clear()
        db.session.delete(user)
        db.session.commit()


    # Get all the Roles, we will randomly assign 1 role to each user
    roles = Role.query.all()
    events = Event.query.all()
    # Faker module
    fake = Faker()

    # Look thru a range
    for i in range(100):

        # Create a dummy user and random role
        user = User(
            name = str(fake.first_name())+" "+str(fake.last_name()),
            email = fake.email(),
            events =random.sample(events, 1),
            roles = random.sample(roles, 1)
        )
        db.session.add(user)
        db.session.commit()
