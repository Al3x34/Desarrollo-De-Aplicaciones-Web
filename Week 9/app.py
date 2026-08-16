# app.py - TechFix - Semana 9
# Aplicacion web con Flask y manejo de rutas

from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para servicios
@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

# Ruta para clientes
@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

# Ruta para tecnicos (proveedores en la estructura)
@app.route("/tecnicos")
def tecnicos():
    return render_template("tecnicos.html")

# Ruta para facturacion
@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html")

if __name__ == "__main__":
    app.run(debug=True)
