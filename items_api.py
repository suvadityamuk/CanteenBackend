from flask import Flask
from flask import request, jsonify
from connector import executeReadQuery, executeWriteQuery

app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    result = {
        result: 'Items APIs working'
    }
    return jsonify(result)

@app.route("/getDailyLunchItems", methods=['GET'])
def getDailyLunchItems():

    SQL_STATEMENT = '''SELECT * FROM Items WHERE item_id IN (22, 103, 166, 188, 77)'''
    data = []

    resultSet = executeReadQuery(SQL_STATEMENT, data)

    result = {
        "dailyLunchItems":resultSet
    }

    return jsonify(result)

@app.route("/getAllItems", methods=['GET'])
def getAllItems():

    SQL_STATEMENT = '''SELECT * FROM Items'''
    data = []

    resultSet = executeReadQuery(SQL_STATEMENT, data)

    result = {
        "items":resultSet
    }

    return jsonify(result)

@app.route("/getPopularItems", methods=['GET'])
def getPopularItems():

    SQL_STATEMENT = '''SELECT * FROM Items WHERE item_id IN 
    (SELECT * FROM 
    (SELECT item_id FROM order_item GROUP BY item_id ORDER BY COUNT(*) DESC LIMIT 1) temp_tab)'''
    data = []

    resultSet = executeReadQuery(SQL_STATEMENT, data)

    result = {
        "popularItems":resultSet
    }

    return jsonify(result)

@app.route("/getMealOfDay", methods=['GET'])
def getMealOfDay():

    SQL_STATEMENT = '''SELECT * FROM Items WHERE item_id IN (2, 7, 235, 202) ORDER BY RAND() LIMIT 1'''
    data = []

    resultSet = executeReadQuery(SQL_STATEMENT, data)

    result = {
        "mealOfDayItems":resultSet
    }

    return jsonify(result)

app.run(debug=True)