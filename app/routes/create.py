from flask import Blueprint, render_template

from app.forms import EventForm

create_bp = Blueprint('create', __name__)


@create_bp.route("/")
def home():
    form = EventForm()
    return render_template(
        "create/home.html",
        form=form)


