from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock

class Buiding(Widget):
    GAP_SIZE = NumericProperty(100)
    Head_SIZE = NumericProperty(20) 
    buid_center = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_head_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_head_position = NumericProperty(0)

    buid_body_texture = ObjectProperty(None)
    lower_buid_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_buid_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buid_body_texture = Image(source="body.png").texture
        self.buid_body_texture.wrap = 'repeat'

    def on_size(self, *args):
        lower_body_size = self.bottom_head_position - self.bottom_body_position

        self.lower_buid_tex_coords[5] = lower_body_size/20.
        self.lower_buid_tex_coords[7] = lower_body_size/20.

        top_body_size = self.top - self.top_body_position

        self.top_buid_tex_coords[5] = top_body_size/20.
        self.top_buid_tex_coords[7] = top_body_size/20.
    
    def on_pipe_center(self, *args):
        Clock.schedule_once(self.on_size, 0)