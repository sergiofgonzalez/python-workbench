"""Implementation of the endpoints of the Kitchen API"""

import copy
import uuid
from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from api.schemas import (
    GetKitchenScheduleParameters,
    GetScheduledOrderSchema,
    GetScheduledOrdersSchema,
    ScheduleOrderSchema,
    ScheduleStatusSchema,
)

blueprint = Blueprint("kitchen", __name__, description="Kitchen API")

schedules = [
    {
        "id": str(uuid.uuid4()),
        "scheduled": datetime.now(),
        "status": "pending",
        "order": [{"product": "capuccino", "quantity": 1, "size": "big"}],
    }
]


def validate_schedule(schedule):
    schedule = copy.deepcopy(schedule)
    schedule["scheduled"] = schedule["scheduled"].isoformat()
    errors = GetScheduledOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)


@blueprint.route("/kitchen/schedules")
class KitchenSchedules(MethodView):
    @blueprint.arguments(GetKitchenScheduleParameters, location="query")
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self, parameters):
        for schedule in schedules:
            validate_schedule(schedule)

        if not parameters:
            return {"schedules": schedules}, 200

        

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
    def post(self, payload):
        return schedules[0], 201


@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSchedule(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        return schedules[0], 200

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id):
        return schedules[0], 200

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        return "", 204


@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
def cancel_schedule(schedule_id):
    return schedules[0], 200


@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
def get_schedule_status(schedule_id):
    return schedules[0], 200
