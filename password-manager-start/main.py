import customtkinter as ctk
from tkinter import messagebox
import json
from PasswordsHandler import PasswordManager
from CryptIt import CryptIt
from Create_Password import AccountHandler
from PIL import Image

class PasswordManagerApp:
    def __init__(self):
        # Set appearance mode and default color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Constants
        self.WINDOWNAME = "Password Manager"
        self.IMAGE = "password-manager-start/logo.png"
        self.FONT_NAME = "JetBrains Mono"
        self.DEFAULT_FONT_SETTINGS = (self.FONT_NAME, 12, "normal")
        self.crypt = CryptIt()

        # Main Window Setup
        self.window = ctk.CTk()
        self.window.title(self.WINDOWNAME)
        self.window.geometry("700x500")
        self.window.resizable(False, False)

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

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Theme Switch (move to top right)
        self.theme_switch = ctk.CTkSwitch(
            self.main_frame,
            text="Light Mode",
            command=self.toggle_theme,
            font=self.DEFAULT_FONT_SETTINGS
        )
        self.theme_switch.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

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

        # User ID
        self.user_id_frame = ctk.CTkFrame(self.main_frame)
        self.user_id_frame.pack(pady=10, padx=20, fill="x")
        
        self.user_id_label = ctk.CTkLabel(self.user_id_frame, text="User ID:", font=self.DEFAULT_FONT_SETTINGS)
        self.user_id_label.pack(side="left", padx=5)
        self.user_id_entry = ctk.CTkEntry(self.user_id_frame, width=300, font=self.DEFAULT_FONT_SETTINGS)
        self.user_id_entry.pack(side="right", padx=5)
        self.user_id_entry.focus()

        # User Password
        self.user_pass_frame = ctk.CTkFrame(self.main_frame)
        self.user_pass_frame.pack(pady=10, padx=20, fill="x")
        
        self.user_pass_label = ctk.CTkLabel(self.user_pass_frame, text="Password:", font=self.DEFAULT_FONT_SETTINGS)
        self.user_pass_label.pack(side="left", padx=5)
        self.user_pass_entry = ctk.CTkEntry(self.user_pass_frame, width=300, font=self.DEFAULT_FONT_SETTINGS, show="•")
        self.user_pass_entry.pack(side="right", padx=5)

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=30, padx=20, fill="x")

        # Login Button
        self.login_button = ctk.CTkButton(
            self.button_frame,
            text="Login",
            command=self.login,
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#1f538d",
            hover_color="#14375e",
            height=40
        )
        self.login_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Create/Reset Button
        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="Create/Reset Password",
            command=self.account_handle,
            font=self.DEFAULT_FONT_SETTINGS,
            fg_color="#2d7d46",
            hover_color="#1e5c32",
            height=40
        )
        self.reset_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Configure grid weights
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.window.mainloop()

    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Light Mode")

    def login(self):
        userid = self.user_id_entry.get()
        pwrd = self.user_pass_entry.get()
        userkey = self.crypt.getKey(userid)

        if not userid or not pwrd:
            messagebox.showwarning(title="Fields Empty", message="Please fill all the fields.")
            return

        try:
            with open("user_account_list.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No users found.")
            return

        encryptuser = self.crypt.getEncrypt(userid, userkey)

        if encryptuser in data and self.crypt.checkHash(pwrd, data[encryptuser]["current_password"]):
            key = self.crypt.getKey(data[encryptuser]["initial_password"])
            with open("password-manager-start/setting.json", "r") as sdata:
                settings = json.load(sdata)
            self.window.destroy()
            PasswordManager(userid, key, settings)
        else:
            messagebox.showerror(title="Error", message="Invalid credentials.")

    def account_handle(self):
        AccountHandler()

if __name__ == "__main__":
    PasswordManagerApp()
