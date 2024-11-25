document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let allValid = true;

    const nombreField = document.getElementById("nombre");
    const apellidoField = document.getElementById("apellido");
    const emailField = document.getElementById("email");
    const contraseñaField = document.getElementById("contraseña");
    const confirmarContraseñaField = document.getElementById("confirmarcontraseña");

    // Validación de campos requeridos
    [nombreField, apellidoField, emailField, contraseñaField, confirmarContraseñaField].forEach(field => {
        if (!field.value.trim()) {
            field.classList.add("is-invalid");
            field.nextElementSibling.textContent = "Este campo es obligatorio";
            allValid = false;
        } else {
            field.classList.remove("is-invalid");
            field.nextElementSibling.textContent = "";
        }
    });

    // Validación específica: nombre
    nombreField.addEventListener("input", () => {
        const nombrePattern = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/; // Solo letras y espacios
        const errorMessage = document.getElementById("nombreError"); // Contenedor para el error

        if (!nombrePattern.test(nombreField.value)) {
            errorMessage.textContent = "El nombre solo puede contener letras y espacios.";
            nombreField.classList.add("is-invalid");
        } else {
            errorMessage.textContent = "";
            nombreField.classList.remove("is-invalid");
        }
    });

    // Restringe la entrada del campo de nombre
    nombreField.addEventListener("keypress", (e) => {
        const validChars = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]$/; // Solo letras y espacios
        if (!validChars.test(e.key)) {
            e.preventDefault(); // Bloquea el carácter no permitido
        }
    });

    // Restringe la entrada del campo de apellido
    apellidoField.addEventListener("keypress", (e) => {
        const validChars = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]$/; // Solo letras y espacios
        if (!validChars.test(e.key)) {
            e.preventDefault(); // Bloquea el carácter no permitido
        }
    });

    // Validación específica: apellido
    apellidoField.addEventListener("input", () => {
        const apellidoPattern = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/; // Solo letras y espacios
        const errorMessage = document.getElementById("apellidoError"); // Contenedor para el error

        if (!apellidoPattern.test(apellidoField.value)) {
            errorMessage.textContent = "El apellido solo puede contener letras y espacios.";
            apellidoField.classList.add("is-invalid");
        } else {
            errorMessage.textContent = "";
            apellidoField.classList.remove("is-invalid");
        }
    });

    // Validación específica: correo electrónico
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(emailField.value)) {
        emailField.classList.add("is-invalid");
        document.getElementById("emailError").textContent = "Ingrese un correo válido (ejemplo@dominio.com).";
        allValid = false;
    }

    // Validación dinámica de contraseñas con mensajes dinámicos
    const contraseñaPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    const contraseñaError = document.getElementById("contraseñaError");

    let contraseñaErrorMessage = "";

    if (contraseñaField.value.length < 8) {
        contraseñaErrorMessage += "Debe tener al menos 8 caracteres. ";
    }
    if (!/[A-Z]/.test(contraseñaField.value)) {
        contraseñaErrorMessage += "Debe contener al menos una letra mayúscula. ";
    }
    if (!/[a-z]/.test(contraseñaField.value)) {
        contraseñaErrorMessage += "Debe contener al menos una letra minúscula. ";
    }
    if (!/\d/.test(contraseñaField.value)) {
        contraseñaErrorMessage += "Debe contener al menos un número. ";
    }
    if (!/[@$!%*?&]/.test(contraseñaField.value)) {
        contraseñaErrorMessage += "Debe contener al menos un símbolo especial (@$!%*?&). ";
    }

    if (contraseñaErrorMessage) {
        contraseñaField.classList.add("is-invalid");
        contraseñaError.textContent = contraseñaErrorMessage;
        allValid = false;
    } else {
        contraseñaField.classList.remove("is-invalid");
        contraseñaError.textContent = "";
    }

    // Validación de contraseñas coincidentes
    if (contraseñaField.value !== confirmarContraseñaField.value) {
        confirmarContraseñaField.classList.add("is-invalid");
        document.getElementById("confirmarContraseñaError").textContent = "Las contraseñas no coinciden.";
        allValid = false;
    }

    // Si todos los campos son válidos, puedes proceder
    if (allValid) {
        alert("¡Gracias por registrarse! Será redirigido al inicio.");
        window.location.href = "CreateAcc";  // Redirige a la página de éxito o al inicio
    } else {
        alert("Por favor, corrija los errores.");
    }
});
