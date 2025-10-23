from flask import Blueprint, render_template, request, redirect, url_for

lab2 = Blueprint('lab2', __name__)

flowers = [
    {"name": "Роза", "price": 150},
    {"name": "Тюльпан", "price": 90},
    {"name": "Незабудка", "price": 120},
    {"name": "Ромашка", "price": 80}
]

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')
@lab2.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers.html', flowers=flowers)

@lab2.route('/lab2/flowers/add', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')

    if not name:
        return "Вы не задали имя цветка", 400
    if not price or not price.isdigit():
        return "Цена должна быть числом", 400

    flowers.append({"name": name, "price": int(price)})
    return redirect('/lab2/flowers') 

@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flowers):
        flowers.pop(flower_id)
    return redirect('/lab2/flowers')

@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flowers.clear()
    return redirect('/lab2/flowers')

@lab2.route('/lab2/example')
def example():
    name = 'Горшков Андрей'
    nomer = '2'
    group = 'ФБИ-33'
    kurs = '3 курс'
    lab_num = '2'
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 100}, 
        {'name': 'апельсины', 'price': 100},
        {'name': 'мандарины', 'price': 100}, 
        {'name': 'манго', 'price': 100}
    ]
    return render_template('example.html', name=name, nomer=nomer, kurs=kurs, group=group, lab_num=lab_num, fruits=fruits)

@lab2.route('/lab2/filters')
def filters():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filters.html', phrase=phrase)

@lab2.route('/lab2/books')
def show_books():
    books = [
        {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 640},
        {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
    ]
    return render_template('books.html', books=books)

@lab2.route('/lab2/Berry')
def show_Berry():
    berries = [
        {"name": "Арбуз", "img": "lab2/Berry/ar.jpg", "desc": "Крупная сладкая ягода"},
        {"name": "Клубника", "img": "lab2/Berry/klub.jpg", "desc": "Сочная и ароматная ягода"},
    ]
    return render_template('Berry.html', berries=berries)