import pygame
from pygame.locals import *
import time
import os



class PyGameView(object):
    """
    Provides a view of the environment in a pygame window
    """


    def __init__(self, model, size):
        """
        Initialize model
        """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.bg = pygame.image.load("background.bmp")
        # self.bg = pygame.transform.scale(self.bg,(800,600))
        self.screen.blit(self.bg,(0,0))

    def draw_circle(self, x, y):
        pygame.draw.circle(
            self.screen,
            pygame.Color(255, 0, 0, 255),
            (x, y),
            5
        )
        pygame.display.update()


class Model(object):
    """
    Represents the state of all entities in the environment and drawing
    parameters
    """


    def __init__(self, width, height):
        """
        initialize model, environment, and default keyboard controller states

        Args:
            width (int): width of window in pixels
            height (int): height of window in pixels
        """
        #window parameters / drawing

        self.height = height
        self.width = width

        self.spriteX = 0
        self.spriteY = 0
        self.drawNew = 0



class PyGameController(object):
    """
        Controller that responds to mouse input
    """


    def __init__(self, model):
        """
        Creates controller

        Args:
            model (object): contains attributes of the environment
        """
        self.model = model

    def handle_event(self, event):
        """
        Look for left and right keypresses to modify the x position of the paddle

        Args:
            event (pygame class): type of event
        """
        if event.type != KEYDOWN:
            return True
        elif event.key == pygame.K_SPACE:
            return False
        elif event.key == pygame.K_q:
            self.model.spriteX, self.model.spriteY = pygame.mouse.get_pos()
            self.model.drawNew = 1
        elif event.key == pygame.K_SPACE:
            return False
            # if pygame.mouse.get_pressed()[0] == 0:
            #     #get current pen mode
            #     (mouseX, mouseY) = pygame.mouse.get_pos()
            #     self.model.sprite.coords = (mouseX, mouseY)
            #     #draw that sprite at the current point

        return True


if __name__ == '__main__':
    pygame.init()
    size = (800, 600)

    model = Model(size[0], size[1])
    view = PyGameView(model, size)
    controller = PyGameController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                # handle event can end pygame loop
                if not controller.handle_event(event):
                    running = False

            if controller.model.drawNew == 1:
                controller.model.drawNew = 0
                view.draw_circle(controller.model.spriteX, controller.model.spriteY)
        # view.draw_sprite()
        # time.sleep(model.sleep_time)
