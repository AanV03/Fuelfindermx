// script.js

/* Script de Reporte */
// Mostrar un mensaje de agradecimiento y redirigir al inicio
document.getElementById("reportForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevenir que el formulario se envíe tradicionalmente

    // Verificar si hay algún campo vacío obligatorio
    let allValid = true;
    const requiredFields = form.querySelectorAll("[required]");
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            allValid = false;
        }
    });

    if (!allValid) {
        // Si algún campo obligatorio está vacío, mostramos el mensaje de completar campos
        alert("Por favor, complete todos los campos obligatorios.");
        return; // Salimos de la función para no verificar los errores después de este mensaje
    }

    // Verificar si hay errores de validación en los campos (con la clase is-invalid)
    if (document.querySelectorAll(".is-invalid").length > 0) {
        // Si hay errores de validación, mostramos el mensaje de verificación
        alert("Por favor, verifique los errores en los campos.");
        return; // Salimos de la función para no mostrar el mensaje de agradecimiento
    }

    // Si no hay campos vacíos y no hay errores de validación, mostramos el mensaje de éxito
    alert("¡Gracias por reportar el error! Nuestro equipo lo revisará pronto.");
    window.location.href = "Inicio.html"; // Redirigir al inicio
});

// Validaciones dinámicas del formulario
const form = document.getElementById("reportForm");
const nombreField = document.getElementById("nombre");
const apellidoField = document.getElementById("apellido");
const emailField = document.getElementById("email");
const telefonoField = document.getElementById("telefono");
const errorField = document.getElementById("error");

// Validación de nombre y apellido (solo letras y espacios)
document.getElementById("nombre").addEventListener("input", () => {
    const nombrePattern = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/;
    const errorMessage = document.getElementById("nombreError");

    if (!nombrePattern.test(nombreField.value)) {
        errorMessage.textContent = "El nombre solo puede contener letras y espacios.";
        nombreField.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        nombreField.classList.remove("is-invalid");
    }
});

document.getElementById("apellido").addEventListener("input", () => {
    const apellidoPattern = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/;
    const errorMessage = document.getElementById("apellidoError");

    if (!apellidoPattern.test(apellidoField.value)) {
        errorMessage.textContent = "El apellido solo puede contener letras y espacios.";
        apellidoField.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        apellidoField.classList.remove("is-invalid");
    }
});

// Validación del correo electrónico
emailField.addEventListener("input", () => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const errorMessage = document.getElementById("emailError");

    if (!emailPattern.test(emailField.value)) {
        errorMessage.textContent = "Ingrese un correo válido (ejemplo@dominio.com).";
        emailField.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        emailField.classList.remove("is-invalid");
    }
});

// Validación del teléfono
telefonoField.addEventListener("input", () => {
    const telefonoPattern = /^[0-9]{10}$/;
    const errorMessage = document.getElementById("telefonoError");

    if (!telefonoPattern.test(telefonoField.value)) {
        errorMessage.textContent = "El teléfono debe tener 10 dígitos.";
        telefonoField.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        telefonoField.classList.remove("is-invalid");
    }
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
