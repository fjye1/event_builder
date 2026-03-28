from flask import Blueprint, render_template

from app.forms import EventForm

edit_bp = Blueprint('edit', __name__)


@edit_bp.route("/edit")
def home():
    form = EventForm()
    return render_template(
        "edit/home.html",
        form=form)