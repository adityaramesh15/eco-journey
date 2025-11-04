import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_port = int(os.getenv("DB_PORT", 3306))

try:
    # Pass the variables to the connect function
    db_connection = MySQLdb.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        db=db_name,
        port=db_port
    )

    db_connection.cursor()


except MySQLdb.Error as e:
    print(f"Eror connectingf to DB {e}")