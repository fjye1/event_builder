from flask import Blueprint, render_template

from app.forms import EventForm

profile_bp = Blueprint('profile', __name__)


@profile_bp.route("/profile")
def home():
    form = EventForm()
    return render_template(
        "profile/home.html",
        form=form)