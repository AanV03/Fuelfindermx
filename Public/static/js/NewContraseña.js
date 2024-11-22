
// Función para cambiar el tipo de contraseña y el icono de visibilidad
function togglePasswordVisibility(inputId, iconId) {
    const passwordField = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    // Cambiar entre "password" y "text" para mostrar u ocultar la contraseña
    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    } else {
        passwordField.type = "password";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    }
}

// Validación de formulario
document.getElementById("PassForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevenir que el formulario se envíe tradicionalmente

    // Obtener los valores de las contraseñas
    const contraseña = document.getElementById("contraseña").value;
    const confirmarContraseña = document.getElementById("confirmarContraseña").value;

    // Validar si los campos están vacíos
    if (!contraseña || !confirmarContraseña) {
        alert("Por favor, complete todos los campos obligatorios.");
        return;
    }

    // Verificar que las contraseñas coincidan
    if (contraseña !== confirmarContraseña) {
        alert("Las contraseñas no coinciden. Por favor, inténtelo nuevamente.");
        return;
    }

    // Si todo es válido, mostrar mensaje de éxito y redirigir
    alert("¡Su contraseña ha sido restablecida exitosamente!");
    window.location.href = "IniciarSesion";
});