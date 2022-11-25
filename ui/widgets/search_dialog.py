from threading import Thread

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from util.search_tools import search_places, make_csv_file

Builder.load_string("""
<SearchDialogContent>:
    orientation: "vertical"
    spacing: "5dp"
    size_hint_y: None
    height: "400dp"
    Widget:
        size_hint_y: 0.05    
    BoxLayout:
        orientation: "horizontal"
        MDLabel:
            text: "Business Name:"
            font_style: "H6"
            bold: True
        Widget:
    BoxLayout:
        orientation: "horizontal"
        Widget:   
            size_hint_x: 0.1    
        MDLabel:
            text: root.business_name
            font_style: "Subtitle1"
            halign: "left"
        Widget:   
            size_hint_x: 0.1    
    BoxLayout:
        orientation: "horizontal"
        MDLabel:
            text: "Business Address:"
            font_style: "H6"
            bold: True
        Widget:
    BoxLayout:
        orientation: "horizontal"
        Widget:   
            size_hint_x: 0.1    
        MDLabel:
            text: root.business_address
            font_style: "Subtitle1"
            halign: "left"
        Widget:   
            size_hint_x: 0.1   
    BoxLayout:
        orientation: "horizontal"
        MDLabel:
            size_hint_x: 0.25
            text: "Website:"
            font_style: "H6"
            bold: True
        Widget:
    BoxLayout:
        orientation: "horizontal"
        Widget:   
            size_hint_x: 0.1    
        MDLabel:
            text: root.website_address
            halign: "left"
            font_style: "Subtitle1"
        Widget:   
            size_hint_x: 0.1    
    BoxLayout:
        orientation: "horizontal"
        MDLabel:
            size_hint_x: 0.25
            text: "Email:"
            font_style: "H6"
            bold: True
        Widget:
        Widget:
    BoxLayout:
        orientation: "horizontal"
        Widget:   
            size_hint_x: 0.1     
        MDLabel:
            text: root.email_address
            font_style: "Subtitle1"
            halign: "left"
        Widget:
            size_hint_x: 0.1     
    Widget:
    Widget:
    MDProgressBar:
        value: root.progress
    BoxLayout:
        orientation: "horizontal"
        Widget:
            size_hint_x: 0.1     
        MDLabel:
            text: root.progress_text
            font_style: "Caption"
            bold: True
            halign: "center"
        Widget:
            size_hint_x: 0.1     
""")


class SearchDialogContent(BoxLayout):
    business_name = StringProperty("")
    business_address = StringProperty("")
    website_address = StringProperty("")
    email_address = StringProperty('')
    progress = NumericProperty(0)
    progress_text = StringProperty("")

    def __init__(self, **kwargs):
        super(SearchDialogContent, self).__init__(**kwargs)
        self.cancel = False

    def cancel_search(self, business_emails):
        if self.cancel:
            self.return_callback(business_emails)
            return True
        return False

    def get_map(self):
        return App.get_running_app().content.current_screen.get_map()

    def get_menu(self):
        return App.get_running_app().content.current_screen.get_menu()

    def on_dismiss(self, dialog):
        dialog.dismiss()

    def on_open(self, *args):
        thread = Thread(target=self.start_search_thread)
        thread.start()

    def start_search_thread(self):
        polygons = self.get_map().set_polygons
        search_radius = 0
        search_points = []
        for polygon in polygons:
            if search_radius < polygon.search_radius:
                search_radius = polygon.search_radius
            search_points = search_points + polygon.search_points

        search_places(
            search_points,
            search_radius,
            keyword=self.get_menu().search_term,
            key=App.get_running_app().google_key,
            gui_update=self.set_gui,
            request_cancel=self.cancel_search,
            return_callback=self.return_callback
        )

    def set_gui(self, name, address, website, email, count, total):
        self.progress_text = f"{count}/{total} points"
        self.progress = round(count/total, 2)*100
        self.business_name = name
        self.business_address = address
        self.website_address = website
        self.email_address = email

    def reset_gui(self):
        self.business_name = ""
        self.business_address = ""
        self.website_address = ""
        self.email_address = ""
        self.progress = 0
        self.progress_text = 0

    def return_callback(self, business_emails):
        file_name = self.get_menu().file_name
        make_csv_file(file_name, business_emails)
        self.cancel = False
        self.parent.parent.parent.dismiss()