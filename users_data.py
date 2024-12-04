from users import Users

database_study_var = Users()


def add_command(name, surname, login, course_id, password):
    database_study_var.insert(name, surname, login, course_id, password)


def view_command():
    for row in database_study_var.view():
        print(row)


for i in range(20):
    add_command(input("Введите имя: "),
                input("Введите фамилию: "),
                input("Введите логин: "),
                input("Введите id курса: "),
                input("Введите пароль: "))


view_command()