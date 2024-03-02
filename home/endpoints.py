import logging
import os
from typing import Annotated

import jinja2
from fastapi import APIRouter, Depends
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.middleware import SessionsAuthBackend
from starlette.requests import Request, HTTPConnection
from starlette.responses import HTMLResponse

from home.tables import Points, PointTypes

ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(__file__), "templates")
    )
)
HOME_TEMPLATE = ENVIRONMENT.get_template("home.html")
router = APIRouter()
log = logging.getLogger(__name__)
session_backend = SessionsAuthBackend()


async def get_user(request: Request):
    conn = HTTPConnection(request.scope)
    auth_result = await session_backend.authenticate(conn)
    return auth_result[1].user  # type: ignore


@router.get("/")
async def get_home(current_user: Annotated[BaseUser, Depends(get_user)]):
    points: list[Points] = await Points.objects().where(Points.user == current_user.id)
    current_points: list[Points] = [p for p in points if p.is_current]

    sum_air_nz = sum(
        p.value
        for p in current_points
        if p.point_type in (PointTypes.NZ_FLIGHT, PointTypes.STATUS_BOOST)
    )
    sum_a_star = sum(
        p.value for p in current_points if p.point_type == PointTypes.A_STAR_FLIGHT
    )
    sum_other = sum(p.value for p in current_points if p.point_type == PointTypes.OTHER)
    sum_total = sum_air_nz + sum_a_star + sum_other

    content = HOME_TEMPLATE.render(
        title=f"Points Dashboard for {current_user.username}",
        sum_air_nz=sum_air_nz,
        sum_a_star=sum_a_star,
        sum_other=sum_other,
        sum_total=sum_total,
    )
    return HTMLResponse(content)
