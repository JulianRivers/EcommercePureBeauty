$(document).ready(function() {
    $('#agregar-viatico').click(function() {
        $.ajax({
            url: "{% url 'empleado:agregarViatico'  idEvento=evento.id %}",
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                console.log('hola')
            },
            error: function(xhr, textStatus, error) {
                console.log('error')
            }
        });
    });
});