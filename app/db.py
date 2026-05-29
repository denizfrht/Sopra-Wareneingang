import os
import pyodbc
from dotenv import load_dotenv


# Lädt die Werte aus der .env-Datei
load_dotenv()


def get_db_connection():
    """
    Erstellt eine Verbindung zum SQL Server.
    Die Zugangsdaten kommen aus der .env-Datei.
    """

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
        "Encrypt=yes;"
    )

    return pyodbc.connect(connection_string)


def rows_to_dicts(cursor, rows):
    """
    Wandelt SQL-Ergebnisse in Dictionaries um.
    """

    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def fetch_all(query, params=None):
    """
    Führt eine SELECT-Abfrage aus und gibt alle Zeilen zurück.
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        return rows_to_dicts(cursor, rows)

    finally:
        cursor.close()
        connection.close()


def fetch_one(query, params=None):
    """
    Führt eine SELECT-Abfrage aus und gibt eine Zeile zurück.
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params or [])
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    finally:
        cursor.close()
        connection.close()


def execute_query(query, params=None):
    """
    Führt INSERT, UPDATE oder DELETE aus.
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params or [])
        connection.commit()
        return True

    finally:
        cursor.close()
        connection.close()