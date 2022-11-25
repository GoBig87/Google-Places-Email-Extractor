import json

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from ui.widgets.toggle_row import ToggleRow
from ui.widgets.api_row import APIRow


Builder.load_string("""
<SettingsScreen>
    FloatLayout:
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            MDCard:
                size_hint: 0.9, 0.8
                orientation: "vertical"
                padding: dp(20), dp(20)
                spacing: dp(30)
                elevation: 1.5
                BoxLayout:
                    size_hint_y: 0.15
                    orientation: "horizontal"
                    MDLabel:
                        size_hint_x: 0.25
                        text: "GUI Params"
                        font_style: "H6"
                    Widget:
                        size_hint_x: 0.75
                ToggleRow:
                    id: theme_style
                    label: "Light/Dark Mode"
                    name: "theme_style"
                    size_hint_y: 0.15
                MDSeparator:
                    height: dp(1)
                BoxLayout:
                    size_hint_y: 0.15
                    orientation: "horizontal"
                    MDLabel:
                        size_hint_x: 0.25
                        text: "API Keys"
                        font_style: "H6"
                    Widget:
                        size_hint_x: 0.75
                APIRow:
                    id: google_api_key
                    label: "Google API Key"
                    icon_press: root.google_key_screen
                    size_hint_y: 0.15
                APIRow:
                    id: mapbox_api_key
                    label: "Mapbox API Key"
                    icon_press: root.mapbox_key_screen
                    size_hint_y: 0.15
                MDSeparator:
                    height: dp(1)
                BoxLayout:
                    size_hint_y: 0.15
                    orientation: "horizontal"
                    MDLabel:
                        size_hint_x: 0.25
                        text: "App Settings"
                        font_style: "H6"
                    Widget:
                        size_hint_x: 0.75
                APIRow:
                    id: clear_cache
                    label: "Clear Google Places ID cache"
                    icon: "delete"
                    icon_press: root.clear_cache
                    size_hint_y: 0.15
                APIRow:
                    id: reset_defaults
                    label: "Reset App to Default"
                    icon: "delete"
                    icon_press: root.reset_defaults
                    size_hint_y: 0.15
                Widget:
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "top"
            MDLabel:
                text: "Settings"
                font_style: "H6"
                bold: True
                halign: "center"
                valign: "bottom"
                size_hint_y:  None
                height: 50
        AnchorLayout:
            anchor_x: "left"
            anchor_y: "top"
            MDIconButton:
                icon: "keyboard-backspace"
                theme_icon_color: "Custom"
                icon_color: (0.5, 0.5, 0.5, 1)
                pos_hint: {"center_x": .5, "center_y": .5}
                on_press: root.map_screen()
            
""")


class SettingsScreen(Screen):
    google_key_screen = ObjectProperty()
    mapbox_key_screen = ObjectProperty()

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.ids["theme_style"].toggle_cb = self.handle_toggle_theme_style

    def clear_cache(self):
        with open("./cache.json", "w") as f:
            cache = []
            f.write(json.dumps(cache))

    def handle_toggle_theme_style(self, *args):
        self.clear_widgets()
        self.__init__()

    def google_key_screen(self):
        App.get_running_app().content.current = "settings_google_key"

    def mapbox_key_screen(self):
        App.get_running_app().content.current = "settings_mapbox_key"

    def map_screen(self):
        App.get_running_app().content.current = "main"

    def reset_defaults(self):
        with open("./settings.json", "w") as f:
            settings = {
                "color_mode": "Light",
                "zoom": 3,
                "lat": 40.5,
                "lon": -99.0
            }
            f.write(json.dumps(settings))