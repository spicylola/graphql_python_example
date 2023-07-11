import graphene
#
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField

from graphql_python_example.models import User as UserModel
from graphql_python_example.models import Permission as PermissionModel
from graphql_python_example.models import Role as RoleModel

from graphql_python_example.app import db
from sqlalchemy.sql import functions as func


class CustomNode(relay.Node):
    class Meta:
        name = 'CustomNode'

    # These two methods were to override the Base 64 encoding that comes with
    @classmethod
    def from_global_id(cls, global_id):
        return global_id

    @staticmethod
    def to_global_id(type, id):
        return id


class CustomField(FilterableConnectionField):
    filter_arg = 'where'

    @classmethod
    def get_query(cls, model, info: 'ResolveInfo', sort=None, **args):
        """Standard get_query with filtering."""

        # If Page comes in as 0, to get around the boolean of Page #0 being treated as false
        page = int(args.get('page')) + 1 if args.get('page') is not None else None
        limit = args.get('limit')

        query = super().get_query(model, info, sort, **args)

        request_filters = args.get(cls.filter_arg)
        if request_filters:
            filter_set = cls.get_filter_set(info)
            query = filter_set.filter(info, query, request_filters)

        # Hacky solution to work around Page/Limit
        info.variable_values['total_count'] = query.count()

        if limit:
            if page:
                # To get page back to correct number, if its done in the query, PEMDAS will cause issues
                page = page - 1
                query = query.offset(int(page) * int(limit))
            query = query.limit(limit)
        return query


##### GRAPHENE OBJECT TYPE DEFINITIONS#########

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (CustomNode,)


class Permission(SQLAlchemyObjectType):
    class Meta:
        model = PermissionModel
        interfaces = (CustomNode,)


class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (CustomNode,)


# ROLE MUTATION DEFINITIONS ########

class CreateRole(graphene.Mutation):
    role = graphene.Field(lambda: Role, description="Mutation for creating a new role")

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, **data):
        role = RoleModel.create(data)
        return CreateRole(role=role)


class UpdateRole(graphene.Mutation):
    role = graphene.Field(lambda: Role, description="Role updated by this mutation.")

    class Arguments:
        id = graphene.Int(required=True, description="id of role to be updated")
        name = graphene.String(required=True, description="name of role to be updated")

    def mutate(self, info, **data):
        role = RoleModel.update_data(data)
        return UpdateRole(role=role)


class DeleteRole(graphene.Mutation):
    role_id = graphene.Int(description="Role deleted by this mutation.")

    class Arguments:
        id = graphene.Int(required=True, description="id of role to be deleted")

    def mutate(self, info, **data):
        role = db.session.query(RoleModel).get(data['id'])
        # Remove assosiations
        role.permissions.clear()
        role.users.clear()
        db.session.delete(role)
        db.session.commit()
        return DeleteRole(role_id=data['id'])


# Permission MUTATION DEFINITIONS #######
class CreatePermission(graphene.Mutation):
    permission = graphene.Field(lambda: Permission, description="Mutation for creating a new permission")

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True, description="what the permission does")
        role_id = graphene.Int(required=True, description="role id associated with permission")

    def mutate(self, info, **data):
        permission = PermissionModel.create(data)
        return CreatePermission(permission=permission)


class UpdatePermission(graphene.Mutation):
    permission = graphene.Field(lambda: Permission, description="Permission updated by this mutation.")

    class Arguments:
        id = graphene.Int(required=True, description="id of permission to be updated")
        name = graphene.String()
        description = graphene.String()


    def mutate(self, info, **data):
        permission = PermissionModel.update_data(data)
        return UpdatePermission(permission=permission)


class DeletePermission(graphene.Mutation):
    permission_id = graphene.Int(description="Permission deleted by this mutation.")

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **data):
        permission = db.session.query(PermissionModel).get(data['id'])
        # Remove associations
        permission.role_id.clear()
        db.session.delete(event)
        db.session.commit()
        return DeletePermission(permission_id=data['id'])


######### USER MUTATIONS ########
class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda: User, description="Mutation for creating a new user")

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String()
        role_ids = graphene.List(graphene.Int, required=False)

    def mutate(self, info, **data):
        user = UserModel.create(data)
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(lambda: User, description="User updated by this mutation.")

    class Arguments:
        id = graphene.Int(required=True)
        email = graphene.String()
        name = graphene.String()
        role_ids = graphene.List(graphene.Int, required=False)

    def mutate(self, info, **data):
        user = UserModel.update_data(data)
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    user_id = graphene.Int(description="User deleted by this mutation.")

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **data):
        user = db.session.query(UserModel).get(data['id'])
        # Remove associations
        user.roles.clear()
        db.session.delete(user)
        db.session.commit()
        return DeleteUser(user_id=data['id'])
