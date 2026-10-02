# app.py - TechFix - Semana 16 (Proyecto final)
# Incluye: Flask, Jinja2, Flask-WTF, SQLite, Flask-Login
# - Login y registro de usuarios con contrasenas cifradas (Werkzeug)
# - CRUD completo de servicios, clientes, tecnicos y facturas
# - La tabla facturas se relaciona con clientes, servicios y tecnicos (claves foraneas)

import sqlite3
import os
from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms.servicio_form import ServicioForm
from forms.cliente_form import ClienteForm
from forms.tecnico_form import TecnicoForm
from forms.facturacion_form import FacturacionForm
from forms.auth_forms import LoginForm, RegistroForm

app = Flask(__name__)
app.secret_key = 'techfix_clave_secreta_2026'

# Proteccion CSRF para todos los formularios POST (incluidos los de eliminar)
csrf = CSRFProtect(app)

# Ruta a la base de datos (se calcula desde la carpeta del proyecto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'techfix.db')

# ---------------------------------------------------------------
# Configuracion de Flask-Login
# ---------------------------------------------------------------
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesion para acceder a esta seccion.'
login_manager.login_message_category = 'warning'


class Usuario(UserMixin):
    def __init__(self, id, nombre, usuario, password_hash):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.password_hash = password_hash

    @staticmethod
    def desde_fila(fila):
        if fila is None:
            return None
        return Usuario(fila['id'], fila['nombre'], fila['usuario'], fila['password_hash'])


@login_manager.user_loader
def cargar_usuario(user_id):
    conn = get_db()
    fila = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return Usuario.desde_fila(fila)


# ---------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # SQLite necesita activar las claves foraneas en cada conexion
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    ''')

    # Tabla principal: cada factura pertenece a un cliente, un servicio y un tecnico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            servicio_id INTEGER NOT NULL,
            tecnico_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE RESTRICT,
            FOREIGN KEY (servicio_id) REFERENCES servicios (id) ON DELETE RESTRICT,
            FOREIGN KEY (tecnico_id) REFERENCES tecnicos (id) ON DELETE RESTRICT
        )
    ''')

    conn.commit()
    cargar_datos_iniciales(conn)
    conn.close()


def cargar_datos_iniciales(conn):
    # Usuario administrador de prueba (solo se crea si no hay usuarios)
    if conn.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0] == 0:
        conn.execute(
            'INSERT INTO usuarios (nombre, usuario, password_hash) VALUES (?, ?, ?)',
            ('Administrador', 'admin', generate_password_hash('admin123'))
        )

    # Datos de ejemplo para la demostracion (solo si la base esta vacia)
    if conn.execute('SELECT COUNT(*) FROM servicios').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO servicios (nombre, descripcion, categoria, precio) VALUES (?, ?, ?, ?)',
            [
                ('Mantenimiento preventivo', 'Limpieza interna y cambio de pasta termica.', 'Hardware', 25.00),
                ('Formateo e instalacion', 'Formateo del equipo e instalacion de Windows y drivers.', 'Sistema', 30.00),
                ('Instalacion de software', 'Instalacion de Office, antivirus y programas basicos.', 'Software', 15.00),
                ('Configuracion de red WiFi', 'Configuracion del router y la red domestica.', 'Redes', 20.00),
            ]
        )
    if conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO clientes (nombre, correo, telefono) VALUES (?, ?, ?)',
            [
                ('Maria Lopez', 'maria.lopez@correo.com', '0991234567'),
                ('Jorge Paredes', 'jorge.paredes@correo.com', '0987654321'),
                ('Lucia Andrade', 'lucia.andrade@correo.com', '0974561230'),
            ]
        )
    if conn.execute('SELECT COUNT(*) FROM tecnicos').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO tecnicos (nombre, especialidad) VALUES (?, ?)',
            [
                ('Carlos Mendoza', 'Mantenimiento'),
                ('Luis Torres', 'Redes'),
                ('Ana Suarez', 'Software'),
            ]
        )
    if conn.execute('SELECT COUNT(*) FROM facturas').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO facturas (cliente_id, servicio_id, tecnico_id, fecha, total) VALUES (?, ?, ?, ?, ?)',
            [
                (1, 1, 1, '2026-09-20', 25.00),
                (2, 4, 2, '2026-09-24', 20.00),
                (3, 3, 3, '2026-09-28', 15.00),
            ]
        )
    conn.commit()


