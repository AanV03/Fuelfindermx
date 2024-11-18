/* Script de Reporte */

// Seleccionar los elementos del formulario y campos
const form = document.getElementById("reportForm");
const nombreField = document.getElementById("nombre");
const apellidoField = document.getElementById("apellido");
const emailField = document.getElementById("email");
const telefonoField = document.getElementById("telefono");
const errorField = document.getElementById("error");

// Función para manejar la validación y mostrar el mensaje de error
function validarCampo(field, pattern, errorMessage, errorElement) {
    if (!pattern.test(field.value)) {
        errorElement.textContent = errorMessage;
        field.classList.add("is-invalid");
    } else {
        errorElement.textContent = "";
        field.classList.remove("is-invalid");
    }
}

// Validaciones dinámicas del formulario

// Validación de nombre y apellido (solo letras y espacios)
nombreField.addEventListener("input", () => {
    const nombrePattern = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/;
    const nombreError = document.getElementById("nombreError");
    validarCampo(nombreField, nombrePattern, "El nombre solo puede contener letras y espacios.", nombreError);
});

apellidoField.addEventListener("input", () => {
    const apellidoPattern = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/;
    const apellidoError = document.getElementById("apellidoError");
    validarCampo(apellidoField, apellidoPattern, "El apellido solo puede contener letras y espacios.", apellidoError);
});

// Validación del correo electrónico
emailField.addEventListener("input", () => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const emailError = document.getElementById("emailError");
    validarCampo(emailField, emailPattern, "Ingrese un correo válido (ejemplo@dominio.com).", emailError);
});

// Validación del teléfono
telefonoField.addEventListener("input", () => {
    const telefonoPattern = /^[0-9]{10}$/;
    const telefonoError = document.getElementById("telefonoError");
    validarCampo(telefonoField, telefonoPattern, "El teléfono debe tener 10 dígitos.", telefonoError);
});

// Validación de la descripción del error
errorField.addEventListener("input", () => {
    const errorMessage = document.getElementById("errorError");

    if (errorField.value.trim() === "") {
        errorMessage.textContent = "La descripción del error es obligatoria.";
        errorField.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        errorField.classList.remove("is-invalid");
    }
});

// Validación al enviar el formulario
form.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevenir que el formulario se envíe tradicionalmente

    // Verificar si hay errores
    if (document.querySelectorAll(".is-invalid").length > 0) {
        alert("Corrige los errores antes de enviar.");
        return; // Si hay errores, no continuar con el envío
    }

    // Si no hay errores, se muestra el mensaje de éxito y redirige
    alert("¡Gracias por reportar el error! Nuestro equipo lo revisará pronto.");
    window.location.href = "Inicio.html"; // Redirige a la página de inicio
});
