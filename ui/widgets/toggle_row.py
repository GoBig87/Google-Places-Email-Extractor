from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


Builder.load_string("""
<ToggleRow>
    orientation: "vertical"
    BoxLayout:
        orientation: "horizontal"
        MDLabel:   
            text: root.label
            font_style: "Subtitle2"
        Widget:
        MDSwitch:
            id: switch
            name: root.name
            on_active: root.handle_toggle(self)
            active: root.switch_state
            pos_hint: {'center_x': .5, 'center_y': .5}
        MDIcon:
            icon: root.icon_name
            padding: "20dp", 0
            pos_hint: {'center_x': .5, 'center_y': .5}
""")


class ToggleRow(BoxLayout):
    icon_name = StringProperty("moon-waxing-crescent")
    label = StringProperty("")
    name = StringProperty("")
    handle_toggle = ObjectProperty()
    switch_state = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if App.get_running_app().theme_cls.theme_style == "Dark":
            self.icon_name = "moon-waxing-crescent"
            self.switch_state = False
        else:
            self.switch_state = True
            self.icon_name = "weather-sunny"

    def toggle_cb(self, *args):
        # Override in parent
        pass

    def handle_toggle(self, *args):
        App.get_running_app().toggle_theme_style()
        if App.get_running_app().theme_cls.theme_style == "Dark":
            self.icon_name = "moon-waxing-crescent"
        else:
            self.icon_name = "weather-sunny"
        self.toggle_cb()
