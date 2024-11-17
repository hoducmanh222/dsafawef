# login_screen.py
from kivymd.uix.screen import MDScreen
import json
import os
from hashlib import sha256

class LoginScreen(MDScreen):
    def login(self):
        try:
            username = self.ids.username_field.text.strip()
            password = self.ids.password_field.text.strip()
            
            if not username or not password:
                self.ids.error_label.text = "Please fill all fields"
                return
                
            # Get data file path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            data_file = os.path.join(parent_dir, 'data', 'data.json')
            
            print(f"Looking for data file at: {data_file}")  # Debug
            
            with open(data_file, 'r') as f:
                data = json.load(f)
                
            # Hash password for comparison
            hashed_password = sha256(password.encode()).hexdigest()
            print(f"Checking credentials for user: {username}")  # Debug
            
            # Check credentials
            for user in data.get('users', []):
                if user['username'] == username and user['password'] == hashed_password:
                    print("Login successful - switching to hello screen")  # Debug
                    self.ids.error_label.text = ""
                    self.manager.current = 'hello'
                    return
                    
            print("Invalid credentials")  # Debug
            self.ids.error_label.text = "Invalid username or password"
            
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug
            self.ids.error_label.text = f"Login failed: {str(e)}"

        