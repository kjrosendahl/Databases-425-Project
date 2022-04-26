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

"; drop tables"

sql = """SELECT *
        FROM course
        WHERE credits = 4"""

sql = """insert into departments (department_id, department_name)
          values (:dept_id, :dept_name)"""
cursor.execute(sql, [280, "Facility"])

cursor.execute(sql)

for row in cursor:
    print(row)

connection.close()