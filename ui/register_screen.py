# register_screen.py
from kivymd.uix.screen import MDScreen
import json
import os
from hashlib import sha256

class RegisterScreen(MDScreen):
    def register(self):
        try:
            username = self.ids.username_field.text.strip()
            password = self.ids.password_field.text.strip()
            
            if not username or not password:
                self.ids.error_label.text = "Please fill all fields"
                return

            # Get absolute path to data directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)  # Go up one level
            data_dir = os.path.join(parent_dir, 'data')
            data_file = os.path.join(data_dir, 'data.json')

            # Create data directory if it doesn't exist
            os.makedirs(data_dir, exist_ok=True)

            # Load or create data
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {'users': []}

            # Add new user
            hashed_password = sha256(password.encode()).hexdigest()
            data['users'].append({
                'username': username,
                'password': hashed_password
            })

            # Save data
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Saved data to: {data_file}")  # Debug print
            self.manager.current = 'login'

        except Exception as e:
            print(f"Error saving data: {str(e)}")  # Debug print
            self.ids.error_label.text = f"Registration failed: {str(e)}"