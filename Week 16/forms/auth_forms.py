# forms/auth_forms.py - Formularios de inicio de sesion y registro de usuarios

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

class LoginForm(FlaskForm):
    usuario = StringField(
        'Usuario',
        validators=[DataRequired(message='El usuario es obligatorio.')]
    )
    password = PasswordField(
        'Contrasena',
        validators=[DataRequired(message='La contrasena es obligatoria.')]
    )
    recordar = BooleanField('Recordarme')
    submit = SubmitField('Iniciar sesion')

class RegistroForm(FlaskForm):
    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, message='El nombre debe tener al menos 3 caracteres.')]
    )
    usuario = StringField(
        'Usuario',
        validators=[DataRequired(message='El usuario es obligatorio.'),
                    Length(min=4, max=20, message='El usuario debe tener entre 4 y 20 caracteres.'),
                    Regexp(r'^[A-Za-z0-9_.]+$', message='Usa solo letras, numeros, punto o guion bajo.')]
    )
    password = PasswordField(
        'Contrasena',
        validators=[DataRequired(message='La contrasena es obligatoria.'),
                    Length(min=6, message='La contrasena debe tener al menos 6 caracteres.')]
    )
    confirmar = PasswordField(
        'Confirmar contrasena',
        validators=[DataRequired(message='Confirma la contrasena.'),
                    EqualTo('password', message='Las contrasenas no coinciden.')]
    )
    submit = SubmitField('Crear cuenta')
