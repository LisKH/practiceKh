import sqlite3


def is_user_in_db(login, password, db_path="sqlite:///D:\\practice Kh\\study_var.db"):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE login = ? AND password = ?"
    cursor.execute(query, (login, password))
    result = cursor.fetchone()
    connection.close()
    return result[0] > 0