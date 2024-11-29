document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");

    // Validaciones en tiempo real
    document.getElementById("nombre").addEventListener("input", () => {
        validarCampo("nombre", /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/, "El nombre solo puede contener letras y espacios.");
    });

    document.getElementById("apellido").addEventListener("input", () => {
        validarCampo("apellido", /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/, "El apellido solo puede contener letras y espacios.");
    });

    registerForm.addEventListener("submit", function (e) {
        e.preventDefault(); // Evita el envío del formulario por defecto

        let allValid = true;

        // Validaciones generales
        const fields = ["nombre", "apellido", "email", "contraseña", "confirmarcontraseña"];
        fields.forEach(id => {
            const field = document.getElementById(id);
            if (!field.value.trim()) {
                field.classList.add("is-invalid");
                field.nextElementSibling.textContent = "Este campo es obligatorio.";
                allValid = false;
            } else {
                field.classList.remove("is-invalid");
                field.nextElementSibling.textContent = "";
            }
        });

        // Validación de correo
        const emailField = document.getElementById("email");
        if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(emailField.value)) {
            emailField.classList.add("is-invalid");
            document.getElementById("emailError").textContent = "Ingrese un correo válido.";
            allValid = false;
        }

        // Validación de contraseñas
        const contraseñaField = document.getElementById("contraseña");
        const confirmarContraseñaField = document.getElementById("confirmarcontraseña");
        if (contraseñaField.value !== confirmarContraseñaField.value) {
            confirmarContraseñaField.classList.add("is-invalid");
            document.getElementById("confirmarContraseñaError").textContent = "Las contraseñas no coinciden.";
            allValid = false;
        }

        // Si todo es válido, enviar el formulario
        if (allValid) {
            const formData = new FormData(registerForm);

            fetch("/CreateAcc", {
                method: "POST",
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        alert("¡Cuenta creada exitosamente!");
                        window.location.href = "/success";
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
});

function validarCampo(id, pattern, errorMsg) {
    const field = document.getElementById(id);
    const error = document.getElementById(id + "Error");

    if (!pattern.test(field.value)) {
        error.textContent = errorMsg;
        field.classList.add("is-invalid");
    } else {
        error.textContent = "";
        field.classList.remove("is-invalid");
    }
}
