import mariadb

def obtenirConnexion():
    try:
        conn = mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
                database="tp1_web")
        return conn
    except mariadb.Error as e:
        print(e)