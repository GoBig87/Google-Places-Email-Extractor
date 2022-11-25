from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from ui.widgets.search_dialog import SearchDialogContent
from ui.widgets.selected_area_row import SelectedAreaRow
from util.search_tools import create_search_points

Builder.load_string("""
<MenuWidget>:
    id: menu_widget
    anchor_x: "left"
    anchor_y: "center"
    MDCard:
        orientation: 'vertical'
        radius: 0
        BoxLayout:
            orientation: "vertical"
            size_hint_y: 0.25
            Widget:
                size_hint_y: 0.075
            MDLabel:
                text: "Selected Areas"
                font_style: "Subtitle2"
                padding:  dp(10), dp(20)
                size_hint_y: 0.10   
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                MDBoxLayout:
                    id: selection
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
            MDRectangleFlatIconButton:
                text: "Add Section"
                icon: "map-marker-plus-outline"
                line_color: 0, 0, 0, 0
                theme_icon_color: "Custom"
                icon_color: app.theme_cls.primary_color if root.polygon_active else root.inactive_color
                text_color: app.theme_cls.primary_color if root.polygon_active else root.inactive_color
                on_press: root.add_map_section()
                pos_hint: {"center_x": .5, "center_y": 1}
            Widget:
                size_hint_y: 0.05
        MDSeparator:
        BoxLayout:
            id: settings
            orientation: 'vertical'
            size_hint_y: 0.20
            MDLabel:
                text: "Search Area Params"
                font_style: "Subtitle2"
                padding:  dp(10), dp(20)
                size_hint_y: 0.25
            BoxLayout:
                orientation: 'horizontal'
                padding:  dp(15), dp(10)
                size_hint_y: 0.25
                MDTextField:
                    id: calc_field
                    hint_text: "Search Radius (m)"
                    input_filter: 'int'
                    on_text: root.handle_calc_field()
            MDRectangleFlatIconButton:
                text: "Calculate Search Points"
                icon: "calculator"
                line_color: 0, 0, 0, 0
                icon_color: app.theme_cls.primary_color if root.calc_ready else root.inactive_color
                text_color: app.theme_cls.primary_color if root.calc_ready else root.inactive_color
                pos_hint: {"center_x": .5, "center_y": 1}
                on_press: root.calculate_search_area()
            Widget:
                size_hint_y: 0.05       
        MDSeparator:
        BoxLayout:
            id: settings
            orientation: 'vertical'
            size_hint_y: 0.15
            Widget:
                size_hint_y: 0.05
            MDLabel:
                text: "Select File"
                font_style: "Subtitle2"
                padding:  dp(10), dp(20)
                size_hint_y: 0.10   
            BoxLayout:
                orientation: 'horizontal'
                padding:  dp(15), dp(15)
                size_hint_y: 0.20
                MDTextField:
                    id: file_field
                    hint_text: "File Name"
                    on_text: root.handle_file_field()
                MDIconButton:
                    icon: "file"
                    pos_hint: {"center_x": .5, "center_y": 1}
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color if root.area_set else root.inactive_color
                    on_press: root.delete_polygon()
        MDSeparator:
        BoxLayout:
            id: settings
            orientation: 'vertical'
            size_hint_y: 0.20
            Widget:
                size_hint_y: 0.05
            MDLabel:
                text: "Search Term Params"
                font_style: "Subtitle2"
                padding:  dp(10), dp(20)
                size_hint_y: 0.10   
            BoxLayout:
                orientation: 'horizontal'
                padding:  dp(15), dp(15)
                size_hint_y: 0.20
                MDTextField:
                    id: search_field
                    hint_text: "Search Term"
                    on_text: root.handle_search_field()
            MDRectangleFlatIconButton:
                text: "Start Search"
                icon: "email-search"
                line_color: 0, 0, 0, 0
                icon_color: app.theme_cls.primary_color if root.search_ready else root.inactive_color
                text_color: app.theme_cls.primary_color if root.search_ready else root.inactive_color
                pos_hint: {"center_x": .5, "center_y": 1}
                on_press: root.start_search()
        Widget:
            size_hint_y: 0.05
                
""")


class MenuWidget(AnchorLayout):
    polygon_active = BooleanProperty(False)
    area_set = BooleanProperty(False)
    calc_ready = BooleanProperty(False)
    search_ready = BooleanProperty(False)
    inactive_color = ListProperty([147/255, 147/255, 147/255, 1])
    search_radius = NumericProperty()
    file_name = StringProperty()
    search_term = StringProperty()
    search_started = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MenuWidget, self).__init__(**kwargs)
        self.selected_polygon = None
        self.search_points = []
        self.stored_polygon = []
        Clock.schedule_once(self.build_selection)

        self.search_dialog_content = SearchDialogContent()
        self.dialog = MDDialog(
            title="Searching...",
            type="custom",
            auto_dismiss=False,
            content_cls=self.search_dialog_content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=App.get_running_app().theme_cls.primary_color,
                    on_release=self.request_cancel,
                ),
            ],
        )
        self.dialog.on_open = self.search_dialog_content.on_open

    def request_cancel(self, *args):
        self.search_dialog_content.cancel = True

    def add_map_section(self):
        if self.selected_polygon:
            print(f"polygon id: {self.selected_polygon.id}")
            self.get_map().store_polygon(self.selected_polygon)

    def build_selection(self, dt):
        print(self.ids)
        self.ids.selection.clear_widgets()
        if not self.stored_polygon:
            self.ids.selection.add_widget(MDLabel(
                text="No Areas Selected",
                size_hint=(1, None),
                height=dp(50),
                padding=(dp(29), 0),
                halign="left",
                theme_text_color="Custom",
                text_color=self.inactive_color,
            ))
        else:
            for polygon in self.stored_polygon:
                self.ids.selection.add_widget(SelectedAreaRow(polygon))

    def calculate_search_area(self):
        self.get_map().calculate_search_area(self.search_radius)

    def get_map(self):
        return App.get_running_app().content.current_screen.get_map()

    def handle_calc_field(self):
        self.search_radius = int(self.ids.calc_field.text)
        if self.area_set and self.search_radius >= 1:
            self.calc_ready = True
        else:
            self.calc_ready = False

    def handle_file_field(self):
        self.file_name = self.ids.file_field.text
        if self.file_name and self.calc_ready:
            self.search_ready = True
        else:
            self.search_ready = False

    def handle_search_field(self):
        self.search_field = self.ids.search_field.text

    def set_polygon_active(self, polygon):
        self.selected_polygon = polygon
        self.polygon_active = True

    def start_search(self):
        print("starting search")
        self.search_started = True
        self.dialog.open()

    def unset_polygon_active(self):
        self.selected_polygon = None
        self.polygon_active = False

    def update_set_polygons(self, set_polygons):
        self.stored_polygon = set_polygons
        Clock.schedule_once(self.build_selection)
        if self.stored_polygon:
            self.area_set = True
        else:
            self.area_set = False
