import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

conn = sqlite3.connect('study_var.db')
cursor = conn.cursor()


def register_user():

    def save_user():

        name = entry_reg_name.get().strip()
        surname = entry_reg_surname.get().strip()
        login = entry_reg_login.get().strip()
        password = entry_reg_password.get().strip()
        confirm_password = entry_reg_confirm_password.get().strip()

        if not name or not surname or not login or not password or not confirm_password:
            messagebox.showerror(title='Ошибка', message='Пожалуйста, заполните все поля.')
            return

        if password != confirm_password:
            messagebox.showerror(title='Ошибка', message='Пароли не совпадают.')
            return

        try:
            cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (?, ?, ?, ?)",
                           (name, surname, login, password))
            conn.commit()
            messagebox.showinfo(title='Успех', message=f'Пользователь {name} {surname} успешно зарегистрирован!')
            reg_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror(title='Ошибка', message='Имя пользователя уже занято. Пожалуйста, выберите другое.')

    reg_window = tk.Toplevel(root)
    reg_window.title('Регистрация')

    label_reg_name = ttk.Label(reg_window, text='Имя:')
    label_reg_surname = ttk.Label(reg_window, text='Фамилия:')
    label_reg_login = ttk.Label(reg_window, text='Логин:')
    label_reg_password = ttk.Label(reg_window, text='Пароль:')
    label_reg_confirm_password = ttk.Label(reg_window, text='Подтвердите пароль:')

    entry_reg_name = ttk.Entry(reg_window)
    entry_reg_surname = ttk.Entry(reg_window)
    entry_reg_login = ttk.Entry(reg_window)
    entry_reg_password = ttk.Entry(reg_window, show='*')
    entry_reg_confirm_password = ttk.Entry(reg_window, show='*')

    button_save = ttk.Button(reg_window, text='Зарегистрироваться', command=save_user)

    label_reg_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')
    entry_reg_name.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

    label_reg_surname.grid(row=1, column=0, padx=10, pady=5, sticky='w')
    entry_reg_surname.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

    label_reg_login.grid(row=2, column=0, padx=10, pady=5, sticky='w')
    entry_reg_login.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

    label_reg_password.grid(row=3, column=0, padx=10, pady=5, sticky='w')
    entry_reg_password.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

    label_reg_confirm_password.grid(row=4, column=0, padx=10, pady=5, sticky='w')
    entry_reg_confirm_password.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

    button_save.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


def login():
    login = entry_login.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    user = cursor.fetchone()

    if user is not None:
        root.destroy()
        main_window(user)
    else:
        label_error.config(text="Неверный логин или пароль")


