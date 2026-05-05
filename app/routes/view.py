from flask import Blueprint, render_template
from datetime import datetime
from app.forms import EventForm
from app.models import Event
from collections import defaultdict
from datetime import date
from sqlalchemy.orm import joinedload

view_bp = Blueprint('view', __name__)






@view_bp.route("/view")
def home():
    today = date.today()

    events = (
        Event.query
        .options(joinedload(Event.event_products))
        .filter(Event.date >= today)
        .order_by(Event.date.asc())
        .all()
    )

    grouped = defaultdict(list)

    for event in events:
        grouped[event.date].append(event)  # ← pass full object

    grouped = dict(sorted(grouped.items()))

    return render_template("view/home.html", grouped=grouped)