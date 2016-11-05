import pygame
from pygame.locals import *
import time
import os
from leapUs import *



class PyGameView(object):
    """
    Provides a view of the environment in a pygame window
    """

    def __init__(self, model, size):
        """
        Initialize model
        """

        self.color = pygame.Color(0)
        self.color.hsva = (0, 100, 100, 100)
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.bg = pygame.image.load("background.bmp")
        self.ch = pygame.image.load("crosshair.png")
        # self.bg = pygame.transform.scale(self.bg,(800,600))
        self.screen.blit(self.bg,(0,0))
        pygame.display.update()


    def draw_background(self):
        self.screen.blit(self.bg,(0,0))
        pygame.display.update()

    def draw_circle(self, x, y):
        pygame.draw.circle(
            self.screen,
            self.color,
            (x, y),
            5
        )
        pygame.display.update()

    def draw_line(self, lastPoint, currentPoint):
        """
        Draw anti-aliased line between lastPoint and currentPoint.
        Both are (x,y) tuples.
        """
        pygame.draw.aaline(self.screen, self.color, lastPoint, currentPoint)
        pygame.display.update()

    def draw_lock(self, is_locked):
        if is_locked:
            color = pygame.Color("black")
        else:
            color = self.color

        wrecked = pygame.Rect((676, 55), (704-676, 83-55))
        pygame.draw.rect(
            self.screen,
            color,
            wrecked,
            2
            )
        pygame.display.update()

    def draw_crosshair(self, x, y):
        self.screen.blit(self.ch, (x, y))

    def set_color(self, angle):
        if self.color.hsva[0] != angle: # Only do things if color has changed
            self.color.hsva = (angle, 100, 100, 100)
            wrecked = pygame.Rect((676, 55), (704-676, 83-55))
            pygame.draw.rect(
                self.screen,
                self.color,
                wrecked
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
        self.mode = ''
        self.reset = False

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
            if self.mode == 0:
                self.mode = 1
            else:
                self.mode = 0
        elif event.key == pygame.K_r:
            self.reset = not self.reset
        elif event.key == pygame.K_SPACE:
            return False
            # if pygame.mouse.get_pressed()[0] == 0:
            #     #get current pen mode
            #     (mouseX, mouseY) = pygame.mouse.get_pos()
            #     self.model.sprite.coords = (mouseX, mouseY)
            #     #draw that sprite at the current point

        return True


if __name__ == '__main__':
    #leap motion
    # Create a sample listener and controller
    listener = SampleListener()
    controllerLeap = Leap.Controller()

    # Have the sample listener receive events from the controller
    controllerLeap.add_listener(listener)


    #pygame
    pygame.init()
    size = (800, 600)
    model = Model(size[0], size[1])
    view = PyGameView(model, size)
    controller = PyGameController(model)
    running = True

    graspLength = 750 #ms. How long does the hand have to be grasping to count as reset
    graspStart = 0 # Counter

    lastPoint = None

    while running:
        everything = literallyEverything(controllerLeap)
        x, y = everything['position']
        x = int(x)
        y = int(y)
        controller.mode = everything['mode']

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False
            else:
                # handle event can end pygame loop
                if not controller.handle_event(event):
                    running = False

        if controller.mode == 'clear':
            if graspStart == -1:
                graspStart = pygame.time.get_ticks()

            print "\ncurrent time: {}, graspStart: {}".format(pygame.time.get_ticks(), graspStart)
            if (pygame.time.get_ticks() - graspStart) >= graspLength:
                controller.reset = True
        else:
            graspStart = -1
            if controller.mode == 'draw':
                # x, y = pygame.mouse.get_pos()

                # Draw individual points
                view.draw_circle(x, y)

                # # Draw lines between points
                # if lastPoint:
                #     view.draw_line(lastPoint, (x,y))
            # else:
            #     view.draw_crosshair(x, y)

        if controller.reset:
            controller.reset = False
            view.draw_background()

        if everything['color'] != None:
            view.draw_lock(False)
            view.set_color(everything['color'])
        else:
            view.draw_lock(True)

        lastPoint = (x, y)

            # if controller.model.drawNew == 1:
            #     controller.model.drawNew = 0
            #     view.draw_circle(controller.model.spriteX, controller.model.spriteY)
        # view.draw_sprite()
        # time.sleep(model.sleep_time)

    controllerLeap.remove_listener(listener)
