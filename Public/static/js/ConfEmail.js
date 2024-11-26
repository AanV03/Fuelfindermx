const form = document.getElementById("EmailForm");
const emailField = document.getElementById("email");
const confirmEmailField = document.getElementById("confirmEmail");
const emailError = document.getElementById("emailError");
const confirmEmailError = document.getElementById("confirmEmailError");

// Validación personalizada al enviar el formulario
form.addEventListener("submit", function (e) {
    e.preventDefault(); // Prevenir envío tradicional

    // Verificar campos obligatorios
    let allValid = true;
    const requiredFields = form.querySelectorAll("[required]");
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            allValid = false;
        }
    });

    if (!allValid) {
        alert("Por favor, complete todos los campos obligatorios.");
        return;
    }

    // Verificar si hay errores de validación en los campos
    if (document.querySelectorAll(".is-invalid").length > 0) {
        alert("Por favor, verifique los errores en los campos.");
        return;
    }

    // Verificar que los correos coincidan
    if (emailField.value !== confirmEmailField.value) {
        confirmEmailError.textContent = "Los correos electrónicos no coinciden.";
        confirmEmailField.classList.add("is-invalid");
        return;
    }

    // Si todo es correcto, continuar
    alert("¡Se registró correctamente!");
    window.location.href = "NewContraseña";
});

// Validación de formato del correo electrónico
emailField.addEventListener("input", () => {
    validateEmail(emailField, "emailError");
    compareEmails(); // Verificar coincidencia en tiempo real
});

confirmEmailField.addEventListener("input", () => {
    validateEmail(confirmEmailField, "confirmEmailError");
    compareEmails(); // Verificar coincidencia en tiempo real
});

// Función para validar correos
function validateEmail(field, errorId) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const errorMessage = document.getElementById(errorId);

    if (!emailPattern.test(field.value)) {
        errorMessage.textContent = "Ingrese un correo válido (ejemplo@dominio.com).";
        field.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        field.classList.remove("is-invalid");
    }
}

// Función para comparar los correos
function compareEmails() {
    if (emailField.value === confirmEmailField.value) {
        confirmEmailError.textContent = "";
        confirmEmailField.classList.remove("is-invalid");
    } else {
        confirmEmailError.textContent = "Los correos electrónicos no coinciden.";
        confirmEmailField.classList.add("is-invalid");
    }
}