def obtener_o_404(conn, tabla, id):
    fila = conn.execute(f'SELECT * FROM {tabla} WHERE id = ?', (id,)).fetchone()
    if fila is None:
        conn.close()
        abort(404)
    return fila


def eliminar_registro(tabla, id, descripcion):
    # Elimina un registro; si tiene facturas asociadas, la clave foranea lo impide
    conn = get_db()
    obtener_o_404(conn, tabla, id)
    try:
        conn.execute(f'DELETE FROM {tabla} WHERE id = ?', (id,))
        conn.commit()
        flash(f'Se elimino {descripcion} correctamente.', 'success')
    except sqlite3.IntegrityError:
        flash(f'No se puede eliminar {descripcion} porque tiene facturas asociadas. '
              'Elimina o edita primero esas facturas.', 'danger')
    finally:
        conn.close()


# Inicializar la base de datos al arrancar
init_db()


# ---------------------------------------------------------------
# Autenticacion
# ---------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('panel'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = get_db()
        fila = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (form.usuario.data.strip(),)).fetchone()
        conn.close()
        usuario = Usuario.desde_fila(fila)
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            login_user(usuario, remember=form.recordar.data)
            flash(f'Bienvenido, {usuario.nombre}.', 'success')
            siguiente = request.args.get('next')
            # Solo se permite redirigir a rutas internas
            if not siguiente or not siguiente.startswith('/') or siguiente.startswith('//'):
                siguiente = url_for('panel')
            return redirect(siguiente)
        flash('Usuario o contrasena incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('panel'))
    form = RegistroForm()
    if form.validate_on_submit():
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO usuarios (nombre, usuario, password_hash) VALUES (?, ?, ?)',
                (form.nombre.data.strip(), form.usuario.data.strip(), generate_password_hash(form.password.data))
            )
            conn.commit()
            flash('Cuenta creada correctamente. Ya puedes iniciar sesion.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            form.usuario.errors.append('Ese nombre de usuario ya esta registrado.')
        finally:
            conn.close()
    return render_template('auth/registro.html', form=form)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada correctamente.', 'info')
    return redirect(url_for('login'))


# ---------------------------------------------------------------
# Paginas generales
# ---------------------------------------------------------------
@app.route('/')
def index():
    nombre_empresa = 'TechFix'
    return render_template('index.html', nombre_empresa=nombre_empresa)


@app.route('/panel')
@login_required
def panel():
    conn = get_db()
    totales = {
        'servicios': conn.execute('SELECT COUNT(*) FROM servicios').fetchone()[0],
        'clientes': conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0],
        'tecnicos': conn.execute('SELECT COUNT(*) FROM tecnicos').fetchone()[0],
        'facturas': conn.execute('SELECT COUNT(*) FROM facturas').fetchone()[0],
        'ingresos': conn.execute('SELECT COALESCE(SUM(total), 0) FROM facturas').fetchone()[0],
    }
    ultimas = conn.execute('''
        SELECT f.id, f.fecha, f.total, c.nombre AS cliente, s.nombre AS servicio, t.nombre AS tecnico
        FROM facturas f
        JOIN clientes c ON c.id = f.cliente_id
        JOIN servicios s ON s.id = f.servicio_id
        JOIN tecnicos t ON t.id = f.tecnico_id
        ORDER BY f.fecha DESC, f.id DESC
        LIMIT 5
    ''').fetchall()
    conn.close()
    return render_template('panel.html', totales=totales, ultimas=ultimas)


# ---------------------------------------------------------------
# CRUD Servicios
# ---------------------------------------------------------------
@app.route('/servicios')
@login_required
def servicios():
    conn = get_db()
    lista = conn.execute('SELECT * FROM servicios ORDER BY id').fetchall()
    conn.close()
    return render_template('servicios.html', servicios=lista)


