# from flask_ckeditor import CKEditorField
# from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TimeField, TextAreaField, SubmitField, \
    PasswordField, EmailField, SelectMultipleField, IntegerField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Optional, EqualTo, Email, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app.models import Client, ProductExtra, Product


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={"autocomplete": "username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"autocomplete": "current-password"})
    submit = SubmitField("Let Me In!")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField("Sign Me Up!")


class EventForm(FlaskForm):
    # Date of the event
    date = DateField('Event Date', validators=[DataRequired()])
    # Times
    unit_start_time = TimeField('Arrive at Unit', validators=[Optional()])
    venue_start_time = TimeField('Arrive at Venue', validators=[Optional()])
    start_time = TimeField('Start Service', validators=[DataRequired()])
    end_time = TimeField('End Service', validators=[DataRequired()])

    company_id = SelectField('Company', coerce=int)
    client_id = SelectField('Client', coerce=int)
    venue_id = SelectField('Venue', coerce=int)

    staff = SelectMultipleField('Staff', coerce=int, validators=[Optional()])
    product = SelectMultipleField('Product', coerce=int, validators=[Optional()])
    extra = SelectMultipleField('Extra', coerce=int, validators=[Optional()])

    invoice = StringField('Invoice', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])

    submit = SubmitField('Create Event')


class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    submit = SubmitField('Create Company')


class ClientForm(FlaskForm):
    name = StringField('Client Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])

    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Create Client')


class VenueForm(FlaskForm):
    name = StringField('Venue Name', validators=[DataRequired()])
    address = StringField('Address')

    # Multiple clients can be selected
    clients = SelectMultipleField('Clients', coerce=int)

    submit = SubmitField('Create Venue')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # populate choices dynamically
        self.clients.choices = [(c.id, c.name) for c in Client.query.all()]


class VehicleForm(FlaskForm):
    name = StringField("Vehicle Name", validators=[DataRequired()])
    license_plate = StringField("License Plate")
    miles_per_gallon = IntegerField("Miles per Gallon")
    product_space = IntegerField("How many products can this vehicle hold",
                                 validators=[DataRequired(), NumberRange(min=1, max=4)])
    passenger_space = IntegerField("How many passengers can travel in this vehicle",
                                   validators=[DataRequired(), NumberRange(min=1)])

    fuel_type = SelectField(
        "Fuel Type",
        choices=[
            ("electric", "Electric"),
            ("petrol", "Petrol"),
            ("diesel", "Diesel"),
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Vehicle")


class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    price = DecimalField('Price (£)', validators=[DataRequired(), NumberRange(min=0)], places=2)
    submit = SubmitField("Save Product")


class ProductExtraForm(FlaskForm):
    name = StringField("Extra Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    price = DecimalField("Price (£)", validators=[NumberRange(min=0)])
    product_id = SelectField("Product", coerce=int, validators=[DataRequired()])  # dropdown
    submit = SubmitField("Save Extra")


class SkillForm(FlaskForm):
    name = StringField("Skill Name", validators=[DataRequired()])
    products = QuerySelectMultipleField(
        "Attach to Products",
        query_factory=lambda: Product.query.order_by(Product.name).all(),
        get_label="name",
        allow_blank=True
    )
    product_extras = QuerySelectMultipleField(
        "Attach to Product Extras",
        query_factory=lambda: ProductExtra.query.order_by(ProductExtra.name).all(),
        get_label="name",
        allow_blank=True
    )
    submit = SubmitField("Save Skill")


class StaffForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=14, max=100)])
    phone = StringField("Phone", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])
    active = BooleanField("Active", default=True)
    price = DecimalField("Hourly Rate (£)", places=2, validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Create Staff")
