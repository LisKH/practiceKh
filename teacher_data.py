from teacher import Teacher

database_study_var = Teacher()


def add_command(name, surname, middlename, course_id, lesson_id):
    database_study_var.insert(name, surname, middlename, course_id, lesson_id)


def view_command():
    for row in database_study_var.view():
        print(row)


for i in range(20):
    add_command(input("Введите имя: "),
                input("Введите фамилию: "),
                input("Введите отчество: "),
                input("Введите id курса: "),
                input("Введите id урока: "))


view_command()