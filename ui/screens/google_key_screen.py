import webbrowser

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

from ui.widgets.menu_widget import MenuWidget
from ui.widgets.map_widget import MapWidget
from ui.widgets.hyper_link import HyperLink
from ui.widgets.paste_textinput import RightClickTextInput


Builder.load_string("""
<GoogleKeyScreen>
    FloatLayout:
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            MDCard:
                id: google_card
                size_hint: 0.9, 0.7
                orientation: "vertical"
                padding: dp(20), dp(20)
                spacing: dp(20)
                elevation: 1.5
                BoxLayout:
                    size_hint_y: 0.15
                    orientation: "horizontal"
                    MDLabel:
                        size_hint_x: 0.4
                        text: "Google Places API Key"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: root.icon_color
                    Widget:
                        size_hint_x: 0.6
                MDLabel:
                    size_hint: 1, 0.25
                    text: "In order to make requests withe the Google Places API an API key is required.  API keys can be obtained from Google from the link below.  Then paste the API key below."
                    font_style: "Body1"
                    theme_text_color: "Custom"
                    text_color: root.icon_color
                HyperLink:
                    size_hint_y: 0.15
                    text: "Link to Google Places API Key"
                    font_style: "Subtitle2"
                    font_size: '14dp'
                    on_release: root.open_url(root.google_url)
                RightClickTextInput:
                    id: key_input
                    hint_text: "Paste Key Here"
                    mode: "rectangle"
                    multiline: True
                    use_bubble: True
                    on_text: root.handle_textinput()
                BoxLayout: 
                    orientation: "horizontal"
                    Widget:
                    MDFlatButton:
                        text: "Save Key"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        on_press: root.save_key()
                    Widget:
                Widget:   
                    size_hint_y: 0.15
        AnchorLayout:
            anchor_x: "right"
            anchor_y: "top"
            padding: dp(5), dp(10)
            id: switch_anchor
            MDCard:
                id: switch_card
                size_hint: None, None
                height: "50dp"
                width: "120dp"
                border_radius: 50
                radius: [25]
                elevation: 1
                Widget:
                MDSwitch:
                    id: switch
                    name: root.name
                    on_active: root.handle_toggle(self)
                    active: root.switch_state
                    pos_hint: {'center_x': .5, 'center_y': .5}
                MDIcon:
                    id: switch_icon
                    icon: root.icon_name
                    padding: "20dp", 0
                    theme_text_color: "Custom"
                    text_color: root.icon_color
                    pos_hint: {'center_x': .5, 'center_y': .5}
        AnchorLayout:
            anchor_x: "left"
            anchor_y: "top"
            MDIconButton:
                id: back
                icon: "keyboard-backspace"
                theme_icon_color: "Custom"
                icon_color: (0.5, 0.5, 0.5, 1)
                pos_hint: {"center_x": .5, "center_y": .5}
                on_press: root.settings_screen()
""")


class GoogleKeyScreen(Screen):
    google_url = StringProperty("https://developers.google.com/maps/documentation/places/web-service/get-api-key")
    google_key = StringProperty("")
    icon_name = StringProperty("moon-waxing-crescent")
    label = StringProperty("")
    name = StringProperty("")
    handle_toggle = ObjectProperty()
    switch_state = BooleanProperty(False)
    icon_color = ListProperty([1, 1, 1, 1])
    from_settings = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(GoogleKeyScreen, self).__init__(**kwargs)
        if App.get_running_app().theme_cls.theme_style == "Dark":
            self.icon_name = "moon-waxing-crescent"
            self.icon_color = [1, 1, 1, 1]
        else:
            self.icon_name = "weather-sunny"
            self.icon_color = [0, 0, 0, 1]

        Clock.schedule_once(self.add_corner_icons, 0.1)

    def add_corner_icons(self, dt):
        if self.from_settings:
            self.ids.switch_anchor.clear_widgets()
        else:
            self.ids.back.clear_widgets()

    def handle_textinput(self, *args):
        self.google_key = self.ids.key_input.text

    def handle_toggle(self, *args):
        App.get_running_app().toggle_theme_style()
        if App.get_running_app().theme_cls.theme_style == "Dark":
            self.icon_name = "moon-waxing-crescent"
            self.icon_color = [1, 1, 1, 1]
        else:
            self.icon_name = "weather-sunny"
            self.icon_color = [0, 0, 0, 1]

        Clock.schedule_once(self.ids.key_input.set_default_colors)
        self.ids.google_card.update_md_bg_color(self.ids.google_card, self.ids.google_card.theme_cls.theme_style)
        self.ids.google_card.update_md_bg_color(self.ids.google_card, self.ids.google_card.theme_cls.theme_style)
        self.ids.switch_card.update_md_bg_color(self.ids.switch_card, self.ids.switch_card.theme_cls.theme_style)
        self.ids.switch_card.update_md_bg_color(self.ids.switch_card, self.ids.switch_card.theme_cls.theme_style)

    def open_url(self, url):
        webbrowser.open(url)

    def save_key(self):
        if self.google_key:
            with open(".secrets/googlekey", "w") as f:
                f.write(self.google_key)
            App.get_running_app().google_key = self.google_key
            App.get_running_app().content.current = "mapboxkey"

    def settings_screen(self):
        App.get_running_app().content.current = "settings"
