$(function() {
    var segundos = 60;
    var contagem_regressiva = segundos;

    var refreshInterval = setInterval(function() {
        contagemRegressiva();
    }, 1000);

    trazerRegistros();

    function contagemRegressiva() {
        if(contagem_regressiva == 0) {
            contagem_regressiva = segundos;
            trazerRegistros();
        }
    
        if(contagem_regressiva < 10)
            document.getElementById("refresh_time").textContent = 'Atualizando em 0' + contagem_regressiva + 'seg...';
        else
            document.getElementById("refresh_time").textContent = 'Atualizando em ' + contagem_regressiva + 'seg...';
    
        contagem_regressiva = contagem_regressiva - 1;
    }

    function trazerRegistros() {
        let i = 0;

        limpar_lista_registros();
    
        fetch(url)
        .then(res => {return res.json();})
        .then(data => {
            data.forEach(el => {
                tr = document.createElement('tr');
                tr.setAttribute('id', el.cod_prod);
                lista.appendChild(tr);

                td1 = document.createElement('td');
                td1.textContent = el.cod_prod;
                tr.appendChild(td1);
    
                td2 = document.createElement('td');
                td2.textContent = el.preco_mp;
                tr.appendChild(td2);
    
                td3 = document.createElement('td');
                td3.textContent = el.preco_p;
                tr.appendChild(td3);
    
                td4 = document.createElement('td');
                td4.textContent = el.estoque_mp;
                tr.appendChild(td4);
    
                td5 = document.createElement('td');
                td5.textContent = el.estoque_p;
                tr.appendChild(td5);
    
                td6 = document.createElement('td');
                td6.textContent = el.id_meus_pedidos;
                tr.appendChild(td6);
    
                td7 = document.createElement('td');
                td7.textContent = el.ultima_alt;
                tr.appendChild(td7);
    
                td8 = document.createElement('td');
                span = document.createElement('span');
                span.className = 'badge rounded-pill bg-danger';

                i1 = document.createElement('i');
                i1.className = 'fa-solid fa-x';

                tr.appendChild(td8);
                td8.appendChild(span);
                span.appendChild(i1);

                i++;
            });

            $('#total-registros').text('Total de registros: ' + i);

            if(i >= 100)
                atualizaEstoquePrecoLanmax();
        })
    }
    
    function limpar_lista_registros() {
        // remove filhos previos
        while(lista.firstChild)
            lista.removeChild(lista.firstChild);
    }

    function atualizaEstoquePrecoLanmax() {
        clearInterval(refreshInterval);
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
            var html_badge = "<td><span class='badge rounded-pill bg-success'><i class='fa-solid fa-check'></i></span></td>"
        } else {
            var html_badge = "<td><span class='badge rounded-pill bg-danger'><i class='fa-solid fa-x'></i></span></td>"
        }
        
        $(tr).append(html_badge)
    }
});