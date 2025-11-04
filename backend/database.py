# database.py
import MySQLdb
import MySQLdb.cursors
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.db_port = int(os.getenv("DB_PORT", 3306))

    def _get_connection(self):
        """
        Creates and returns a new database connection.
        Using DictCursor to get results as dictionaries.
        """
        try:
            return MySQLdb.connect(
                host=self.db_host,
                user=self.db_user,
                passwd=self.db_pass,
                db=self.db_name,
                port=self.db_port,
                cursorclass=MySQLdb.cursors.DictCursor 
            )
        except MySQLdb.Error as e:
            print(f"Error connecting to DB: {e}")
            raise

    def execute(self, query, params=None, fetchall=False, fetchone=False, commit=False):
        """
        Executes a query safely with parameters.
        
        :param query: The SQL query string with %s placeholders.
        :param params: A tuple or list of parameters to substitute into the query.
        :param fetchall: True to fetch all results for a SELECT.
        :param fetchone: True to fetch one result for a SELECT.
        :param commit: True to commit changes for INSERT, UPDATE, DELETE.
        :return: Query results or row count.
        """
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            

            cursor.execute(query, params)
            
            if commit:
                conn.commit()
                return cursor.rowcount  
            
            if fetchone:
                return cursor.fetchone()
                
            if fetchall:
                return cursor.fetchall()

            return None 
            
        except MySQLdb.Error as e:
            print(f"Database query error: {e}")
            if conn:
                conn.rollback()  
            raise 
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

db = Database()