from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

g = -0.5

class FireBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def determineVelocity(self):
        self.velocity_y = self.velocity_y + g

    def move(self):
        # print(self.pos[1])
        self.pos = Vector(*self.velocity) + self.pos
        # if (self.y < 0):
        #     self.y = 0

class FireGame(Widget):
    ball = ObjectProperty(None)

    def on_touch_down(self, touch):
        with self.canvas:
            x_pos = touch.x - self.ball.size[0] / 2
            y_pos = touch.y - self.ball.size[1] / 2
            if (x_pos < self.ball.size[0]):
                x_pos = self.ball.size[0]+0
            if (y_pos < self.ball.size[1]):
                y_pos = self.ball.size[1]+0
            self.ball.center = (x_pos,y_pos)
            self.ball.velocity = Vector(randint(2, 6), randint(0, 3)).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.determineVelocity()
        self.ball.move()

        # bounce off bottom
        if (self.ball.y < 0):
            self.ball.y = 0
            self.ball.velocity_y *= -1*.85
            self.ball.velocity_x *= 1*.99

        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1



class FireApp(App):
    def build(self):
        game = FireGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
	FireApp().run()