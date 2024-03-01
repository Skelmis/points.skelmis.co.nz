import os
from dotenv import load_dotenv
from piccolo.engine import SQLiteEngine

from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry

load_dotenv()

DB = PostgresEngine(
    config={
        "database": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "host": os.environ["POSTGRES_HOST"],
        "port": int(os.environ["POSTGRES_PORT"]),
    },
    extensions=tuple(),
)

APP_REGISTRY = AppRegistry(
    apps=[
        "home.piccolo_app",
        "piccolo_admin.piccolo_app",
        "piccolo.apps.user.piccolo_app",
        "piccolo_api.session_auth.piccolo_app",
    ]
)
