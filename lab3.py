from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)
@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp
@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp
@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните имя!'
    er_age = {}
    age = request.args.get('age')
    if age == '':
        er_age['age'] = 'Заполните возраст!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors, er_age=er_age)
@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')
@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)
@lab3.route('/lab3/payment')
def payment():
    price = request.args.get('price')
    return render_template('lab3/payment.html', price=price)
@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    if color or bg_color or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    
    return render_template('lab3/settings.html', 
                         color=color, 
                         bg_color=bg_color, 
                         font_size=font_size)
@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age_str = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    travel_date = request.args.get('travel_date')
    insurance = request.args.get('insurance') == 'on'
    
    form_submitted = any([fio, shelf, age_str, departure, destination, travel_date])
    
    if form_submitted:
        if not fio:
            errors['fio'] = 'Заполните ФИО пассажира'
        if not shelf:
            errors['shelf'] = 'Выберите полку'
        if not age_str:
            errors['age'] = 'Заполните возраст'
        elif not age_str.isdigit() or not (1 <= int(age_str) <= 120):
            errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        if not departure:
            errors['departure'] = 'Заполните пункт выезда'
        if not destination:
            errors['destination'] = 'Заполните пункт назначения'
        if not travel_date:
            errors['travel_date'] = 'Выберите дату поездки'
        
        if errors:
            return render_template('lab3/ticket.html', 
                                 errors=errors,
                                 fio=fio,
                                 shelf=shelf,
                                 linen=linen,
                                 luggage=luggage,
                                 age=age_str,
                                 departure=departure,
                                 destination=destination,
                                 travel_date=travel_date,
                                 insurance=insurance,
                                 show_result=False)
        
        age = int(age_str)
        if age < 18:
            price = 700
        else:
            price = 1000
        
        if shelf in ['lower', 'side_lower']:
            price += 100
        if linen:
            price += 75
        if luggage:
            price += 250
        if insurance:
            price += 150
        
        return render_template('lab3/ticket.html',
                             fio=fio,
                             shelf=shelf,
                             linen=linen,
                             luggage=luggage,
                             age=age,
                             departure=departure,
                             destination=destination,
                             travel_date=travel_date,
                             insurance=insurance,
                             price=price,
                             show_result=True)
    
    return render_template('lab3/ticket.html', show_result=False)
@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color') 
    resp.delete_cookie('font_size')
    return resp
# Список комиксов DC
dc_comics = [
    {"title": "Бэтмен: Возвращение Тёмного Рыцаря", "price": 1500, "year": 1986, "hero": "Бэтмен"},
    {"title": "Хранители", "price": 1800, "year": 1986, "hero": "Хранители"},
    {"title": "Супермен: Красный Сын", "price": 1200, "year": 2003, "hero": "Супермен"},
    {"title": "Бэтмен: Долгий Хэллоуин", "price": 1400, "year": 1996, "hero": "Бэтмен"},
    {"title": "Чудо-женщина: Боги и смертные", "price": 1100, "year": 1987, "hero": "Чудо-женщина"},
    {"title": "Флэш: Возвращение Барри Аллена", "price": 950, "year": 2009, "hero": "Флэш"},
    {"title": "Аквамен: Становление", "price": 850, "year": 2016, "hero": "Аквамен"},
    {"title": "Зелёный Фонарь: Секретное происхождение", "price": 1000, "year": 2008, "hero": "Зелёный Фонарь"},
    {"title": "Лига Справедливости: Трон Атлантиды", "price": 1300, "year": 2013, "hero": "Лига Справедливости"},
    {"title": "Харли Квинн: Безумие", "price": 900, "year": 2014, "hero": "Харли Квинн"},
    {"title": "Бэтмен: Убийственная Шутка", "price": 1600, "year": 1988, "hero": "Бэтмен"},
    {"title": "Супермен: Все Звёзды", "price": 1250, "year": 2005, "hero": "Супермен"},
    {"title": "Чудо-женщина: Кровь", "price": 1150, "year": 2012, "hero": "Чудо-женщина"},
    {"title": "Флэшпойнт", "price": 1350, "year": 2011, "hero": "Флэш"},
    {"title": "Зелёный Фонарь: Война Зелёных Фонарей", "price": 1050, "year": 2011, "hero": "Зелёный Фонарь"},
    {"title": "Бэтмен: Год первый", "price": 1450, "year": 1987, "hero": "Бэтмен"},
    {"title": "Супермен: Рождение", "price": 950, "year": 1986, "hero": "Супермен"},
    {"title": "Харли Квинн и Бэтмен", "price": 800, "year": 2017, "hero": "Харли Квинн"},
    {"title": "Аквамен: Империя Зла", "price": 750, "year": 2018, "hero": "Аквамен"},
    {"title": "Лига Справедливости: Тёмнейшая ночь", "price": 1700, "year": 2010, "hero": "Лига Справедливости"},
    {"title": "Бэтмен: Тихий рыцарь", "price": 1550, "year": 1999, "hero": "Бэтмен"},
    {"title": "Супермен: Завтрашний человек", "price": 1100, "year": 2004, "hero": "Супермен"},
    {"title": "Чудо-женщина: Истина", "price": 1200, "year": 2016, "hero": "Чудо-женщина"}
]

@lab3.route('/lab3/comics')
def comics():
    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')
    
    min_price_arg = request.args.get('min_price', min_price_cookie)
    max_price_arg = request.args.get('max_price', max_price_cookie)
    reset = request.args.get('reset')
    
    if reset:
        resp = make_response(redirect('/lab3/comics'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    min_price_all = min(comic['price'] for comic in dc_comics)
    max_price_all = max(comic['price'] for comic in dc_comics)
    
    filtered_comics = dc_comics
    message = ""
    
    if min_price_arg or max_price_arg:
        try:
            min_price = int(min_price_arg) if min_price_arg else min_price_all
            max_price = int(max_price_arg) if max_price_arg else max_price_all
            
            if min_price > max_price:
                min_price, max_price = max_price, min_price
            
            filtered_comics = [
                comic for comic in dc_comics
                if min_price <= comic['price'] <= max_price
            ]
            
            count = len(filtered_comics)
            if count == 0:
                message = "Не найдено ни одного комикса в заданном диапазоне цен"
            else:
                message = f"Найдено комиксов: {count}"
                
            if min_price_arg or max_price_arg:
                resp = make_response(render_template('lab3/comics.html',
                    comics=filtered_comics,
                    min_price=min_price,
                    max_price=max_price,
                    min_price_all=min_price_all,
                    max_price_all=max_price_all,
                    message=message
                ))
                if min_price_arg:
                    resp.set_cookie('min_price', min_price_arg)
                if max_price_arg:
                    resp.set_cookie('max_price', max_price_arg)
                return resp
                
        except ValueError:
            message = "Ошибка: введите корректные числовые значения"
    
    return render_template('lab3/comics.html',
        comics=filtered_comics,
        min_price=min_price_arg,
        max_price=max_price_arg,
        min_price_all=min_price_all,
        max_price_all=max_price_all,
        message=message or f"Всего комиксов: {len(filtered_comics)}"
    )