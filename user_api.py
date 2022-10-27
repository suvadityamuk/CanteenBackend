from flask import Flask
from flask import request, jsonify
from connector import executeReadQuery, executeWriteQuery

app = Flask(__name__)

@app.route("/userHealth", methods=['GET'])
def health():
    result = {
        'result': 'User APIs working'
    }
    return jsonify(result)

@app.route("/createUser", methods=['POST'])
def createUser():

    username = request.args.get('username')
    password = request.args.get('pwd')
    mobile_num = request.args.get('mobile_num')
    name = request.args.get('name')
    email = request.args.get('email')

    SQL_STATEMENT = '''INSERT INTO Users(username, pwd, mobile_num, name, email) 
    VALUES (%(username)s, %(password)s, %(mobile_num)s, %(name)s, %(email)s)'''
    data = {
        'username':username,
        'password':password,
        'mobile_num':mobile_num,
        'name':name,
        'email':email
    }

    resultSet = executeWriteQuery(SQL_STATEMENT, data)

    result = {
        "outcome":resultSet
    }

    return jsonify(result)
    

@app.route("/deleteUser", methods=['POST'])
def deleteUser():

    username = request.args.get('username')
    password = request.args.get('pwd')

    SQL_STATEMENT = '''DELETE FROM Users WHERE username=%s AND pwd=%s'''
    data = [username, password]

    resultSet = executeWriteQuery(SQL_STATEMENT, data)

    result = {
        "outcome":resultSet
    }

    return jsonify(result)

@app.route("/updateUser", methods=['POST'])
def updateUser():
    username = request.args.get('username').split(',')
    password = request.args.get('password').split(',')
    update_columns = request.args.get('update_cols').split(',')
    update_vals = request.args.get('update_vals').split(',')
    update_set = []

    for column, val in zip(update_columns, update_vals):
        update_set.append(f'{column}={val}')

    SQL_STATEMENT = f'''UPDATE Users SET {*update_set,} WHERE username=%s AND pwd=%s'''
    data = [username, password]

    resultSet = executeWriteQuery(SQL_STATEMENT, data)

    result = {
        "outcome":resultSet
    }

    return jsonify(result)

@app.route("/authUser", methods=['GET'])
def authUser():
    username = request.args.get('username')
    password = request.args.get('password')

    SQL_STATEMENT = '''SELECT * FROM Users WHERE username=%s'''
    data = [username]

    resultSet = executeReadQuery(SQL_STATEMENT, data)
    
    db_pwd = resultSet[0][2]

    if db_pwd == password:

        db_userid = resultSet[0][0]
        db_name = resultSet[0][1]
        db_email = resultSet[0][3]
        db_mobile_num = resultSet[0][4]
        db_username = resultSet[0][5]

        result = {
            "outcome": "Success",
            "username":db_username,
            "user_id":db_userid,
            "pwd":db_pwd,
            "email":db_email,
            "mobile_num":db_mobile_num,
            "name":db_name
        }

        return jsonify(result)

    else:

        result = {
            "outcome": "Failure"
        }

        return jsonify(result)

app.run(debug=True)