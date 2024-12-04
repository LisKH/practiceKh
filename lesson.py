import sqlite3


class Lesson:


    def __init__(self):
        self.con = sqlite3.connect("study_var.db")
        self.cur = self.con.cursor()
        self.cur.execute(
        "CREATE TABLE IF NOT EXISTS lesson "
        "(lesson_id INTEGER PRIMARY KEY,"
        "lesson_name TEXT,"
        "course_id INT )"
    )

        self.con.commit()

    def __del__(self):

        self.con.close()

    def view(self):

        self.cur.execute("SELECT * FROM lesson")
        rows = self.cur.fetchall()
        return rows

    def insert(self, lesson_name, course_id):

        self.cur.execute("INSERT INTO lesson "
                     "VALUES (NULL, ?, ?)",
                     (lesson_name, course_id,))
        self.con.commit()

    def update(self, lesson_name, course_id, lesson_id):

        self.cur.execute("UPDATE lesson SET "
                     "lesson_name=?, course_id=? "
                     "WHERE lesson_id = ?",
                     (lesson_name, course_id, lesson_id))
        self.con.commit()

    def delete(self, lesson_id):

        self.cur.execute("DELETE FROM lesson "
                     "WHERE lesson_id=?", (lesson_id,))
        self.con.commit()

    def search(self, lesson_name):

        self.cur.execute("SELECT course_id FROM lesson "
                         "WHERE lesson_name=?", (lesson_name,))
        rows = self.cur.fetchall()
        return rows