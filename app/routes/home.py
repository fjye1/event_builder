from flask import Blueprint, render_template

from app.forms import EventForm

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():

    return render_template(
        "home/start.html")