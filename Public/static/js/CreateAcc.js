document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Evita el envío predeterminado del formulario
    let allValid = true;

    const nombreField = document.getElementById("nombre");
    const apellidoField = document.getElementById("apellido");
    const emailField = document.getElementById("email");
    const contraseñaField = document.getElementById("contraseña");
    const confirmarContraseñaField = document.getElementById("confirmarcontraseña");

    // Validación básica de campos requeridos
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

    // Validación de correo electrónico
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(emailField.value)) {
        emailField.classList.add("is-invalid");
        document.getElementById("emailError").textContent = "Ingrese un correo válido.";
        allValid = false;
    } else {
        emailField.classList.remove("is-invalid");
        document.getElementById("emailError").textContent = "";
    }

    // Validación de contraseñas
    if (contraseñaField.value !== confirmarContraseñaField.value) {
        confirmarContraseñaField.classList.add("is-invalid");
        document.getElementById("confirmarContraseñaError").textContent = "Las contraseñas no coinciden.";
        allValid = false;
    } else {
        confirmarContraseñaField.classList.remove("is-invalid");
        document.getElementById("confirmarContraseñaError").textContent = "";
    }

    // Si todo es válido, enviar datos al servidor
    if (allValid) {
        const formData = new FormData(document.getElementById("registerForm")); // Captura datos del formulario

        fetch("/CreateAcc", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert("¡Cuenta creada exitosamente!");
                window.location.href = "/success"; // Redirige a la página de éxito
            } else {
                alert("Hubo un error al crear la cuenta.");
            }
        })
        .catch(error => {
            console.error("Error en la solicitud:", error);
            alert("Hubo un error inesperado.");
        });
    } else {
        alert("Por favor, corrija los errores.");
    }
});