"""Create database models to represent tables for a running shoes app."""
from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.orm import backref
import enum


class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)


class ShoeCategory(FormEnum):
    DAILY_TRAINER = "Daily Trainer"
    TEMPO = "Tempo"
    RACER = "Racer"
    TRAIL = "Trail"
    WALKING = "Walking"
    OTHER = "Other"


class Manufacturer(db.Model):
    """Manufacturer model (e.g., Nike, Adidas, Hoka)."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    country = db.Column(db.String(80))

    shoes = db.relationship('Shoe', back_populates='manufacturer')

    def __str__(self):
        return f'<Manufacturer: {self.name}>'

    def __repr__(self):
        return f'<Manufacturer: {self.name}>'


class Shoe(db.Model):
    """Shoe model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)  
    model_year = db.Column(db.Integer)
    size = db.Column(db.Float)   
    category = db.Column(db.Enum(ShoeCategory), default=ShoeCategory.DAILY_TRAINER)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
    manufacturer = db.relationship('Manufacturer', back_populates='shoes')

    users_who_favorited = db.relationship(
        'User',
        secondary='user_shoe',
        back_populates='favorite_shoes'
    )

    def __str__(self):
        return f'<Shoe: {self.name}>'

    def __repr__(self):
        return f'<Shoe: {self.name}>'


class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200), nullable=False)

    favorite_shoes = db.relationship(
        'Shoe',
        secondary='user_shoe',
        back_populates='users_who_favorited'
    )

    def __repr__(self):
        return f'<User: {self.username}>'

favorite_shoes_table = db.Table(
    'user_shoe',
    db.Column('shoe_id', db.Integer, db.ForeignKey('shoe.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)
