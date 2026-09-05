# app.py - TechFix - Semana 12
# Incluye: Flask, Jinja2, Flask-WTF, SQLite

import sqlite3
import os
from flask import Flask, render_template, redirect, url_for, flash
from forms.servicio_form import ServicioForm
from forms.cliente_form import ClienteForm
from forms.tecnico_form import TecnicoForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.secret_key = 'techfix_clave_secreta_2026'

# Ruta a la base de datos
DB_PATH = os.path.join('data', 'techfix.db')

# Funcion para conectar a la base de datos
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Crear las tablas si no existen
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            servicio TEXT NOT NULL,
            total REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar
init_db()

# Ruta principal
@app.route('/')
def index():
    nombre_empresa = 'TechFix'
    return render_template('index.html', nombre_empresa=nombre_empresa)

# Ruta servicios - lista
@app.route('/servicios')
def servicios():
    conn = get_db()
    lista = conn.execute('SELECT * FROM servicios').fetchall()
    conn.close()
    return render_template('servicios.html', servicios=lista)

# Ruta formulario servicios
@app.route('/servicios/nuevo', methods=['GET', 'POST'])
def nuevo_servicio():
    form = ServicioForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute(
            'INSERT INTO servicios (nombre, descripcion, categoria) VALUES (?, ?, ?)',
            (form.nombre.data, form.descripcion.data, form.categoria.data)
        )
        conn.commit()
        conn.close()
        flash('Servicio registrado correctamente.', 'success')
        return redirect(url_for('servicios'))
    return render_template('formulario_servicio.html', form=form)

# Ruta clientes - lista
@app.route('/clientes')
def clientes():
    conn = get_db()
    lista = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=lista)

# Ruta formulario clientes
@app.route('/clientes/nuevo', methods=['GET', 'POST'])
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
    return render_template('formulario_cliente.html', form=form)

# Ruta tecnicos - lista
@app.route('/tecnicos')
def tecnicos():
    conn = get_db()
    lista = conn.execute('SELECT * FROM tecnicos').fetchall()
    conn.close()
    return render_template('tecnicos.html', tecnicos=lista)

# Ruta formulario tecnicos
@app.route('/tecnicos/nuevo', methods=['GET', 'POST'])
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
    return render_template('formulario_tecnico.html', form=form)

# Ruta facturacion - lista
@app.route('/facturacion')
def facturacion():
    conn = get_db()
    lista = conn.execute('SELECT * FROM facturas').fetchall()
    conn.close()
    return render_template('facturacion.html', facturas=lista)

# Ruta formulario facturacion
@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_factura():
    form = FacturacionForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute(
            'INSERT INTO facturas (cliente, servicio, total) VALUES (?, ?, ?)',
            (form.cliente.data, form.servicio.data, float(form.total.data))
        )
        conn.commit()
        conn.close()
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
