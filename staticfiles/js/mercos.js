$(function() {
    var myTimeout = setTimeout(function() {
        location.reload();
    }, 60000);

    if($('table > tbody > tr').length >= 100) {
        clearInterval(myTimeout);
        $('#overlay').fadeIn();
        var totalRows = $('table > tbody > tr').length;
        var countRows = 0;
        
        $('table > tbody > tr').each(function(index, tr) {
            var codigo = $(this).find('td:eq(0)').html();
            var status = $(this).find('td:eq(7)');

            $.ajax({
                type: 'GET',
                url: url_atualiza_mercos + '?codigo=' + codigo,
                dataType: 'json',
                success: function(response) {
                    if(response.status == 200) {
                        status.fadeOut("slow", function() {
                            $(this).remove();
                            buildBadgeStatus(tr, response.status);
                        });
                    }

                    countRows++;

                    if(totalRows == countRows) {
                        redireciona();
                        /*
                        $('#overlay').fadeOut();
                        myTimeout = setTimeout(function() {
                            location.reload();
                        }, 5000);
                        */
                    }
                },
                error: function(error) {
                    console.log(error)
                    countRows++;

                    if(totalRows == countRows) {
                        redireciona();
                        /*
                        $('#overlay').fadeOut();
                        myTimeout = setTimeout(function() {
                            location.reload();
                        }, 5000);
                        */
                    }
                }
            });
        });
    }
    
    function redireciona() {
        let data_atual = new Date();
        let hora_atual = String(data_atual.getHours()).padStart(2, '0') + ':00:00';

        data_atual = data_atual.toLocaleDateString();
        location.replace(url_atualiza_lanmax + "?data=" + data_atual + "&hora=" + hora_atual);
    }

    function buildBadgeStatus(tr, status) {
        if(status == 200) {
            var html_badge = "<td><span class='badge rounded-pill bg-success'>" +
                "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-check-lg' viewBox='0 0 16 16'>" +
                "<path d='M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z'/>" +
                "</svg></span></td>"
        } else {
            var html_badge = "<td><span class='badge rounded-pill bg-danger'>" +
                "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x-lg' viewBox='0 0 16 16'>" +
                "<path d='M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z'/>" +
                "</svg></span></td>"
        }
        
        $(tr).append(html_badge)
    }
});