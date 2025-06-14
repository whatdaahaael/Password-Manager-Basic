import json
import customtkinter as ctk
from CryptIt import CryptIt as crypt

WINDOWNAME = "Password Data"
FONT_NAME = "JetBrains Mono"
DEFAULT_FONT_SETTINGS = (FONT_NAME, 12, "normal")
crypt = crypt()

class PasswordScreen:
    def __init__(self, data, key):
        self.data = data
        self.key = key
        self.setup_ui()

    def setup_ui(self):
        # Create the main window
        self.window = ctk.CTk()
        self.window.title(WINDOWNAME)
        self.window.geometry("800x600")
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

        # Main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Saved Passwords",
            font=(FONT_NAME, 20, "bold")
        )
        self.title_label.pack(pady=10)

        # Create a frame for the listbox and scrollbar
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create a text widget for displaying data
        self.text_widget = ctk.CTkTextbox(
            self.list_frame,
            font=DEFAULT_FONT_SETTINGS,
            width=700,
            height=400,
            wrap="word"
        )
        self.text_widget.pack(pady=10, padx=10, fill="both", expand=True)

        # Populate the text widget with data
        self.populate_data()

        # Close button
        self.close_button = ctk.CTkButton(
            self.main_frame,
            text="Close",
            command=self.window.destroy,
            font=DEFAULT_FONT_SETTINGS,
            fg_color="#7d2d2d",
            hover_color="#5c1e1e"
        )
        self.close_button.pack(pady=10)

        # Theme switch
        self.theme_switch = ctk.CTkSwitch(
            self.main_frame,
            text="Light Mode",
            command=self.toggle_theme,
            font=DEFAULT_FONT_SETTINGS
        )
        self.theme_switch.pack(pady=10)

        self.window.mainloop()

    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Light Mode")

    def populate_data(self):
        """Adds data to the text widget."""
        for website, details in self.data.items():
            encrypted_website = website
            encrypted_email = details.get('email', 'N/A')
            encrypted_password = details.get('password', 'N/A')

            # Decrypt the values using the key
            decrypted_website = crypt.getDecrypt(encrypted_website, self.key) if encrypted_website != 'N/A' else 'N/A'
            decrypted_email = crypt.getDecrypt(encrypted_email, self.key) if encrypted_email != 'N/A' else 'N/A'
            decrypted_password = crypt.getDecrypt(encrypted_password, self.key) if encrypted_password != 'N/A' else 'N/A'

            # Format and insert the data
            self.text_widget.insert("end", f"Website: {decrypted_website}\n", "website")
            self.text_widget.insert("end", f"  Email: {decrypted_email}\n", "email")
            self.text_widget.insert("end", f"  Password: {decrypted_password}\n", "password")
            self.text_widget.insert("end", "-" * 50 + "\n\n", "separator")

        # Configure tags for different text styles
        self.text_widget.tag_config("website", font=(FONT_NAME, 14, "bold"))
        self.text_widget.tag_config("email", font=(FONT_NAME, 12))
        self.text_widget.tag_config("password", font=(FONT_NAME, 12))
        self.text_widget.tag_config("separator", foreground="gray")

        # Make the text widget read-only
        self.text_widget.configure(state="disabled")


