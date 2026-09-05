# forms/facturacion_form.py - Formulario para el modulo de facturacion

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class FacturacionForm(FlaskForm):
    cliente = StringField(
        'Nombre del cliente',
        validators=[DataRequired(message='El cliente es obligatorio.'),
                    Length(min=3, message='El nombre debe tener al menos 3 caracteres.')]
    )
    servicio = StringField(
        'Servicio prestado',
        validators=[DataRequired(message='El servicio es obligatorio.')]
    )
    total = DecimalField(
        'Total ($)',
        validators=[DataRequired(message='El total es obligatorio.'),
                    NumberRange(min=1, message='El total debe ser mayor a 0.')]
    )
    submit = SubmitField('Registrar factura')
