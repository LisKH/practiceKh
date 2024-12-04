from lesson import Lesson

database_study_var = Lesson()


def add_command(lesson_name, course_id):
    database_study_var.insert(lesson_name, course_id)


def view_command():
    for row in database_study_var.view():
        print(row)


for i in range(20):
    add_command(input("Введите название урока(лекции): "),
                input("Введите id курса: "))


view_command()