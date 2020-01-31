from tkinter import Frame, Label, Entry, Button, StringVar, BOTH, messagebox
import config

import config

class Connect(Frame):
    """
    Класс виджета для создания подключения к базе данных
    """

    def __init__(self, root, connect_process, connect_window_process):
        Frame.__init__(self, root)
        self.root = root
        self.connect_process = connect_process
        self.connect_window_process = connect_window_process
        self.host, self.name, self.user, self.password = StringVar(), StringVar(), StringVar(), StringVar()
        self.init_window()

    def init_window(self):
        """
        метод инициализации окна
        """

        self.root.title(config.TITLE)
        self.root.geometry('%dx%d+%d+%d'%(config.CONNECT_WIDTH,
                                          config.CONNECT_HEIGHT,
                                          round(self.root.winfo_screenwidth()/2 - config.CONNECT_WIDTH/2, 1),
                                          round(self.root.winfo_screenheight()/2 - config.CONNECT_HEIGHT/2, 1)))
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.close_root_process)
        self.init_widgets()

    def init_widgets(self):
        """
        метод инициализации виджетов
        """

        self.pack(fill = BOTH, expand = 1)
        Label(self, text='host', font='Calibri 10', relief='groove').place(x=5, y=5, width=75, height=30)
        Label(self, text='name', font='Calibri 10', relief='groove').place(x=5, y=40, width=75, height=30)
        Label(self, text='user', font='Calibri 10', relief='groove').place(x=5, y=75, width=75, height=30)
        Label(self, text='password', font='Calibri 10', relief='groove').place(x=5, y=110, width=75, height=30)
        Entry(self, textvariable=self.host, font='Calibri 10').place(x=85, y=5, width=155, height=30)
        Entry(self, textvariable=self.name, font='Calibri 10').place(x=85, y=40, width=155, height=30)
        Entry(self, textvariable=self.user, font='Calibri 10').place(x=85, y=75, width=155, height=30)
        Entry(self, textvariable=self.password, show='*', font='Calibri 10').place(x=85, y=110, width=155, height=30)
        Button(self, text='Connect', font='Calibri 10', relief='groove', command=self.set_connect).place(x=5, y=145, width=240, height=30)

    def set_connect(self):
        """
        метод проверки полей, вызова метода подключения к базе данных
        """

        if not False in list(map(lambda x: len(x) > 0, [self.host.get(),
                                                        self.name.get(),
                                                        self.user.get(),
                                                        self.password.get()])):
            if self.connect_process(self.host.get(),
                                    self.name.get(),
                                    self.user.get(),
                                    self.password.get()):
                self.close_root_process()
                messagebox.showinfo('PyFiles', 'Сonnection to the database was successful')
            else:
                self.host.set('')
                self.name.set('')
                self.user.set('')
                self.password.set('')
                messagebox.showerror('PyFiles', 'Failed to connect to database')
        else:
            messagebox.showerror('PyFiles', 'All fields must be filled')

    def close_root_process(self):
        """
        метод закрытия виджета
        """
        
        self.connect_window_process()
        self.root.destroy()

class SignUp(Frame):
    """
    Класс виджета регистрации пользователя
    """

    def __init__(self, root, sign_up_process, sign_up_window_process):
        Frame.__init__(self, root)
        self.root = root
        self.sign_up_process = sign_up_process
        self.sign_up_window_process = sign_up_window_process
        self.email = StringVar()
        self.password = StringVar()
        self.password_r = StringVar()
        self.init_window()

    def init_window(self):
        """
        метод инициализации окна
        """

        self.root.title(config.TITLE)
        self.root.geometry('%dx%d+%d+%d'%(config.SIGN_UP_WIDTH,
                                          config.SIGN_UP_HEIGHT,
                                          round(self.root.winfo_screenwidth()/2 - config.SIGN_UP_WIDTH/2, 1),
                                          round(self.root.winfo_screenheight()/2 - config.SIGN_UP_HEIGHT/2, 1)))
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.close_root_process)
        self.init_widgets()

    def init_widgets(self):
        """
        метод инициализации виджетов
        """

        self.pack(fill=BOTH, expand=1)
        Label(self, text='email', font='Calibri 10', relief='groove').place(x=5, y=5, width=75, height=30)
        Label(self, text='password', font='Calibri 10', relief='groove').place(x=5, y=40, width=75, height=30)
        Label(self, text='password x2', font='Calibri 10', relief='groove').place(x=5, y=75, width=75, height=30)
        Entry(self, font='Calibri 10', textvariable=self.email).place(x=85, y=5, width=155, height=30)
        Entry(self, font='Calibri 10', show='*', textvariable=self.password).place(x=85, y=40, width=155, height=30)
        Entry(self, font='Calibri 10', show='*', textvariable=self.password_r).place(x=85, y=75, width=155, height=30)
        Button(self, text='Sign up', font='Calibri 10', relief='groove', command=self.set_sign_up).place(x=5, y=110, width=240, height=30)

    def set_sign_up(self):
        """
        метод проверки полей, вызова метода регистрации пользователя
        """

        if not False in list(map(lambda x: len(x) > 0, [self.email.get(), self.password.get(), self.password_r.get()])):
            if len(self.password.get()) >= 7 and self.password.get() == self.password_r.get():
                if self.sign_up_process(self.email.get(), self.password.get()):
                    self.close_root_process()
                    messagebox.showinfo('PyFiles', 'Registration completed successfully')
                else:
                    self.email.set('')
                    self.password.set('')
                    self.password_r.set('')
                    messagebox.showinfo('PyFiles', 'Failed to register')
            elif len(self.password.get()) < 7:
                messagebox.showerror('PyFiles', 'Password consists of at least 7 characters')
            elif self.password.get() != self.password_r.get():
                messagebox.showerror('PyFiles', 'Passwords must match')
        else:
            messagebox.showerror('PyFiles', 'All fields must be filled')

    def close_root_process(self):
        """
        метод закрытия виджета
        """

        self.sign_up_window_process()
        self.root.destroy()

