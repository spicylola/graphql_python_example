from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship
'''
Sqlalchemy models
for key_values table
along with serializers/deserializers
'''

from graphql_python_example.app_settings import db
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property


UserRole = db.Table('user_roles',
                 Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
                 Column('role_id', Integer, ForeignKey('roles.id'), nullable=False),
                    )


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)

    @hybrid_method
    def create(self, data):
        try:
            role= self(**data)
            db.session.add(role)
            db.session.commit()
            return role
        except Exception as e:
            raise Exception(getattr(e, "orig", str(e)))

    @hybrid_method
    def update_data(self, data):
        try:
            role = db.session.query(self).get(data['id'])
            for elt in data:
                setattr(role, elt, data[elt])
            db.session.commit()
            return role
        except Exception as e:
            raise Exception(getattr(e, "orig", str(e)))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    events = db.relationship("Event", backref='users', lazy=True)
    roles = db.relationship(Role, secondary=UserRole, backref='users',
                         lazy=True, cascade='delete,all')

    @hybrid_method
    def create(self, data):
        try:
            if "role_ids" in data:
                role_ids = data.pop('role_ids')

                # In order to add the Roles to User Object through sqlachemy, need actual list of roles objects, not list of ints
                result = db.session.query(Role).filter(Role.id.in_(role_ids)).all()
                data['roles'] = result

            user = self(**data)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            raise Exception(getattr(e, "orig", str(e)))

    @hybrid_method
    def update_data(self, data):
        try:
            if "role_ids" in data:
                role_ids = data.pop('role_ids')

                # In order to add the Roles to User Object through sqlachemy, need actual list of roles objects, not list of ints
                result = db.session.query(Role).filter(Role.id.in_(role_ids)).all()
                data['roles'] = result

            user = db.session.query(self).get(data['id'])
            for elt in data:
                setattr(user, elt, data[elt])
            db.session.commit()
            return user
        except Exception as e:
            raise Exception(e)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    created_by = db.Column(Integer, ForeignKey('users.id'))
    description = db.Column(String)

    @hybrid_method
    def create(self, data):
        try:
            event = self(**data)
            db.session.add(event)
            db.session.commit()
            return event
        except Exception as e:
            raise Exception(e)

    @hybrid_method
    def update_data(self, data):
        try:
            event = db.session.query(self).get(data['id'])
            for elt in data:
                setattr(event, elt, data[elt])
            db.session.commit()
            return event
        except Exception as e:
            raise Exception(e)
