$(function() {
    function send_email() {
        $('#overlay').fadeIn()

        $.ajax({
            method: 'POST',
            url: url_email,
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(response) {
                $.each(response.retorno, function(i, v) {
                    if(v.status === 200) {
                        $('#log').append("<li class='text-success'>" + v.msg + "</li>")
                    } else if(v.status === 403) {
                        $('#log').append("<li class='text-danger'>" + v.msg + "</li>")
                    }
                })
            },
            complete: function() {
                $('#overlay').fadeOut()
                
                setTimeout(function() {
                    send_email()
                }, 300000)
            }
        })
    }

    function gera_email_gnre() {
        $('#overlay').fadeIn()

        $.ajax({
            method: 'POST',
            url: url_gnre_email,
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(response) {
                $.each(response.retorno, function(i, v) {
                    if(v.status === 200) {
                        $('#log').append("<li class='text-success'>" + v.msg + "</li>")
                    } else if(v.status === 403) {
                        $('#log').append("<li class='text-danger'>" + v.msg + "</li>")
                    }
                })

                $('#overlay').fadeOut()
            },
            complete: function() {
                setTimeout(function() {
                    gera_email_gnre()
                }, 3600000)
            }
        })
    }

    gera_email_gnre()
    send_email()
})