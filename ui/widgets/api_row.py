from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


Builder.load_string("""
<APIRow>
    orientation: "vertical"
    BoxLayout:
        orientation: "horizontal"
        MDLabel:   
            text: root.label
            font_style: "Subtitle2"
        Widget:
        MDLabel:
            id: switch
            text: root.key
            font_style: "Caption"
            halign: "right"
        MDIconButton:
            icon: root.icon
            pos_hint: {"center_x": .5, "center_y": 1}
            theme_icon_color: "Custom"
            icon_color: root.inactive_color
            on_press: root.icon_press()
""")


class APIRow(BoxLayout):
    icon = StringProperty("pencil")
    key = StringProperty("")
    label = StringProperty("")
    name = StringProperty("")
    icon_press = ObjectProperty()
    inactive_color = ListProperty([147/255, 147/255, 147/255, 1])

    def __init__(self, icon_press=None, **kwargs):
        super().__init__(**kwargs)
        self.on_icon_press = icon_press

