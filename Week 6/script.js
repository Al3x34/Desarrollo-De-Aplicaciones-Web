// script.js - TechFix - Semana 6
// Funcionalidad: registrar solicitudes de servicio con validaciones dinamicas
// Se mantiene la logica de crear, mostrar, contar y eliminar de la Semana 5

var contador = 0;

document.addEventListener("DOMContentLoaded", function () {

    var formulario = document.getElementById("formSolicitud");
    var totalTexto = document.getElementById("totalRegistros");

    var inputNombre = document.getElementById("nombreCliente");
    var inputDescripcion = document.getElementById("descripcionServicio");
    var selectCategoria = document.getElementById("categoriaServicio");

    var errorNombre = document.getElementById("errorNombre");
    var errorDescripcion = document.getElementById("errorDescripcion");
    var errorCategoria = document.getElementById("errorCategoria");

    var mensajeError = document.getElementById("mensajeError");
    var mensajeExito = document.getElementById("mensajeExito");

    // Marca un campo como invalido y muestra el texto de error
    function marcarInvalido(campo, elementoError, texto) {
        campo.classList.remove("is-valid");
        campo.classList.add("is-invalid");
        elementoError.textContent = texto;
    }

    // Marca un campo como valido y limpia el texto de error
    function marcarValido(campo, elementoError) {
        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");
        elementoError.textContent = "";
    }

    // Validar el campo nombre del cliente
    function validarNombre() {
        var valor = inputNombre.value.trim();

        if (valor === "") {
            marcarInvalido(inputNombre, errorNombre, "El nombre es obligatorio.");
            return false;
        }

        if (valor.length < 3) {
            marcarInvalido(inputNombre, errorNombre, "El nombre debe tener al menos 3 caracteres.");
            return false;
        }

        marcarValido(inputNombre, errorNombre);
        return true;
    }

    // Validar el campo descripcion del problema
    function validarDescripcion() {
        var valor = inputDescripcion.value.trim();

        if (valor === "") {
            marcarInvalido(inputDescripcion, errorDescripcion, "La descripcion es obligatoria.");
            return false;
        }

        if (valor.length < 10) {
            marcarInvalido(inputDescripcion, errorDescripcion, "Describe el problema con mas detalle (minimo 10 caracteres).");
            return false;
        }

        marcarValido(inputDescripcion, errorDescripcion);
        return true;
    }

    // Validar que se haya seleccionado una categoria
    function validarCategoria() {
        var valor = selectCategoria.value;

        if (valor === "") {
            marcarInvalido(selectCategoria, errorCategoria, "Selecciona una categoria.");
            return false;
        }

        marcarValido(selectCategoria, errorCategoria);
        return true;
    }

    // Validaciones en tiempo real mientras el usuario escribe o sale del campo
    inputNombre.addEventListener("input", validarNombre);
    inputNombre.addEventListener("blur", validarNombre);

    inputDescripcion.addEventListener("input", validarDescripcion);
    inputDescripcion.addEventListener("blur", validarDescripcion);

    selectCategoria.addEventListener("change", validarCategoria);
    selectCategoria.addEventListener("blur", validarCategoria);

    // Envio del formulario
    formulario.addEventListener("submit", function (e) {
        e.preventDefault(); // evitar que la pagina se recargue

        var nombreValido = validarNombre();
        var descripcionValida = validarDescripcion();
        var categoriaValida = validarCategoria();

        // Si algun campo no es valido, mostrar mensaje general y no registrar
        if (!nombreValido || !descripcionValida || !categoriaValida) {
            mensajeExito.style.display = "none";
            mensajeError.textContent = "Por favor corrige los campos marcados antes de continuar.";
            mensajeError.style.display = "block";
            return;
        }

        // Ocultar mensaje de error si estaba visible
        mensajeError.style.display = "none";

        var nombre = inputNombre.value.trim();
        var descripcion = inputDescripcion.value.trim();
        var categoria = selectCategoria.value;

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

        // Mostrar mensaje de exito
        mensajeExito.textContent = "Solicitud registrada correctamente.";
        mensajeExito.style.display = "block";

        // Limpiar el formulario y las clases de validacion
        formulario.reset();
        inputNombre.classList.remove("is-valid", "is-invalid");
        inputDescripcion.classList.remove("is-valid", "is-invalid");
        selectCategoria.classList.remove("is-valid", "is-invalid");

        // Ocultar el mensaje de exito despues de unos segundos
        setTimeout(function () {
            mensajeExito.style.display = "none";
        }, 3000);
    });

});
