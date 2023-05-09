from django.shortcuts import render, redirect
from django.contrib import messages
from itertools import cycle
import requests, json

LENGTH_CNPJ = 14

def is_cnpj_valido(cnpj: str) -> bool:
    if len(cnpj) != LENGTH_CNPJ:
        return False

    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False

    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False

    return True

def index(request):
    return render(request, 'sintegra/index.html')

def consulta(request):
    if request.method == 'POST':
        if is_cnpj_valido(request.POST.get('cnpj')):
            url = 'https://publica.cnpj.ws/cnpj/' + request.POST.get('cnpj')
            response = requests.get(url)

            if response.status_code == 200:
                json_response = json.loads(response.text)

                if len(json_response['estabelecimento']['inscricoes_estaduais']) == 0:
                    messages.warning(request, 'Contribuinte isento ou não contribuinte')
                    return redirect('sintegra_index')
                
                tem_ie_ativo = False

                for ie in json_response['estabelecimento']['inscricoes_estaduais']:
                    if ie['ativo']:
                        tem_ie_ativo = True
                        break
                
                if not tem_ie_ativo:
                    messages.error(request, 'Inscrição estadual não habilitada')
                    return redirect('sintegra_index')
                
                return render(request, 'sintegra/consulta.html', {'json_response': json_response})
            else:
                messages.error(request, 'Serviço indisponível')
                return redirect('sintegra_index')
        else:
            messages.error(request, 'CNPJ inválido')
            return redirect('sintegra_index')
    else:
        return redirect('sintegra_index')