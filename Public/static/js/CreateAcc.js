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

    // Validación de contraseñas
    if (contraseñaField.value.trim().length < 6) {
        contraseñaField.classList.add("is-invalid");
        document.getElementById("contraseñaError").textContent = "La contraseña debe tener al menos 6 caracteres.";
        allValid = false;
    }

    if (contraseñaField.value !== confirmarContraseñaField.value) {
        confirmarContraseñaField.classList.add("is-invalid");
        document.getElementById("confirmarContraseñaError").textContent = "Las contraseñas no coinciden.";
        allValid = false;
    }

    if (allValid) {
        alert("¡Gracias por registrarse! Será redirigido al inicio.");
        window.location.href = "Inicio";
    } else {
        alert("Por favor, corrija los errores.");
    }
});
