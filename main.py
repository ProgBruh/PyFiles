from tkinter import Tk, Frame, Scrollbar, Menu, Listbox, Label, Button, Toplevel,\
                                                    BOTH, messagebox, filedialog
from base64 import b64encode
from os import walk, path, makedirs

from modules import Connect, SignIn, SignUp, PasswordUpdate
import psycopg2
import config

class App(Frame):
    """
    Класс главного виджета(Frame), который включает все остальные виджеты
    """

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.menu = None
        self.account_menu = None
        self.connect_menu = None
        self.help_menu = None
        self.connect = None
        self.session = None
        self.connect_window = None
        self.sign_up_window = None
        self.sign_in_window = None
        self.update_password_window = None
        self.init_window()

    def init_window(self):
        """
        метод инициализации окна
        """

        self.root.title(config.TITLE)
        self.root.geometry('%dx%d+%d+%d'%(config.ROOT_WIDTH,
                                          config.ROOT_HEIGHT,
                                          round(self.root.winfo_screenwidth()/2 - config.ROOT_WIDTH/2, 1),
                                          round(self.root.winfo_screenheight()/2 - config.ROOT_HEIGHT/2, 1)))
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.close_root_process)
        self.init_menu()

    def init_menu(self):
        """
        метод инициализации меню
        """

        self.menu = Menu(self)
        self.account_menu = Menu(self.menu, tearoff=0)
        self.account_menu.add_command(label='Sign up', command=self.sign_up_open_window)
        self.account_menu.add_command(label='Sign in', command=self.sign_in_open_window)
        self.connect_menu = Menu(self.menu, tearoff=0)
        self.connect_menu.add_command(label='Create', command=self.connect_open_window)
        self.connect_menu.add_command(label='Close', command=self.close_connect)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label='About', command=lambda: messagebox.showinfo(config.TITLE, config.ABOUT))
        self.help_menu.add_command(label='How to use it', command=lambda: messagebox.showinfo(config.TITLE, config.HOW_TO_USE))
        self.menu.add_cascade(label='Account', menu=self.account_menu)
        self.menu.add_cascade(label='Connect', menu=self.connect_menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
        self.init_widgets()
        self.root['menu'] = self.menu

    def init_widgets(self):
        """
        метод инициализации виджетов
        """

        self.pack(fill=BOTH, expand=1)
        self.repositories = Listbox(self, highlightthickness=0, borderwidth=1)
        self.repositories.place(x=5, y=5, width=310, height=140)
        Button(self, text='download', font='Calibri 11', relief='groove', command=self.download_repository).place(x=5, y=150, width=100, height=35)
        Button(self, text='add', font='Calibri 11', relief='groove', command=self.add_repository).place(x=110, y=150, width=100, height=35)
        Button(self, text='delete', font='Calibri 11', relief='groove', command=self.delete_repository).place(x=215, y=150, width=100, height=35)

    def connect_open_window(self):
        """
        метод создания виджета для подключения к базе данных
        """

        if self.connect == None and self.connect_window == None:
            self.connect_window = Connect(Toplevel(), self.connect_process, self.remove_connect_window)
        elif self.connect != None and self.connect_window == None:
            v = messagebox.askyesno(title = 'PyFiles', message = 'Close current connection?')
            if v:
                self.connect.close()
                self.connect = None
                self.connect_window = Connect(Toplevel(), self.connect_process, self.remove_connect_window)

    def remove_connect_window(self):
        """
        метод удаления виджета подключения к базе данных из памяти
        """

        self.connect_window = None

    def close_connect(self):
        """
        метод разрыва подключения к базе данных
        """

        if self.connect:
            if self.session:
                self.logout()
            self.connect.close()
            self.connect = None
            messagebox.showinfo('PyFiles', 'Connection terminated successfully')
        else:
            messagebox.showerror('PyFiles', 'No active database connection')

    def connect_process(self, host, name, user, password):
        """
        метод создания подключения к базе данных
        """

        try:
            self.connect = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"%(host, name, user, password))
            return True
        except:
            return False

    def sign_up_open_window(self):
        """
        метод создания виджета регистрации пользователя
        """

        if self.connect:
            if not self.sign_up_window:
                self.sign_up_window = SignUp(Toplevel(), self.sign_up, self.remove_sign_up_window)
        else:
            messagebox.showerror('PyFiles', 'Need to connect to the database')

    def remove_sign_up_window(self):
        """
        метод удаления окна регистрации пользователя из памяти
        """

        self.sign_up_window = None

    def sign_up(self, email, password):
        """
        метод регистрации пользователя
        """

        cursor = self.connect.cursor()
        cursor.execute("""
                SELECT
                    *
                FROM
                    py_users
                WHERE
                    email = %s;
                """, (email, ))
        if not cursor.rowcount:
            cursor.execute("""
                INSERT INTO
                    py_users (
                        email, password
                        )
                VALUES
                    (%s, %s)
                """, (email, b64encode(password.encode()).decode('utf-8')))
            self.connect.commit()
            cursor.close()
            return True
        else:
            cursor.close()

    def sign_in_open_window(self):
        """
        метод создания виджета авторизации пользователя
        """

        if self.connect:
            if not self.sign_in_window:
                self.sign_in_window = SignIn(Toplevel(), self.sign_in, self.remove_sign_in_window)
        else:
            messagebox.showerror('PyFiles', 'Need to connect to the database')

    def remove_sign_in_window(self):
        """
        метод удаления виджета авторизации пользователя из памяти
        """

        self.sign_in_window = None

    def sign_in(self, email, password):
        """
        метод авторизации пользователя
        """

        cursor = self.connect.cursor()
        cursor.execute("""
            SELECT
                *
            FROM
                py_users
            WHERE
                email = %s
                AND
                password = %s;
            """, (email, b64encode(password.encode()).decode('utf-8')))
        if bool(cursor.rowcount):
            self.session = cursor.fetchone()
            self.change_menu()
            self.get_repositories()
            cursor.close()
            return True
        else:
            cursor.close()

    def logout(self):
        """
        метод деавторизации пользователя
        """

        self.session = None
        self.change_menu()
        self.repositories.delete(0, 'end')
        messagebox.showinfo('PyFiles', 'You have successfully logged out')

    def change_menu(self):
        """
        метод изменения структуры меню
        """

        if self.session:
            self.account_menu.delete('Sign up')
            self.account_menu.delete('Sign in')
            self.account_menu.add_command(label='Update password', command=self.update_password_open_window)
            self.account_menu.add_command(label='Exit', command=self.logout)
        else:
            self.account_menu.delete('Update password')
            self.account_menu.delete('Exit')
            self.account_menu.add_command(label='Sign up', command=self.sign_up_open_window)
            self.account_menu.add_command(label='Sign in', command=self.sign_in_open_window)

    def get_repositories(self):
        """
        метод получения, отображения репозиториев пользователя
        """

        self.repositories.delete(0, 'end')
        repositories = []
        cursor = self.connect.cursor()
        cursor.execute("""
            SELECT
                *
            FROM
                py_files
            WHERE
                user_id = %s;
            """, (self.session[0], ))
        files = cursor.fetchall()
        if files:
            for file in files:
                if not (file[1] in repositories):
                    self.repositories.insert('end', file[1])
                    repositories.append(file[1])
        cursor.close()

    def add_repository(self):
        """
        метод добавления репозитория в список репозиториев пользователя
        """

        if self.session:
            cursor = self.connect.cursor()
            place = filedialog.askdirectory()
            #если dirs, files пустые и текущий раздел(root) отличается от раздела, заданного пользователем(p), то это пустой каталог
            for root, dirs, files in walk(place):
                if len(files) > 0:
                    for file in files:
                        r = '' if root == place else root.replace(place, '')
                        f = open(root + '/' + file, 'rb')
                        cursor.execute("""
                            INSERT INTO
                                py_files (
                                    rep, root, name, data, user_id
                                    )
                            VALUES
                                (%s, %s, %s, %s, %s);
                            """, (place, r, file, f.read(), self.session[0]))
                        f.close()
                        self.connect.commit()
                elif root != place and not files and not dirs:
                    cursor.execute("""
                        INSERT INTO
                        py_files (
                            rep, root, user_id
                            )
                        VALUES
                            (%s, %s, %s)
                        """, (place, root.replace(place, ''),self.session[0]))
            cursor.close()
            self.repositories.insert('end', place)
        else:
            messagebox.showerror('PyFiles', 'Need to login')

    def download_repository(self):
        """
        метод загрузки репозитория пользователя в выбранную директорию
        """

        if self.session:
            repository = self.repositories.curselection()
            if repository:
                cursor = self.connect.cursor()
                place = filedialog.askdirectory()
                if place:
                    cursor.execute("""
                        SELECT
                            *
                        FROM
                            py_files
                        WHERE
                            user_id = %s
                            AND
                            rep = %s;
                        """, (self.session[0], self.repositories.get(repository[0])))
                    files = cursor.fetchall()
                    for file in files:
                        if not path.exists(place + file[2]):
                            makedirs(place + file[2])
                        if file[3] != None:
                            f = open(place + file[2] + '/' + file[3], 'w+b')
                            f.write(file[4])
                            f.close()
                cursor.close()
            else:
                messagebox.showerror('PyFiles', 'Need to select a repository')
        else:
            messagebox.showerror('PyFiles', 'Need to login')

    def delete_repository(self):
        """
        метод удаления репозитория из списка репозиториев пользователя
        """

        if self.session:
            repository = self.repositories.curselection()
            if repository:
                cursor = self.connect.cursor()
                cursor.execute("""
                    DELETE FROM
                        py_files
                    WHERE
                        user_id = %s
                        AND
                        rep = %s;
                    """, (self.session[0], self.repositories.get(repository[0])))
                self.connect.commit()
                cursor.close()
                self.get_repositories()
                messagebox.showinfo('PyFiles', 'Repository deleted successfully')
            else:
                messagebox.showerror('PyFiles', 'Need to select a repository')
        else:
            messagebox.showerror('PyFiles', 'Need to login')

    def update_password_open_window(self):
        """
        метод создания виджета обновления пароля пользователя
        """
        if self.session:
            if not self.update_password_window:
                self.update_password_window = PasswordUpdate(Toplevel(), self.update_password, self.remove_update_password_window)
        else:
            messagebox.showerror('PyFiles', 'Need to login')

    def remove_update_password_window(self):
        """
        метод удаления виджета обновления пароля пользователя из памяти
        """

        self.update_password_window = None

    def update_password(self, password, new_password):
        """
        метод обновления пароля пользователя
        """

        if b64encode(password.encode()).decode('utf-8') == self.session[2] and\
           b64encode(new_password.encode()).decode('utf-8') != self.session[2]:
            cursor = self.connect.cursor()
            cursor.execute("""
                UPDATE
                    py_users
                SET
                    password = %s
                WHERE
                    id = %s;
                """, (b64encode(new_password.encode()).decode('utf-8'), self.session[0]))
            self.connect.commit()
            cursor.close()
            return True

    def close_root_process(self):
        """
        метод закрытия приложения
        """

        if self.connect:
            self.connect.close()
        self.root.destroy()

def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()

