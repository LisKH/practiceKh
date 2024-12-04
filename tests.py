import sqlite3


class Test:


    def __init__(self):
        self.con = sqlite3.connect("study_var.db")
        self.cur = self.con.cursor()
        self.cur.execute(
        "CREATE TABLE IF NOT EXISTS test "
        "(test_id INTEGER PRIMARY KEY,"
        "mark TEXT,"
        "importance INT )"
    )

        self.con.commit()

    def __del__(self):

        self.con.close()

    def view(self):

        self.cur.execute("SELECT * FROM test")
        rows = self.cur.fetchall()
        return rows

    def insert(self, mark, importance):

        self.cur.execute("INSERT INTO test "
                     "VALUES (NULL, ?, ?)",
                     (mark, importance,))
        self.con.commit()

    def update(self, mark, importance, test_id):

        self.cur.execute("UPDATE test SET "
                     "mark=?, importance=? "
                     "WHERE test_id = ?",
                     (mark, importance, test_id))
        self.con.commit()

    def delete(self, test_id):

        self.cur.execute("DELETE FROM test "
                     "WHERE test_id=?", (test_id,))
        self.con.commit()

    def search(self, mark):

        self.cur.execute("SELECT importance FROM test "
                         "WHERE mark=?", (mark,))
        rows = self.cur.fetchall()
        return rows