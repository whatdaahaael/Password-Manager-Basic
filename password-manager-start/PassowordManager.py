from tkinter import *
from tkinter import messagebox
import json
from PasswordsHandler import PasswordManager
from CryptIt import CryptIt
from Create_Passowrd import AccountHandler
class PasswordManagerApp:
    def __init__(self):
        # Constants
        self.WINDOWNAME = "Password Manager"
        self.IMAGE = "logo.png"
        self.FONT_NAME = "JetBrains Mono"
        self.DEFAULT_FONT_SETTINGS = (self.FONT_NAME, 12, "normal")
        self.crypt=CryptIt()

        # Main Window Setup
        self.window = Tk()
        self.window.title(self.WINDOWNAME)
        self.window.config(padx=50, pady=50)

        # Canvas Widget
        self.canvas = Canvas(width=200, height=200, highlightthickness=0)
        self.logo_img = PhotoImage(file=self.IMAGE)
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(column=0, row=0, columnspan=2)

        # User ID
        self.user_id_label = Label(text="User ID:", font=self.DEFAULT_FONT_SETTINGS)
        self.user_id_label.grid(column=0, row=1, pady=5)
        self.user_id_entry = Entry(width=21, font=self.DEFAULT_FONT_SETTINGS)
        self.user_id_entry.grid(column=1, row=1, pady=5)
        self.user_id_entry.focus()

        # User Password
        self.user_pass_label = Label(text="Password:", font=self.DEFAULT_FONT_SETTINGS)
        self.user_pass_label.grid(column=0, row=2, pady=5)
        self.user_pass_entry = Entry(width=21, font=self.DEFAULT_FONT_SETTINGS, show="*")
        self.user_pass_entry.grid(column=1, row=2, pady=5)


        # Buttons
        self.login_button = Button(text="Login", width=20, command=self.login, font=self.DEFAULT_FONT_SETTINGS)
        self.login_button.grid(column=0, row=4, pady=5, columnspan=2)

        self.reset_button = Button(text="Create/Reset Password", width=20, command=self.account_handle,
                                    font=self.DEFAULT_FONT_SETTINGS)
        self.reset_button.grid(column=0, row=5, columnspan=2, pady=5)

        self.window.mainloop()

    def login(self):
        userid = self.user_id_entry.get()
        pwrd = self.user_pass_entry.get()
        userkey=self.crypt.getKey(userid)


        if not userid or not pwrd:
            messagebox.showwarning(title="Fields Empty", message="Please fill all the fields.")
            return

        try:
            with open("user_account_list.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No users found.")
            return

        encryptuser=self.crypt.getEncrypt(userid, userkey)

        if encryptuser in data and self.crypt.checkHash(pwrd, data[encryptuser]["current_password"]):
            key=self.crypt.getKey(data[encryptuser]["initial_password"])
            with open("setting.json", "r") as sdata:
                settings = json.load(sdata)
            # for widget in self.window.winfo_children():
            #     widget.destroy()
            self.window.destroy()
            PasswordManager(userid, key, settings)
        else:
            messagebox.showerror(title="Error", message="Invalid credentials.")

    def account_handle(self):
        AccountHandler()


if __name__ == "__main__":
    PasswordManagerApp()
