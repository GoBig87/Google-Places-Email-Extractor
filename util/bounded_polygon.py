import shortuuid
from kivy.app import App

from ui.constats import DEACTIVE_COLOR, ACTIVE_COLOR


class BoundedPolygon:
    def __init__(self, start_lat, start_lon, stop_lat, stop_lon, active):
        self.id = shortuuid.uuid()
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.active = active

        # unset params
        self.search_radius = 0
        self.search_points = []
        self.markers = []

    def toggle_state(self):
        self.active = not self.active

    def build_geo_feature(self):
        if self.active:
            color = ACTIVE_COLOR
        else:
            if App.get_running_app().theme_cls.theme_style == "Dark":
                color = "#FFFFFF50"
            else:
                color = DEACTIVE_COLOR
        return {
            "type": "Feature",
            "properties": {
                "id": self.id,
                "color": color,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [self.start_lon, self.start_lat],
                        [self.stop_lon, self.start_lat],
                        [self.stop_lon, self.stop_lat],
                        [self.start_lon, self.stop_lat],
                    ]
                ]
            },
        }
