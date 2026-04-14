from datetime import datetime
from app.extensions import db
import enum

# ------------------
# User
# ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

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

    events = db.relationship('Event', secondary='event_vehicle', backref='vehicles')

# Association table for many-to-many Event <-> Vehicle
event_vehicle = db.Table('event_vehicle',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'))
)
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
    db.Column('event_product_id', db.Integer, db.ForeignKey('event_product.id')),
    db.Column('product_extra_id', db.Integer, db.ForeignKey('product_extra.id'))
)

class EventProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product')
    # NEW
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    extras = db.relationship('ProductExtra', secondary=event_product_extra)


# ------------------
# Staff
# ------------------
# Association table for many-to-many Event <-> Staff
### This table is going to change
event_staff = db.Table(
    'event_staff',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id'), primary_key=True)
)


class Staff(db.Model, PriceMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)

    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    # Relationships
    events = db.relationship('Event', secondary='event_staff', backref='staff_members')
    skills = db.relationship('StaffSkill', backref='staff', cascade="all, delete-orphan")  # ← keep this




# ------------------
# Event
# ------------------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    unit_start_time = db.Column(db.Time)
    venue_start_time = db.Column(db.Time)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    products = db.relationship('EventProduct', backref='event')

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    extra = db.Column(db.String(200))
    invoice = db.Column(db.String(100))
    notes = db.Column(db.Text)