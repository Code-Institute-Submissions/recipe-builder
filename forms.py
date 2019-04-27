from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.validators import DataRequired

    
class RecipeSearchForm(Form):
    choices = [('Recipe', 'Recipe'),
               ('Category', 'Category'),
               ('Serves', 'Serves'),
               ('Allergen', 'Allergen')]
    select = SelectField('Search for recipes:', choices=choices)
    search = StringField('')
