document.addEventListener('DOMContentLoaded', function() {
    toastr.options = {
        "closeButton": true,                   // Botón de cerrar
        "progressBar": true,                   // Barra de progreso
        "timeOut": "3000"                      // Duración (3 segundos)
    };

    fetch('/get_messages')
        .then(response => response.json())
        .then(messages => {
            messages.forEach(message => {
                toastr[message.category](message.text);
            });
        });
});