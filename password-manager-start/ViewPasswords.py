import json
from tkinter import *
from CryptIt import CryptIt as crypt

WINDOWNAME = "Password Data"
FONT_NAME = "JetBrains Mono"
DEFAULT_FONT_SETTINGS = (FONT_NAME, 12, "normal")
crypt=crypt()

class PasswordScreen:
    def __init__(self, data, key):
        self.data = data
        self.key = key
        self.setup_ui()

    def setup_ui(self):
        # Create the main window
        self.window = Tk()
        self.window.title(WINDOWNAME)
        self.window.config(padx=50, pady=50)

        # Create a frame to hold the Listbox and scrollbar
        frame = Frame(self.window)
        frame.grid(column=0, row=0, sticky="nsew")

        # Create a Listbox to display data
        self.listbox = Listbox(frame, font=DEFAULT_FONT_SETTINGS, width=50, height=15)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar
        frame_sb = Scrollbar(frame, orient="vertical", command=self.listbox.yview)
        frame_sb.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=frame_sb.set)

        # Populate the Listbox with data
        self.populate_listbox()

        # Configure row and column weights for resizing
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Start the main loop
        self.window.mainloop()

    def populate_listbox(self):
        """Adds data to the Listbox."""
        for website, details in self.data.items():
            encrypted_website = website
            encrypted_email = details.get('email', 'N/A')
            encrypted_password = details.get('password', 'N/A')
            print(encrypted_website)
            # Decrypt the values using the key
            decrypted_website = crypt.getDecrypt(encrypted_website, self.key) if encrypted_website != 'N/A' else 'N/A'
            decrypted_email = crypt.getDecrypt(encrypted_email, self.key) if encrypted_email != 'N/A' else 'N/A'
            decrypted_password = crypt.getDecrypt(encrypted_password,
                                                  self.key) if encrypted_password != 'N/A' else 'N/A'

            # Check the decrypted values (debugging)
            # print(f"Decrypted Website: {decrypted_website}")
            # print(f"Decrypted Email: {decrypted_email}")
            # print(f"Decrypted Password: {decrypted_password}")

            # Insert the decrypted website, email, and password into the Listbox
            self.listbox.insert(END, f"Website: {decrypted_website}")
            self.listbox.insert(END, f"  Email: {decrypted_email}")
            self.listbox.insert(END, f"  Password: {decrypted_password}")
            self.listbox.insert(END, "-" * 50)


