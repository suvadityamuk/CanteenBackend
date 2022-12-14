from flask import Flask, render_template
from flask import request, jsonify
from connector import executeReadQuery, executeWriteQuery
import razorpay

"""
    Main file for application. 

    create_app is the function that returns the Flask App for WSGI
"""


def create_app():
    app = Flask(__name__)

    """
        Returns a simple home page
    """

    @app.route("/")
    def home():
        return render_template("index.html")

    """
        Returns a simple health-check endpoint
    """

    @app.route("/userHealth")
    def health():
        result = {"result": "User APIs working"}
        return jsonify(result)

    """
        API to create new individual user on personal database
        Requires:
            username : User's unique identifier
            password : User's password
            mobile_num : User's mobile number
            name : User's name
            email : User's email
    """

    @app.route("/createUser", methods=["POST"])
    def createUser():

        username = request.args.get("username")
        password = request.args.get("pwd")
        mobile_num = request.args.get("mobile_num")
        name = request.args.get("name")
        email = request.args.get("email")

        SQL_STATEMENT = """INSERT INTO Users(username, pwd, mobile_num, name, email)
        VALUES (%(username)s, %(password)s, %(mobile_num)s, %(name)s, %(email)s)"""
        data = {
            "username": username,
            "password": password,
            "mobile_num": mobile_num,
            "name": name,
            "email": email,
        }

        resultSet = executeWriteQuery(SQL_STATEMENT, data)

        result = {"outcome": resultSet}

        return jsonify(result)

    """
        API to delete User

        Requires: 
            username : User's unique identifier
            password : User's password
    """

    @app.route("/deleteUser", methods=["POST"])
    def deleteUser():

        username = request.args.get("username")
        password = request.args.get("pwd")

        SQL_STATEMENT = """DELETE FROM Users WHERE username=%s AND pwd=%s"""
        data = [username, password]

        resultSet = executeWriteQuery(SQL_STATEMENT, data)

        result = {"outcome": resultSet}

        return jsonify(result)

    """
        API to update users on database
        Requires:
            username : User's unique identifier
            password : User's password
            update_cols : Fields to be updated
            update_vals : Values to be updated in the chosen fields
    """

    @app.route("/updateUser", methods=["POST"])
    def updateUser():
        username = request.args.get("username").split(",")
        password = request.args.get("password").split(",")
        update_columns = request.args.get("update_cols").split(",")
        update_vals = request.args.get("update_vals").split(",")
        update_set = []

        for column, val in zip(update_columns, update_vals):
            update_set.append(f"{column}={val}")

        SQL_STATEMENT = (
            f"""UPDATE Users SET {*update_set,} WHERE username=%s AND pwd=%s"""
        )
        data = [username, password]

        resultSet = executeWriteQuery(SQL_STATEMENT, data)

        result = {"outcome": resultSet}

        return jsonify(result)

    """
        API to authenticate user
        Requires:
            username : User's unique identifier
            password : User's password
    """

    @app.route("/authUser", methods=["GET"])
    def authUser():
        username = request.args.get("username")
        password = request.args.get("password")

        SQL_STATEMENT = """SELECT * FROM Users WHERE username=%s"""
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
                "username": db_username,
                "user_id": db_userid,
                "pwd": db_pwd,
                "email": db_email,
                "mobile_num": db_mobile_num,
                "name": db_name,
            }

            return jsonify(result)

        else:

            result = {"outcome": "Failure"}

            return jsonify(result)

    """
        API to fetch current daily lunch items
        Has no parameters
    """

    @app.route("/getDailyLunchItems", methods=["GET"])
    def getDailyLunchItems():

        SQL_STATEMENT = (
            """SELECT * FROM Items WHERE item_id IN (22, 103, 166, 188, 77)"""
        )
        data = []

        resultSet = executeReadQuery(SQL_STATEMENT, data)

        result = {"items": resultSet}

        return jsonify(result)

    """
        API to get all food and beverage options present and available on database
        Has no parameters
    """

    @app.route("/getAllItems", methods=["GET"])
    def getAllItems():

        SQL_STATEMENT = """SELECT * FROM Items"""
        data = []

        resultSet = executeReadQuery(SQL_STATEMENT, data)

        result = {"items": resultSet}

        return jsonify(result)

    """
        API to get all most popular items present and available on database as per order frequency
        Has no parameters
    """

    @app.route("/getPopularItems", methods=["GET"])
    def getPopularItems():

        SQL_STATEMENT = """SELECT * FROM Items WHERE item_id IN
        (SELECT * FROM
        (SELECT item_id FROM order_item GROUP BY item_id ORDER BY COUNT(*) DESC LIMIT 1) temp_tab)"""
        data = []

        resultSet = executeReadQuery(SQL_STATEMENT, data)

        result = {"items": resultSet}

        return jsonify(result)

    """
        API to get Meal of the Day options
        Has no parameters
    """

    @app.route("/getMealOfDay", methods=["GET"])
    def getMealOfDay():

        SQL_STATEMENT = """SELECT * FROM Items WHERE item_id IN (2, 7, 235, 202) ORDER BY RAND() LIMIT 1"""
        data = []

        resultSet = executeReadQuery(SQL_STATEMENT, data)

        result = {"items": resultSet}

        return jsonify(result)

    """
        API to create an order on the database and store the information onto database
        Requires:
            payment_id : Unique payment ID generated by payment gateway
            paid_status : Payment status according to payment gateway
            total_price : Grand total price to pay
    """

    @app.route("/createOrder", methods=["POST"])
    def createOrder():
        items = list(map(int, request.args.get("items").split(",")))
        payment_id = request.args.get("payment_id")
        paid_status = request.args.get("paid_status")
        total_price = request.args.get("total_price")

        SQL_1 = """INSERT INTO Orders(total_price, payment_id, paid) VALUES (%(total_price)s, %(payment_id)s, %(paid)s)"""
        sql1_data = {
            "total_price": total_price,
            "payment_id": payment_id,
            "paid": paid_status,
        }

        resultSet1 = executeWriteQuery(SQL_1, sql1_data)

        order_id = resultSet1

        item_set = [(order_id, int(i)) for i in items]
        item_set = f"{*item_set,}"
        item_set = item_set[1 : len(item_set) - 1]

        SQL_2 = f"""INSERT INTO order_item(order_id, item_id) VALUES {item_set}"""
        resultSet2 = executeWriteQuery(SQL_2)

        result = {
            "outcome": "Success" if isinstance(resultSet2, int) else "Failure",
            "order_id": resultSet2 if isinstance(resultSet2, int) else 0,
        }

        return jsonify(result)

    """
        API to generate an order ID for Razorpay Payment gateway integration
        Requires:
            total_price : Final price to be charged
    """

    @app.route("/generateOrderId", methods=["GET"])
    def generateOrderId():
        total_price = request.args.get("total_price")
        key_id = "<INSERT_RAZORPAY_KEY_ID_HERE>"
        key_secret = "<INSERT_RAZORPAY_KEY_SECRET_HERE>"
        client = razorpay.Client(auth=(key_id, key_secret))
        DATA = {"amount": total_price, "currency": "INR", "receipt": "random_receipt"}
        order = client.order.create(DATA)
        order_id = order["id"]
        result = {"order_id": order_id}
        return jsonify(result)

    """
        API to delete an order from the database
    """

    @app.route("/deleteOrder", methods=["POST"])
    def deleteOrder():
        order_id = request.args.get("order_id")

        SQL_1 = """DELETE FROM order_item WHERE order_id=%s"""
        data = [order_id]

        resultSet1 = executeWriteQuery(SQL_1, data)

        SQL_2 = """DELETE FROM Orders WHERE order_id=%s"""
        data = [order_id]

        resultSet2 = executeWriteQuery(SQL_2, data)
        result = {"outcome": "Success" if isinstance(resultSet2, int) else "Failure"}

        return jsonify(result)

    # if __name__=='__main__':
    # app.run()
    return app
