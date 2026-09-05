# forms/servicio_form.py - Formulario para el modulo de servicios

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ServicioForm(FlaskForm):
    nombre = StringField(
        'Nombre del servicio',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, message='El nombre debe tener al menos 3 caracteres.')]
    )
    descripcion = StringField(
        'Descripcion',
        validators=[DataRequired(message='La descripcion es obligatoria.'),
                    Length(min=10, message='La descripcion debe tener al menos 10 caracteres.')]
    )
    categoria = SelectField(
        'Categoria',
        choices=[('', '-- Selecciona una categoria --'),
                 ('Hardware', 'Hardware'),
                 ('Sistema', 'Sistema'),
                 ('Software', 'Software'),
                 ('Redes', 'Redes')],
        validators=[DataRequired(message='Selecciona una categoria.')]
    )
    submit = SubmitField('Registrar servicio')
