$(function() {
    setTimeout(function() {
        location.reload();
    }, 60000);

    $.ajax({
        type: 'POST',
        url: url_libera_pagto,
        data: {
            csrfmiddlewaretoken: csrf_token
        },
        dataType: 'json',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error)
        }
    });
});