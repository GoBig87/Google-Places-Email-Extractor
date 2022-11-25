from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivy.core.window import Window


HYPER_LINK = [95/255, 181/255, 225/255]
HYPER_LINK_HOVER = [61/255,	147/255, 185/255]


class HyperLink(ButtonBehavior, MDLabel):
    def __init__(self, **kwargs):
        super(HyperLink, self).__init__(**kwargs)
        self.theme_text_color = "Custom"
        self.text_color = HYPER_LINK_HOVER
        Window.bind(mouse_pos=self.pos_check)

    def pos_check(self, inst, pos):
        if self.collide_point(*pos):
            self.text_color = HYPER_LINK_HOVER
        else:
            self.text_color = HYPER_LINK
