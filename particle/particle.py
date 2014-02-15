import sys, pygame, random, euclid, math
from pygame.locals import *

clock = pygame.time.Clock() #set up the clock
fps_limit = 30 #limit how fast the while loop runs

clicks = 0

# establish colors
black = 0,0,0
white = 255,255,255
red = 255,0,0
green=0,255,0
blue=0,0,255
colors = [black, red, green, blue] #put colors in array
#======================================================


#establish parameters
gravity = euclid.Vector2(0.0, 80.0)
drag = 0.1
elasticity = .1
min_velocity = 15
max_velocity = 25
initial_velocity = 20;
#===================================================

max_circles_on_screen = 60
my_circles = [] #set up empty array to contain my list of objects


def populate():
    mx, my = pygame.mouse.get_pos() #saves x and y position of cursor as mx and my respectively
    mx += random.randint(-2,2)
    my += random.randint(-2,2)
    size = 30 #the inner radius of circles in pixels
    color = random.choice(colors) #chooses random element of colors list
    velocity = get_random_velocity() #runs the get_random_velocity definition
    #establishes my_circle as a class object
    my_circle = MySun(euclid.Vector2(mx,my),size,color,velocity, gravity)
    my_circles.append(my_circle) #adds the my_circle object to the list


def get_random_velocity():
    new_angle = random.uniform(0, math.pi*2) #creates random angle
    new_x = math.sin(new_angle) #does math
    new_y = math.cos(new_angle)
    new_vector = euclid.Vector2(new_x,new_y)
    new_vector.normalize()
    new_vector *= random.randint(min_velocity,max_velocity) #pixels per second
    return new_vector #when definition is invoked, new_vector is put forth as an arguement

#class that has properties of each circle
class MySun:
    def __init__(self, position, size, color = (255,255,255), velocity = euclid.Vector2(0,0), acceleration = euclid.Vector2(0.0), width = 1, stopped=0):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.stopped = stopped
        self.size = size
        self.color = color
        self.width = width

    def delete(object):
        game._display_surf.fill(white)
        my_circles.pop(my_circles.index(object))
        for i, my_circle in enumerate(my_circles):
            my_circle.display()


    def display(self):
        #draws the circle
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(game._display_surf, self.color, (rx,ry), self.size, self.width)


    def move(self):
        #changes positons and invoke function to change velocities
        self.position += self.velocity*game.dtime + 0.5*self.acceleration*(game.dtime**2)
        self.change_velocity(self.velocity)
        self.bounce()

    def change_velocity(self, velocity):
        #changes positions
        self.velocity += self.acceleration*game.dtime
        self.velocity -= self.velocity*drag*game.dtime


    def bounce(self):
        #set conditions for bouncing off walls
        if self.position.x < self.size:
            self.position.x = 2*self.size - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1,0))
            self.velocity *=elasticity
        elif self.position.x > game.width - self.size:
            self.position.x = 2*(game.width - self.size) - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1,0))
            self.velocity *=elasticity
        elif self.position.y < self.size:
            self.position.y = 2*self.size - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0,1))
            self.velocity *=elasticity
        elif self.position.y > game.height - self.size:
            self.position.y = 2*(game.height - self.size) - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0,1))
            self.velocity *= elasticity

    def surface_distance(self, other, time):
        #calculates the distance between two objects given
        radiiAB = self.size + other.size
        posA = self.position + self.velocity * time + .5 * self.acceleration * (time**2)
        posB = other.position + other.velocity * time + .5 * other.acceleration * (time**2)
        posAB = abs(posA - posB)
        return posAB - radiiAB

    def collide(self,other):
        #finds a vector that points from object A to object B. result velocity of each object is reflection of that vector. I think it also needs to be perpendicular and not just a reflection
        if self.surface_distance(other,game.dtime) <= 0:
            collision_vector = self.position - other.position #position should be from center. I don't think this is the center
            collision_vector.normalize()
            self.velocity = self.velocity.reflect(collision_vector)
            other.velocity = other.velocity.reflect(collision_vector)



#this is where our game runs
class Game(object):
    def __init__(self):
        #runs at t=0ms
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.size = self.width, self.height = 300, 300
        pygame.display.set_caption('Particle Game')
    def on_init(self):
        #runs at t=498ms
        pygame.init() #initializes all imported pygame modules
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)#idon't know what this does
        self._display_surf.fill(white) #establishes the game screen
        self._running = True
    def on_event(self, event):
        #events are things like pushing keys or clicking the mouse. These take priority and will interrupt other functions (i think. maybe)
        if event.type == pygame.QUIT:
            self._running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # populate()
    def on_loop(self):
        #updates the time
        self.dtime_ms = clock.tick(fps_limit)
        self.dtime = self.dtime_ms/1000.0
        for i, my_circle in enumerate(my_circles):
            if (my_circle.position[1] > (self.height-my_circle.size-1) and abs(my_circle.velocity[1]) < 2.00 ):
                my_circle.stopped += 1
                if (my_circle.stopped == 10):
                    MySun.delete(my_circle)

    def on_render(self):
        #i don't know what screen lock does
        self._display_surf.lock()
        self._display_surf.fill(white) #delete old images. remove for funky lines
        for i, my_circle in enumerate(my_circles): #research enumerate. this makes it so an item in circle list is only compared against elements that come after it
            my_circle.move()
            for my_circle2 in my_circles[i+1:]:
                my_circle.collide(my_circle2)
            my_circle.display()
        self._display_surf.unlock()
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit() #makes sure to quit the pygame module before you just break it by closing it (proper shutdown vs. hard shut down)
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ): #runs the loop and render defintions, but checks for events before running either
            if pygame.mouse.get_pressed()[0]:
                populate()
                if len(my_circles) >= max_circles_on_screen:
                    MySun.delete(my_circles[0])
                for i, my_circle in enumerate(my_circles):
                    if (my_circle.position[1] > (self.height-my_circle.size-1) and abs(my_circle.velocity[1]) < 2.00 ):
                        my_circle.stopped += 1
                        if (my_circle.stopped == 10):
                            MySun.delete(my_circle)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup() #when you click on "close" the while function is broken and the self.cleanup() is run


if __name__=='__main__': #don't know what if name = main means
    game = Game()
    game.on_execute()