from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock 

from buiding import Buiding

class Background(Widget):
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def on_size(self, *args):
        self.floor_texture.uvsize = (self.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):
        self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + time_passed)%Window.width, self.floor_texture.uvpos[1])

        texture = self.property('floor_texture')
        texture.dispatch(self)

from random import randint

class MainApp(App):
    buids = []

    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)
    
    def start_game(self):
        Clock.schedule_interval(self.move_bird, 1/60.)

        num_buids = 5 
        distance_between_buids = Window.width / (num_buids - 1)
        for i in range(num_buids):
            buid = Buiding()
            buid.buid_center = randint(96 + 100, self.root.height - 100)
            buid.size_hint = (None, None)
            buid.pos = (i*distance_between_buids, 96)
            buid.size = (64, self.root.height - 96)

            self.buids.append(buid)
            self.root.add_widget(buid)

        Clock.schedule_interval(self.move_buids, 1/60.)
    
    def move(self, time_passed):
        for buid in self.buids:
            buid.x -= time_passed * 100
        
        num_buids = 5
        distance_between_buids = Window.width / (num_buids - 1)
        buid_xs = list(map(lambda buid: buid.x, self.buids))
        right_most_x = max(buid_xs)
        if right_most_x <= Window.width - distance_between_buids:
            most_left_buid = self.buids[buid_xs.index(min(buid_xs))]
            most_left_buid.x = Window.width