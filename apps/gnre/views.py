from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.utils import InterfaceError
from django.http import JsonResponse
import json

@login_required
def index(request, db='lanmax'):
    return render(request, 'gnre/index.html', {'db': db})

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
    
def api_gnre_nao_liberadas(request, db='lanmax'):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT CodPedido, Tipo, NFe, Empresa, UF, FORMAT(DataEmissao, 'dd/MM/yyyy HH:mm:ss ') DataEmissao, FORMAT(DataValidacao, 'dd/MM/yyyy HH:mm:ss ') DataValidacao, Valor FROM " + db.capitalize() + ".dbo.GNRE_Pagamentos WHERE Status = 2 ORDER BY DataValidacao")
        rows = cursor.fetchall()

        data = []
        keys = ('cod_pedido', 'tipo', 'nfe', 'empresa', 'uf', 'data_emissao', 'data_validacao', 'valor')

        for row in rows:
            data.append(dict(zip(keys, row)))

        cursor.close()
    except InterfaceError:
        print('Erro de comunicacao com o banco de dados')
        return JsonResponse({}, safe=False)
    else:
        return JsonResponse(list(data), safe=False)