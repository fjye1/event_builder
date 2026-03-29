from flask import Blueprint, render_template, url_for, redirect, flash

from app.extensions import db
from app.forms import EventForm, CompanyForm, ClientForm, VenueForm, VehicleForm, ProductForm
from app.models import Company, Client, Venue, Vehicle, FuelType, Product

create_bp = Blueprint('create', __name__)


@create_bp.route("/create")
def home():
    return render_template(
        "create/home.html")


@create_bp.route("/create/company", methods=['GET', 'POST'])
def company():
    form = CompanyForm()

    if form.validate_on_submit():
        new_company = Company(
            name=form.name.data,
        )
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template(
        "create/company.html", form=form)


@create_bp.route("/create/client", methods=['GET', 'POST'])
def client():
    form = ClientForm()

    # Load companies for the select field
    companies = Company.query.all()
    # Add a blank option for no company
    form.company_id.choices = [(0, "— None —")] + [(c.id, c.name) for c in companies]

    if form.validate_on_submit():
        company_id = form.company_id.data
        if company_id == 0:
            company_id = None  # no company selected

        new_client = Client(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_id=company_id
        )

        db.session.add(new_client)
        db.session.commit()

        flash(f"Client '{new_client.name}' created successfully.", "success")
        return redirect(url_for('home.index'))

    return render_template("create/client.html", form=form)


@create_bp.route("/create/venue", methods=['GET', 'POST'])
def venue():
    form = VenueForm()

    form.clients.choices = [(c.id, f"{c.name} ({c.company.name})") for c in Client.query.all()]

    if form.validate_on_submit():
        # Create new Venue instance
        new_venue = Venue(
            name=form.name.data,
            address=form.address.data
        )

        # Assign selected clients (many-to-many), allow empty selection
        if form.clients.data:
            selected_clients = Client.query.filter(Client.id.in_(form.clients.data)).all()
            new_venue.clients = selected_clients
        else:
            new_venue.clients = []  # no clients selected

        db.session.add(new_venue)
        db.session.commit()

        flash(f"Venue '{new_venue.name}' created successfully.", "success")
        return redirect(url_for('home.index'))

    return render_template("create/venue.html", form=form)


@create_bp.route("/create/vehicle", methods=['GET', 'POST'])
def vehicle():
    form = VehicleForm()
    db.Enum(FuelType)

    if form.validate_on_submit():
        vehicle = Vehicle(
            name=form.name.data,
            license_plate=form.license_plate.data,
            mileage=form.mileage.data,
            fuel_type=FuelType(form.fuel_type.data)
        )

        db.session.add(vehicle)
        db.session.commit()

        return redirect(url_for("home.index"))
    return render_template("create/vehicle.html", form=form)


@create_bp.route("/create/product", methods=['GET', 'POST'])
def product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash("Product created successfully!", "success")
        return redirect(url_for("home.index"))
    return render_template("create/product.html", form=form)



@create_bp.route("/create/event")
def event():
    form = EventForm()
    return render_template(
        "create/event.html",
        form=form)