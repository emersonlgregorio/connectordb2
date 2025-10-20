import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template, Environment, FileSystemLoader


def send_email(to_email, subject, title_email,body_email,task_link):
    # Defina o servidor SMTP e os detalhes de autenticação
    smtp_server = "smtp-mail.outlook.com"  # Exemplo: smtp.gmail.com
    smtp_port = 587  # Porta padrão para TLS
    from_email = "integracoes@agrocrestani.com.br"
    password = "1nt3gr4@2900$"

    env = Environment(loader=FileSystemLoader('/spiff/uteis'))
    template = env.get_template('email_template.html')


    dados = {
        "titulo": title_email,
        "mensagem": body_email,
        "link": task_link
    }

    email_html = template.render(dados)

    # Cria a mensagem MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adiciona o conteúdo em HTML ao e-mail
    msg.attach(MIMEText(email_html, 'html'))

    try:
        # Conectando ao servidor SMTP com TLS
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciando a criptografia TLS
        server.login(from_email, password)  # Fazendo login

        # Enviando o e-mail
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"E-mail enviado com sucesso para {to_email}!")
    except Exception as e:
        print(f"Falha ao enviar e-mail. Erro: {e}")
    finally:
        server.quit()  # Encerrando a conexão


# # Exemplo de uso:
# to_email = "emerson.gregorio@agrocrestani.com.br"
# subject = "Assunto do E-mail"
# title_email = "Solicitação de Compra Cantina"
# body_email = "Você tem uma tarefa que precisa da sua atenção. Por favor clique no botão abaixo."
# task_link = "https://example.com/confirmacao"
#
# send_email(to_email, subject, title_email,body_email,task_link)

# http://192.168.1.222:8001/tasks/4465/a43aa6db-5afa-49b4-b20c-417256f5b7dd
# http://http//192.168.1.222:8001/tasks/4465/a43aa6db-5afa-49b4-b20c-417256f5b7dd