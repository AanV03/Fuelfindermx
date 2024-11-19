document.addEventListener("DOMContentLoaded", function() {
    // Función para validar y mover el foco entre los campos
    function validateAndMoveFocus(input) {
        // Si el valor no es un número, borra el carácter
        if (!/^[0-9]$/.test(input.value)) {
            input.value = '';  // Limpiar el campo si no es un número
            return;
        }

        // Si el valor tiene la longitud máxima, mueve el foco al siguiente campo
        if (input.value.length === input.maxLength) {
            let nextInput = input.nextElementSibling;
            // Buscar el siguiente input de texto
            while (nextInput && nextInput.tagName !== "INPUT") {
                nextInput = nextInput.nextElementSibling;
            }
            if (nextInput) {
                nextInput.focus();  // Mover el foco al siguiente campo
            }
        }
    }

    // Asignar el evento de validación a cada input de código
    const tokenInputs = document.querySelectorAll('input[type="text"]');
    tokenInputs.forEach(input => {
        input.addEventListener("input", function () {
            validateAndMoveFocus(input);
        });
    });

    // Manejo del formulario cuando se envía
    document.getElementById("TokenForm").addEventListener("submit", function (e) {
        e.preventDefault(); // Prevenir que el formulario se envíe tradicionalmente

        // Obtener el código ingresado por el usuario
        let token = "";
        tokenInputs.forEach(input => {
            token += input.value;
        });

        // Verificar si el token tiene la longitud esperada (6 dígitos)
        if (token.length === 6) {
            console.log("Token ingresado: " + token);
            // Aquí puedes agregar la lógica de verificación del token (API, etc.)
            window.location.href = "NewContraseña.html"; // Redirigir a la siguiente página si el token es válido
        } else {
            alert("Por favor, ingrese un token válido.");
        }
    });
});