const form = document.getElementById("EmailForm");
const emailField = document.getElementById("email");
const confirmEmailField = document.getElementById("confirmEmail");
const emailError = document.getElementById("emailError");
const confirmEmailError = document.getElementById("confirmEmailError");

// Validación personalizada al enviar el formulario
form.addEventListener("submit", function (e) {
    e.preventDefault(); // Prevenir el envío tradicional del formulario

    // Validar ambos correos y su coincidencia
    const isEmailValid = validateEmail(emailField, emailError);
    const isConfirmEmailValid = validateEmail(confirmEmailField, confirmEmailError);
    const isEmailsMatching = compareEmails();

    // Si todo es válido, continuar con el flujo
    if (isEmailValid && isConfirmEmailValid && isEmailsMatching) {
        alert("¡Formulario enviado correctamente!");
        form.submit(); // Envía el formulario al servidor
    } else {
        alert("Por favor, verifica los errores en el formulario.");
    }
});

// Validación en tiempo real para los campos de correo
emailField.addEventListener("input", () => {
    validateEmail(emailField, emailError);
    compareEmails(); // Revalida la coincidencia
});

confirmEmailField.addEventListener("input", () => {
    validateEmail(confirmEmailField, confirmEmailError);
    compareEmails(); // Revalida la coincidencia
});

// Función para validar formato del correo electrónico
function validateEmail(field, errorField) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!field.value.trim()) {
        errorField.textContent = "Este campo es obligatorio.";
        field.classList.add("is-invalid");
        return false;
    } else if (!emailPattern.test(field.value)) {
        errorField.textContent = "Ingrese un correo válido (ejemplo@dominio.com).";
        field.classList.add("is-invalid");
        return false;
    } else {
        errorField.textContent = "";
        field.classList.remove("is-invalid");
        return true;
    }
}

// Función para comparar correos electrónicos
function compareEmails() {
    if (emailField.value.trim() === confirmEmailField.value.trim()) {
        confirmEmailError.textContent = "";
        confirmEmailField.classList.remove("is-invalid");
        return true;
    } else {
        confirmEmailError.textContent = "Los correos electrónicos no coinciden.";
        confirmEmailField.classList.add("is-invalid");
        return false;
    }
}
