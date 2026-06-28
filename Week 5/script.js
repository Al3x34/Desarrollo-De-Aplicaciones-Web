// script.js - TechFix - Semana 5
// Funcionalidad: registrar solicitudes de servicio dinámicamente

var contador = 0;

// Esperar a que el documento esté listo
document.addEventListener("DOMContentLoaded", function () {

    var formulario = document.getElementById("formSolicitud");
    var totalTexto = document.getElementById("totalRegistros");

    formulario.addEventListener("submit", function (e) {
        e.preventDefault(); // evitar que la página se recargue

        var nombre = document.getElementById("nombreCliente").value;
        var descripcion = document.getElementById("descripcionServicio").value;
        var categoria = document.getElementById("categoriaServicio").value;

        // Validar que los campos no estén vacíos
        if (nombre === "" || descripcion === "" || categoria === "") {
            document.getElementById("mensajeError").textContent = "Por favor completa todos los campos.";
            document.getElementById("mensajeError").style.display = "block";
            return;
        }

        // Ocultar mensaje de error si estaba visible
        document.getElementById("mensajeError").style.display = "none";

        // Incrementar el contador
        contador++;

        // Crear el elemento de la tarjeta
        var div = document.createElement("div");
        div.className = "card mb-3 shadow-sm";

        var cardBody = document.createElement("div");
        cardBody.className = "card-body";

        var titulo = document.createElement("h5");
        titulo.className = "card-title";
        titulo.textContent = nombre;

        var texto = document.createElement("p");
        texto.className = "card-text";
        texto.textContent = descripcion;

        var badge = document.createElement("span");
        badge.className = "badge bg-secondary me-2";
        badge.textContent = categoria;

        var botonEliminar = document.createElement("button");
        botonEliminar.className = "btn btn-sm btn-danger";
        botonEliminar.textContent = "Eliminar";

        // Evento para eliminar el registro
        botonEliminar.addEventListener("click", function () {
            div.remove();
            contador--;
            totalTexto.textContent = "Total de solicitudes: " + contador;
        });

        // Agregar los elementos al card
        cardBody.appendChild(titulo);
        cardBody.appendChild(texto);
        cardBody.appendChild(badge);
        cardBody.appendChild(botonEliminar);
        div.appendChild(cardBody);

        // Agregar el card a la lista
        document.getElementById("listaSolicitudes").appendChild(div);

        // Actualizar el contador en pantalla
        totalTexto.textContent = "Total de solicitudes: " + contador;

        // Limpiar el formulario
        formulario.reset();
    });

});
