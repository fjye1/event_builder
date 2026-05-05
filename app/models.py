import enum
from sqlalchemy import Enum
from app.extensions import db
from datetime import datetime
from datetime import date


# ------------------
# User
# ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), unique=True, nullable=True)

    # Determines privilege level
    role = db.Column(db.String(50))

    # Relationships
    events = db.relationship('Event', backref='created_by', lazy=True)


# ------------------
# Company
# ------------------
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # One-to-many: a company can have multiple clients
    clients = db.relationship('Client', backref='company', lazy=True)


# ------------------
# Client
# ------------------
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))

    # Optional link to a company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)

    # Many-to-many with venues (via association table)
    venues = db.relationship(
        'Venue',
        secondary='venue_clients',
        back_populates='clients'
    )

    # Optional link to events
    events = db.relationship('Event', backref='client_ref', lazy=True)


# Association table for many-to-many between Venue and Client
venue_clients = db.Table(
    'venue_clients',
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'))
)


# ------------------
# Venue
# ------------------
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))

    # Many-to-many with clients
    clients = db.relationship(
        'Client',
        secondary=venue_clients,
        back_populates='venues'
    )

    # One-to-many with events
    events = db.relationship('Event', backref='venue_ref', lazy=True)


# ------------------
# Vehicle
# ------------------

class FuelType(enum.Enum):
    ELECTRIC = "electric"
    PETROL = "petrol"
    DIESEL = "diesel"


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    license_plate = db.Column(db.String(20))
    miles_per_gallon = db.Column(db.Integer)

    fuel_type = db.Column(db.Enum(FuelType), nullable=False)

    product_space = db.Column(db.Integer, nullable=False, default=1)
    passenger_space = db.Column(db.Integer, nullable=False, default=3)




# ------------------
# Skills
# ------------------
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False, default="core")
    # e.g., "core" = required for doing the product, "service" = optional/service side


# Product ↔ Skill
product_skill = db.Table(
    'product_skill',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

# ProductExtra ↔ Skill
product_extra_skill = db.Table(
    'product_extra_skill',
    db.Column('product_extra_id', db.Integer, db.ForeignKey('product_extra.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)


class StaffSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    proficiency = db.Column(db.Integer, default=0)

    # staff relationship removed — Staff handles it
    skill = db.relationship('Skill', backref='staff_members')


# ------------------
# Product
# ------------------

class PriceMixin:
    """Provides a price column and a Stripe-ready pence property."""
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    @property
    def price_in_pence(self):
        if self.price is None:
            return 0
        # Rounding before casting to int is a safety best-practice
        return int(round(self.price * 100))


# This is the table of the base product like just the espresso bike
class Product(db.Model, PriceMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    skills = db.relationship('Skill', secondary=product_skill, backref='products')


# this is the table of extras that can be applied to a product branding or espresso printer
class ProductExtra(db.Model, PriceMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='extras')
    skills = db.relationship('Skill', secondary=product_extra_skill, backref='product_extras')


# Association table for EventProduct <-> ProductExtra
event_product_extra = db.Table(
    'event_product_extra',
    db.Column('event_product_id', db.Integer,
              db.ForeignKey('event_product.id', ondelete="CASCADE")),  # Add here
    db.Column('product_extra_id', db.Integer, db.ForeignKey('product_extra.id'))
)


class EventProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product')
    # NEW
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    extras = db.relationship('ProductExtra', secondary=event_product_extra)


# ------------------
# Staff
# ------------------
class EventStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    event_product_id = db.Column(db.Integer, db.ForeignKey('event_product.id'), nullable=True)

    arrival_mode = db.Column(
        db.Enum("unit", "venue", name="arrivalmode"),
        nullable=False,
        default="unit"
    )

    # Relationships (ONLY where needed)
    staff = db.relationship('Staff')
    event_product = db.relationship('EventProduct', backref='staff_assignments')


class Staff(db.Model, PriceMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    # Relationships
    skills = db.relationship('StaffSkill', backref='staff', cascade="all, delete-orphan")
    user = db.relationship('User', backref='staff', uselist=False)


# ------------------
# Event
# ------------------

class EventStatus(enum.Enum):
    generated = "generated"
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"




class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=True)
    status = db.Column(
        db.Enum(EventStatus),
        nullable=False,
        default=EventStatus.generated
    )
    enquiry_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    date = db.Column(db.Date, nullable=False, default=date.today)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    product_space = db.Column(db.Integer, nullable=True)
    # 🧠 NEW LOGIC CONTROLS
    load_in_offset = db.Column(db.Integer, default=0)
    # 0 = same day, -1 = day before, -2 etc

    pickup_offset = db.Column(db.Integer, default=0)
    # 0 = same day, +1 = next day, +2 etc
    # Relationships
    event_products = db.relationship(
        'EventProduct',
        backref='event',
        cascade="all, delete-orphan"
    )

    staff_assignments = db.relationship(
        'EventStaff',
        backref='event',
        cascade="all, delete-orphan"
    )



    invoice = db.Column(db.String(100))
    notes = db.Column(db.Text)

    def build_staff_schedule(self):
        schedule = []

        for sa in self.staff_assignments:

            if sa.arrival_mode == "unit":
                arrive = self.arrive_unit_time
            else:
                arrive = self.arrive_venue_time

            schedule.append({
                "staff": sa.staff.name,
                "arrival_mode": sa.arrival_mode,
                "arrive_time": arrive,
                "service_start": self.service_start_time,
                "service_end": self.service_end_time
            })

        return schedule


    def summary(self):  # ← indented inside the class
        data = {
            "event_name": self.event_name or "Unnamed Event",
            "client": self.client_ref.name if self.client_ref else None,
            "venue": self.venue_ref.name if self.venue_ref else None,
            "products": [],
            "extras": set(),
            "staff": [],

        }

        for ep in self.event_products:
            product_info = {
                "name": ep.product.name if ep.product else "Unknown",
                "start": ep.start_time,
                "end": ep.end_time
            }
            data["products"].append(product_info)

            for ex in ep.extras:
                data["extras"].add(ex.name)

        for sa in self.staff_assignments:
            staff_info = {
                "name": sa.staff.name if sa.staff else "Unknown",
                "product": sa.event_product.product.name if sa.event_product and sa.event_product.product else None
            }
            data["staff"].append(staff_info)

        data["extras"] = list(data["extras"])  # ← convert set → list before returning
        return data


class EventMovement(db.Model):


    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    movement_type = db.Column(db.String(20))
    # "delivery" or "pickup"



    # optional overrides
    venue_arrival = db.Column(db.Time, nullable=True)
    venue_pickup = db.Column(db.Time, nullable=True)

    event = db.relationship("Event", backref="movements")