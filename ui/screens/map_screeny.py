from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from ui.widgets.menu_widget import MenuWidget
from ui.widgets.map_widget import MapWidget


Builder.load_string("""
<MainScreen>
    FloatLayout:
        AnchorLayout:
            anchor_x: "center"
            anchor_y: "center"
            MapWidget:
                id: map_widget
                size_hint: 1, 1
        MenuWidget:
            id: menu
            size_hint: 0.3, 1
        AnchorLayout:
            anchor_x: "right"
            anchor_y: "top"
            MDIconButton:
                icon: "cog"
                theme_icon_color: "Custom"
                icon_color: (0.5, 0.5, 0.5, 1)
                pos_hint: {"center_x": .5, "center_y": .5}
                on_press: root.settings_screen()
""")


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def get_menu(self):
        return self.ids["menu"]

    def get_map(self):
        return self.ids["map_widget"]

    def settings_screen(self):
        App.get_running_app().content.current = "settings"
