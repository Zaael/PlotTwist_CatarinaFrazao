import mysql.connector

try:
    connection = mysql.connector.connect(
    host='localhost',
    database='ope-impacta',
    user='root',
    password='1234',
    auth_plugin='mysql_native_password')
    if connection.is_connected():
        print("MySQL is connected")

except mysql.connector.Error as error:
    print("Error in MySQL: {}".format(error))
    
finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")