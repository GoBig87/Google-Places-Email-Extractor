from kivy.base import EventLoop
from kivymd.uix.textfield import MDTextField


class RightClickTextInput(MDTextField):
    def on_touch_down(self, touch):
        super(RightClickTextInput, self).on_touch_down(touch)
        if touch.button == 'right':
            print("right mouse clicked")
            pos = super(RightClickTextInput, self).to_local(*self._touch_down.pos, relative=True)
            self._show_cut_copy_paste(touch.pos, EventLoop.window, mode='paste')


