from flask import Blueprint, render_template

from app.forms import EventForm

create_bp = Blueprint('create', __name__)


@create_bp.route("/create")
def home():
    form = EventForm()
    return render_template(
        "create/home.html")

@create_bp.route("/create/company")
def company():
    form = EventForm()
    return render_template(
        "create/home.html")


@create_bp.route("/create/event")
def event():
    form = EventForm()
    return render_template(
        "create/event.html",
        form=form)
