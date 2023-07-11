#!/usr/bin/env python
import logging

from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from graphql_python_example.config import  LocalConfig


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
logger = logging.getLogger()


def create_app(config_class=LocalConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Python is barbaric
    from graphql_python_example.schema import schema

    app.add_url_rule(
        "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
     )

    return app

app = create_app()
# LOAD SEED DETA
# This looks a little ratchet but to avoid circular imports

@app.cli.command('load_roles')
def load_seed_demo_roles():
    from graphql_python_example.seeds import load_roles
    load_roles()

@app.cli.command('load_users')
def load_seed_demo_user():
    from graphql_python_example.seeds import load_users
    load_users()

@app.cli.command('load_permissions')
def load_seed_permissions():
    from graphql_python_example.seeds import load_permissions
    load_permissions()

