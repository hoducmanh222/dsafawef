import json
import os
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from ui.ui import LoginScreen, HelloScreen, AccountScreen, DeadlinesScreen, Feature3_Screen, Feature4_Screen, RegisterScreen
from kivy.core.window import Window

Window.size = (360, 800)

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None  # Store current username

    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.screen_manager = ScreenManager()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        Builder.load_file('ui/kv/login.kv')
        Builder.load_file('ui/kv/hello.kv')
        Builder.load_file('ui/kv/account.kv')
        Builder.load_file('ui/kv/deadlines.kv')
        Builder.load_file('ui/kv/feature3.kv')
        Builder.load_file('ui/kv/feature4.kv')
        Builder.load_file('ui/kv/register.kv')
        
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(HelloScreen(name='hello'))
        self.screen_manager.add_widget(AccountScreen(name='account'))
        self.screen_manager.add_widget(DeadlinesScreen(name='deadlines'))
        self.screen_manager.add_widget(Feature3_Screen(name='feature3'))
        self.screen_manager.add_widget(Feature4_Screen(name='feature4'))
        self.screen_manager.add_widget(RegisterScreen(name='register'))

        return self.screen_manager

    def switch_screen(self, screen_name):
        try:
            print(f"Switching to screen: {screen_name}")  # Debug
            self.screen_manager.current = screen_name
        except Exception as e:
            print(f"Error switching screens: {str(e)}")

if __name__ == '__main__':
    MainApp().run()