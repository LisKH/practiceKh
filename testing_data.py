from tests import Test

database_study_var = Test()


def add_command(mark, importance):
    database_study_var.insert(mark, importance)


def view_command():
    for row in database_study_var.view():
        print(row)


for i in range(20):
    add_command(input("Введите оценку: "),
                input("Введите важность теста: "))


view_command()