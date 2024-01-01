"""Implementation of the endpoints of the Kitchen API"""

import copy
import uuid
from datetime import datetime

from flask import abort
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

schedules = dict()


def validate_schedule(schedule):
    schedule = copy.deepcopy(schedule)
    schedule["scheduled"] = schedule["scheduled"].isoformat()
    errors = GetScheduledOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)  # Will force a 500 Internal Server Error


@blueprint.route("/kitchen/schedules")
class KitchenSchedules(MethodView):
    """Implementation logic for /kitchen/schedules"""

    @blueprint.arguments(GetKitchenScheduleParameters, location="query")
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self, parameters):
        for schedule in schedules.values():
            validate_schedule(schedule)

        if not parameters:
            return {"schedules": schedules.values()}

        query_resultset = list(schedules.values())
        progress = parameters.get("progress")
        if progress is not None:
            if progress:
                query_resultset = [
                    schedule
                    for schedule in query_resultset
                    if schedule["status"] == "progress"
                ]
            else:
                query_resultset = [
                    schedule
                    for schedule in query_resultset
                    if schedule["status"] != "progress"
                ]

        since = parameters.get("since")
        if since is not None:
            query_resultset = [
                schedule
                for schedule in query_resultset
                if schedule["scheduled"] >= since
            ]

        limit = parameters.get("limit")
        if limit is not None and len(query_resultset) > limit:
            query_resultset = query_resultset[:limit]

        return {"schedules": query_resultset}

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
    def post(self, payload):
        schedule_id = str(uuid.uuid4())
        schedule = {
            "id": schedule_id,
            "order": payload["order"],
            "scheduled": datetime.utcnow(),
            "status": "progress",
        }
        validate_schedule(schedule)
        schedules[schedule_id] = schedule
        return schedule


@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSchedule(MethodView):
    """Implementation logic for /kitchen/schedules/{schedule_id} endpoint"""

    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        if schedule_id in schedules:
            validate_schedule(schedules[schedule_id])
            return schedules[schedule_id]
        else:
            abort(404, description=f"Resource with ID {schedule_id} not found")

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id):
        if schedule_id in schedules:
            schedules[schedule_id]["order"] = payload["order"]
            validate_schedule(schedules[schedule_id])
            return schedules[schedule_id]
        else:
            abort(404, description=f"Resource with ID {schedule_id} not found")

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        if schedule_id in schedules:
            del schedules[schedule_id]
        return


@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
def cancel_schedule(schedule_id):
    if schedule_id in schedules:
        schedules[schedule_id]["status"] = "cancelled"
        validate_schedule(schedules[schedule_id])
        return schedules[schedule_id]
    else:
        abort(404, description=f"Resource with ID {schedule_id} not found")


@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["GET"])
@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
def get_schedule_status(schedule_id):
    if schedule_id in schedules:
        return {"status": schedules[schedule_id]["status"]}
    else:
        abort(404, description=f"Resource with ID {schedule_id} not found")
