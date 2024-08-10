import mysql.connector

try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "hanuman",
        database = "employees"
    )
    cur = conn.cursor()
    cur.execute("select * from employees;")
    for row in cur.fetchall():
        print(row)
except mysql.connector.Error as e:
    print(e)