from flask import Blueprint, render_template
from datetime import datetime
from app.forms import EventForm
from app.models import Event
from collections import defaultdict

view_bp = Blueprint('view', __name__)






@view_bp.route("/view")
def home():
    events = Event.query.order_by(Event.date.asc()).all()

    grouped = defaultdict(list)

    for event in events:
        summary = event.summary()

        grouped[event.date].append({
            "id": event.id,
            "name": summary["event_name"],
            "client": summary["client"],
            "venue": summary["venue"],

            # 🕒 TIMING (ADD THIS)
            "arrive_unit_time": summary.get("arrive_unit_time"),
            "leave_unit_time": summary.get("leave_unit_time"),
            "arrive_venue_time": summary.get("arrive_venue_time"),
            "service_start_time": summary.get("service_start_time"),
            "service_end_time": summary.get("service_end_time"),

            # existing
            "products": summary["products"],
            "staff_count": len(summary["staff"]),
            "staff": summary["staff"],
        })

    grouped = dict(sorted(grouped.items()))

    return render_template("view/home.html", grouped=grouped)