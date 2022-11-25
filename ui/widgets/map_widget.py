from functools import partial

from kivy.app import App
from kivy.properties import ListProperty, ObjectProperty
from kivy_garden.mapview import MapView, MapSource, MapMarker, MarkerMapLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer

from ui.constats import DARK_URL, LIGHT_URL, ATTR, ACTIVE_COLOR, DEACTIVE_COLOR
from util.bounded_polygon import BoundedPolygon
from util.search_tools import create_search_points


class MapWidget(MapView):
    map_markers = ListProperty([])

    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(
            zoom=3,
            lat=40.5,
            lon=-99.0,
    )
        if App.get_running_app().theme_cls.theme_style == "Dark":
            url = DARK_URL + App.get_running_app().mapbox_key
        else:
            url = LIGHT_URL + App.get_running_app().mapbox_key
        self.map_source = MapSource(url=url, image_ext="png", attribution=ATTR)
        self.active_polygon = None
        self.set_polygons = []
        self.collection = {
            "type": "FeatureCollection",
            "features": [],
        }

        self.geo_layer = GeoJsonMapLayer(geojson=self.collection)
        self.search_layer = MarkerMapLayer()

    def build_geo_layer(self):
        if self.geo_layer in self._layers:
            self.remove_layer(self.geo_layer)

        self.build_geo_features()

    def build_geo_features(self):
        if self.geo_layer in self._layers:
            self.remove_layer(self.geo_layer)
        if self.search_layer in self._layers:
            self.remove_layer(self.search_layer)

        # Add the active map polygon
        active_feature = []
        if self.active_polygon:
            active_feature = [self.active_polygon.build_geo_feature()]
            self.get_menu().set_polygon_active(
                self.active_polygon
            )
        else:
            self.get_menu().unset_polygon_active()
        # Add set polygons
        set_features = []
        for polygon in self.set_polygons:
            polygon.active = False
            set_features.append(polygon.build_geo_feature())

        # Add all polygons to layer
        self.collection["features"] = set_features + active_feature
        self.geo_layer = GeoJsonMapLayer(geojson=self.collection)
        self.add_layer(self.geo_layer)

        # Add search point markers if available
        self.search_layer = MarkerMapLayer()
        self.add_layer(self.search_layer)
        for polygon in self.set_polygons:
            polygon.markers = []
            for point in polygon.search_points:
                lat = point[0]
                lon = point[1]
                polygon.markers.append(MapMarker(lon=lon, lat=lat))
                self.add_marker(polygon.markers[-1], self.search_layer)

        self.do_update(0)

    def calculate_search_area(self, search_radius):
        for polygon in self.set_polygons:
            search_points = create_search_points(
                polygon.start_lat,
                polygon.stop_lat,
                polygon.start_lon,
                polygon.stop_lon,
                search_radius,
            )
            polygon.search_points = search_points
            polygon.search_radius = search_radius
        self.build_geo_features()

    def get_menu(self):
        return App.get_running_app().content.current_screen.get_menu()

    def remove_polygon(self, polygon):
        if self.active_polygon:
            if polygon.id == self.active_polygon.id:
                self.active_polygon = None
        if polygon in self.set_polygons:
            self.set_polygons.remove(polygon)
        self.build_geo_features()
        self.get_menu().update_set_polygons(self.set_polygons)

    def toggle_polygon(self, polygon):
        if polygon in self.set_polygons:
            if polygon.active:
                polygon.active = False
                self.active_polygon = None
                self.set_polygons.append(polygon)
            else:
                polygon.active = True
                self.active_polygon = polygon
                self.set_polygons.remove(polygon)
            self.build_geo_features()

    def store_polygon(self, polygon):
        polygon.active = False
        self.set_polygons.append(polygon)
        self.active_polygon = None
        for marker in self.map_markers:
            self.remove_marker(marker)
        self.map_markers = []
        self.build_geo_features()
        self.get_menu().update_set_polygons(self.set_polygons)

    def select_polygon(self, polygon):
        for p in self.set_polygons:
            p.active = False
            if p.id == polygon.id:
                p.active = True
                self.active_polygon = polygon
                self.set_polygons.remove(polygon)
        self.build_geo_features()

    def deselect_polygon(self, polygon):
        self.active_polygon = None
        polygon.active = False
        self.set_polygons.append(polygon)
        self.build_geo_features()

    def on_touch_down(self, touch):
        if touch.button == 'right':
            point = self.get_latlon_at(touch.x, touch.y, self.zoom)
            if len(self.map_markers) > 1:
                marker = self.map_markers.pop(1)
                self.remove_marker(marker)
            marker = MapMarker(lon=point.lon, lat=point.lat)
            marker_callback = partial(self.remove_marker_on_press, marker)
            marker.bind(on_press=marker_callback)
            self.map_markers.append(marker)
            self.add_marker(self.map_markers[-1])
            if len(self.map_markers) == 2:
                self.active_polygon = BoundedPolygon(
                    self.map_markers[0].lat,
                    self.map_markers[0].lon,
                    self.map_markers[1].lat,
                    self.map_markers[1].lon,
                    True
                )
                self.build_geo_layer()
            return
        return super().on_touch_down(touch)

    def remove_marker_on_press(self, marker, *args):
        self.map_markers.remove(marker)
        self.remove_marker(marker)
        if self.geo_layer in self._layers:
            self.remove_layer(self.geo_layer)
            self.get_menu().unset_polygon_active()
