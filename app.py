from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
app = Flask(__name__)

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
                <li><a href="''' + url_for('lab1') + '''">Первая лабораторная</a></li>
                <li><a href="''' + url_for('lab2') + '''">Вторая лабораторная</a></li>
            </menu>
        </main>
        <footer>
            Горшков Андрей Максимович, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''

@app.route("/lab1")
def lab1():
    return '''<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <h1>Первая лабораторная работа</h1>
            
            <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.</p>
            
            <a href="''' + url_for('index') + '''">Вернуться на главную</a>
            
            <h2>Список роутов</h2>
            <ul>
                <li><a href="''' + url_for('web') + '''">Web-сервер на Flask</a></li>
                <li><a href="''' + url_for('author') + '''">Об авторе</a></li>
                <li><a href="''' + url_for('image') + '''">Изображение</a></li>
                <li><a href="''' + url_for('counter') + '''">Счетчик посещений</a></li>
                <li><a href="''' + url_for('info') + '''">Перенаправление</a></li>
                <li><a href="''' + url_for('unauthorized') + '''">401</a></li>
                <li><a href="''' + url_for('payment_required') + '''">402</a></li>
                <li><a href="''' + url_for('forbidden') + '''">403</a></li>
                <li><a href="''' + url_for('method_not_allowed') + '''">405</a></li>
                <li><a href="''' + url_for('teapot') + '''">418</a></li>
                <li><a href="''' + url_for('server_error_test') + '''">Тест ошибки 500</a></li>
            </ul>
        </main>
        <footer>
            Горшков Андрей Максимович, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''

@app.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
            </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Горшков Андрей Максимович"
    group = "ФБИ-33"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="''' + url_for('web') + '''">web</a>
            </body>
        </html>'''

@app.route("/lab1/image")
def image():
    image_path = url_for("static", filename="shield-hero.jpg")
    css_path = url_for("static", filename="main.css")
    
    html_content = '''<!DOCTYPE html>
<html>
    <head>
        <title>Наофуми Иватани</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <div class="container">
            <h1>Наофуми Иватани</h1>
            <img src="''' + image_path + '''" alt="Наофуми Иватани">
            <p class="description">Главный герой аниме "Восхождение героя щита"</p>
        </div>
    </body>
</html>'''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Anime-Character': 'Naofumi Iwatani',
        'X-Series-Name': 'The Rising of the Shield Hero',
        'X-Server-Technology': 'Flask Python Framework',
        'Content-Type': 'text/html; charset=utf-8'
    }
count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = str(datetime.datetime.today())
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP адрес: ''' + client_ip + '''<br>
        <hr>
        <a href="''' + url_for('reset_counter') + '''">Сбросить счетчик</a>
    </body>
</html>'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано</i></div>
    </body>
</html>
''', 201

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
@app.route('/lab2/a')
def a():
    return 'без слэша'
@app.route("/lab2/a/")
def a2():
    return 'со слэшем'
flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    else:
        flower_name = flower_list[flower_id]
        return f"""
<!doctype html>
<html>
    <body>
        <h1>Цветок с ID {flower_id}</h1>
        <p>Название: <b>{flower_name}</b></p>
        <p><a href="/lab2/flowers_list">Посмотреть все цветы</a></p>
    </body>
</html>
"""

@app.route('/lab2/flowers/<name>')
def add_flower(name):
    flower_list.append(name)
    return f"""
<!doctype html>
<html>
    <body>
        <h1>Добавлен цветок</h1>
        <p>Название нового цветка: <b>{name}</b></p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <p><a href="/lab2/flowers_list">Посмотреть все цветы</a></p>
    </body>
</html>
"""

@app.route('/lab2/flowers/')
def add_flower_no_name():
    return """
<!doctype html>
<html>
    <body>
        <h1>Ошибка 400</h1>
        <p style="color:red;">Вы не задали имя цветка!</p>
        <p><a href="/lab2/flowers_list">Посмотреть все цветы</a></p>
    </body>
</html>
""", 400

@app.route('/lab2/flowers_list')
def show_flowers():
    flowers_html = "<ul>" + "".join([f"<li>{f}</li>" for f in flower_list]) + "</ul>"
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        {flowers_html}
        <p><a href="/lab2/clear_flowers">Очистить список</a></p>
    </body>
</html>
'''
@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <p><a href="/lab2/flowers_list">Посмотреть все цветы</a></p>
    </body>
