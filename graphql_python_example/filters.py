import graphene
from graphene import Connection
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from .models import User, Role, Event



class RolesFilter(FilterSet):
    class Meta:
        model = Role
        fields = {"id":['eq', 'ne', 'gt','gte', 'lt', 'lte'],
            'name': ['eq', 'ne', 'in', 'ilike']}

class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = { "id":['eq', 'ne', 'gt','gte', 'lt', 'lte'],
                  'name': ['eq', 'ne', 'in', 'like'],
                  "descripition": ['eq', 'ne', 'like', 'in']}

class UserFilter(FilterSet):
    class Meta:
        model = User
        fields ={
            "id":['eq', 'ne', 'gt','gte', 'lt', 'lte'],
            "email": ['eq', 'ne', 'like', 'in'],
            "name": ['eq', 'ne', 'like', 'in'],
        }



# class MyFilterableConnectionField(FilterableConnectionField):
#     filters = {Users: UserFilter(), Roles: RoleFilter()}