from flask import Blueprint, render_template, url_for, redirect, flash

from app.extensions import db
from app.forms import EventForm, CompanyForm, ClientForm, VenueForm, VehicleForm, ProductForm, ProductExtraForm, \
    SkillForm, StaffForm, EventProductForm, EventStaffForm
from app.models import Company, Client, Venue, Vehicle, FuelType, Product, ProductExtra, Skill, Staff, Event, \
    EventProduct, EventStaff

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
            miles_per_gallon=form.miles_per_gallon.data,
            fuel_type=FuelType(form.fuel_type.data)
        )

        db.session.add(vehicle)
        db.session.commit()
        flash(f"Vehicle '{vehicle.name}' created successfully.", "success")
        return redirect(url_for("home.index"))
    return render_template("create/vehicle.html", form=form)


@create_bp.route("/create/product", methods=['GET', 'POST'])
def product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(product)
        db.session.commit()
        flash(f"Product '{product.name}' created successfully.", "success")
        return redirect(url_for("home.index"))
    return render_template("create/product.html", form=form)


@create_bp.route("/create/product-extra", methods=['GET', 'POST'])
def product_extra():
    form = ProductExtraForm()
    # populate dropdown with existing products
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name).all()]

    if form.validate_on_submit():
        extra = ProductExtra(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            product_id=form.product_id.data
        )
        db.session.add(extra)
        db.session.commit()
        flash(f"Product extra '{extra.name}' built on base of '{extra.product.name}' created successfully.", "success")
        return redirect(url_for("home.index"))

    return render_template("create/product_extra.html", form=form)


@create_bp.route("/create/skill", methods=['GET', 'POST'])
def skill():
    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill(name=form.name.data)
        # attach selected products
        skill.products = list(form.products.data)
        skill.product_extras = list(form.product_extras.data)
        db.session.add(skill)
        db.session.commit()
        flash("Skill created successfully!", "success")
        return redirect(url_for("home.index"))

    return render_template("create/skill.html", form=form)


@create_bp.route("/create/staff", methods=['GET', 'POST'])
def staff():
    form = StaffForm()
    if form.validate_on_submit():
        staff_member = Staff(
            name=form.name.data,
            age=form.age.data,
            phone=form.phone.data,
            email=form.email.data,
            active=form.active.data,
            price=form.price.data,
            notes=form.notes.data
        )
        db.session.add(staff_member)
        db.session.commit()
        flash("Staff member created successfully!", "success")
        return redirect(url_for("home.index"))

    return render_template("create/staff.html", form=form)


@create_bp.route("/create/event", methods=["GET", "POST"])
def event():
    form = EventForm()

    # Company dropdown
    companies = Company.query.all()
    form.company_id.choices = [(0, "— None —")] + [(c.id, c.name) for c in companies]

    # Clients depend on company
    company_id = form.company_id.data or 0
    clients = Client.query.filter_by(company_id=company_id).all() if company_id else []
    form.client_id.choices = [(0, "— Select Client —")] + [(c.id, c.name) for c in clients]

    # Venues depend on client
    client_id = form.client_id.data or 0
    client = Client.query.get(client_id) if client_id else None
    venues = client.venues if client else []
    form.venue_id.choices = [(0, "— None —")] + [(v.id, v.name) for v in venues]

    if form.validate_on_submit():
        new_event = Event(
            date=form.date.data,
            company_id=company_id if company_id else None,
            client_id=form.client_id.data if form.client_id.data else None,
            venue_id=form.venue_id.data if form.venue_id.data else None,
            invoice=form.invoice.data,
            notes=form.notes.data
        )

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("create.add_event_product", event_id=new_event.id))

    return render_template("create/event.html", form=form)


@create_bp.route("/create/event/<int:event_id>/product", methods=["GET", "POST"])
def add_event_product(event_id):
    form = EventProductForm()
    event = Event.query.get_or_404(event_id)

    # Populate product choices
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]

    # Populate extras based on selected product
    product_id = form.product_id.data
    if product_id:
        extras = ProductExtra.query.filter_by(product_id=product_id).all()
    else:
        extras = []

    form.extras.choices = [(e.id, e.name) for e in extras]

    if form.validate_on_submit():
        new_event_product = EventProduct(
            event_id=event.id,
            product_id=form.product_id.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )

        # Attach extras
        if form.extras.data:
            selected_extras = ProductExtra.query.filter(
                ProductExtra.id.in_(form.extras.data)
            ).all()
            new_event_product.extras = selected_extras

        db.session.add(new_event_product)
        db.session.commit()

        return redirect(
            url_for("create.add_event_staff", event_product_id=new_event_product.id)
        )

    return render_template(
        "create/event_product.html",
        form=form,
        event=event
    )


@create_bp.route("/create/event_product/<int:event_product_id>/staff", methods=["GET", "POST"])
def add_event_staff(event_product_id):
    form = EventStaffForm()

    event_product = EventProduct.query.get_or_404(event_product_id)
    event = event_product.event
    form.staff_id.choices = [(s.id, s.name) for s in Staff.query.filter_by(active=True).all()]

    if form.validate_on_submit():
        new_event_staff = EventStaff(
            event_id=event.id,
            staff_id=form.staff_id.data,
            event_product_id=form.event_product_id.data or None,
            arrive_unit_time=form.arrive_unit_time.data,
            arrive_venue_time=form.arrive_venue_time.data
        )

        db.session.add(new_event_staff)
        db.session.commit()

        return redirect(url_for("create.add_event_staff", event_product_id=event_product.id))

    return render_template(
        "create/event_staff.html",
        form=form,
        event=event,
        event_product=event_product
    )
