$(function() {
    $('#id_data').mask('00/00/0000');
    $('#id_hora').mask('00:00:00');

    $('#overlay').fadeIn();
    $('form').submit();

    /*
    if($('#id_data').val() == '' && $('#id_hora').val() == '') {
        var data_atual = new Date();
        var hora_atual = data_atual.getHours() + ":00:00"

        $('#id_data').val(data_atual.toLocaleDateString());
        $('#id_hora').val(hora_atual)
    }

    $.validator.messages.required = 'Campo obrigatório'

    var validator = $('form').validate({
        messages: {
            data: {
                minlength: 'Informe uma data o formato DD/MM/YYYY'
            },
            hora: {
                minlength: 'Informe uma hora válida no formato HH:MM:SS'
            }
        }
    });

    $('#btnAtProdLanmax').on('click', function() {
        if($('form').valid()) {
            $('#overlay').fadeIn();
            $('form').submit();
        }
    });
    */
});