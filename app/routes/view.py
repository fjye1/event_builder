from flask import Blueprint, render_template

from app.forms import EventForm

view_bp = Blueprint('view', __name__)


@view_bp.route("/view")
def home():
    form = EventForm()
    return render_template(
        "view/home.html",
        form=form)
