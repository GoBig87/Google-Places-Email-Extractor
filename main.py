import json
import os.path

from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import StringProperty
from kivy.config import Config

from ui.screens.google_key_screen import GoogleKeyScreen
from ui.screens.mapbox_key_screen import MapboxKeyScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.map_screeny import MainScreen

Config.set('input', 'mouse', 'mouse,disable_multitouch')


class MainApp(MDApp):
    google_key = StringProperty("")
    mapbox_key = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(".secrets"):
            os.mkdir(".secrets")
        if os.path.isfile(".secrets/googlekey"):
            with open(".secrets/googlekey", "r") as f:
                self.google_key = f.read()
        if os.path.isfile(".secrets/mapboxkey"):
            with open(".secrets/mapboxkey", "r") as f:
                self.mapbox_key = f.read()
        if not os.path.isfile("settings.json"):
            with open("./settings.json", "w") as f:
                settings = {
                      "color_mode": "Light",
                      "zoom": 3,
                      "lat": 40.5,
                      "lon": -99.0
                }
                f.write(json.dumps(settings))
        with open("settings.json") as f:
            self.settings = json.loads(f.read())

    def build(self):
        self.theme_cls.theme_style = self.settings.get("color_mode", "Light")
        self.mainbox = FloatLayout()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.content = ScreenManager()
        self.content.transition = NoTransition()
        self.main_screen = MainScreen(name="main")
        self.content.add_widget(self.main_screen)
        self.content.add_widget(SettingsScreen(name="settings"))
        self.content.add_widget(GoogleKeyScreen(name="googlekey", from_settings=False))
        self.content.add_widget(MapboxKeyScreen(name="mapboxkey", from_settings=False))
        self.content.add_widget(GoogleKeyScreen(name="settings_google_key", from_settings=True))
        self.content.add_widget(MapboxKeyScreen(name="settings_mapbox_key", from_settings=True))
        self.screens.add_widget(self.content)
        self.mainbox.add_widget(self.screens)

        if not self.google_key:
            self.content.current = "googlekey"
        elif not self.mapbox_key:
            self.content.current = "mapboxkey"
        else:
            self.content.current = "main"

        return self.mainbox

    def toggle_theme_style(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
        self.main_screen.clear_widgets()
        self.main_screen.__init__(name="main")
        self.settings["color_mode"] = self.theme_cls.theme_style
        with open("settings.json", "w") as f:
            f.write(json.dumps(self.settings))


MainApp().run()

