from flask import Blueprint, render_template, redirect, url_for

from app.models import Event, Company
from app.forms import CompanyForm
from app.extensions import db

edit_bp = Blueprint('edit', __name__)


@edit_bp.route("/edit")
def home():
    return render_template("edit/home.html")


# --- EVENT ---



# --- COMPANY ---
@edit_bp.route("/edit/companies")
def company_list():
    companies = Company.query.all()
    return render_template("edit/company/list.html", companies=companies)


@edit_bp.route("/edit/company/<int:company_id>", methods=["GET", "POST"])
def company_edit(company_id):
    company = Company.query.get_or_404(company_id)
    form = CompanyForm(obj=company)

    if form.validate_on_submit():
        form.populate_obj(company)
        db.session.commit()
        return redirect(url_for("edit.company_list"))

    return render_template("edit/company/edit.html", form=form, company=company)


# --- CLIENT ---
@edit_bp.route("/edit/clients")
def client_list():
    pass


@edit_bp.route("/edit/client/<int:client_id>", methods=["GET", "POST"])
def client_edit(client_id):
    pass


# --- VENUE ---
@edit_bp.route("/edit/venues")
def venue_list():
    pass


@edit_bp.route("/edit/venue/<int:venue_id>", methods=["GET", "POST"])
def venue_edit(venue_id):
    pass


# --- VEHICLE ---
@edit_bp.route("/edit/vehicles")
def vehicle_list():
    pass


@edit_bp.route("/edit/vehicle/<int:vehicle_id>", methods=["GET", "POST"])
def vehicle_edit(vehicle_id):
    pass


# --- PRODUCT ---
@edit_bp.route("/edit/products")
def product_list():
    pass


@edit_bp.route("/edit/product/<int:product_id>", methods=["GET", "POST"])
def product_edit(product_id):
    pass


# --- PRODUCT EXTRA ---
@edit_bp.route("/edit/product_extras")
def product_extra_list():
    pass


@edit_bp.route("/edit/product_extra/<int:product_extra_id>", methods=["GET", "POST"])
def product_extra_edit(product_extra_id):
    pass


# --- SKILL ---
@edit_bp.route("/edit/skills")
def skill_list():
    pass


@edit_bp.route("/edit/skill/<int:skill_id>", methods=["GET", "POST"])
def skill_edit(skill_id):
    pass


# --- STAFF ---
@edit_bp.route("/edit/staff")
def staff_list():
    pass


@edit_bp.route("/edit/staff/<int:staff_id>", methods=["GET", "POST"])
def staff_edit(staff_id):
    pass
