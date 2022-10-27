from flask import Flask
from flask import request, jsonify
from connector import executeReadQuery, executeWriteQuery

app = Flask(__name__)

@app.route("/orderHealth", methods=['GET'])
def health():
    result = {
        result: 'Order APIs working'
    }
    return jsonify(result)

@app.route("/createOrder", methods=['POST'])
def createOrder():
    items = request.args.get('items').split(',')
    payment_mode = request.args.get('payment_mode')
    paid_status = request.args.get('paid_status')
    total_price = request.args.get('total_price')

    SQL_1 = '''INSERT INTO Orders(total_price, payment_mode, paid) VALUES (%(total_price)s, %(payment_mode)s, %(paid)s)'''
    sql1_data = {
        'total_price':total_price,
        'payment_mode':payment_mode,
        'paid':paid_status
    }

    resultSet1 = executeWriteQuery(SQL_1, sql1_data)
    
    order_id = resultSet1

    item_set = [(order_id, int(i)) for i in items]
    item_set = f'{*item_set,}'
    item_set = item_set[1:len(item_set)-1]

    SQL_2 = f'''INSERT INTO order_item(order_id, item_id) VALUES {item_set}'''
    resultSet2 = executeWriteQuery(SQL_2)

    result = {
        "outcome":'Success' if isinstance(resultSet2, int) else 'Failure'
    }

    return jsonify(result)

@app.route("/deleteOrder", methods=['POST'])
def deleteOrder():
    order_id = request.args.get('order_id')

    SQL_1 = '''DELETE FROM order_item WHERE order_id=%s'''
    data = [order_id]

    resultSet1 = executeWriteQuery(SQL_1, data)

    SQL_2 = '''DELETE FROM Orders WHERE order_id=%s'''
    data = [order_id]

    resultSet2 = executeWriteQuery(SQL_2, data)
    result = {
        "outcome":'Success' if isinstance(resultSet2, int) else 'Failure'
    }

    return jsonify(result)

app.run(debug=True)