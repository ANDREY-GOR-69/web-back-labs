from flask import Blueprint, render_template, request, session
import psycopg2

lab6 = Blueprint('lab6', __name__)

def get_db_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='andrey_gorshkov_knowledge_base',
        user='andrey_gorshkov_knowledge_base',
        password='091205051209'
    )

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    conn = get_db_connection()
    cur = conn.cursor()

    if data['method'] == 'info':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
        rows = cur.fetchall()

        offices = []
        for r in rows:
            offices.append({
                "number": r[0],
                "tenant": r[1],
                "price": r[2]
            })

        cur.close()
        conn.close()

        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Unauthorized'},
            'id': id
        }
    if data['method'] == 'booking':
        office_number = data['params']
        cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
        row = cur.fetchone()

        if not row:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 5, 'message': 'Office not found'},
                'id': id
            }

        if row[0] != '':
            return {
                'jsonrpc': '2.0',
                'error': {'code': 2, 'message': 'Already booked'},
                'id': id
            }

        cur.execute(
            "UPDATE offices SET tenant = %s WHERE number = %s",
            (login, office_number)
        )
        conn.commit()

        cur.close()
        conn.close()

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancelation':
        office_number = data['params']

        cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
        row = cur.fetchone()

        if not row:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 5, 'message': 'Office not found'},
                'id': id
            }

        if row[0] == '':
            return {
                'jsonrpc': '2.0',
                'error': {'code': 3, 'message': 'Office is not booked'},
                'id': id
            }

        if row[0] != login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 4, 'message': "Cannot cancel other user's booking"},
                'id': id
            }

        cur.execute(
            "UPDATE offices SET tenant = '' WHERE number = %s",
            (office_number,)
        )
        conn.commit()

        cur.close()
        conn.close()

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Method not found'},
        'id': id
    }
