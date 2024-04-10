$(function() {
    var segundos = 60;
    var contagem_regressiva = segundos;

    var refreshInterval = setInterval(function() {
        contagemRegressiva();
    }, 1000);

    trazerRegistros();

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        }
    }

    fetch(url_libera_pagto, options)
        .then(res => {return res.json();})

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
        limpar_lista_registros();
    
        fetch(url)
        .then(res => {return res.json();})
        .then(data => {
            data.forEach(el => {
                tr = document.createElement('tr');
                tr.setAttribute('id', el.cod_pedido);
                lista.appendChild(tr);

                td1 = document.createElement('td');
                td1.textContent = el.cod_pedido;
                tr.appendChild(td1);
    
                td2 = document.createElement('td');
                td2.textContent = el.tipo;
                tr.appendChild(td2);
    
                td3 = document.createElement('td');
                td3.textContent = el.nfe;
                tr.appendChild(td3);
    
                td4 = document.createElement('td');
                td4.textContent = el.empresa;
                tr.appendChild(td4);
    
                td5 = document.createElement('td');
                td5.textContent = el.uf;
                tr.appendChild(td5);
    
                td6 = document.createElement('td');
                td6.textContent = el.data_emissao;
                tr.appendChild(td6);
    
                td7 = document.createElement('td');
                td7.textContent = el.data_validacao;
                tr.appendChild(td7);
    
                td8 = document.createElement('td');
                td8.textContent = el.valor;
                tr.appendChild(td8);
            });
        })
    }
    
    function limpar_lista_registros() {
        // remove filhos previos
        while(lista.firstChild)
            lista.removeChild(lista.firstChild);
    }
});