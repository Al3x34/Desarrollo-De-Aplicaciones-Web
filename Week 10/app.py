# app.py - TechFix - Semana 10
# Se agregan datos de ejemplo en cada ruta y se envian a las plantillas

from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    nombre_empresa = "TechFix"
    return render_template("index.html", nombre_empresa=nombre_empresa)

# Ruta para servicios
@app.route("/servicios")
def servicios():
    lista_servicios = [
        {"nombre": "Mantenimiento", "descripcion": "Limpieza y mantenimiento preventivo de hardware.", "categoria": "Hardware", "disponible": True},
        {"nombre": "Formateo y Respaldo", "descripcion": "Formateo del sistema y respaldo de datos.", "categoria": "Sistema", "disponible": True},
        {"nombre": "Software", "descripcion": "Instalacion de programas y optimizacion del sistema.", "categoria": "Software", "disponible": False},
        {"nombre": "Redes", "descripcion": "Configuracion de redes y cableado estructurado.", "categoria": "Redes", "disponible": True}
    ]
    return render_template("servicios.html", servicios=lista_servicios)

# Ruta para clientes
@app.route("/clientes")
def clientes():
    lista_clientes = [
        {"id": 1, "nombre": "Juan Perez", "correo": "juan@correo.com", "telefono": "0991234567", "activo": True},
        {"id": 2, "nombre": "Maria Lopez", "correo": "maria@correo.com", "telefono": "0987654321", "activo": True},
        {"id": 3, "nombre": "Carlos Rios", "correo": "carlos@correo.com", "telefono": "0976543210", "activo": False},
        {"id": 4, "nombre": "Ana Torres", "correo": "ana@correo.com", "telefono": "0965432109", "activo": True}
    ]
    return render_template("clientes.html", clientes=lista_clientes)

# Ruta para tecnicos
@app.route("/tecnicos")
def tecnicos():
    lista_tecnicos = [
        {"nombre": "Carlos Mendoza", "especialidad": "Mantenimiento", "disponible": True},
        {"nombre": "Luis Torres", "especialidad": "Redes", "disponible": False},
        {"nombre": "Ana Suarez", "especialidad": "Software", "disponible": True},
        {"nombre": "Pedro Ramos", "especialidad": "Formateo y Respaldo", "disponible": False},
        {"nombre": "Maria Leon", "especialidad": "Mantenimiento", "disponible": True}
    ]
    return render_template("tecnicos.html", tecnicos=lista_tecnicos)

# Ruta para facturacion
@app.route("/facturacion")
def facturacion():
    lista_facturas = [
        {"id": "001", "cliente": "Juan Perez", "servicio": "Mantenimiento", "fecha": "2026-07-01", "total": 25.00, "pagado": True},
        {"id": "002", "cliente": "Maria Lopez", "servicio": "Formateo y Respaldo", "fecha": "2026-07-05", "total": 35.00, "pagado": True},
        {"id": "003", "cliente": "Carlos Rios", "servicio": "Redes", "fecha": "2026-07-10", "total": 40.00, "pagado": False},
        {"id": "004", "cliente": "Ana Torres", "servicio": "Software", "fecha": "2026-07-15", "total": 20.00, "pagado": True}
    ]
    return render_template("facturacion.html", facturas=lista_facturas)

if __name__ == "__main__":
    app.run(debug=True)
