$(function() {
    setTimeout(function() {
        location.reload();
    }, 5000);

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