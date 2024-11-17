import json
from kivymd.uix.screen import MDScreen
from datetime import datetime, timedelta
from kivy.metrics import dp
from calendar import day_name
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar
import os

class HelloScreen(MDScreen):
    def __init__(self, **kwargs):
        self.app = kwargs.pop('app', None)
        super(HelloScreen, self).__init__(**kwargs)
        self.dialog = None
        self.calendar_populated = False
        self.current_date = datetime.now()
        self.day_offset = 0
        self.schedules = self.load_schedules()  # Load schedules from JSON file

    def on_enter(self, *args):
        super().on_enter(*args)
        self.update_greeting()
        if not self.calendar_populated:
            self.populate_calendar_bar()
            self.calendar_populated = True
        self.show_schedules_for_day(self.current_date)  # Show today's schedule by default

    def update_greeting(self):
        current_time = datetime.now().time()
        
        try:
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json')
            with open(data_path, 'r') as f:
                user_data = json.load(f)
                username = user_data.get('username', 'User')
        except FileNotFoundError:
            username = self.manager.get_screen('login').ids.username.text


        if current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
            greeting = "Good Morning"
        elif current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        self.ids.greeting_label.text = f"{greeting},\n{username}!"


    def populate_calendar_bar(self):
        self.ids.calendar_bar.clear_widgets()
        self.display_week(self.current_date)

    def display_week(self, center_date=datetime.now()):
        now = center_date
        day_width = self.width / 10
        
        temp_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), padding=[dp(10), dp(20), dp(10), dp(10)])

        for i in range(-3, 4):  # Display a week (3 days before, today, and 3 days after)
            date = now + timedelta(days=i)
            day_label = MDLabel(
                text=str(date.day),
                halign='center',
                theme_text_color='Primary',
                size_hint=(None, None),
                size=(day_width, day_width),
                font_style='H6',
                font_size='14.5sp'
            )

            weekday_label = MDLabel(
                text=day_name[date.weekday()][:3],
                halign='center',
                theme_text_color='Secondary',
                size_hint=(None, None),
                size=(day_width, dp(20)),
                font_style='Caption',
                font_size='12sp'
            )

            day_box = MDBoxLayout(orientation='vertical', size_hint=(None, None), size=(day_width, day_width + dp(10)))
            day_box.add_widget(day_label)
            day_box.add_widget(weekday_label)

            # Highlight today's date only
            if date.date() == datetime.now().date():
                with day_box.canvas.before:
                    Color(252/255.0, 221/255.0, 230/255.0, 1)  # Highlight color with red for the day of today
                    self.today_rect = RoundedRectangle(size=(day_box.width + dp(20), day_box.height + dp(20)),
                                                       pos=(day_box.x - dp(10), day_box.y - dp(10)),
                                                       radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
                    day_box.bind(size=self.update_today_rect, pos=self.update_today_rect)

            # Highlight the selected date with pastel blue
            if date.date() == self.current_date.date() and date.date() != datetime.now().date():
                with day_box.canvas.before:
                    Color(0.68, 0.85, 0.90, 1)  # Pastel blue color
                    self.selected_date_rect = RoundedRectangle(size=(day_box.width + dp(20), day_box.height + dp(20)),
                                                               pos=(day_box.x - dp(10), day_box.y - dp(10)),
                                                               radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
                    day_box.bind(size=self.update_selected_date_rect, pos=self.update_selected_date_rect)

            day_box.bind(on_touch_down=lambda instance, touch, date=date: self.on_day_selected(instance, touch, date=date))

            temp_layout.add_widget(day_box)

        self.ids.calendar_bar.add_widget(temp_layout)

    def on_day_selected(self, instance, touch, date):
        if instance.collide_point(*touch.pos):
            self.current_date = date
            self.day_offset = 0  # Reset the day offset to center around the selected date
            self.populate_calendar_bar()
            self.show_schedules_for_day(date)

    def update_today_rect(self, instance, _):
        if self.today_rect:
            self.today_rect.pos = (instance.x - dp(10), instance.y - dp(10))
            self.today_rect.size = (instance.width + dp(20), instance.height + dp(20))

    def update_selected_date_rect(self, instance, _):
        if self.selected_date_rect:
            self.selected_date_rect.pos = (instance.x - dp(10), instance.y - dp(10))
            self.selected_date_rect.size = (instance.width + dp(20), instance.height + dp(20))

    def show_add_schedule_dialog(self):
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="400dp"
        )

        self.schedule_title = MDTextField(
            hint_text="Enter schedule title",
            size_hint_y=None,
            height="40dp"
        )
        self.schedule_description = MDTextField(
            hint_text="Enter schedule description",
            size_hint_y=None,
            height="40dp"
        )

        self.schedule_date = MDTextField(
            hint_text="Select schedule date",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )

        self.schedule_time = MDTextField(
            hint_text="Select schedule time",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )

        date_button = MDRaisedButton(
            text="Pick Date",
            size_hint_y=None,
            height="35dp",
            width="100dp",
            on_release=self.show_date_picker
        )

        time_button = MDRaisedButton(
            text="Pick Time",
            size_hint_y=None,
            height="40dp",
            on_release=self.show_time_picker
        )

        layout.add_widget(self.schedule_title)
        layout.add_widget(self.schedule_description)
        layout.add_widget(self.schedule_date)
        layout.add_widget(date_button)
        layout.add_widget(self.schedule_time)
        layout.add_widget(time_button)

        self.dialog = MDDialog(
            title="Add Schedule",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="ADD",
                    on_release=self.add_schedule
                )
            ]
        )

        self.dialog.open()

    def add_schedule(self, *_):
        title = self.schedule_title.text
        description = self.schedule_description.text
        date = self.schedule_date.text
        time = self.schedule_time.text

        if date not in self.schedules:
            self.schedules[date] = []

        self.schedules[date].append({
            'title': title,
            'description': description,
            'time': time
        })

        self.save_schedules()  # Save schedules to JSON file

        self.dialog.dismiss()
        self.populate_calendar_bar()  # Refresh the calendar to show the new schedule

    def close_dialog(self, *_):
        self.dialog.dismiss()

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.schedule_date.text = value.strftime('%d/%m/%Y')

    def show_time_picker(self, *args):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.on_time_selected)
        time_dialog.open()

    def on_time_selected(self, instance, time):
        self.schedule_time.text = str(time)

    def show_schedules_for_day(self, date):
        date_str = date.strftime('%d/%m/%Y')
        schedules = self.schedules.get(date_str, [])

        self.ids.schedule_box.clear_widgets()

        if not schedules:
            self.ids.schedule_box.add_widget(
                MDLabel(
                    text="No schedules for this day.",
                    halign='center',
                    valign='middle',
                    theme_text_color='Secondary',
                    size_hint_y=None,
                    height=dp(50),
                    text_size=(self.ids.schedule_scroll.width - dp(20), None),
                    font_style='H6',  # Adjust font style as needed
                    bold=True
                )
            )
            return

        # Sort schedules by time, ignoring empty time fields
        schedules.sort(
            key=lambda x: datetime.strptime(x['time'], '%H:%M:%S') if x['time'] else datetime.min
        )

        for schedule in schedules:
            schedule_layout = MDCard(
                orientation='horizontal',
                padding=dp(10),
                size_hint_y=None,
                height=dp(60),
                md_bg_color=(0.9, 0.9, 0.9, 1)
            )

            clock_icon = MDIconButton(
                icon='calendar-clock',
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                theme_text_color='Primary'
            )
            time_label = MDLabel(
                text=datetime.strptime(schedule['time'], '%H:%M:%S').strftime('%H:%M') if schedule['time'] else '',
                halign='left',
                theme_text_color='Primary',
                size_hint=(None, None),
                size=(dp(60), dp(40)),
                font_style='H6',
                font_size='9sp'
            )

            title_label = MDLabel(
                text=schedule['title'],
                halign='left',
                theme_text_color='Primary',
                size_hint=(None, None),
                size=(dp(65), dp(40)),
                font_style='H6',
                font_size='9sp'
            )

            description_label = MDLabel(
                text=schedule['description'],
                halign='left',
                theme_text_color='Secondary',
                size_hint=(None, None),
                size=(dp(95), dp(40)),
                font_style='Caption',
                font_size='9sp'
            )

            edit_button = MDIconButton(
                icon='pencil',
                size_hint=(None, None),
                size=(dp(10), dp(24)),
                theme_text_color='Primary',
                on_release=lambda x, s=schedule: self.edit_schedule(date_str, s)
            )

            delete_button = MDIconButton(
                icon='delete',
                size_hint=(None, None),
                size=(dp(20), dp(24)),
                theme_text_color='Error',
                on_release=lambda x, s=schedule: self.delete_schedule(date_str, s)
            )

            schedule_layout.add_widget(clock_icon)
            schedule_layout.add_widget(time_label)
            schedule_layout.add_widget(title_label)
            schedule_layout.add_widget(description_label)
            schedule_layout.add_widget(edit_button)
            schedule_layout.add_widget(delete_button)

            self.ids.schedule_box.add_widget(schedule_layout)

    from kivymd.uix.dialog import MDDialog

    def delete_schedule(self, date_str, schedule):
        self.schedules[date_str].remove(schedule)
        self.save_schedules()
        self.show_schedules_for_day(self.current_date)
        
        # Create and show the dialog
        self.dialog = MDDialog(
            text="Schedule deleted",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def edit_schedule(self, date_str, schedule):
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="400dp"
        )

        self.schedule_title = MDTextField(
            text=schedule['title'],
            hint_text="Title",
            size_hint_y=None,
            height="40dp"
        )
        self.schedule_description = MDTextField(
            text=schedule['description'],
            hint_text="Description",
            size_hint_y=None,
            height="40dp"
        )
        self.schedule_date = MDTextField(
            text=date_str,
            hint_text="Date",
            readonly=True,
            size_hint_y=None,
            height="40dp"
        )
        self.schedule_time = MDTextField(
            text=schedule['time'],
            hint_text="Time",
            readonly=True,
            size_hint_y=None,
            height="40dp"
        )

        date_button = MDRaisedButton(
            text="Pick Date",
            size_hint=(None, None),
            height="40dp",
            pos_hint={'center_x': 0.5},
            on_release=self.show_date_picker
        )

        time_button = MDRaisedButton(
            text="Pick Time",
            size_hint=(None, None),
            height="40dp",
            pos_hint={'center_x': 0.5},
            on_release=self.show_time_picker
        )

        layout.add_widget(self.schedule_title)
        layout.add_widget(self.schedule_description)
        layout.add_widget(self.schedule_date)
        layout.add_widget(date_button)
        layout.add_widget(self.schedule_time)
        layout.add_widget(time_button)

        self.dialog = MDDialog(
            title="Edit Schedule",
            type="custom",
            content_cls=layout,
            size_hint=(0.8, None),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="SAVE",
                    theme_text_color="Custom",
                    on_release=lambda x: self.save_edited_schedule(schedule)
                ),
            ],
        )
        self.dialog.open()

    def save_edited_schedule(self, old_schedule):
        title = self.schedule_title.text
        description = self.schedule_description.text
        date = self.schedule_date.text
        time = self.schedule_time.text

        if title and date:
            for schedule in self.schedules[date]:
                if schedule == old_schedule:
                    schedule['title'] = title
                    schedule['description'] = description
                    schedule['day'] = date
                    schedule['time'] = time
                    break
            
            self.save_schedules()
            self.show_schedules_for_day(self.current_date)
            self.dialog.dismiss()



    def load_schedules(self):
        try:
            with open(r'..\data\schedules.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_schedules(self):
        with open(r'..\data\schedules.json', 'w') as f:
            json.dump(self.schedules, f)

    from kivy.properties import StringProperty
    photo_path1 = StringProperty()
    photo_path2 = StringProperty()
    photo_path3 = StringProperty()
    
    def get_photo_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while not os.path.basename(current_dir).lower().endswith('app-master'):
            current_dir = os.path.dirname(current_dir)
        return os.path.join(current_dir, 'photo')
        
    def on_kv_post(self, *args):
        photo_dir = self.get_photo_path()
        self.photo_path1 = os.path.join(photo_dir, 'photo3.png')
        self.photo_path2 = os.path.join(photo_dir, 'photo5.png')
        self.photo_path3 = os.path.join(photo_dir, 'photo6.png')

