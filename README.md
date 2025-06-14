# Basic Password Manager

A simple, modern password manager built with Python and a beautiful UI using customTkinter. Securely store, generate, and manage your passwords locally.

## Features
- Modern, user-friendly interface (customTkinter)
- Secure password encryption
- Password generator
- View, search, and manage saved passwords
- Account creation and password reset

## How It Works

1. **Account Creation:**
   - When you first use the app, create a user account with a username and password.
   - Your password is securely hashed and stored locally.

2. **Login:**
   - Enter your username and password to log in.
   - The app verifies your credentials using secure hashing.

3. **Password Management:**
   - After logging in, you can add new passwords for different websites.
   - Each password entry includes a website, email/username, and password.
   - Passwords are encrypted using a key derived from your username and password.

4. **Password Generation:**
   - Use the built-in password generator to create strong, random passwords.
   - Generated passwords can be copied to your clipboard for easy use.

5. **Viewing and Searching:**
   - View all your saved passwords in a secure, organized list.
   - Search for passwords by website name.
   - All data is decrypted only when you are logged in.

6. **Data Storage:**
   - All user data and passwords are stored locally in JSON files.
   - No data is sent to the cloud or any external server.

7. **Security:**
   - Passwords are encrypted and can only be decrypted with your login credentials.
   - If you forget your password, you must reset it; passwords cannot be recovered.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Password-Manager-Basic
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```bash
   cd password-manager-start
   python3 main.py
   ```
2. Follow the on-screen instructions to create an account, log in, and manage your passwords.

## Dependencies
- customtkinter
- pyperclip
- pillow
- Python standard libraries: json, hashlib, random

## Credits
- UI: [customTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Developed by the open-source community

---
**Note:** All data is stored locally. Keep your encryption key and password safe!
