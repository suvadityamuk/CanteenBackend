# import MySQLdb
import mysql.connector
from env import mysqlConfig


def executeReadQuery(query, data=None):
    """
    Used for executing a Select or Reading query.
    Returns:
        - List object as a JSON result from the database
    Warning:
        - No middleware functions or work to be done here, this is only for returning
        data from the table. All other processes to be done in separate file
    """
    mydb_connection = mysql.connector.connect(
        host=mysqlConfig["MYSQL_ADDON_HOST"],
        user=mysqlConfig["MYSQL_ADDON_USER"],
        password=mysqlConfig["MYSQL_ADDON_PASSWORD"],
        database=mysqlConfig["MYSQL_ADDON_DB"],
        port=3306,
    )
    cursor = mydb_connection.cursor()
    cursor.execute(query, data)
    print("Query executed")
    result = [i for i in cursor]
    cursor.close()
    mydb_connection.close()
    return result


def executeWriteQuery(query, data=None):
    """
    Used for executing a query.
    Returns:
        - List object as a JSON result from the database
    Warning:
        - No middleware functions or work to be done here, this is only for returning
        data from the table. All other processes to be done in separate file
    """
    mydb_connection = mysql.connector.connect(
        host=mysqlConfig["MYSQL_ADDON_HOST"],
        user=mysqlConfig["MYSQL_ADDON_USER"],
        password=mysqlConfig["MYSQL_ADDON_PASSWORD"],
        database=mysqlConfig["MYSQL_ADDON_DB"],
        port=mysqlConfig["MYSQL_ADDON_PORT"],
    )
    cursor = mydb_connection.cursor()
    print("Cursor connection established")
    cursor.execute(query, data)
    mydb_connection.commit()
    print("Query executed")
    result = cursor.lastrowid
    cursor.close()
    mydb_connection.close()
    return result
