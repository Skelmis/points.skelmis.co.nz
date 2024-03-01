from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder
from piccolo_api.session_auth.endpoints import session_login, session_logout
from starlette.authentication import AuthenticationError
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from home import endpoints
from home.piccolo_app import APP_CONFIG


app = FastAPI(
    routes=[
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)
app.include_router(endpoints.router)
app.mount("/login/", session_login())
app.mount("/logout/", session_logout())


@app.exception_handler(AuthenticationError)
async def handle_auth_failure(request: Request, exception: AuthenticationError):
    return RedirectResponse(url="/login")


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
