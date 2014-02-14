import sys, pygame, random, euclid, math
from pygame.locals import *

# pygame.init()
#clock = pygame.time.Clock()

# SunSurfaceObj = pygame.image.load('img/sun.png')
# windowSurfaceObj = pygame.display.set_mode((640,480))
#pygame.display.set_caption('Particle Game')

clock = pygame.time.Clock()
fps_limit = 60

black = 0,0,0
white = 255,255,255
red = 255,0,0
green=0,255,0
blue=0,0,255

colors = [black, red, green, blue]

initial_velocity = 20;
number_of_circles = 10
my_circles = []
# for n in range(number_of_circles):
#     size = random.randint(10,20)
#     x = random.randint(size, game.width-size)
#     y = random.randit(size, game.height-size)
#     color = random.choice(colors)
#     my_circles.append(MySun((x,y),size,color))


redColor = 255,0,0
whiteColor = pygame.Color(255,255,255)
mousex, mousey = 250,250

direction_tick = 0.0

def populate():
    for n in range(number_of_circles):
            size = random.randint(10,20)
            x = random.randint(size, game.width-size)
            y = random.randint(size, game.height-size)
            color = random.choice(colors)
            velocity = get_random_velocity()
            my_circle = MySun(euclid.Vector2(x,y),size,color,velocity)
            my_circles.append(my_circle)

def get_random_velocity():
    new_angle = random.uniform(0, math.pi*2)
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = euclid.Vector2(new_x,new_y)
    new_vector.normalize()
    new_vector *= initial_velocity #pixels per second
    return new_vector

class MySun:
    def __init__(self, position, size, color = (255,255,255), velocity = euclid.Vector2(0,0), width = 1):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.color = color
        self.width = width

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        self._image_surf = pygame.image.load('img/sun.png').convert()
        pygame.draw.circle(game._display_surf, self.color, (rx,ry), self.size, self.width)
        #self._display_surf.blit(self._image_surf,(x,y))

    def move(self):
        self.position += self.velocity*game.dtime
        self.bounce()

    def change_velocity(self, velocity):
        self.velocity = velocity

    def bounce(self):
        if self.position.x <= self.size:
            self.position.x = 2*self.size - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1,0))
        elif self.position.x >= game.width - self.size:
            self.position.x = 2*(game.width - self.size) - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1,0))
        elif self.position.y <= self.size:
            self.position.y = 2*self.size - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0,1))
        elif self.position.y >= game.height - self.size:
            self.position.y = 2*(game.height - self.size) - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0,1))




class Game(object):
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.size = self.width, self.height = 1040, 650
        pygame.display.set_caption('Particle Game')
    def on_init(self):
        pygame.init()
        self.direction_tick = 0.0
        # clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(whiteColor)
        #self._image_surf = pygame.image.load('img/sun.png').convert()
        populate() 
        self._running = True
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        self.dtime_ms = clock.tick(fps_limit)
        self.dtime = self.dtime_ms/1000.0

        self.direction_tick +=self.dtime
        if (self.direction_tick > 1.0):
            self.direction_tick = 0.0
            random_circle = random.choice(my_circles)
            new_velocity = get_random_velocity()
            random_circle.change_velocity(new_velocity)
        pygame.display.flip()



    def on_render(self):
        #my_sun = MySun((100,100),20, redColor)
        #my_sun.display()
        #\self._display_surf.blit(self._image_surf,(200,100))
        self._display_surf.lock()
        self._display_surf.fill(white)
        for my_circle in my_circles:
            my_circle.move()
            my_circle.display()
        #pygame.display.flip()
        # self._display_surf.lock()
        # self._display_surf.fill(white)
        self._display_surf.unlock()
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__=='__main__':
    game = Game()
    game.on_execute()