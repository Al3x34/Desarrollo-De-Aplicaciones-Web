# forms/tecnico_form.py - Formulario para el modulo de tecnicos

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class TecnicoForm(FlaskForm):
    nombre = StringField(
        'Nombre del tecnico',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, message='El nombre debe tener al menos 3 caracteres.')]
    )
    especialidad = SelectField(
        'Especialidad',
        choices=[('', '-- Selecciona una especialidad --'),
                 ('Mantenimiento', 'Mantenimiento'),
                 ('Redes', 'Redes'),
                 ('Software', 'Software'),
                 ('Formateo y Respaldo', 'Formateo y Respaldo')],
        validators=[DataRequired(message='Selecciona una especialidad.')]
    )
    submit = SubmitField('Registrar tecnico')
