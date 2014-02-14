import sys, pygame, random
from pygame.locals import *

# pygame.init()
clock = pygame.time.Clock()

# SunSurfaceObj = pygame.image.load('img/sun.png')
# windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('Particle Game')

whiteColor = pygame.Color(255,255,255)
mousex, mousey = 250,250

class Game(object):
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.size = self.width, self.height = 640, 400
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._image_surf = pygame.image.load('img/sun.png').convert()
        self._running = True
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.blit(self._image_surf,(200,100))
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