@app.route('/servicios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_servicio():
    form = ServicioForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute(
            'INSERT INTO servicios (nombre, descripcion, categoria, precio) VALUES (?, ?, ?, ?)',
            (form.nombre.data, form.descripcion.data, form.categoria.data, float(form.precio.data))
        )
        conn.commit()
        conn.close()
        flash('Servicio registrado correctamente.', 'success')
        return redirect(url_for('servicios'))
    return render_template('formulario_servicio.html', form=form, titulo='Registrar Servicio')


@app.route('/servicios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_servicio(id):
    conn = get_db()
    servicio = obtener_o_404(conn, 'servicios', id)
    form = ServicioForm(data=dict(servicio) if request.method == 'GET' else None)
    form.submit.label.text = 'Guardar cambios'
    if form.validate_on_submit():
        conn.execute(
            'UPDATE servicios SET nombre = ?, descripcion = ?, categoria = ?, precio = ? WHERE id = ?',
            (form.nombre.data, form.descripcion.data, form.categoria.data, float(form.precio.data), id)
        )
        conn.commit()
        conn.close()
        flash('Servicio actualizado correctamente.', 'success')
        return redirect(url_for('servicios'))
    conn.close()
    return render_template('formulario_servicio.html', form=form, titulo='Editar Servicio')


@app.route('/servicios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_servicio(id):
    eliminar_registro('servicios', id, 'el servicio')
    return redirect(url_for('servicios'))


# ---------------------------------------------------------------
# CRUD Clientes
# ---------------------------------------------------------------
@app.route('/clientes')
@login_required
def clientes():
    conn = get_db()
    lista = conn.execute('''
        SELECT c.*, COUNT(f.id) AS num_facturas
        FROM clientes c
        LEFT JOIN facturas f ON f.cliente_id = c.id
        GROUP BY c.id
        ORDER BY c.id
    ''').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=lista)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute(
            'INSERT INTO clientes (nombre, correo, telefono) VALUES (?, ?, ?)',
            (form.nombre.data, form.correo.data, form.telefono.data)
        )
        conn.commit()
        conn.close()
        flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form, titulo='Registrar Cliente')


@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    conn = get_db()
    cliente = obtener_o_404(conn, 'clientes', id)
    form = ClienteForm(data=dict(cliente) if request.method == 'GET' else None)
    form.submit.label.text = 'Guardar cambios'
    if form.validate_on_submit():
        conn.execute(
            'UPDATE clientes SET nombre = ?, correo = ?, telefono = ? WHERE id = ?',
            (form.nombre.data, form.correo.data, form.telefono.data, id)
        )
        conn.commit()
        conn.close()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))
    conn.close()
    return render_template('formulario_cliente.html', form=form, titulo='Editar Cliente')


@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_cliente(id):
    eliminar_registro('clientes', id, 'el cliente')
    return redirect(url_for('clientes'))


# ---------------------------------------------------------------
# CRUD Tecnicos
# ---------------------------------------------------------------
@app.route('/tecnicos')
@login_required
def tecnicos():
    conn = get_db()
    lista = conn.execute('''
        SELECT t.*, COUNT(f.id) AS num_facturas
        FROM tecnicos t
        LEFT JOIN facturas f ON f.tecnico_id = t.id
        GROUP BY t.id
        ORDER BY t.id
    ''').fetchall()
    conn.close()
    return render_template('tecnicos.html', tecnicos=lista)


