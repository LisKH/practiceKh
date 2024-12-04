import sqlite3
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, messagebox


class LoginWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.conn = sqlite3.connect('study_var.db')
        self.cursor = self.conn.cursor()

        self.login_var = StringVar()
        self.password_var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        header_label = Label(self, text="Вход в систему")
        header_label.grid(row=0, columnspan=2, pady=(20, 10))

        login_label = Label(self, text="Логин:")
        login_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        login_entry = Entry(self, textvariable=self.login_var)
        login_entry.grid(row=1, column=1, padx=10, pady=5)

        password_label = Label(self, text="Пароль:")
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        password_entry = Entry(self, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        login_button = Button(self, text="Войти", command=self.validate_login)
        login_button.grid(row=3, columnspan=2, pady=15)

    def validate_login(self):
        username = self.login_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните оба поля.")
            return

        query = """SELECT * FROM users WHERE login = ? AND password = ?"""
        result = self.cursor.execute(query, (username, password)).fetchone()

        if result is None:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")
        else:
            messagebox.showinfo("Успех", f"Здравствуйте, {result[2]} {result[1]}! Вы успешно вошли.")

            self.master.destroy()
            MainWindow(result).run()


class MainWindow(Tk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.title(f"{user_data[2]} {user_data[1]} - Главная страница")

        welcome_label = Label(self, text=f"Здравствуйте, {user_data[2]} {user_data[1]}!")
        welcome_label.pack(padx=50, pady=30)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = LoginWindow(master=root)
    app.mainloop()