from flask import Flask, url_for, request, redirect, abort, render_template, session
from datetime import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
app = Flask(__name__)
app.secret_key = 'секретно-секретный ключ'
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)

@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <menu>
                <li><a href="''' + url_for('lab1.lab') + '''">Первая лабораторная</a></li>
                <li><a href="''' + url_for('lab2.lab') + '''">Вторая лабораторная</a></li>
                <li><a href="''' + url_for('lab3.lab') + '''">Третья лабораторная</a></li>
                <li><a href="''' + url_for('lab4.lab') + '''">Четвертая лабораторная</a></li>
            </menu>
        </main>
        <footer>
            Горшков Андрей Максимович, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''

not_found_logs = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестно')
    
    log_entry = {
        'ip': client_ip,
        'time': access_time,
        'url': requested_url,
        'user_agent': user_agent
    }
    not_found_logs.append(log_entry)
    
    if len(not_found_logs) > 20:
        not_found_logs.pop(0)
    
    log_html = '<h3>История 404 ошибок:</h3><table border="1" style="width: 100%; border-collapse: collapse;">'
    log_html += '<tr><th>Время</th><th>IP-адрес</th><th>Запрошенный URL</th><th>User-Agent</th></tr>'
    
    for entry in reversed(not_found_logs):
        log_html += f'''
        <tr>
            <td style="padding: 5px;">{entry["time"]}</td>
            <td style="padding: 5px;">{entry["ip"]}</td>
            <td style="padding: 5px;">{entry["url"]}</td>
            <td style="padding: 5px; font-size: 12px;">{entry["user_agent"][:50]}...</td>
        </tr>'''
    
    log_html += '</table>'
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #d32f2f; }}
            .info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            table {{ margin-top: 20px; font-size: 14px; width: 100%; border-collapse: collapse; }}
            th {{ background: #e0e0e0; padding: 10px; text-align: left; }}
            td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>404 - Страница не найдена</h1>
            
            <div class="info">
                <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
                <p><strong>Дата и время доступа:</strong> {access_time}</p>
                <p><strong>Запрошенный URL:</strong> {requested_url}</p>
            </div>
            
            <p>К сожалению, запрашиваемая страница не существует.</p>
            <p>Вернитесь на <a href="{url_for('index')}">главную страницу</a> или воспользуйтесь меню навигации.</p>
            
            {log_html}
        </div>
    </body>
</html>
''', 404

@app.route('/401')
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
    </body>
</html>
''', 401

@app.route('/402')
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу.</p>
    </body>
</html>
''', 402

@app.route('/403')
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
    </body>
</html>
''', 403

@app.route('/405')
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
    </body>
</html>
''', 405

@app.route('/418')
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник и не могу заваривать кофе.</p>
        <p>Это шуточный код ошибки из April Fools' Day RFC 2324.</p>
    </body>
</html>
''', 418
@app.route('/server_error')
def server_error_test():
    result = 10 / 0
    return "Этот код никогда не выполнится"

@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
    </head>
    <body>
        <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
            <h1 style="color: #d32f2f;">500 - Внутренняя ошибка сервера</h1>
            <p>Что-то пошло не так на нашей стороне. Не волнуйтесь, мы уже работаем над решением!</p>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>Возможные причины:</strong></p>
                <ul style="text-align: left; max-width: 300px; margin: 0 auto;">
                    <li>Временные технические неполадки</li>
                    <li>Ошибка в коде приложения</li>
                    <li>Проблемы с подключением к базе данных</li>
                </ul>
            </div>
            
            <div style="background: #ffebee; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>Что вы можете сделать:</strong></p>
                <ul style="text-align: left; max-width: 300px; margin: 0 auto;">
                    <li>Обновите страницу через несколько минут</li>
                    <li>Вернитесь на <a href="''' + url_for('index') + '''">главную страницу</a></li>
                    <li>Сообщите об ошибке администратору</li>
                </ul>
            </div>
            
            <div style="margin: 25px 0;">
                <details>
                    <summary><strong>Техническая информация (для разработчиков)</strong></summary>
                    <p>Код ошибки: 500 Internal Server Error</p>
                    <p>Тип ошибки: ''' + str(type(err).__name__) + '''</p>
                    <p>Сообщение: ''' + str(err) + '''</p>
                </details>
            </div>
            
            <div style="font-style: italic; color: #666;">
                <p>"Каждая ошибка - это шаг к более стабильному коду"</p>
            </div>
        </div>
    </body>
</html>
''', 500
