from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, IntegerField, FloatField,
    SelectField, SubmitField
)
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email, ValidationError

from app.models import ShoeCategory, Shoe, Manufacturer, User


class ShoeForm(FlaskForm):
    """Form to create or edit a shoe."""
    name = StringField(
        'Shoe Name',
        validators=[DataRequired(), Length(min=3, max=120)]
    )

    year = IntegerField(
        'Model Year',
        validators=[NumberRange(min=1900, max=2100, message="Enter a valid year.")]
    )
    size = FloatField(
        'Size (US)',
        validators=[DataRequired(), NumberRange(min=1, max=20, message="Enter a valid shoe size.")]
    )

    manufacturer = QuerySelectField(
        'Manufacturer',
        query_factory=lambda: Manufacturer.query,
        allow_blank=False
    )
    category = SelectField(
        'Category',
        choices=ShoeCategory.choices()
    )
    submit = SubmitField('Submit')


class ManufacturerForm(FlaskForm):
    """Form to create or edit a manufacturer."""
    name = StringField(
        'Manufacturer Name', 
        validators=[DataRequired(), Length(min=2, max=80)]
    )
    country = StringField(
        'Country',
        validators=[Length(max=80)]
    )
    submit = SubmitField('Submit')
