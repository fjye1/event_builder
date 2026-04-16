from datetime import date

from flask import Blueprint, render_template

from app.models import User

profile_bp = Blueprint('profile', __name__)


@profile_bp.route("/profile")
def home():
    user = User.query.first()

    age = None
    job_stats = {
        "total_jobs": None,
        "most_common_job": None
    }

    staff_skills = {
        "total_skills": None
    }

    if user and user.staff and user.staff.dob:
        today = date.today()

        age = today.year - user.staff.dob.year - (
            (today.month, today.day) < (user.staff.dob.month, user.staff.dob.day)
        )


    return render_template(
        "profile/home.html",
        user=user,
        age=age,
        job_stats=job_stats,
        staff_skills=staff_skills,
    )