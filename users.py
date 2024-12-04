import sqlite3


class Users:


    def __init__(self):
        self.con = sqlite3.connect("study_var.db")
        self.cur = self.con.cursor()
        self.cur.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(user_id INTEGER PRIMARY KEY,"
        "name TEXT,"
        "surname TEXT, "
        "login TEXT,"
        "course_id INT,"
        "password TEXT )"
    )

        self.con.commit()

    def __del__(self):

        self.con.close()

    def view(self):

        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, surname, login, course_id, password):

        self.cur.execute("INSERT INTO users "
                     "VALUES (NULL, ?, ?, ?, ?, ?)",
                     (name, surname, login, course_id, password,))
        self.con.commit()

    def update(self, user_id, name, surname, login, course_id, password):

        self.cur.execute("UPDATE users SET "
                     "name=?, surname=?, login=?, course_id=?, password=? "
                     "WHERE user_id = ?",
                     (name, surname, login, course_id, password, user_id))
        self.con.commit()

    def delete(self, user_id):

        self.cur.execute("DELETE FROM users "
                     "WHERE user_id=?", (user_id,))
        self.con.commit()

    def search(self, name):

        self.cur.execute("SELECT surname, login, course_id, password FROM users "
                         "WHERE name=?", (name,))
        rows = self.cur.fetchall()
        return rows