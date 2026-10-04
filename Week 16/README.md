# TechFix - Proyecto Final (Semana 16)

Sistema web para gestionar un negocio de soporte técnico: servicios, clientes, técnicos y facturas.
Desarrollado con **Flask**, **Jinja2**, **Flask-WTF**, **Flask-Login** y **SQLite**.

**Autor:** Steven Castro - Desarrollo de Aplicaciones Web - 2026

## Video de demostración

[Ver el video del funcionamiento del sistema](https://ueaeduec-my.sharepoint.com/:v:/g/personal/sa_castrov_uea_edu_ec/IQApUzayf7rBQpOmv0vrH_WHAZhhek0cJFNjahDFd9FIqo4?e=f8PTfn&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

El video muestra la navegación del sistema, el login, el CRUD de las tablas relacionadas y una explicación general del funcionamiento.

## Funcionalidades

- **Login y autenticación**: registro de usuarios, inicio y cierre de sesión con Flask-Login.
  Las contraseñas se guardan cifradas con Werkzeug (`generate_password_hash`).
  Todas las secciones de gestión exigen haber iniciado sesión.
- **CRUD completo** (crear, leer, actualizar y eliminar) en 4 tablas: servicios, clientes, técnicos y facturas.
- **Tablas relacionadas**: cada factura se vincula a un cliente, un servicio y un técnico mediante claves foráneas.
  El sistema no permite eliminar un cliente, servicio o técnico que tenga facturas asociadas.
- **Panel de gestión** con totales, ingresos y últimas facturas (consultas con `JOIN`).
- Validaciones en todos los formularios, protección CSRF, modal de confirmación antes de eliminar
  y total de la factura autocompletado con el precio del servicio.

## Modelo de datos

```
usuarios (id, nombre, usuario, password_hash)

clientes  (id, nombre, correo, telefono)  ──┐
servicios (id, nombre, descripcion,         ├──<  facturas (id, cliente_id, servicio_id,
           categoria, precio)             ──┤                tecnico_id, fecha, total)
tecnicos  (id, nombre, especialidad)      ──┘
```

## Cómo ejecutarlo

```bash
cd "Week 16"
pip install -r requirements.txt
python app.py
```

Abrir <http://127.0.0.1:5000> en el navegador.

La base de datos `data/techfix.db` se crea automáticamente la primera vez, con datos de ejemplo.
Para empezar de cero, basta con borrar ese archivo y volver a ejecutar `app.py`.

**Usuario de prueba:** `admin` / `admin123` (también se pueden crear cuentas nuevas desde "Registrarse").

## Estructura

```
Week 16/
├── app.py                 # Rutas, login, CRUD y base de datos
├── requirements.txt
├── forms/                 # Formularios Flask-WTF (login, registro y uno por tabla)
├── templates/
│   ├── base.html
│   ├── auth/              # login.html, registro.html
│   ├── components/        # navbar, footer, mensajes, macros, modal de eliminar
│   ├── panel.html
│   ├── servicios.html, clientes.html, tecnicos.html, facturacion.html
│   └── formulario_*.html  # Formularios de crear/editar
├── static/                # css, js, img
└── data/                  # techfix.db (se genera al ejecutar)
```