def main_window(user):

    def view_courses():
        cursor.execute("SELECT course_id, course_name FROM courses")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=(row[0], row[1]))

    def enroll_in_course(course_id):
        cursor.execute("UPDATE users SET course_id = ? WHERE user_id = ?", (course_id, user[0]))
        conn.commit()
        messagebox.showinfo("Успех", f"Вы успешно записались на курс {course_id}")

    def select_item(event):
        try:
            item = tree.selection()[0]
            global selected_course_id
            selected_course_id = tree.item(item)["values"][0]
            button_enroll.config(state='normal')
        except IndexError:
            pass

    def view_teachers():
        teachers_window = tk.Toplevel(main_window_frame)
        teachers_window.title("Преподаватели")

        frame_treeview_teachers = ttk.Frame(teachers_window)
        frame_treeview_teachers.pack(pady=20)

        tree_teachers = ttk.Treeview(frame_treeview_teachers, columns=("ФИО", "Курс"))
        tree_teachers.heading("#0", text="ФИО")
        tree_teachers.heading("#1", text="Курс")
        tree_teachers.column("#0", width=150)
        tree_teachers.column("#1", width=200)
        tree_teachers.pack()

        cursor.execute("SELECT name, surname, middlename, course_id FROM teacher")
        rows = cursor.fetchall()

        for row in rows:
            full_name = f"{row[1]} {row[0]} {row[2]}"
            cursor.execute("SELECT course_name FROM courses WHERE course_id = ?", (row[3],))
            course_name = cursor.fetchone()[0]
            tree_teachers.insert("", "end", values=(full_name, course_name))

        button_back = ttk.Button(teachers_window, text="Назад", command=teachers_window.destroy)
        button_back.pack(pady=10)
        teachers_window.config(background="#93a9e6")

    def view_lectures():
        lectures_window = tk.Toplevel(main_window_frame)
        lectures_window.title("Лекции")

        frame_treeview_lectures = ttk.Frame(lectures_window)
        frame_treeview_lectures.pack(pady=20)

        tree_lectures = ttk.Treeview(frame_treeview_lectures, columns=("Название лекции", "Курс"))
        tree_lectures.heading("#0", text="Название лекции")
        tree_lectures.heading("#1", text="Курс")
        tree_lectures.column("#0", width=150)
        tree_lectures.column("#1", width=200)
        tree_lectures.pack()

        cursor.execute("SELECT lesson_name, course_id FROM lesson")
        rows = cursor.fetchall()

        for row in rows:
            cursor.execute("SELECT course_name FROM courses WHERE course_id = ?", (row[1],))
            course_name = cursor.fetchone()[0]
            tree_lectures.insert("", "end", values=(row[0], course_name))

        button_back = ttk.Button(lectures_window, text="Назад", command=lectures_window.destroy)
        button_back.pack(pady=10)
        lectures_window.config(background="#9393e6")

    def open_profile():
        profile_window = tk.Toplevel(main_window_frame)
        profile_window.title("Личный кабинет")

        frame_input = ttk.Frame(profile_window)
        frame_input.pack(padx=30, pady=15)

        image = Image.open('images//profile.png')
        image = image.resize((150, 150), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(profile_window, image=image)
        image_label.image = image
        image_label.pack()

        frame_input = ttk.Frame(profile_window)
        frame_input.pack(pady=20)

        label_name = ttk.Label(frame_input, text="Имя:")
        label_surname = ttk.Label(frame_input, text="Фамилия:")
        label_login = ttk.Label(frame_input, text="Логин:")
        label_password = ttk.Label(frame_input, text="Пароль:")

        entry_name = ttk.Entry(frame_input, width=25)
        entry_surname = ttk.Entry(frame_input, width=25)
        entry_login = ttk.Entry(frame_input, width=25)
        entry_password = ttk.Entry(frame_input, width=25, show="*")

        entry_name.insert(0, user[1])
        entry_surname.insert(0, user[2])
        entry_login.insert(0, user[3])
        entry_password.insert(0, user[5])

        label_name.grid(row=0, column=0, padx=5, pady=5)
        label_surname.grid(row=1, column=0, padx=5, pady=5)
        label_login.grid(row=2, column=0, padx=5, pady=5)
        label_password.grid(row=3, column=0, padx=5, pady=5)

        entry_name.grid(row=0, column=1, padx=5, pady=5)
        entry_surname.grid(row=1, column=1, padx=5, pady=5)
        entry_login.grid(row=2, column=1, padx=5, pady=5)
        entry_password.grid(row=3, column=1, padx=5, pady=5)

        button_save_changes = ttk.Button(
            frame_input,
            text="Сохранить изменения",
            command=lambda: save_changes(
                entry_name.get(),
                entry_surname.get(),
                entry_login.get(),
                entry_password.get()
            )
        )
        button_save_changes.grid(row=4, columnspan=2, pady=10)

        frame_courses = ttk.Frame(profile_window)
        frame_courses.pack(pady=20)

        label_courses_title = ttk.Label(frame_courses, text="Ваши курсы:", font=("Arial", 12, "bold"))
        label_courses_title.grid(row=0, column=0, pady=10, sticky="w")

        cursor.execute("""
            SELECT course_id 
            FROM users 
            WHERE user_id = ?
        """, (user[0],))

        course_id = cursor.fetchone()[0]

        if course_id:
            cursor.execute("""
                SELECT course_name 
                FROM courses 
                WHERE course_id = ?
            """, (course_id,))

            course = cursor.fetchone()
            if course:
                course_label = ttk.Label(frame_courses, text=f"1. {course[0]}")
                course_label.grid(row=1, column=0, pady=5, sticky="w")
            else:
                no_courses_label = ttk.Label(frame_courses, text="Курс с указанным ID не найден.")
                no_courses_label.grid(row=1, column=0, pady=5, sticky="w")
        else:
            no_courses_label = ttk.Label(frame_courses, text="Вы не записаны на курсы.")
            no_courses_label.grid(row=1, column=0, pady=5, sticky="w")

        profile_window.config(background="#93a9e6")

        def save_changes(name, surname, login, password):
            cursor.execute("""
                UPDATE users 
                SET name=?, surname=?, login=?, password=? 
                WHERE user_id=?
            """, (name, surname, login, password, user[0]))

            conn.commit()
            messagebox.showinfo("Успешно!", "Изменения сохранены.")
            profile_window.destroy()

    main_window_frame = tk.Tk()
    main_window_frame.title(f"Привет, {user[1]}!")

    frame_treeview = ttk.Frame(main_window_frame)
    frame_treeview.pack(pady=20)

    tree = ttk.Treeview(frame_treeview, columns=("ID курса", "Название курса"))
    tree.heading("#0", text="ID курса")
    tree.heading("#1", text="Название курса")
    tree.column("#0", width=100)
    tree.column("#1", width=300)
    tree.bind("<<TreeviewSelect>>", select_item)
    tree.pack()

    button_view_all = ttk.Button(frame_treeview, text="Просмотреть курсы", command=view_courses)
    button_view_all.pack(pady=10)

    button_enroll = ttk.Button(frame_treeview, text="Записаться на курс",
                               command=lambda: enroll_in_course(selected_course_id), state='disabled')
    button_enroll.pack(pady=10)

    button_view_teachers = ttk.Button(main_window_frame, text="Посмотреть преподавателей", command=view_teachers)
    button_view_teachers.pack(pady=10)

    button_view_lectures = ttk.Button(main_window_frame, text="Посмотреть лекции", command=view_lectures)
    button_view_lectures.pack(pady=10)

    button_open_profile = ttk.Button(main_window_frame, text="Открыть профиль", command=open_profile)
    button_open_profile.pack(pady=10)

    main_window_frame.config(background="#93a9e6")


root = tk.Tk()
root.title('Авторизация')

label_login = ttk.Label(root, text='Логин:')
label_password = ttk.Label(root, text='Пароль:')
entry_login = ttk.Entry(root)
entry_password = ttk.Entry(root, show='*')
button_login = ttk.Button(root, text='Войти', command=login)
button_register = ttk.Button(root, text='Зарегистрироваться', command=register_user)
label_error = ttk.Label(root, foreground='red')

label_login.pack(padx=10, pady=5)
entry_login.pack(fill='x', padx=20)
label_password.pack(padx=10, pady=5)
entry_password.pack(fill='x', padx=20)
button_login.pack(pady=10)
button_register.pack(pady=5)
label_error.pack()

root.mainloop()