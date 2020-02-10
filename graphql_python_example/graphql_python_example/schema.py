import graphene
from graphene import relay

from graphene import Connection

from graphql_python_example.filters import UserFilter, EventFilter, RolesFilter
from graphql_python_example.base import (User, Event, Role, CustomField,
                                         CreateEvent, UpdateEvent, DeleteEvent,
                                         CreateUser, UpdateUser, DeleteUser,
                                         CreateRole, UpdateRole, DeleteRole
                                         )

class UserFilterConnection(Connection):
    total_count = graphene.Int()
    limit = graphene.Int()

    def resolve_total_count(self, info):
        return info.variable_values['total_count']

    class Meta:
        node = User

class EventFilterConnection(Connection):
    total_count = graphene.Int()
    limit = graphene.Int()

    def resolve_total_count(self, info):
        return info.variable_values['total_count']

    class Meta:
        node = Event

class RoleFilterConnection(Connection):
    total_count = graphene.Int()
    limit = graphene.Int()

    def resolve_total_count(self, info):
        return info.variable_values['total_count']

    class Meta:
        node = Role


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    events = CustomField(EventFilterConnection, where=EventFilter(), page=graphene.Int(),
                               limit=graphene.Int())
    roles = CustomField(RoleFilterConnection, where=RolesFilter(), page=graphene.Int(), limit=graphene.Int())
    users = CustomField(UserFilterConnection, where=UserFilter(), page=graphene.Int(), limit=graphene.Int())

class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

    create_role = CreateRole.Field()
    update_role = UpdateRole.Field()
    delete_role = DeleteRole.Field()




schema = graphene.Schema(query=Query, mutation=Mutations)