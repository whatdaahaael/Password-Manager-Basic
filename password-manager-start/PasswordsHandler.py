import json
import customtkinter as ctk
from tkinter import messagebox
import pyperclip
from PasswordGenerator import GeneratePassword as GP
from ViewPasswords import PasswordScreen as psb
from CryptIt import CryptIt
from PIL import Image


class PasswordManager:
    # ---------------------------- CONSTANTS ------------------------------- #

    def __init__(self, UserID, KEY, settings):
        # Set appearance mode and default color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize the main window
        self.WINDOWNAME = settings["WIN"]
        self.IMAGE = "password-manager-start/logo.png"
        self.FONT_NAME = settings["FONT_NAME"]

        self.DEFUALT_FONT_SETTINGS = tuple(settings["DEFUALT_FONT_SETTINGS"].values())
        self.userid = UserID
        self.key = KEY
        self.window = ctk.CTk()
        self.window.title(f"{self.WINDOWNAME} : {self.userid}")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.crypt=CryptIt()

        # Set window icon
        try:
            self.window.iconbitmap('password-manager-start/logo.png')
        except Exception:
            try:
                from PIL import Image, ImageTk
                icon_img = Image.open('password-manager-start/logo.png')
                icon = ImageTk.PhotoImage(icon_img)
                self.window.iconphoto(True, icon)
            except Exception:
                pass

        # Setup main UI
        self.setup_ui()
        self.window.mainloop()


    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Logo
        try:
            self.logo_img = ctk.CTkImage(
                light_image=Image.open(self.IMAGE),
                dark_image=Image.open(self.IMAGE),
                size=(200, 200)
            )
            self.logo_label = ctk.CTkLabel(self.main_frame, image=self.logo_img, text="")
            self.logo_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Create a placeholder label if image loading fails
            self.logo_label = ctk.CTkLabel(
                self.main_frame,
                text="Password Manager",
                font=(self.FONT_NAME, 24, "bold")
            )
            self.logo_label.pack(pady=20)

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        # Website input
        self.website_frame = ctk.CTkFrame(self.input_frame)
        self.website_frame.pack(pady=10, padx=10, fill="x")
        self.website_label = ctk.CTkLabel(self.website_frame, text="Website:", font=self.DEFUALT_FONT_SETTINGS)
        self.website_label.pack(side="left", padx=5)
        self.website_name = ctk.CTkEntry(self.website_frame, width=300, font=self.DEFUALT_FONT_SETTINGS)
        self.website_name.pack(side="right", padx=5)
        self.website_name.focus()

        # Email input
        self.email_frame = ctk.CTkFrame(self.input_frame)
        self.email_frame.pack(pady=10, padx=10, fill="x")
        self.email_label = ctk.CTkLabel(self.email_frame, text="Email / Username:", font=self.DEFUALT_FONT_SETTINGS)
        self.email_label.pack(side="left", padx=5)
        self.email_name = ctk.CTkEntry(self.email_frame, width=300, font=self.DEFUALT_FONT_SETTINGS)
        self.email_name.pack(side="right", padx=5)

        # Password input
        self.password_frame = ctk.CTkFrame(self.input_frame)
        self.password_frame.pack(pady=10, padx=10, fill="x")
        self.password_label = ctk.CTkLabel(self.password_frame, text="Password:", font=self.DEFUALT_FONT_SETTINGS)
        self.password_label.pack(side="left", padx=5)
        self.pwrd_name = ctk.CTkEntry(self.password_frame, width=300, font=self.DEFUALT_FONT_SETTINGS, show="•")
        self.pwrd_name.pack(side="right", padx=5)

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20, padx=20, fill="x")

        # Generate Password button
        self.generate_button = ctk.CTkButton(
            self.button_frame,
            text="Generate Password",
            command=self.Generate_Password,
            font=self.DEFUALT_FONT_SETTINGS,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.generate_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add button
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add",
            command=self.Add_Pass,
            font=self.DEFUALT_FONT_SETTINGS,
            fg_color="#2d7d46",
            hover_color="#1e5c32"
        )
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Search button
        self.search_button = ctk.CTkButton(
            self.button_frame,
            text="Search",
            command=self.Find_Pass,
            font=self.DEFUALT_FONT_SETTINGS,
            fg_color="#7d2d2d",
            hover_color="#5c1e1e"
        )
        self.search_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Show Passwords button
        self.show_button = ctk.CTkButton(
            self.button_frame,
            text="Show Passwords",
            command=self.Show_Passowrds,
            font=self.DEFUALT_FONT_SETTINGS,
            fg_color="#2d7d7d",
            hover_color="#1e5c5c"
        )
        self.show_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Configure grid weights
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.main_frame,
            text="Light Mode",
            command=self.toggle_theme,
            font=self.DEFUALT_FONT_SETTINGS
        )
        self.theme_switch.pack(pady=10)

    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Light Mode")

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def Generate_Password(self):
        # Clear any available text
        self.pwrd_name.delete(0, 'end')

        # Replace with new password
        pwrd = GP().GetNewPass()
        self.pwrd_name.insert(0, pwrd)
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
            if encrypted_userid in data and self.crypt.getEncrypt(website, self.key) in data[encrypted_userid]:
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

