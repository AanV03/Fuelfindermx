document.addEventListener("DOMContentLoaded", function () {
    // Manejador de validación y movimiento entre campos
    function validateAndMoveFocus(input) {
        if (!/^[0-9]$/.test(input.value)) {
            input.value = '';
            return;
        }
        if (input.value.length === input.maxLength) {
            let nextInput = input.nextElementSibling;
            while (nextInput && nextInput.tagName !== "INPUT") {
                nextInput = nextInput.nextElementSibling;
            }
            if (nextInput) {
                nextInput.focus();
            }
        }
    }

    // Manejador de cambio de foco con flechas
    function handleKeyDown(event, input) {
        if (event.key === "ArrowRight") {
            let nextInput = input.nextElementSibling;
            while (nextInput && nextInput.tagName !== "INPUT") {
                nextInput = nextInput.nextElementSibling;
            }
            if (nextInput) {
                nextInput.focus();
                setTimeout(() => {
                    nextInput.select();
                }, 0);
            }
        } else if (event.key === "ArrowLeft") {
            let previousInput = input.previousElementSibling;
            while (previousInput && previousInput.tagName !== "INPUT") {
                previousInput = previousInput.previousElementSibling;
            }
            if (previousInput) {
                previousInput.focus();
                setTimeout(() => {
                    previousInput.select();
                }, 0);
            }
        }
    }

    // Asignar eventos a cada input
    const tokenInputs = document.querySelectorAll('input[type="text"]');
    tokenInputs.forEach(input => {
        input.addEventListener("input", function () {
            validateAndMoveFocus(input);
        });
        input.addEventListener("keydown", function (event) {
            handleKeyDown(event, input);
        });
        input.addEventListener("focus", function () {
            setTimeout(() => {
                input.select();
            }, 0);
        });
    });

    // Manejo del formulario cuando se envía
    document.getElementById("TokenForm").addEventListener("submit", function (e) {
        e.preventDefault();
        let token = "";
        tokenInputs.forEach(input => {
            token += input.value;
        });
        if (token.length === 6) {
            console.log("Token ingresado: " + token);
            window.location.href = "NewContraseña.html";
        } else {
            alert("Por favor, ingrese un token válido.");
        }
    });
});
