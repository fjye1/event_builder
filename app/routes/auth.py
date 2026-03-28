from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user
from app.extensions import login_manager
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

auth_bp    = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # 1️ Look up user by email
        user = User.query.filter_by(email=form.email.data).first()

        # 2️ Check password
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))

        # 3️ Log the user in
        login_user(user)



        # 5️ Redirect to create page
        return redirect(url_for('create.index'))

    # 6️ Render login template with form
    return render_template("auth/login.html", form=form)
