from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship
'''
Sqlalchemy models
for key_values table
along with serializers/deserializers
'''

from graphql_python_example.app import db
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property


UserRole = db.Table('user_roles',
                 Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
                 Column('role_id', Integer, ForeignKey('roles.id'), nullable=False),
                    )


RolePermission = db.Table('role_permissions',
                 Column('perm_id', Integer, ForeignKey('permissions.id'), nullable=False),
                 Column('role_id', Integer, ForeignKey('roles.id'), nullable=False),
                    )


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    permission = db.relationship("Permission", backref='roles', lazy=True)

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
            if not role:
                raise Exception("The Role does not exist")

            # Update role data
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
    roles = db.relationship(Role, secondary=UserRole, backref='users',
                         lazy=True, cascade='delete,all')

    @hybrid_method
    def create(self, data):
        try:
            if "role_id" in data:
                role_ids = data.pop('role_id')
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
            user = db.session.query(self).get(data['id'])
            if not user:
                raise Exception("The User does not exist")
            if "role_ids" in data:
                role_ids = data.pop('role_ids')
                # In order to add the Roles to User Object through sqlachemy, need actual list of roles objects, not list of ints
                result = db.session.query(Role).filter(Role.id.in_(role_ids)).all()
                data['roles'] = result

            for elt in data:
                setattr(user, elt, data[elt])
            db.session.commit()
            return user
        except Exception as e:
            raise Exception(e)


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    role_id = db.Column(Integer, ForeignKey('roles.id'))
    description = db.Column(String)

    @hybrid_method
    def create(self, data):
        try:
            permission = self(**data)
            db.session.add(permission)
            db.session.commit()
            return permission
        except Exception as e:
            raise Exception(e)

    @hybrid_method
    def update_data(self, data):
        try:
            permission = db.session.query(self).get(data['id'])
            if not permission:
                raise Exception("The Permission does not exist")
            for elt in data:
                setattr(permission, elt, data[elt])
            db.session.commit()
            return event
        except Exception as e:
            raise Exception(e)
