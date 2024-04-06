import mysql.connector
from decouple import config

mydb = mysql.connector.connect(
    host=config('DB_HOST'),
    user=config('DB_USER'),
    passwd=config('DB_PASSWORD')
    )

my_cursor = mydb.cursor()
try:
    my_cursor.execute(f"CREATE DATABASE {config('DB_NAME')}")
except Exception as e:
    print("Error creating database/n")
    print(e)

my_cursor.execute("SHOW DATABASES")
print("The existing databases are:")
for db in my_cursor:
    print(db)
