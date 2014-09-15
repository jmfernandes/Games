from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint



class FireBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class FireGame(Widget):
    ball = ObjectProperty(None)

    def on_touch_down(self, touch):
        with self.canvas:
            self.ball.center = (touch.x - self.ball.size[0] / 2, touch.y - self.ball.size[1] / 2)
            self.ball.velocity = Vector(randint(2, 6), randint(0, 3)).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()



class FireApp(App):
    def build(self):
        game = FireGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
	FireApp().run()