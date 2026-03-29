# from flask_ckeditor import CKEditorField
# from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TimeField, TextAreaField, SubmitField, \
    PasswordField, EmailField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms.validators import EqualTo, Email
from app.models import Client


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
    # Example SelectField for client
    client = SelectField(
        'Client',
        choices=[('client1', 'Client 1'), ('client2', 'Client 2')],  # replace with your real clients
        validators=[DataRequired()]
    )

    client_contact_details = StringField('Client Contact Details', validators=[Optional()])
    client_venue = StringField('Client Venue', validators=[Optional()])

    staff = StringField('Staff', validators=[Optional()])

    product = StringField('Product', validators=[Optional()])
    extra = StringField('Extra', validators=[Optional()])
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
    submit = SubmitField("Save Product")
