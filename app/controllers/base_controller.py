from fastapi import APIRouter, Response, Request
from fastapi.responses import HTMLResponse
from app.responses.damage_response import DamageResponse, SpecificVolumeResponse
from app.constants.damage_constants import damage_constant
from loguru import logger
import random


api = APIRouter()

damaged_system = random.choice(list(damage_constant.keys()))


@api.get(path="/status")
def get_damage() -> DamageResponse:
    return DamageResponse(damaged_system=damaged_system)


@api.get("/repair-bay", response_class=HTMLResponse)
def get_repair_bay():
    repair_code = damage_constant[damaged_system]
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
        <div class="anchor-point">{repair_code}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@api.post("/teapot")
def post_teapot():
    return Response(status_code=418)


@api.get("/phase-change-diagram")
def specific_volume_change(request: Request):
    query_params = dict(request.query_params)
    logger.info(query_params)
    if 'pressure' in query_params.keys():
        liquid = specific_volume(y=float(query_params['pressure']), variable='pressure', type='liquid')
        vapor = specific_volume(y=float(query_params['pressure']), variable='pressure', type='vapor')
    elif 'temperature' in query_params.keys():
        liquid = specific_volume(y=float(query_params['temperature']), variable='temperature', type='liquid')
        vapor = specific_volume(y=float(query_params['temperature']), variable='temperature', type='vapor')

    return SpecificVolumeResponse(specific_volume_liquid=liquid, specific_volume_vapor=vapor)


def specific_volume(y, variable='pressure', type='liquid'):
    if variable == 'pressure':
        m = 4061.224489795918
        b = -4.2142857142857135
        if type == 'vapor':
            m = -0.3317053656259897
            b = 10.001160968779692
    elif variable == 'temperature':
        m = 191836.73469387754
        b = -171.42857142857142
        if type == 'vapor':
            m = -15.668494657710065
            b = 500.05483973130197

    return (y - b) / m


def safe_str_to_number(s):
    try:
        return int(s) if s.isdigit() else float(s)
    except ValueError:
        return None  # or raise an error
