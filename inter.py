import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Предположим, что вы уже создали соединение с базой данных
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

def register_user():
    """Функция для регистрации нового пользователя."""

    def save_user():
        """Внутренняя функция для сохранения введенных данных."""

        name = entry_reg_name.get().strip()
        surname = entry_reg_surname.get().strip()
        login = entry_reg_login.get().strip()
        password = entry_reg_password.get().strip()
        confirm_password = entry_reg_confirm_password.get().strip()
        role = role_var.get()

        if not name or not surname or not login or not password or not confirm_password:
            messagebox.showerror(title='Ошибка', message='Пожалуйста, заполните все поля.')
            return

        if password != confirm_password:
            messagebox.showerror(title='Ошибка', message='Пароли не совпадают.')
            return

        try:
            cursor.execute("INSERT INTO users (name, surname, login, password, role) VALUES (?, ?, ?, ?, ?)",
                           (name, surname, login, password, role))
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
    label_reg_role = ttk.Label(reg_window, text='Роль:')

    entry_reg_name = ttk.Entry(reg_window)
    entry_reg_surname = ttk.Entry(reg_window)
    entry_reg_login = ttk.Entry(reg_window)
    entry_reg_password = ttk.Entry(reg_window, show='*')
    entry_reg_confirm_password = ttk.Entry(reg_window, show='*')

    # Добавление выпадающего списка для выбора роли
    role_var = tk.StringVar(value="student")  # Значение по умолчанию
    role_options = ttk.Combobox(reg_window, textvariable=role_var)
    role_options['values'] = ('teacher', 'student')
    role_options.grid(row=5, column=1, padx=10, pady=5)

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

    label_reg_role.grid(row=5, column=0, padx=10, pady=5, sticky='w')

    role_options.grid(row=5, column=1)

    button_save.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


def login():
    """Функция для проверки логина и пароля"""
    login_input = entry_login.get()
    password_input = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE login=? AND password=?", (login_input, password_input))
    user = cursor.fetchone()

    if user is not None:
        root.destroy()
        main_window(user)  # Передаем данные пользователя в основное окно
        # Здесь можно добавить логику для обработки ролей
        role = user[-1]  # Предполагаем что роль - это последний элемент в выборке
        if role == 'teacher':
            print("Добро пожаловать учитель!")
        else:
            print("Добро пожаловать студент!")
    else:
        label_error.config(text="Неверный логин или пароль")
