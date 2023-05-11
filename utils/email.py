import os

from django.core.mail import EmailMultiAlternatives


def send_styled_email(subject, to, text_content, titulo, msg):
    # Substitua pelo domínio do seu projeto e a porta, se necessário
    from_email = os.environ["EMAIL_HOST_USER"]
    html_content = f'''
        <html>

        <head>
            <style>
                h1 {{
                    color: #ff6702;
                    font-size: 18px;
                    text-align: center;
                }}

                p {{
                    color: rgb(39, 39, 39);
                    font-size: 16px;
                    line-height: 2;
                    text-align: justify;
                }}

                .container {{
                    margin: 10px auto;
                    width: 70%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: rgb(39, 40, 44);
                    padding: 0.5rem;
                }}

                .l-box {{
                    margin-left: 1rem;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}

                .main-content {{
                    margin: 0 auto;
                    width: 70%;
                    display: flex;
                    justify-content: center;
                    align-items: left;
                    flex-direction: column;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <img src="https://i.imgur.com/zC9GqgO.png" alt="logo" border="0" width="50" height="50">
                <div class="l-box">
                    <h1>{titulo}</h1>
                </div>
            </div>
            <div class="main-content">
                <div>
                    <p>{msg}</p>
                    <p>Cordialmentemente,</p>
                    <p style="font-weight: bold;">Equipe de Desenvolvimento Dai</p>
                </div>

            </div>
        </body>

        </html>
    '''
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    ...