class SignIn(Frame):
    """
    Класс виджета авторизации пользователя
    """

    def __init__(self, root, sign_in_process, sign_in_window_process):
        Frame.__init__(self, root)
        self.root = root
        self.sign_in_process = sign_in_process
        self.sign_in_window_process = sign_in_window_process
        self.email = StringVar()
        self.password = StringVar()
        self.init_window()

    def init_window(self):
        """
        метод инициализации окна
        """

        self.root.title(config.TITLE)
        self.root.geometry('%dx%d+%d+%d'%(config.SIGN_IN_WIDTH,
                                          config.SIGN_IN_HEIGHT,
                                          round(self.root.winfo_screenwidth()/2 - config.SIGN_IN_WIDTH/2, 1),
                                          round(self.root.winfo_screenheight()/2 - config.SIGN_IN_HEIGHT/2, 1)))
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.close_root_process)
        self.init_widgets()

    def init_widgets(self):
        """
        метод инициализации виджетов
        """

        self.pack(fill=BOTH, expand=1)
        Label(self, text='email', font='Calibri 11', relief='groove').place(x=5, y=5, width=75, height=30)
        Label(self, text='password', font='Calibri 11', relief='groove').place(x=5, y=40, width=75, height=30)
        Entry(self, font='Calibri 10', textvariable=self.email).place(x=85, y=5, width=155, height=30)
        Entry(self, font='Calibri 10', show='*', textvariable=self.password).place(x=85, y=40, width=155, height=30)
        Button(self, text='Sign in', font='Calibri 10', relief='groove', command=self.set_sign_in).place(x=5, y=75, width=240, height=30)

    def set_sign_in(self):
        """
        метод проверки полей, вызова метода авторизации пользователя
        """

        if not False in list(map(lambda x: len(x) > 0, [self.email.get(), self.password.get()])):
            if self.sign_in_process(self.email.get(), self.password.get()):
                self.close_root_process()
                messagebox.showinfo('PyFiles', 'Authorization was successful')
            else:
                self.email.set('')
                self.password.set('')
                messagebox.showinfo('PyFiles', 'Failed to login')
        else:
            messagebox.showerror('PyFiles', 'All fields must be filled')

    def close_root_process(self):
        """
        метод закрытия виджета
        """

        self.sign_in_window_process()
        self.root.destroy()

class PasswordUpdate(Frame):
    """
    Класс виджета обновления пароля пользователя
    """

    def __init__(self, root, password_update_process, password_update_window_process):
        Frame.__init__(self, root)
        self.root = root
        self.password_update_process = password_update_process
        self.password_update_window_process = password_update_window_process
        self.password = StringVar()
        self.new_password = StringVar()
        self.new_password_r = StringVar()
        self.init_window()

    def init_window(self):
        """
        метод инициализации окна
        """

        self.root.title(config.TITLE)
        self.root.geometry('%dx%d+%d+%d'%(config.UPDATE_WIDTH,
                                          config.UPDATE_HEIGHT,
                                          round(self.root.winfo_screenwidth()/2 - config.UPDATE_WIDTH/2, 1),
                                          round(self.root.winfo_screenheight()/2 - config.UPDATE_HEIGHT/2, 1)
                                          ))
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.close_root_process)
        self.init_widgets()

    def init_widgets(self):
        """
        метод инициализации виджетов
        """

        self.pack(fill=BOTH, expand=1)
        Label(self, text='password', font='Calibri 11', relief='groove').place(x=5, y=5, width=75, height=30)
        Label(self, text='new pswd', font='Calibri 11', relief='groove').place(x=5, y=40, width=75, height=30)
        Label(self, text='new pswd x2', font='Calibri 10', relief='groove').place(x=5, y=75, width=75, height=30)
        Entry(self, font='Calibri 11', show='*', textvariable=self.password).place(x=85, y=5, width=155, height=30)
        Entry(self, font='Calibri 11', show='*', textvariable=self.new_password).place(x=85, y=40, width=155, height=30)
        Entry(self, font='Calibri 11', show='*', textvariable=self.new_password_r).place(x=85, y=75, width=155, height=30)
        Button(self, text='Update password', font='Calibri 10', relief='groove', command = self.set_password_update).place(x=5, y=110, width=240, height=30)

    def set_password_update(self):
        """
        метод проверки полей, вызова метода обновления пароля пользователя
        """

        if not False in list(map(lambda x: len(x) > 0, [self.password.get(), self.new_password.get(), self.new_password_r.get()])):
            if self.new_password.get() == self.new_password_r.get():
                if self.password_update_process(self.password.get(), self.new_password.get()):
                    self.close_root_process()
                    messagebox.showinfo('PyFiles', 'Password updated successfully')
                else:
                    self.password.set('')
                    self.new_password.set('')
                    self.new_password_r.set('')
                    messagebox.showerror('PyFiles', 'Failed to update password')
            else:
                messagebox.showerror('PyFiles', 'Passwords must match')
        else:
            messagebox.showerror('PyFiles', 'All fields must be filled')

    def close_root_process(self):
        """
        метод закрытия виджета
        """
        
        self.password_update_window_process()
        self.root.destroy()
