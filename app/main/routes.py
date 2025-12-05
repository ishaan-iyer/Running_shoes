"""Import packages and modules."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import Shoe, Manufacturer, User
from app.main.forms import ShoeForm, ManufacturerForm


# Import app and db from app package so that we can run app
from app.extensions import app, db

main = Blueprint("main", __name__)


############################
#        Routes            #
##############3#############




@main.route('/')
def homepage():
    """Homepage showing all shoes and manufacturers."""
    all_shoes = Shoe.query.all()
    all_manufacturers = Manufacturer.query.all()
    return render_template(
        'home.html',
        all_shoes=all_shoes,
        all_manufacturers=all_manufacturers
    )

@main.route('/create_shoe', methods=['GET', 'POST'])
@login_required
def create_shoe():
    """Create a new shoe."""
    form = ShoeForm()


    if form.validate_on_submit():
        new_shoe = Shoe(
            name=form.name.data,
            model_year=form.year.data,
            size=form.size.data,
            manufacturer=form.manufacturer.data,
            category=form.category.data
        )
        db.session.add(new_shoe)
        db.session.commit()

        flash('New shoe was created successfully.')
        # You can change this to a shoe_detail route if you add one
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_shoe.html', form=form)


@main.route('/create_manufacturer', methods=['GET', 'POST'])
@login_required
def create_manufacturer():
    """Create a new manufacturer."""
    form = ManufacturerForm()


    if form.validate_on_submit():
        new_manufacturer = Manufacturer(
            name=form.name.data,
            country=form.country.data
        )
        db.session.add(new_manufacturer)
        db.session.commit()


        flash('New manufacturer created successfully.')
        return redirect(url_for('main.homepage'))
    

    # if form was not valid, or was not submitted yet
    return render_template('create_manufacturer.html', form=form)