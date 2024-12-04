from courses import Course

database_study_var = Course()


def add_command(course_name, hours, teacher_id, user_id, test_id):
    database_study_var.insert(course_name, hours, teacher_id, user_id, test_id)


def view_command():
    for row in database_study_var.view():
        print(row)


for i in range(20):
    add_command(input("Введите название курса: "),
                input("Введите количество часов: "),
                input("Введите id учителя: "),
                input("Введите id пользователя(ученика): "),
                input("Введите id теста: "))


view_command()
