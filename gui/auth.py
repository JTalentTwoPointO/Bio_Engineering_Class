# gui/auth.py
import tkinter as tk
from tkinter import messagebox

from database import Session, User


class Auth:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login
        self.session = Session()
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        tk.Label(self.frame, text="Username").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Password").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        self.frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            self.frame.pack_forget()
            self.on_login(user.role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
