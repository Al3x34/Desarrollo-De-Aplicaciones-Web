# forms/cliente_form.py - Formulario para el modulo de clientes

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    nombre = StringField(
        'Nombre del cliente',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, message='El nombre debe tener al menos 3 caracteres.')]
    )
    correo = StringField(
        'Correo electronico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingresa un correo valido.')]
    )
    telefono = StringField(
        'Telefono',
        validators=[DataRequired(message='El telefono es obligatorio.'),
                    Length(min=7, message='Ingresa un telefono valido.')]
    )
    submit = SubmitField('Registrar cliente')
