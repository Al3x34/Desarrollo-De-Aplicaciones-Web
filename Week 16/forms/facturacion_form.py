# forms/facturacion_form.py - Formulario para el modulo de facturacion
# Las listas de cliente, servicio y tecnico se llenan desde la base de datos (app.py)

from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente_id = SelectField(
        'Cliente',
        coerce=int,
        validators=[NumberRange(min=1, message='Selecciona un cliente.')]
    )
    servicio_id = SelectField(
        'Servicio prestado',
        coerce=int,
        validators=[NumberRange(min=1, message='Selecciona un servicio.')]
    )
    tecnico_id = SelectField(
        'Tecnico responsable',
        coerce=int,
        validators=[NumberRange(min=1, message='Selecciona un tecnico.')]
    )
    fecha = DateField(
        'Fecha',
        validators=[DataRequired(message='La fecha es obligatoria.')]
    )
    total = DecimalField(
        'Total ($)',
        places=2,
        validators=[DataRequired(message='El total es obligatorio.'),
                    NumberRange(min=1, message='El total debe ser mayor a 0.')]
    )
    submit = SubmitField('Registrar factura')
