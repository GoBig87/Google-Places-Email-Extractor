from kivy.app import App
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty, ListProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

Builder.load_string("""
<SelectedAreaRow>:
    size_hint: (1, None)
    height:  dp(50)
    orientation: "horizontal"
    background_color: 0.5,.5,.5,.5
    padding: dp(25), 0
    MDFlatButton:
        id: button
        text: root.gps_start
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: root.toggle_selection()
    Widget:
        size_hint_x: 0.01
    MDIconButton:
        icon: "delete"
        pos_hint: {"center_x": .5, "center_y": .5}
        theme_icon_color: "Custom"
        icon_color: app.theme_cls.primary_color
        on_press: root.delete_polygon()
""")


class SelectedAreaRow(MDCard, ButtonBehavior):
    selected = BooleanProperty(False)
    gps_start = StringProperty("32.11 -80.32")
    inactive_color = ListProperty([147/255, 147/255, 147/255, 1])
    background_color = ListProperty([0.1, 0.5, 0.9, 1])
    toggle_selection = ObjectProperty()

    def __init__(self, polygon, **kwargs):
        super(SelectedAreaRow, self).__init__(**kwargs,)
        self.polygon = polygon
        self.gps_start = f"{round(self.polygon.start_lat, 2)}, " \
                         f"{round(self.polygon.start_lon, 2)}"

    def delete_polygon(self):
        self.get_map().remove_polygon(self.polygon)

    def get_menu(self):
        return App.get_running_app().content.current_screen.get_menu()

    def get_map(self):
        return App.get_running_app().content.current_screen.get_map()

    def toggle_selection(self):
        if not self.selected:
            self.ids.button.md_bg_color = self.inactive_color
            self.get_map().select_polygon(self.polygon)
        else:
            self.ids.button.md_bg_color = [1, 1, 1, 1]
            self.get_map().deselect_polygon(self.polygon)
        self.selected = not self.selected
