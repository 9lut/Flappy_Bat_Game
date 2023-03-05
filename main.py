from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock 
from kivy.core.audio import SoundLoader

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
from kivy.properties import NumericProperty

class Bat(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "bat2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bat1.png"
        super().on_touch_up(touch)
    
class MainApp(App):
    buids = []
    GRAVITY = 300
    was_colliding = False

    #def on_start(self):
       #Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)

    def move_bat(self, time_passed):
        bat = self.root.ids.bat
        bat.y = bat.y + bat.velocity * time_passed
        bat.velocity = bat.velocity - self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        bat = self.root.ids.bat
        
        is_colliding = False
        for buid in self.buids:
            if buid.collide_widget(bat):
                is_colliding = True
                
                if bat.y < (buid.buid_center - buid.GAP_SIZE/2.0):
                    self.game_over()
                if bat.top > (buid.buid_center + buid.GAP_SIZE/2.0):
                    self.game_over()
        if bat.y < 96:
            self.game_over()
        if bat.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_colliding = is_colliding
    
    def game_over(self):
        self.root.ids.bat.pos = (20, (self.root.height - 96) / 2.0)
        for buid in self.buids:
            self.root.remove_widget(buid)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

    def next_frame(self, time_passed):
        self.move_bat(time_passed)
        self.move(time_passed)
        self.root.ids.background.scroll_textures(time_passed)

    def start_game(self):
        self.sound = SoundLoader.load("song.mp3")
        self.sound.play()
        
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.buids = []
        #Clock.schedule_interval(self.move_bird, 1/60.)
        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

        num_buids = 5 
        distance_between_buids = Window.width / (num_buids - 1.7)
        for i in range(num_buids):
            buid = Buiding()
            buid.buid_center = randint(96 + 100, self.root.height - 100)
            buid.size_hint = (None, None)
            buid.pos = (Window.width + i*distance_between_buids, 96)
            buid.size = (64, self.root.height - 96)

            self.buids.append(buid)
            self.root.add_widget(buid)

            #Clock.schedule_interval(self.move_buids, 1/60.)
    
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


MainApp().run()   