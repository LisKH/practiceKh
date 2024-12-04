import sqlite3


class Teacher:


    def __init__(self):
        self.con = sqlite3.connect("study_var.db")
        self.cur = self.con.cursor()
        self.cur.execute(
        "CREATE TABLE IF NOT EXISTS teacher "
        "(teacher_id INTEGER PRIMARY KEY,"
        "name TEXT,"
        "surname TEXT, "
        "middlename TEXT,"
        "course_id INT,"
        "lesson_id INT )"
    )

        self.con.commit()

    def __del__(self):

        self.con.close()

    def view(self):

        self.cur.execute("SELECT * FROM teacher")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, surname, middlename, course_id, lesson_id):

        self.cur.execute("INSERT INTO teacher "
                     "VALUES (NULL, ?, ?, ?, ?, ?)",
                     (name, surname, middlename, course_id, lesson_id,))
        self.con.commit()

    def update(self, teacher_id, name, surname, middlename, course_id, lesson_id):

        self.cur.execute("UPDATE teacher SET "
                     "name=?, surname=?, middlename=?, course_id=?, lesson_id=? "
                     "WHERE teacher_id = ?",
                     (name, surname, middlename, course_id, lesson_id, teacher_id))
        self.con.commit()

    def delete(self, teacher_id):

        self.cur.execute("DELETE FROM teacher "
                     "WHERE teacher_id=?", (teacher_id,))
        self.con.commit()

    def search(self, name):

        self.cur.execute("SELECT surname, middlename, course_id FROM teacher "
                         "WHERE name=?", (name,))
        rows = self.cur.fetchall()
        return rows