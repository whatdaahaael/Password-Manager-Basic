import customtkinter as ctk
from tkinter import messagebox
from CryptIt import CryptIt
import json


class AccountHandler:
    def __init__(self):
        # Set appearance mode and default color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Load settings
        with open("password-manager-start/setting.json", "r") as sdata:
            self.settings = json.load(sdata)

        self.WINDOWNAME = self.settings["WIN"]
        self.IMAGE = self.settings["IMAGE"]
        self.FONT_NAME = self.settings["FONT_NAME"]
        self.DEFAULT_FONT_SETTINGS = tuple(self.settings["DEFUALT_FONT_SETTINGS"].values())

        self.window = ctk.CTk()
        self.window.title(self.WINDOWNAME)
        self.window.geometry("800x700")  # Increased height for the new text box
        self.window.resizable(False, False)

        self.crypt = CryptIt()

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
        self.setup_main_ui()
        self.window.mainloop()

    def setup_main_ui(self):
        """
        Setup the main menu to choose between adding a user or resetting a password.
        """
        self.clear_window()

        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Account Management",
            font=(self.FONT_NAME, 24, "bold")
        )
        self.title_label.pack(pady=20)

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20, padx=20, fill="x")

        # Create Account button
        self.create_button = ctk.CTkButton(
            self.button_frame,
            text="Create Account",
            command=self.create_account_ui,
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#2d7d46",
            hover_color="#1e5c32",
            height=40
        )
        self.create_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Reset Password button
        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="Reset Password",
            command=self.reset_password_ui,
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#1f538d",
            hover_color="#14375e",
            height=40
        )
        self.reset_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        # Theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.main_frame,
            text="Light Mode",
            command=self.toggle_theme,
            font=self.DEFAULT_FONT_SETTINGS
        )
        self.theme_switch.pack(pady=20)

    def create_account_ui(self):
        """
        Setup the UI for creating a new user account.
        """
        self.clear_window()

        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Create Account",
            font=(self.FONT_NAME, 24, "bold")
        )
        self.title_label.pack(pady=20)

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        # Name input
        self.name_frame = ctk.CTkFrame(self.input_frame)
        self.name_frame.pack(pady=10, padx=10, fill="x")
        self.name_label = ctk.CTkLabel(self.name_frame, text="Enter Name:", font=self.DEFAULT_FONT_SETTINGS)
        self.name_label.pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(self.name_frame, width=300, font=self.DEFAULT_FONT_SETTINGS)
        self.name_entry.pack(side="right", padx=5)

        # Password input
        self.pass1_frame = ctk.CTkFrame(self.input_frame)
        self.pass1_frame.pack(pady=10, padx=10, fill="x")
        self.pass1_label = ctk.CTkLabel(self.pass1_frame, text="Enter Password:", font=self.DEFAULT_FONT_SETTINGS)
        self.pass1_label.pack(side="left", padx=5)
        self.pass1_entry = ctk.CTkEntry(self.pass1_frame, width=300, font=self.DEFAULT_FONT_SETTINGS, show="•")
        self.pass1_entry.pack(side="right", padx=5)

        # Confirm password input
        self.pass2_frame = ctk.CTkFrame(self.input_frame)
        self.pass2_frame.pack(pady=10, padx=10, fill="x")
        self.pass2_label = ctk.CTkLabel(self.pass2_frame, text="Confirm Password:", font=self.DEFAULT_FONT_SETTINGS)
        self.pass2_label.pack(side="left", padx=5)
        self.pass2_entry = ctk.CTkEntry(self.pass2_frame, width=300, font=self.DEFAULT_FONT_SETTINGS, show="•")
        self.pass2_entry.pack(side="right", padx=5)

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20, padx=20, fill="x")

        # Submit button
        self.submit_button = ctk.CTkButton(
            self.button_frame,
            text="Submit",
            command=lambda: self.add_user(
                self.name_entry.get(),
                self.pass1_entry.get(),
                self.pass2_entry.get()
            ),
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#2d7d46",
            hover_color="#1e5c32",
            height=40
        )
        self.submit_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Back button
        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="Back",
            command=self.setup_main_ui,
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#7d2d2d",
            hover_color="#5c1e1e",
            height=40
        )
        self.back_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        # Configure grid weights
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def reset_password_ui(self):
        """
        Setup the UI for resetting an existing user's password.
        """
        self.clear_window()

        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Reset Password",
            font=(self.FONT_NAME, 24, "bold")
        )
        self.title_label.pack(pady=20)

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        # Name input
        self.name_frame = ctk.CTkFrame(self.input_frame)
        self.name_frame.pack(pady=10, padx=10, fill="x")
        self.name_label = ctk.CTkLabel(self.name_frame, text="Enter Name:", font=self.DEFAULT_FONT_SETTINGS)
        self.name_label.pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(self.name_frame, width=300, font=self.DEFAULT_FONT_SETTINGS)
        self.name_entry.pack(side="right", padx=5)

        # Current password input
        self.pass1_frame = ctk.CTkFrame(self.input_frame)
        self.pass1_frame.pack(pady=10, padx=10, fill="x")
        self.pass1_label = ctk.CTkLabel(self.pass1_frame, text="Enter Current Password:", font=self.DEFAULT_FONT_SETTINGS)
        self.pass1_label.pack(side="left", padx=5)
        self.pass1_entry = ctk.CTkEntry(self.pass1_frame, width=300, font=self.DEFAULT_FONT_SETTINGS, show="•")
        self.pass1_entry.pack(side="right", padx=5)

        # New password input
        self.pass2_frame = ctk.CTkFrame(self.input_frame)
        self.pass2_frame.pack(pady=10, padx=10, fill="x")
        self.pass2_label = ctk.CTkLabel(self.pass2_frame, text="Enter New Password:", font=self.DEFAULT_FONT_SETTINGS)
        self.pass2_label.pack(side="left", padx=5)
        self.pass2_entry = ctk.CTkEntry(self.pass2_frame, width=300, font=self.DEFAULT_FONT_SETTINGS, show="•")
        self.pass2_entry.pack(side="right", padx=5)

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20, padx=20, fill="x")

        # Submit button
        self.submit_button = ctk.CTkButton(
            self.button_frame,
            text="Submit",
            command=lambda: self.reset_password(
                self.name_entry.get(),
                self.pass1_entry.get(),
                self.pass2_entry.get()
            ),
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#2d7d46",
            hover_color="#1e5c32",
            height=40
        )
        self.submit_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Back button
        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="Back",
            command=self.setup_main_ui,
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#7d2d2d",
            hover_color="#5c1e1e",
            height=40
        )
        self.back_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        # Configure grid weights
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def clear_window(self):
        """
        Clears the current window content.
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Light Mode")

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
            self.setup_main_ui()  # Return to main menu after successful creation

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

        encrypted_name = self.crypt.getEncrypt(name, self.crypt.getKey(name))
        if encrypted_name not in accounts:
            self.show_message("Error", "User does not exist.")
            return

        if not self.crypt.checkHash(current_pass, accounts[encrypted_name]["current_password"]):
            self.show_message("Error", "Current password is incorrect.")
            return

        encrypted_new_pass = self.crypt.getHash(new_pass)
        accounts[encrypted_name]["current_password"] = encrypted_new_pass

        with open("user_account_list.json", "w") as file:
            json.dump(accounts, file, indent=4)
        self.show_message("Success", "Password reset successfully.")
        self.setup_main_ui()  # Return to main menu after successful reset

    def show_message(self, title, message):
        """
        Display a messagebox with a title and message.
        """
        messagebox.showinfo(title, message)


if __name__ == "__main__":
    AccountHandler()
