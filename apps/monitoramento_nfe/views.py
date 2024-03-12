from django.shortcuts import render
from django.db import connections
from django.db.utils import InterfaceError
from django.http import JsonResponse

def index(request):
    return render(request, 'monitoramento_nfe/index.html')

def api_nfe_erro(request):
    if request.method == 'GET':
        try:
            with connections['base_nfe'].cursor() as cursor:
                cursor.execute("SELECT Pedido, ide_nNF, status_sefaz, FORMAT(DataEmissao, 'dd/MM/yyyy HH:mm:ss') DataEmissao, frg_xml, Empresa, Transmitir, CCe, Cancelar, Tempo FROM MonitoramentoNFe ORDER BY Tempo Desc, Empresa")
                rows = cursor.fetchall()

                data = []
                keys = ('pedido', 'nfe', 'status', 'data_emissao', 'frg_xml', 'empresa', 'transmitir', 'cce', 'cancelar', 'tempo')

                for row in rows:
                    data.append(dict(zip(keys, row)))

                cursor.close()
        except InterfaceError:
            print('Erro de comunicacao com o banco de dados')
            return JsonResponse({}, safe=False)
        else:
            return JsonResponse(list(data), safe=False)
    else:
        return JsonResponse({}, safe=False)