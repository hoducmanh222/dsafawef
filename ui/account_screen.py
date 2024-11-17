from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivy.properties import StringProperty
import re
import os

class AccountScreen(Screen):
    profile_image_path = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_profile_image_path()
        
    def set_profile_image_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.profile_image_path = os.path.join(current_dir, '..', 'photo', 'photo5.png')

class EditProfileScreen(Screen):
    pass

class ProfileApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file(os.path.join(os.path.dirname(__file__), 'account_screen.kv'))

    def back_action(self, *args):
        self.root.current = 'hello'


    def change_avatar(self):
        try:
            file_chooser = FileChooserListView()
            file_chooser.filters = ['*.png', '*.jpg', '*.jpeg']
            file_chooser.bind(on_selection=self.load_image)

            cancel_button = MDRaisedButton(
                text="Cancel",
                size_hint=(None, None),
                size=("120dp", "40dp"),
                pos_hint={"center_x": 0.5},
                on_release=self.close_dialog
            )

            self.dialog = MDDialog(
                title="Choose a new avatar",
                type="custom",
                content_cls=file_chooser,
                size_hint=(0.8, 0.8),
                buttons=[cancel_button]
            )
            self.dialog.open()
        except Exception as e:
            print(f"Error opening file chooser: {e}")

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def load_image(self, instance, value):
        if value:
            try:
                selected_image = value[0]
                if os.path.exists(selected_image):
                    self.root.get_screen('main').profile_image_path = selected_image
                    self.dialog.dismiss()
            except Exception as e:
                print(f"Error loading image: {e}")
                self.dialog.dismiss()

    def switch_to_edit_profile(self):
        self.root.current = "edit_profile"

    def back_to_main(self):
        self.root.current = "main"

    def show_country_menu(self, instance):
        # Country list remains the same
        countries = [
            "Afghanistan", "Albania", # ... (keep existing country list)
        ]
        menu_items = [{"viewclass": "OneLineListItem", "text": country, "on_release": lambda x=country: self.set_country(instance, x)} for country in countries]
        self.menu = MDDropdownMenu(caller=instance, items=menu_items, width_mult=4)
        self.menu.open()

    def set_country(self, instance, country):
        instance.text = country
        self.menu.dismiss()

    def toggle_password_visibility(self):
        password_field = self.root.get_screen("edit_profile").ids.password_field
        password_eye_icon = self.root.get_screen("edit_profile").ids.password_eye_icon

        if password_field.password:
            password_field.password = False
            password_eye_icon.icon = "eye"
        else:
            password_field.password = True
            password_eye_icon.icon = "eye-off"

    def save_changes(self):
        edit_screen = self.root.get_screen("edit_profile")
        main_screen = self.root.get_screen("main")
        
        # Validate email
        email = edit_screen.ids.email_field.text
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            self.dialog = MDDialog(
                title="Invalid Email",
                text="Please enter a valid email address.",
                buttons=[MDRectangleFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
            self.dialog.open()
            return

        # Update main screen labels
        main_screen.ids.name_label.text = f"Name: {edit_screen.ids.name_field.text}"
        main_screen.ids.dob_label.text = f"Date of Birth: {edit_screen.ids.dob_field.text}"
        main_screen.ids.country_label.text = f"Country: {edit_screen.ids.country_field.text}"
        main_screen.ids.email_label.text = f"Email: {email}"
        main_screen.ids.password_label.text = "Password: ************"

        self.root.current = "main"
