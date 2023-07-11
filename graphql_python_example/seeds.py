from faker import Faker
import random

from graphql_python_example.models import Role, Permission, User
from graphql_python_example.app import db


# Load dummy roles
def load_roles():
    # First clear all the existing roles
    db.session.query(Role).delete()
    db.session.commit()

    role_names = ['awesome_possum', 'eye_of_the_tiger', 'very_cool_role', 'admin']
    for name in role_names :
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()

# Load dummy events
def load_permissions():
    # First clear all the existing events
    db.session.query(Permission).delete()
    db.session.commit()

    roles = Role.query.all()
    role_ids = [role.id for role in roles]


    fake = Faker()
    for i in range(10):
        permission = Permission(
            name=fake.word(ext_word_list=None),
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None),
            role_id=random.choice(role_ids)
        )
        db.session.add(permission)
        db.session.commit()

def load_users():
    # First delete all users
    users = User.query.all()
    for user in users:
        user.roles.clear()
        db.session.delete(user)
        db.session.commit()

    # Get all the Roles, we will randomly assign 2 role to each user
    roles = Role.query.all()
    # Faker module
    fake = Faker()

    # Generates 10 random users and updates created by for user who hosted event
    for i in range(10):
        # Create a dummy user and random role
        user = User(
            name=str(fake.first_name())+" "+str(fake.last_name()),
            email=fake.email(),
            roles=random.sample(roles, 2)
        )
        db.session.add(user)
        db.session.commit()

