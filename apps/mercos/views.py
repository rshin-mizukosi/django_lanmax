from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
import requests, json, time

def json_produto(produto, excluir):
    query = "SELECT ID_MeusPedidos FROM Lanmax.dbo.Categorias WHERE CodCateg = %s"

    cursor = connection.cursor()
    cursor.execute(query, (str(produto.get('cod_categ')), ))

    result = cursor.fetchone()

    key = ('id_meus_pedidos', )

    categoria = dict(zip(key, result))

    string_json = {
        "nome": produto.get('nome_prod'),
        "preco_tabela": float(produto.get('preco')),
        "preco_minimo": None,
        "codigo": produto.get('cod_prod'),
        "comissao": None,
        "ipi": None,
        "tipo_ipi": "P",
        "st": None,
        "moeda": 0,
        "unidade": "Un",
        "saldo_estoque": produto.get('estoque'),
        "observacoes": produto.get('descricao'),
        "grade_cores": None,
        "grade_tamanhos": None,
        "excluido": excluir,
        "ativo": True,
        "categoria_id": categoria.get('id_meus_pedidos'),
        "codigo_ncm": produto.get('cod_categ'),
        "multiplo": None,
        "peso_bruto": float(produto.get('peso')),
        "largura": None,
        "altura": None,
        "comprimento": None,
        "peso_dimensoes_unitario": True,
        "exibir_no_b2b": False
    }
    
    return string_json

def get_produto(id):
    cursor = connection.cursor()
    cursor.execute("SELECT CodProd,NomeProd,Descricao,CodCateg,Peso,CASE WHEN CodProd = -41343 THEN 89.9 ELSE ROUND(Preco+(Preco*0.031)+(Preco*0.051), 2) END AS Preco,Estoque,ID_MeusPedidos,UltimaAlt_MeusPedidos " \
        "FROM Lanmax.dbo.MeusPedidos_Produtos WHERE ID_MeusPedidos is not null AND CodProd = %s", (str(id), ))
    
    produto = cursor.fetchone()
    
    keys = ('cod_prod', 'nome_prod', 'descricao', 'cod_categ', 'peso', 'preco', 'estoque', 'id_meus_pedidos', 'ultima_alt')

    return dict(zip(keys, produto))

@login_required
def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT mp.CodProd,CASE WHEN mp.CodProd = -41343 THEN 89.9 ELSE ROUND(mp.Preco+(mp.Preco*0.031)+(mp.Preco*0.051), 2) END AS Preco,p.PrecoRef,mp.Estoque,p.Estoque,mp.ID_MeusPedidos,mp.UltimaAlt_MeusPedidos " \
        "FROM Lanmax.dbo.MeusPedidos_Produtos mp INNER JOIN Lanmax.dbo.ProdutosTeste p ON mp.CodProd = p.CodProd " \
        "WHERE (mp.Estoque <> p.Estoque OR CASE WHEN mp.CodProd = -41343 THEN 89.9 ELSE ROUND(mp.Preco+(mp.Preco*0.031)+(mp.Preco*0.051), 2) END <> p.PrecoRef) AND mp.ID_MeusPedidos is not null " \
        #"WHERE (mp.Estoque <> p.Estoque OR CASE WHEN mp.CodProd = -41343 THEN 89.9 ELSE ROUND(mp.Preco+(mp.Preco*0.031)+(mp.Preco*0.051), 2) END <> p.PrecoRef) AND mp.CodProd >= -41315 " \
        "ORDER BY mp.CodProd")
    
    rows = cursor.fetchall()

    result = []
    keys = ('cod_prod', 'preco_mp', 'preco_p', 'estoque_mp', 'estoque_p', 'id_meus_pedidos', 'ultima_alt')

    for row in rows:
        result.append(dict(zip(keys, row)))

    return render(request, 'mercos/index.html', {'result': result})

