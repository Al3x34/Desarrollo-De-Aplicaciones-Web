// script.js - TechFix - Semana 16
// - Modal de confirmacion antes de eliminar cualquier registro
// - Autocompleta el total de la factura con el precio del servicio elegido
// - Oculta los mensajes de exito despues de unos segundos

document.addEventListener("DOMContentLoaded", function () {

    // ---- Confirmacion al eliminar ----
    var modalElemento = document.getElementById("modalConfirmarEliminar");
    var formularioAEliminar = null;

    if (modalElemento) {
        var modalEliminar = new bootstrap.Modal(modalElemento);
        var nombreAEliminar = document.getElementById("nombreAEliminar");
        var btnConfirmar = document.getElementById("btnConfirmarEliminar");

        var formularios = document.querySelectorAll(".form-eliminar");
        for (var i = 0; i < formularios.length; i++) {
            formularios[i].addEventListener("submit", function (e) {
                // En lugar de eliminar directo, se abre el modal de confirmacion
                e.preventDefault();
                formularioAEliminar = this;
                nombreAEliminar.textContent = this.dataset.nombre || "este registro";
                modalEliminar.show();
            });
        }

        btnConfirmar.addEventListener("click", function () {
            if (formularioAEliminar) {
                btnConfirmar.disabled = true;
                formularioAEliminar.submit();
            }
        });
    }

    // ---- Total automatico en el formulario de facturas ----
    var selectServicio = document.getElementById("servicio_id");
    var inputTotal = document.getElementById("total");

    if (selectServicio && inputTotal && typeof preciosServicios !== "undefined") {
        selectServicio.addEventListener("change", function () {
            var precio = preciosServicios[selectServicio.value];
            if (precio !== undefined) {
                inputTotal.value = Number(precio).toFixed(2);
            }
        });
    }

    // ---- Ocultar mensajes de exito automaticamente ----
    var alertasExito = document.querySelectorAll(".alert-success");
    for (var j = 0; j < alertasExito.length; j++) {
        (function (alerta) {
            setTimeout(function () {
                bootstrap.Alert.getOrCreateInstance(alerta).close();
            }, 4000);
        })(alertasExito[j]);
    }

});
