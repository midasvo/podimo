from quart import Blueprint, Response, render_template
from services.health_service import HealthService
import json

bp = Blueprint('health', __name__)
health_service = HealthService()

@bp.route('/health/check')
async def check_health():
    results = await health_service.check_all_feeds()
    return Response(
        json.dumps([result.to_dict() for result in results]),
        mimetype='application/json'
    )

@bp.route('/health')
async def health_page():
    results = await health_service.check_all_feeds()
    return await render_template('health.html', feeds=results) 