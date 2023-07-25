from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json

@login_required
def index(request, db='lanmax'):
    cursor = connection.cursor()
    cursor.execute("SELECT CodPedido, Tipo, NFe, Empresa, UF, DataEmissao,DataValidacao, Valor FROM " + db.capitalize() + ".dbo.GNRE_Pagamentos WHERE Status = 2 ORDER BY DataValidacao")
    rows = cursor.fetchall()

    result = []
    keys = ('cod_pedido', 'tipo', 'nfe', 'empresa', 'uf', 'data_emissao', 'data_validacao', 'valor')

    for row in rows:
        result.append(dict(zip(keys, row)))

    return render(request, 'gnre/index.html', {'result': result, 'db': db})

@login_required
def libera_pagto(request, db='lanmax'):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('EXEC ' + db.capitalize() + '.dbo.GNRE_LiberaPagto')

        json_response = {
            'status': 200
        }

        json_response = json.dumps(json_response)

        return HttpResponse(json_response, content_type='application/json', status=200)