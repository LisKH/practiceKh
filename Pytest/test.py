import sqlite3
import pytest
from your_module import is_user_in_db

@pytest.fixture
def setup_temp_db(tmp_path):
    db_path = tmp_path / "test_study_var.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            login TEXT,
            course_id INT,
            password TEXT
        )
    """)
    cursor.executemany("""
        INSERT INTO users (user_id, name, surname, login, course_id, password)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, 'Сергей', 'Иванов', 'Morolena', 101, 'aS2vVf'),
        (2, 'Анна', 'Смирнова', 'Lley', 102, 'OA6yHe'),
        (3, 'Дмитрий', 'Кузнецов', 'Onaeve', 103, '9mZXNo'),
    ])
    connection.commit()
    connection.close()
    return db_path

@pytest.mark.parametrize("login, password, expected", [
    ("Morolena", "aS2vVf", True),
    ("Lley", "OA6yHe", True),
    ("Onaeve", "9mZXNo", True),
    ("Morolena", "wrongpass", False),
    ("unknown", "aS2vVf", False),
])
def test_is_user_in_db(login, password, expected, setup_temp_db):
    db_path = setup_temp_db
    assert is_user_in_db(login, password, db_path) == expected