// script.js - TechFix - Semana 8
// Se agrega: modal de detalles del tecnico, modal de confirmacion al eliminar
// y spinner simulando carga al registrar una solicitud.
// Se conservan las validaciones (Semana 6) y el renderizado dinamico (Semana 7).

var contador = 0;

// Arreglo de objetos que representa los tecnicos del negocio
var tecnicos = [
    { nombre: "Carlos Mendoza", especialidad: "Mantenimiento", disponible: true },
    { nombre: "Luis Torres", especialidad: "Redes", disponible: false },
    { nombre: "Ana Suarez", especialidad: "Software", disponible: true },
    { nombre: "Pedro Ramos", especialidad: "Formateo y Respaldo", disponible: false },
    { nombre: "Maria Leon", especialidad: "Mantenimiento", disponible: true }
];

// Funcion para mostrar los tecnicos en la pagina
function mostrarTecnicos() {
    var contenedor = document.getElementById("listaTecnicos");

    if (tecnicos.length === 0) {
        contenedor.innerHTML = "<p class='text-muted'>No hay tecnicos registrados.</p>";
        return;
    }

    for (var i = 0; i < tecnicos.length; i++) {
        var tec = tecnicos[i];

        var col = document.createElement("div");
        col.className = "col-md-4";

        var card = document.createElement("div");
        card.className = "card shadow-sm h-100";

        var body = document.createElement("div");
        body.className = "card-body";

        var nombre = document.createElement("h5");
        nombre.className = "card-title";
        nombre.textContent = tec.nombre;

        var especialidad = document.createElement("p");
        especialidad.className = "card-text text-muted";
        especialidad.textContent = "Especialidad: " + tec.especialidad;

        var estado = document.createElement("span");
        if (tec.disponible) {
            estado.className = "badge bg-success";
            estado.textContent = "Disponible";
        } else {
            estado.className = "badge bg-danger";
            estado.textContent = "No disponible";
        }

        var botonDetalles = document.createElement("button");
        botonDetalles.className = "btn btn-sm btn-primary d-block mt-3";
        botonDetalles.textContent = "Ver detalles";
        botonDetalles.addEventListener("click", function (tecnico) {
            return function () {
                mostrarModalTecnico(tecnico);
            };
        }(tec));

        body.appendChild(nombre);
        body.appendChild(especialidad);
        body.appendChild(estado);
        body.appendChild(botonDetalles);
        card.appendChild(body);
        col.appendChild(card);
        contenedor.appendChild(col);
    }
}

// Muestra el modal Bootstrap con la informacion del tecnico seleccionado
function mostrarModalTecnico(tecnico) {
    document.getElementById("modalTecnicoNombre").textContent = tecnico.nombre;
    document.getElementById("modalTecnicoEspecialidad").textContent = tecnico.especialidad;
    document.getElementById("modalTecnicoEstado").textContent = tecnico.disponible ? "Disponible" : "No disponible";

    var modal = new bootstrap.Modal(document.getElementById("modalTecnico"));
    modal.show();
}

document.addEventListener("DOMContentLoaded", function () {

    mostrarTecnicos();

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

    var btnRegistrar = document.getElementById("btnRegistrar");
    var spinnerCarga = document.getElementById("spinnerCarga");
    var textoBoton = document.getElementById("textoBoton");

    // Referencias para el modal de confirmacion de eliminacion
    var modalEliminar = new bootstrap.Modal(document.getElementById("modalConfirmarEliminar"));
    var btnConfirmarEliminar = document.getElementById("btnConfirmarEliminar");
    var tarjetaAEliminar = null;

    function marcarInvalido(campo, elementoError, texto) {
        campo.classList.remove("is-valid");
        campo.classList.add("is-invalid");
        elementoError.textContent = texto;
    }

    function marcarValido(campo, elementoError) {
        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");
        elementoError.textContent = "";
    }

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

    function validarCategoria() {
        var valor = selectCategoria.value;
        if (valor === "") {
            marcarInvalido(selectCategoria, errorCategoria, "Selecciona una categoria.");
            return false;
        }
        marcarValido(selectCategoria, errorCategoria);
        return true;
    }

    inputNombre.addEventListener("input", validarNombre);
    inputNombre.addEventListener("blur", validarNombre);

    inputDescripcion.addEventListener("input", validarDescripcion);
    inputDescripcion.addEventListener("blur", validarDescripcion);

    selectCategoria.addEventListener("change", validarCategoria);
    selectCategoria.addEventListener("blur", validarCategoria);

    // Crea la tarjeta de una solicitud registrada
    function crearTarjetaSolicitud(nombre, descripcion, categoria) {
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

        // En lugar de eliminar directo, se abre el modal de confirmacion
        botonEliminar.addEventListener("click", function () {
            tarjetaAEliminar = div;
            modalEliminar.show();
        });

        cardBody.appendChild(titulo);
        cardBody.appendChild(texto);
        cardBody.appendChild(badge);
        cardBody.appendChild(botonEliminar);
        div.appendChild(cardBody);

        return div;
    }

    // Boton "Eliminar" dentro del modal de confirmacion
    btnConfirmarEliminar.addEventListener("click", function () {
        if (tarjetaAEliminar) {
            tarjetaAEliminar.remove();
            contador--;
            totalTexto.textContent = "Total de solicitudes: " + contador;
            tarjetaAEliminar = null;
        }
        modalEliminar.hide();
    });

    formulario.addEventListener("submit", function (e) {
        e.preventDefault();

        var nombreValido = validarNombre();
        var descripcionValida = validarDescripcion();
        var categoriaValida = validarCategoria();

        if (!nombreValido || !descripcionValida || !categoriaValida) {
            mensajeExito.style.display = "none";
            mensajeError.textContent = "Por favor corrige los campos marcados antes de continuar.";
            mensajeError.style.display = "block";
            return;
        }

        mensajeError.style.display = "none";

        var nombre = inputNombre.value.trim();
        var descripcion = inputDescripcion.value.trim();
        var categoria = selectCategoria.value;

        // Simulacion de carga: se muestra el spinner y se bloquea el boton
        spinnerCarga.classList.remove("d-none");
        textoBoton.textContent = "Registrando...";
        btnRegistrar.disabled = true;

        setTimeout(function () {
            contador++;

            var tarjeta = crearTarjetaSolicitud(nombre, descripcion, categoria);
            document.getElementById("listaSolicitudes").appendChild(tarjeta);

            totalTexto.textContent = "Total de solicitudes: " + contador;

            mensajeExito.textContent = "Solicitud registrada correctamente.";
            mensajeExito.style.display = "block";

            formulario.reset();
            inputNombre.classList.remove("is-valid", "is-invalid");
            inputDescripcion.classList.remove("is-valid", "is-invalid");
            selectCategoria.classList.remove("is-valid", "is-invalid");

            // Se oculta el spinner y se restaura el boton
            spinnerCarga.classList.add("d-none");
            textoBoton.textContent = "Registrar solicitud";
            btnRegistrar.disabled = false;

            setTimeout(function () {
                mensajeExito.style.display = "none";
            }, 3000);
        }, 900);
    });

});
