from tkinter import *
from tkinter import messagebox
from CryptIt import CryptIt
import json


class AccountHandler:
    def __init__(self):
        # Load settings
        with open("setting.json", "r") as sdata:
            self.settings = json.load(sdata)

        self.WINDOWNAME = self.settings["WIN"]
        self.IMAGE = self.settings["IMAGE"]
        self.FONT_NAME = self.settings["FONT_NAME"]
        self.DEFAULT_FONT_SETTINGS = list(self.settings["DEFUALT_FONT_SETTINGS"].values())

        self.window = Tk()
        self.window.title(self.WINDOWNAME)
        self.window.config(padx=50, pady=50)

        self.crypt = CryptIt()

        # Setup main UI
        self.setup_main_ui()
        self.window.mainloop()

    def setup_main_ui(self):
        """
        Setup the main menu to choose between adding a user or resetting a password.
        """
        self.clear_window()
        Label(self.window, text="Account Management", font=self.DEFAULT_FONT_SETTINGS).grid(column=0, row=0, columnspan=2, pady=10)

        Button(self.window, text="Create Account", command=self.create_account_ui, width=20, font=self.DEFAULT_FONT_SETTINGS).grid(column=0, row=1, pady=10)
        Button(self.window, text="Reset Password", command=self.reset_password_ui, width=20, font=self.DEFAULT_FONT_SETTINGS).grid(column=0, row=2, pady=10)

    def create_account_ui(self):
        """
        Setup the UI for creating a new user account.
        """
        self.clear_window()

        Label(self.window, text="Create Account", font=self.DEFAULT_FONT_SETTINGS).grid(column=0, row=0, columnspan=2, pady=10)

        name_entry = self.create_label_entry("Enter Name:", 1)
        pass1_entry = self.create_label_entry("Enter Password:", 2, show="*")
        pass2_entry = self.create_label_entry("Confirm Password:", 3, show="*")

        Button(
            self.window,
            text="Submit",
            command=lambda: self.add_user(name_entry.get(), pass1_entry.get(), pass2_entry.get()),
            width=20,
            font=self.DEFAULT_FONT_SETTINGS
        ).grid(column=0, row=4, columnspan=2, pady=10)

        Button(
            self.window,
            text="Back",
            command=self.setup_main_ui,
            width=20,
            font=self.DEFAULT_FONT_SETTINGS
        ).grid(column=0, row=5, columnspan=2, pady=10)

    def reset_password_ui(self):
        """
        Setup the UI for resetting an existing user's password.
        """
        self.clear_window()

        Label(self.window, text="Reset Password", font=self.DEFAULT_FONT_SETTINGS).grid(column=0, row=0, columnspan=2, pady=10)

        name_entry = self.create_label_entry("Enter Name:", 1)
        pass1_entry = self.create_label_entry("Enter Current Password:", 2, show="*")
        new_pass_entry = self.create_label_entry("Enter New Password:", 3, show="*")

        Button(
            self.window,
            text="Submit",
            command=lambda: self.reset_password(name_entry.get(), pass1_entry.get(), new_pass_entry.get()),
            width=20,
            font=self.DEFAULT_FONT_SETTINGS
        ).grid(column=0, row=4, columnspan=2, pady=10)

        Button(
            self.window,
            text="Back",
            command=self.setup_main_ui,
            width=20,
            font=self.DEFAULT_FONT_SETTINGS
        ).grid(column=0, row=5, columnspan=2, pady=10)

    def create_label_entry(self, label_text, row, show=None):
        """
        Helper to create a label and entry field in the UI.
        """
        Label(self.window, text=label_text, font=self.DEFAULT_FONT_SETTINGS).grid(column=0, row=row, sticky="w", pady=5)
        entry = Entry(self.window, width=30, font=self.DEFAULT_FONT_SETTINGS, show=show)
        entry.grid(column=1, row=row, pady=5)
        return entry

    def clear_window(self):
        """
        Clears the current window content.
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def add_user(self, name, pass1, pass2):
        """
        Add or create a new user account.
        """
        if not name or not pass1 or not pass2:
            self.show_message("Error", "All fields are required.")
            return

        if pass1 != pass2:
            self.show_message("Error", "Passwords do not match.")
            return

        try:
            with open("user_account_list.json", "r") as file:
                accounts = json.load(file)
        except FileNotFoundError:
            accounts = {}

        encrypted_name = self.crypt.getEncrypt(name, self.crypt.getKey(name))
        encrypted_pass = self.crypt.getHash(pass1)

        if encrypted_name in accounts:
            self.show_message("Error", "User already exists.")
        else:
            accounts[encrypted_name] = {
                "initial_password": encrypted_pass,
                "current_password": encrypted_pass,
            }
            with open("user_account_list.json", "w") as file:
                json.dump(accounts, file, indent=4)
            self.show_message("Success", "User created successfully.")

    def reset_password(self, name, current_pass, new_pass):
        """
        Reset an existing user's password.
        """
        if not name or not current_pass or not new_pass:
            self.show_message("Error", "All fields are required.")
            return

        try:
            with open("user_account_list.json", "r") as file:
                accounts = json.load(file)
        except FileNotFoundError:
            self.show_message("Error", "No accounts found.")
            return

        encrypted_name = self.crypt.getEncrypt(name, self.key)
        if encrypted_name not in accounts:
            self.show_message("Error", "User does not exist.")
            return

        encrypted_current_pass = self.crypt.getEncrypt(self.crypt.getHash(current_pass), self.key)
        if accounts[encrypted_name]["current_password"] != encrypted_current_pass:
            self.show_message("Error", "Current password is incorrect.")
            return

        encrypted_new_pass = self.crypt.getEncrypt(self.crypt.getHash(new_pass), self.key)

        accounts[encrypted_name]["current_password"] = encrypted_new_pass

        with open("user_account_list.json", "w") as file:
            json.dump(accounts, file, indent=4)
        self.show_message("Success", "Password reset successfully.")

    def show_message(self, title, message):
        """
        Display a messagebox with a title and message.
        """
        messagebox.showinfo(title, message)


if __name__ == "__main__":
    AccountHandler()