@app.route('/tecnicos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_tecnico():
    form = TecnicoForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute(
            'INSERT INTO tecnicos (nombre, especialidad) VALUES (?, ?)',
            (form.nombre.data, form.especialidad.data)
        )
        conn.commit()
        conn.close()
        flash('Tecnico registrado correctamente.', 'success')
        return redirect(url_for('tecnicos'))
    return render_template('formulario_tecnico.html', form=form, titulo='Registrar Tecnico')


@app.route('/tecnicos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tecnico(id):
    conn = get_db()
    tecnico = obtener_o_404(conn, 'tecnicos', id)
    form = TecnicoForm(data=dict(tecnico) if request.method == 'GET' else None)
    form.submit.label.text = 'Guardar cambios'
    if form.validate_on_submit():
        conn.execute(
            'UPDATE tecnicos SET nombre = ?, especialidad = ? WHERE id = ?',
            (form.nombre.data, form.especialidad.data, id)
        )
        conn.commit()
        conn.close()
        flash('Tecnico actualizado correctamente.', 'success')
        return redirect(url_for('tecnicos'))
    conn.close()
    return render_template('formulario_tecnico.html', form=form, titulo='Editar Tecnico')


@app.route('/tecnicos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_tecnico(id):
    eliminar_registro('tecnicos', id, 'el tecnico')
    return redirect(url_for('tecnicos'))


# ---------------------------------------------------------------
# CRUD Facturas (relaciona clientes, servicios y tecnicos)
# ---------------------------------------------------------------
def cargar_opciones_factura(form, conn):
    # Llena las listas desplegables con los registros de las tablas relacionadas
    form.cliente_id.choices = [(0, '-- Selecciona un cliente --')] + [
        (c['id'], c['nombre']) for c in conn.execute('SELECT id, nombre FROM clientes ORDER BY nombre')
    ]
    servicios = conn.execute('SELECT id, nombre, precio FROM servicios ORDER BY nombre').fetchall()
    form.servicio_id.choices = [(0, '-- Selecciona un servicio --')] + [
        (s['id'], f"{s['nombre']} (${s['precio']:.2f})") for s in servicios
    ]
    form.tecnico_id.choices = [(0, '-- Selecciona un tecnico --')] + [
        (t['id'], f"{t['nombre']} - {t['especialidad']}")
        for t in conn.execute('SELECT id, nombre, especialidad FROM tecnicos ORDER BY nombre')
    ]
    # Precios de cada servicio para autocompletar el total con JavaScript
    return {s['id']: s['precio'] for s in servicios}


@app.route('/facturacion')
@login_required
def facturacion():
    conn = get_db()
    lista = conn.execute('''
        SELECT f.id, f.fecha, f.total,
               c.nombre AS cliente, s.nombre AS servicio, s.categoria, t.nombre AS tecnico
        FROM facturas f
        JOIN clientes c ON c.id = f.cliente_id
        JOIN servicios s ON s.id = f.servicio_id
        JOIN tecnicos t ON t.id = f.tecnico_id
        ORDER BY f.id
    ''').fetchall()
    conn.close()
    return render_template('facturacion.html', facturas=lista)


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
def nueva_factura():
    conn = get_db()
    form = FacturacionForm()
    precios = cargar_opciones_factura(form, conn)
    if request.method == 'GET':
        form.fecha.data = date.today()
    if form.validate_on_submit():
        conn.execute(
            'INSERT INTO facturas (cliente_id, servicio_id, tecnico_id, fecha, total) VALUES (?, ?, ?, ?, ?)',
            (form.cliente_id.data, form.servicio_id.data, form.tecnico_id.data,
             form.fecha.data.isoformat(), float(form.total.data))
        )
        conn.commit()
        conn.close()
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    conn.close()
    return render_template('formulario_facturacion.html', form=form, titulo='Registrar Factura', precios=precios)


@app.route('/facturacion/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_factura(id):
    conn = get_db()
    factura = obtener_o_404(conn, 'facturas', id)
    form = FacturacionForm()
    precios = cargar_opciones_factura(form, conn)
    form.submit.label.text = 'Guardar cambios'
    if request.method == 'GET':
        form.cliente_id.data = factura['cliente_id']
        form.servicio_id.data = factura['servicio_id']
        form.tecnico_id.data = factura['tecnico_id']
        form.fecha.data = date.fromisoformat(factura['fecha'])
        form.total.data = factura['total']
    if form.validate_on_submit():
        conn.execute(
            'UPDATE facturas SET cliente_id = ?, servicio_id = ?, tecnico_id = ?, fecha = ?, total = ? WHERE id = ?',
            (form.cliente_id.data, form.servicio_id.data, form.tecnico_id.data,
             form.fecha.data.isoformat(), float(form.total.data), id)
        )
        conn.commit()
        conn.close()
        flash('Factura actualizada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    conn.close()
    return render_template('formulario_facturacion.html', form=form, titulo='Editar Factura', precios=precios)


@app.route('/facturacion/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_factura(id):
    eliminar_registro('facturas', id, 'la factura')
    return redirect(url_for('facturacion'))


@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
