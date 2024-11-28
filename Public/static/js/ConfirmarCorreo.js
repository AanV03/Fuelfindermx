const form = document.getElementById("EmailForm");
const emailField = document.getElementById("email");
const confirmEmailField = document.getElementById("confirmEmail");
const emailError = document.getElementById("emailError");
const confirmEmailError = document.getElementById("confirmEmailError");

// Validación personalizada al enviar el formulario
form.addEventListener("submit", function (e) {
    e.preventDefault(); // Prevenir envío tradicional

    let allValid = true;

    // Validar formato del correo principal
    validateEmail(emailField, "emailError");
    if (emailField.classList.contains("is-invalid")) {
        allValid = false;
    }

    // Validar formato del correo de confirmación
    validateEmail(confirmEmailField, "confirmEmailError");
    if (confirmEmailField.classList.contains("is-invalid")) {
        allValid = false;
    }

    // Verificar que los correos coincidan
    compareEmails();
    if (confirmEmailField.classList.contains("is-invalid")) {
        allValid = false;
    }

    if (!allValid) {
        alert("Por favor, verifique los errores en los campos.");
        return;
    }

    // Si todo es correcto, continuar
    alert("¡Se registró correctamente!");
    window.location.href = "NuevaContraseña";
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

    if (!field.value.trim()) {
        errorMessage.textContent = "Este campo es obligatorio.";
        field.classList.add("is-invalid");
    } else if (!emailPattern.test(field.value)) {
        errorMessage.textContent = "Ingrese un correo válido (ejemplo@dominio.com).";
        field.classList.add("is-invalid");
    } else {
        errorMessage.textContent = "";
        field.classList.remove("is-invalid");
    }
}

// Función para comparar los correos
function compareEmails() {
    if (emailField.value.trim() === confirmEmailField.value.trim()) {
        confirmEmailError.textContent = "";
        confirmEmailField.classList.remove("is-invalid");
    } else {
        confirmEmailError.textContent = "Los correos electrónicos no coinciden.";
        confirmEmailField.classList.add("is-invalid");
    }
}
