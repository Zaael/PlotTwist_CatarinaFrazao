import mysql.connector


def db_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='ope_impacta',
                                         user='root',
                                         password='12345',
                                         auth_plugin='mysql_native_password')
    return connection
