$(function() {
    $('#cnpj').mask('00.000.000/0000-00', {reverse: true});
    $('#cnpj').focus();

    window.setTimeout(() => {
        $('.alert').alert('close');
    }, 5000);
    
    $('form').on('submit', function(e) {
        $('#cnpj').val($('#cnpj').cleanVal());
        $('#overlay').fadeIn();
    });
});