from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty, \
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class ParticleBall(Widget):
	velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class FireGame(Widget):
	particle = ObjectProperty(None)
	# ball = ObjectProperty(None)

	# def serve_ball(self):
	# 	self.ball.center = self.center
		# self.ball.Color = self.color
	# def on_touch_down(self, touch):
	# 	with self.canvas:
	# 		# Color(1, 1, 0)
	# 		d = 30.
			# self.ball.center = self.center
	# 		# Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
	# 		# self.particle
		

class FireApp(App):
	def build(self):
		game = FireGame()
		# game.serve_ball()
		return game

if __name__ == '__main__':
	FireApp().run()