from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from collections import namedtuple

CHOICES = [
    ('smiles', 'SMILES'),
    ('inchi', 'InChI'),
    ('inchikey', 'InChIKey'),
    # ('mol', 'MDL Molblock')
]

class MolForm(FlaskForm):
    value = StringField("Input", validators=[DataRequired()])
    choices = SelectField("Input Type", choices=CHOICES)
    submit = SubmitField('Submit')

Result = namedtuple('Result', 'input input_value smiles inchi inchikey mb')