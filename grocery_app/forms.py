from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    title = StringField('title', [validators.Length(min=4, max=25)])
    # - address - StringField
    address = StringField('Address', [validators.Length(min=4, max=25)])
    # - submit button
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    name = StringField('Username', [validators.Length(min=4, max=25)])
    # - price - FloatField
    price = FloatField('Price')
    # - category - SelectField (specify the 'choices' param)
    category = SelectField('Category', choices = ['Deli', 'Produce', 'Bakery', 'Pantry', 'Frozen', 'Other'])
    # - photo_url - StringField (use a URL validator)
    photo_url = StringField('Photo URL', [validators.Length(min=4, max=25)])
    # - store - QuerySelectField (specify the `query_factory` param)
    store = QuerySelectField('Store', query_factory = store)
    # - submit button
    submit = SubmitField('Submit')
    
