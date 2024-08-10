import mysql.connector
import pandas as pd

conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "hanuman",
        database = "employees"
    )
    cursor = conn.cursor()
    query1 = "select * from employees"
    cursor.execute(query1)

    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    df = pd.DataFrame(data, columns = column_names)

except mysql.connector.Error as e:
    print(e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()

print(df)

