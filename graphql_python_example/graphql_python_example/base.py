import graphene
#
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField

from graphql_python_example.models import User as UserModel
from graphql_python_example.models import Event as EventModel
from graphql_python_example.models import Role as RoleModel

from graphql_python_example.app_settings import db
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


class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
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
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, **data):
        role = RoleModel.update_data(data)
        return UpdateRole(role=role)


class DeleteRole(graphene.Mutation):
    role_id = graphene.Int(description="Role deleted by this mutation.")

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **data):
        role = db.session.query(RoleModel).get(data['id'])
        # Remove assosiations
        role.users.clear()
        db.session.delete(role)
        db.session.commit()
        return DeleteRole(role_id=data['id'])


# EVENT MUTATION DEFINITIONS #######
class CreateEvent(graphene.Mutation):
    event = graphene.Field(lambda: Event, description="Mutation for creating a new event")

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        created_by = graphene.Int(required=True)

    def mutate(self, info, **data):
        event = EventModel.create(data)
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    event = graphene.Field(lambda: Event, description="Event updated by this mutation.")

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    def mutate(self, info, **data):
        event = EventModel.update_data(data)
        return UpdateEvent(event=event)


class DeleteEvent(graphene.Mutation):
    event_id = graphene.Int(description="Event deleted by this mutation.")

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **data):
        event = db.session.query(EventModel).get(data['id'])
        # Remove associations
        event.created_by.clear()
        db.session.delete(event)
        db.session.commit()
        return DeleteEvent(event_id=data['id'])


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
        email = graphene.String(required=True)
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
        user.events.clear()
        user.roles.clear()
        db.session.delete(user)
        db.session.commit()
        return DeleteUser(user_id=data['id'])
