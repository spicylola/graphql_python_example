from graphql_python_example.config import LocalConfig
from graphql_python_example.app_settings import create_app

app = create_app()


@app.cli.command("load_seed_users")
def load_seed_users():
    from graphql_python_example.seeds import load_users
    load_users()

@app.cli.command("load_seed_roles")
def load_seed_users():
    from graphql_python_example.seeds import load_roles
    load_roles()

@app.cli.command("load_seed_events")
def load_seed_users():
    from graphql_python_example.seeds import load_events
    load_events()