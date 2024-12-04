import sqlite3


class Course:


    def __init__(self):
        self.con = sqlite3.connect("study_var.db")
        self.cur = self.con.cursor()
        self.cur.execute(
        "CREATE TABLE IF NOT EXISTS courses "
        "(course_id INTEGER PRIMARY KEY,"
        "course_name TEXT,"
        "hours INT, "
        "teacher_id INT,"
        "user_id INT,"
        "test_id INT )"
    )

        self.con.commit()

    def __del__(self):

        self.con.close()

    def view(self):

        self.cur.execute("SELECT * FROM courses")
        rows = self.cur.fetchall()
        return rows

    def insert(self, course_name, hours, teacher_id, user_id, test_id):

        self.cur.execute("INSERT INTO courses "
                     "VALUES (NULL, ?, ?, ?, ?, ?)",
                     (course_name, hours, teacher_id, user_id, test_id,))
        self.con.commit()

    def update(self, course_id, course_name, hours, teacher_id, user_id, test_id):

        self.cur.execute("UPDATE courses SET "
                     "course_name=?, hours=?, teacher_id=?, user_id=?, test_id=? "
                     "WHERE course_id = ?",
                     (course_name, hours,
                      teacher_id, user_id, test_id, course_id))
        self.con.commit()

    def delete(self, course_id):

        self.cur.execute("DELETE FROM courses "
                     "WHERE course_id=?", (course_id,))
        self.con.commit()

    def search(self, course_name):

        self.cur.execute("SELECT hours, teacher_id, number FROM courses "
                         "WHERE course_name=?", (course_name,))
        rows = self.cur.fetchall()
        return rows