</html>'''
@app.route('/lab2/example')
def example():
    name = 'Горшков Андрей'
    nomer = '2'
    group = 'ФБИ-33'
    kurs = '3 курс'
    lab_num = '2'
    fruits = [{'name': 'яблоки', 'price': 100}, 
              {'name': 'груши', 'price': 100}, 
              {'name': 'апельсины' , 'price': 100},
              {'name': 'мандарины', 'price': 100}, 
              {'name': 'манго', 'price': 100},]
    return render_template('example.html', name=name, nomer=nomer, kurs=kurs, group=group, lab_num=lab_num, fruits=fruits)
@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')
@app.route('/lab2/filters')
def filters():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filters.html', phrase=phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    if b == 0:
        div_result = "Ошибка: деление на ноль"
    else:
        div_result = a / b

    return f'''
<!doctype html>
<html>
    <body>
        <h1>Калькулятор</h1>
        <p>Первое число: {a}</p>
        <p>Второе число: {b}</p>
        <ul>
            <li>Сумма: {a + b}</li>
            <li>Разность: {a - b}</li>
            <li>Произведение: {a * b}</li>
            <li>Деление: {div_result}</li>
            <li>Возведение в степень: {a ** b}</li>
        </ul>
        <p><a href="/lab2/calc/">Попробовать снова с 1 и 1</a></p>
    </body>
</html>
'''
books = [
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 640},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 320},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 480},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 370},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Сатира", "pages": 420},
    {"author": "Антон Чехов", "title": "Палата №6", "genre": "Повесть", "pages": 95},
    {"author": "Даниэл Киз", "title": "Цветы для Элджернона", "genre": "Фантастика", "pages": 310},
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 350},
    {"author": "Рэй Брэдбери", "title": "451° по Фаренгейту", "genre": "Фантастика", "pages": 256}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)
Berry = [
    {"name": "Арбуз", "img": "Berry/ar.jpg", "desc": "Крупная сладкая ягода с красной мякотью и чёрными семенами."},
    {"name": "Жимолость", "img": "Berry/jim.jpg", "desc": "Синевато-фиолетовая ягода с кисло-сладким вкусом и массой витаминов."},
    {"name": "Клубника", "img": "Berry/klub.jpg", "desc": "Сочная и ароматная ягода, любима во всём мире."},
    {"name": "Клюква", "img": "Berry/klukva.jpg", "desc": "Кислая болотная ягода, используется для морсов и варенья."},
    {"name": "Крыжовник", "img": "Berry/kr.jpg", "desc": "Зелёная или красная ягода с кисло-сладким вкусом, богатая витамином C."},
    {"name": "Красная смородина", "img": "Berry/krasn.jpg", "desc": "Мелкие ярко-красные ягоды с освежающим кисловатым вкусом."},
    {"name": "Малина", "img": "Berry/mal.jpg", "desc": "Мягкая и ароматная ягода, часто используется при простуде."},
    {"name": "Облепиха", "img": "Berry/oblepixa.jpg", "desc": "Оранжевая ягода с терпким вкусом и мощными лечебными свойствами."},
    {"name": "Виктория", "img": "Berry/vic.jpg", "desc": "Сорт садовой земляники, крупная и ароматная."},
    {"name": "Ежевика", "img": "Berry/yjev.jpg", "desc": "Тёмно-фиолетовая ягода с насыщенным вкусом и антоцианами."}
]

@app.route('/lab2/Berry')
def show_Berry():
    return render_template('Berry.html', berries=Berry)