@login_required
def atualiza_produtos_mercos(request):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "ApplicationToken": "b8ce5704-3629-11e9-b016-02ebd944bdac",
        "CompanyToken": "702357d6-1d78-11e8-86ae-02bb1d423b88"
    }
    
    produto = get_produto(request.GET.get('codigo'))

    url = "https://app.mercos.com/api/v1/produtos/" + str(produto.get('id_meus_pedidos'))
    response = requests.put(url, headers=headers, json=json_produto(produto, False))

    if response.status_code == 200:
        cursor = connection.cursor()
        cursor.execute("UPDATE Lanmax.dbo.Produtos SET UltimaAlt_MeusPedidos = %s WHERE CodProd = %s", (datetime.now(), produto.get('cod_prod')))

    json_response = {
        'status': response.status_code
    }

    json_response = json.dumps(json_response)

    time.sleep(3)

    return HttpResponse(json_response, content_type='application/json')

@login_required
def produtos_lanmax(request):
    return render(request, 'mercos/produtos-lanmax.html')

@login_required
def atualiza_produtos_lanmax(request):
    if request.method == 'POST':
        data = datetime.strptime(request.POST.get('data'), '%d/%m/%Y')
        data_formatada = data.strftime('%Y-%m-%d')
        hora = request.POST.get('hora')
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "ApplicationToken": "b8ce5704-3629-11e9-b016-02ebd944bdac",
            "CompanyToken": "702357d6-1d78-11e8-86ae-02bb1d423b88"
        }

        url = "https://app.mercos.com/api/v1/produtos/?alterado_apos=" + data_formatada + "%20" + hora
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            qtd_registros = len(response_json)

            for r in response_json:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE Lanmax.dbo.ProdutosTeste SET " +
                    "UltimaAlt_MeusPedidos = '" + r.get('ultima_alteracao') + "', " +
                    "NomeProd = '" + r.get('nome') + "', " +
                    "PrecoRef = " + str(r.get('preco_tabela')) + ", " +
                    "Estoque = " + str(r.get('saldo_estoque')) + " " +
                    "WHERE ID_MeusPedidos = " + str(r.get('id'))
                )

                if cursor.rowcount == 0:
                    cursor.execute(
                        "INSERT INTO Lanmax.dbo.ProdutosTeste(CodProd, NomeProd, PrecoRef, Estoque, ID_MeusPedidos, UltimaAlt_MeusPedidos) VALUES(" +
                        r.get('codigo') + ", '" + r.get('nome') + "', " + str(r.get('preco_tabela')) + ", " + str(r.get('saldo_estoque')) + ", " +
                        str(r.get('id')) + ", '" + r.get('ultima_alteracao') + "')"
                    )

            if qtd_registros > 0:
                ultima_data = datetime.strptime(response_json[-1].get('ultima_alteracao'), '%Y-%m-%d %H:%M:%S')
                ultima_data_formatada = ultima_data.strftime('%d/%m/%Y')
                ultima_hora = ultima_data.strftime('%H:%M:%S')
            else:
                ultima_data_formatada = request.POST.get('data')
                ultima_hora = request.POST.get('hora')

            if qtd_registros >= 500:
                return render(request, 'mercos/produtos-lanmax.html', {'ultima_data': ultima_data_formatada, 'ultima_hora': ultima_hora})
            else:
                return redirect('mercos_index')

            '''
            if qtd_registros >= 500:
                messages.warning(request, 'Existem ainda produtos a serem atualizados!')
            elif qtd_registros == 0:
                messages.info(request, 'Sem produto a atualizar!')
            else:
                messages.success(request, 'Todos os produtos foram atualizados!')
            
            return render(request, 'mercos/produtos-lanmax.html', {'ultima_data': ultima_data_formatada, 'ultima_hora': ultima_hora})
            '''
        
        messages.error(request, 'Erro!')
        return redirect('mercos_produtos_lanmax')
    else:
        #return redirect('mercos_produtos_lanmax')
        return render(request, 'mercos/produtos-lanmax.html', {'ultima_data': request.GET.get('data'), 'ultima_hora': request.GET.get('hora')})