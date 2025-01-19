import json
from tkinter import *
from tkinter import messagebox
import pyperclip
from PasswordGenerator import GeneratePassword as GP
from ViewPasswords import PasswordScreen as psb
from CryptIt import CryptIt


class PasswordManager:
    # ---------------------------- CONSTANTS ------------------------------- #

    def __init__(self, UserID, KEY, settings):
        # Initialize the main window
        self.WINDOWNAME = settings["WIN"]
        self.IMAGE = settings["IMAGE"]
        self.FONT_NAME = settings["FONT_NAME"]

        self.DEFUALT_FONT_SETTINGS = list(settings["DEFUALT_FONT_SETTINGS"].values())
        self.userid = UserID
        self.key = KEY
        self.window = Tk()
        self.window.title(f"{self.WINDOWNAME} : {self.userid}")
        self.window.config(padx=50, pady=50)
        self.crypt=CryptIt()

        # ---------------------------- UI SETUP ------------------------------- #
        self.setup_ui()
        self.window.mainloop()


    def setup_ui(self):
        # Canvas Widget
        canvas = Canvas(width=200, height=200, highlightthickness=0)
        # Getting hold of the image
        logo_img = PhotoImage(file=self.IMAGE)
        canvas.create_image(100, 100, image=logo_img)
        canvas.grid(column=1, row=0)
        self.logo_img = logo_img  # Keep reference to avoid garbage collection

        # Website text label and input/entry
        self.website_name = self.create_label_entry("Website:", 1, focus=True, entry_width=21)

        # Email/username text label and input/entry
        self.email_name = self.create_label_entry("Email / Username:", 2, entry_width=38,
                                                  default_value="sujanedwin2006@gmail.com")

        # Password text label and input/entry
        self.pwrd_name = self.create_label_entry("Password:", 3, entry_width=21)

        # Buttons
        self.create_button("Generate Password", self.Generate_Password, 2, 3)
        self.create_button("Add", self.Add_Pass, 1, 4, button_width=38, colspan=2)
        self.create_button("Search", self.Find_Pass, 2, 1, button_width=16)
        self.create_button("Show Passwords", self.Show_Passowrds, 2, 5)

    def create_label_entry(self, label_text, row, focus=False, entry_width=21, default_value=None):
        """
        Helper to create a label and entry field in the UI.
        """
        label = Label(text=label_text, font=self.DEFUALT_FONT_SETTINGS)
        label.grid(column=0, row=row)
        entry = Entry(width=entry_width, font=self.DEFUALT_FONT_SETTINGS)
        entry.grid(column=1, row=row, columnspan=(2 if entry_width > 21 else 1))
        if focus:
            entry.focus()
        if default_value:
            entry.insert(END, default_value)
        return entry

    def create_button(self, text, command, col, row, button_width=None, colspan=1):
        """
        Helper to create buttons in the UI.
        """
        button = Button(
            text=text,
            command=command,
            highlightthickness=0,
            font=self.DEFUALT_FONT_SETTINGS,
            width=button_width,
        )
        button.grid(column=col, row=row, columnspan=colspan)

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def Generate_Password(self):
        # Clear any available text
        self.pwrd_name.delete(0, 'end')

        # Replace with new password
        pwrd = GP().GetNewPass()
        self.pwrd_name.insert(END, pwrd)
        pyperclip.copy(pwrd)

    # -------------------------- SEE ALL PASSWORDS ------------------------------- #
    def Show_Passowrds(self):
        # Load data from JSON file and display in the GUI
        try:
            with open("password_list.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showwarning(title="Passwords Empty", message="No Passwords Found")
        else:
            # Use the encrypted userid directly
            encrypted_userid = self.crypt.getEncrypt(self.userid, self.key)

            # Check if the encrypted user exists in the data
            if encrypted_userid in data:
                psb(data[encrypted_userid], self.key)
            else:
                messagebox.showinfo(title="Error", message="No passwords found for this user.")

    # --------------------------- SEARCH WEBSITE -------------------------------- #
    def Find_Pass(self):
        website = self.website_name.get().lower()
        try:
            with open("password_list.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message=f"No Passwords.")
        else:
            encrypted_userid = self.crypt.getEncrypt(self.userid, self.key)

            # Check if the user exists and the website is in their data
            if encrypted_userid in data and crypt.getEncrypt(website, self.key) in data[encrypted_userid]:
                email = self.crypt.getDecrypt(data[encrypted_userid][self.crypt.getEncrypt(website, self.key)]["email"], self.key)
                password = self.crypt.getDecrypt(data[encrypted_userid][self.crypt.getEncrypt(website, self.key)]["password"], self.key)
                message = f"Email: {email}\nPassword: {password}"
                messagebox.showinfo(title=website, message=message)
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} found.")

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def Add_Pass(self):
        website = self.website_name.get().lower()
        email = self.email_name.get()
        pwrd = self.pwrd_name.get()
        encrypted_website = self.crypt.getEncrypt(website, self.key)
        encrypted_email = self.crypt.getEncrypt(email, self.key)
        encrypted_password = self.crypt.getEncrypt(pwrd, self.key)

        # Data to be added/updated
        data_dict = {
            encrypted_website: {
                "email": encrypted_email,
                "password": encrypted_password
            }
        }

        # Check if website and password have data
        if len(website) == 0 or len(pwrd) == 0:
            messagebox.showwarning(title="Fields Empty", message="Please fill all the fields.")
            return
        else:
            try:
                with open("password_list.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                data = {}  # If no file exists, start with an empty dictionary

            encrypted_userid = self.crypt.getEncrypt(self.userid, self.key)

            # Add or update the user's data with the new website/password
            if encrypted_userid in data:
                data[encrypted_userid].update(data_dict)  # Update if user exists
            else:
                data[encrypted_userid] = data_dict  # Add new user if not exists

            with open("password_list.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            # Clear fields after saving
            self.website_name.delete(0, 'end')
            self.pwrd_name.delete(0, 'end')
            messagebox.showinfo(title="Password Added", message=f"Password for {website} added successfully.")







if __name__ == "__main__":
    with open("setting.json", "r") as sdata:
        settings = json.load(sdata)
    crypt = CryptIt()
    name="Example"
    key = crypt.getKey(name)
    PasswordManager(name, key, settings)
