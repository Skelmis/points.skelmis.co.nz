import logging
import os
from typing import Annotated

import jinja2
from fastapi import APIRouter, Depends
from piccolo_api.session_auth.middleware import SessionsAuthBackend
from starlette.authentication import AuthenticationError, BaseUser
from starlette.requests import Request, HTTPConnection
from starlette.responses import HTMLResponse


ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(__file__), "templates")
    )
)
router = APIRouter()
log = logging.getLogger(__name__)
session_backend = SessionsAuthBackend()


async def get_user(request: Request):
    conn = HTTPConnection(request.scope)
    auth_result = await session_backend.authenticate(conn)
    return auth_result[1]


@router.get("/")
async def get_home(current_user: Annotated[BaseUser, Depends(get_user)]):
    template = ENVIRONMENT.get_template("home.html")

    content = template.render(
        title=f"Points Dashboard for {current_user.display_name}",
    )

    return HTMLResponse(content)
