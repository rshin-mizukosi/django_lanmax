from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.db import connections
from django.views.decorators.csrf import csrf_protect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
from datetime import datetime
import smtplib, os
from collections import namedtuple

# Nomeia as colunas do resultado da query
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# funcao para enviar email
def enviar_email(db, email):
    # Configurações SMTP
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT

    if db == 'greenmotor':
        smtp_username = settings.FROM_EMAIL_GREENMOTOR
        smtp_password = settings.EMAIL_PASSWORD_GREENMOTOR
    else:
        smtp_username = settings.FROM_EMAIL_LANMAX
        smtp_password = settings.EMAIL_PASSWORD_LANMAX

    # Dados do remetente e destinatário
    remetente = smtp_username
    
    # Assuntos Email
    subject = email.assunto

    # Corpo E-mail
    conteudo = email.email_body

    # Transformar nossa mensagem em MIMEMultipart
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['to'] = email.email_to
    mime_multipart['cc'] = email.email_cc
    mime_multipart['subject'] = subject
    corpo_email = MIMEText(conteudo, email.body_format, 'utf-8')
    mime_multipart.attach(corpo_email)

    if email.attachments is not None:
        for anexo in email.attachments.split(';'):
            with open(anexo, 'rb') as attachment:
                part = MIMEApplication(
                    attachment.read(),
                    Name=basename(anexo)
                )
            
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(anexo)
            mime_multipart.attach(part)

    try:
        # Envia o e-mail
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(mime_multipart)

            with connections[db].cursor() as cursor:
                cursor.execute("UPDATE EmailsAEnviar SET status = 1 WHERE id = %s", (str(email.id),))
                cursor.close()

            if email.attachments is not None:
                for anexo in email.attachments.split(';'):
                    os.remove(anexo)

            return {
                'msg': f"({datetime.today().strftime('%d/%m/%Y')} {datetime.today().strftime('%H:%M:%S')}) E-mail enviado com sucesso! (ID: {str(email.id)} - {db} - Assunto: '{email.assunto}')",
                'status': 200
            }
    except Exception as e:
        return {
            'msg': f'Erro: {str(e)}',
            'status': 403
        }
    
def criar_email_gnre(db, gnre):
    with connections[db].cursor() as cursor:
        titulo = 'Comprovante GNRE NF-e ' + gnre.NFe
        #email_cc = ''
        anexos = []

        cursor.execute("SELECT Constante FROM aux_Constantes WHERE Tipo = 'GNRE'")
        diretorio_comprovante = namedtuplefetchall(cursor)
        
        anexos.append(diretorio_comprovante[0].Constante + gnre.Mnemonico_GNRE + '\\' + gnre.Comprovante)

        cursor.execute("SELECT Diretorio FROM DiretoriosNFe WHERE CNPJ = %s AND TipoArquivo = 'pdfDANFe'", (gnre.emit_CNPJ,))
        diretorio_danfe = namedtuplefetchall(cursor)

        anexos.append(diretorio_danfe[0].Diretorio + gnre.NFe + '-danfe.pdf')
        
        cnpj_empresa = gnre.emit_CNPJ
        cnpj_empresa_formatado = '{}.{}.{}/{}-{}'.format(cnpj_empresa[:2], cnpj_empresa[2:5], cnpj_empresa[5:8], cnpj_empresa[8:12], cnpj_empresa[12:])

        corpo_email = "<p>Esta mensagem refere-se ao comprovante de pagamento GNRE da NF-e " + gnre.NFe + \
            ", emitida pela empresa " + gnre.emit_xNome + ", CNPJ " + cnpj_empresa_formatado + ".</p>" \
            "<p>Att,</p><br/><p>Equipe Lanmax</p>"
        
        if gnre.Email == gnre.MSN:
            destinatario = gnre.Email
        else:
            destinatario = gnre.Email + ';' + gnre.MSN
        
        cursor.execute("INSERT INTO EmailsAEnviar VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (destinatario, None, titulo, corpo_email, 'html', ';'.join(anexos), datetime.now(), 0))
        cursor.execute("UPDATE GNRE_Pagamentos SET Enviado = 1 WHERE CodPedido = %s", (gnre.CodPedido,))
        cursor.close()

        return {
            'msg': f"({datetime.today().strftime('%d/%m/%Y')} {datetime.today().strftime('%H:%M:%S')}) E-mail da GNRE pedido {gnre.CodPedido} gerado com sucesso!",
            'status': 200
        }

def index(request, db):
    return render(request, 'email_lanmax/index.html', {'db': db})

@csrf_protect
def send_email(request, db):
    with connections[db].cursor() as cursor:
        cursor.execute("SELECT * FROM EmailsAEnviar WHERE status = 0 ORDER BY data")

        emails = namedtuplefetchall(cursor)
        cursor.close()

        retorno = []

        if len(emails) == 0:
            return JsonResponse({'msg': '', 'status': 204})

        for email in emails:
            retorno.append(enviar_email(db, email))
        
        return JsonResponse({'retorno': retorno})

@csrf_protect
def gera_gnre_email(request, db):
    with connections[db].cursor() as cursor:
        query = "SELECT g.CodPedido, g.NFe, g.Comprovante, ISNULL(c.Email, '') Email, ISNULL(c.MSN, '') MSN, e.Mnemonico_GNRE, emit_xNome, emit_CNPJ " \
            "FROM Pedidos p INNER JOIN GNRE_Pagamentos g " \
            "ON p.CodPedido = g.CodPedido INNER JOIN Clientes c " \
            "ON p.CodCliente = c.CodCliente INNER JOIN EmpresaFilial ef " \
            "ON p.EmpresaFilial = ef.EmpresaFilial INNER JOIN Empresas e " \
            "ON ef.EmpresaFilial = e.EmpresaFilial " \
            "WHERE g.Status = 10 AND g.Comprovante IS NOT NULL AND g.Enviado = 0 AND g.DataEmissao >= %s " \
            "ORDER BY e.Mnemonico, g.NFe"

        cursor.execute(query, ('20230701',))
        gnres = namedtuplefetchall(cursor)
        cursor.close()

        retorno = []

        if len(gnres) == 0:
            return JsonResponse({'msg': '', 'status': 204})
    
        for gnre in gnres:
            retorno.append(criar_email_gnre(db, gnre))

        return JsonResponse({'retorno': retorno})