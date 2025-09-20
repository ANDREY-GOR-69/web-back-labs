from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def start():
    return '''<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
                   </html>'''

@app.route("/author")
def author():
    name = "Горшков Андрей Максимович"
    group = "ФБИ-33"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <body>
                <p>Студент: ''' + name + '''<p>
                <p>Группа: ''' + group + '''<p>
                <p>Факультет: ''' + faculty + '''<p>
                <a href='/web'>web</a>
            <body>
        </html>'''

@app.route("/image")
def image():
    path = url_for("static", filename="shield-hero.jpg")
    return '''<!doctupe html>
        <html>
            <body>
                <h1>Наофуми Иватани<h1>
                <img scr="''' + path + '''">
            </body>
        </html>'''

count = 0
@app.route('/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили ''' + str(count) + '''
    <body>
</html>'''