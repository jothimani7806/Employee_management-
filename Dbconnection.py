import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "dbms",        # ← Your MySQL password
    "database": "employee_db"
}

def get_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        raise Exception(f"Database connection failed: {e}")

def initialize_database():
    """Create the database and Employee table if they don't exist."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dbms"    # ← Your MySQL password
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
        cursor.execute("USE employee_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employee (
                Empno          INT PRIMARY KEY AUTO_INCREMENT,
                Empname        VARCHAR(100) NOT NULL,
                Empdesignation VARCHAR(100) NOT NULL,
                Empdepartment  VARCHAR(100) NOT NULL,
                Salary         DECIMAL(10, 2) NOT NULL,
                Phone          VARCHAR(15) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Database initialized successfully."
    except Error as e:
        return False, f"Initialization error: {e}"