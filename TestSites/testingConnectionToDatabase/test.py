# python -m pip install cx_Oracle
# Documentation Link: https://cx-oracle.readthedocs.io/en/latest/user_guide/
import cx_Oracle

connection = cx_Oracle.connect(
    user="noah",
    password="noah",
    dsn="localhost/xepdb1"
)

print("connected")

cursor = connection.cursor()

manager_id = 145
sql = """SELECT *
        FROM course
        WHERE credits = 4"""
cursor.execute(sql)

for row in cursor:
    print(row)

connection.close()