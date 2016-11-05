import pygame
from pygame.locals import QUIT, KEYDOWN
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


    def draw_text(self, text, x, y, size, color=(100, 100, 100)):
        """
        Helper to draw text onto screen.

        Args:
            text (string): text to display
            x (int): horizontal position
            y (int): vertical position
            size (int): font size
            color (3-tuple int): color of text.  Can use pygame colors.
            defualt = (100, 100, 100)
        """
        basicfont = pygame.font.SysFont(None, size)
        text_render = basicfont.render(
            text, True, color)
        self.screen.blit(text_render, (x, y))


    def draw_sprite(self, x, y):
        if this.model.sprite == 0:
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

        self.sprite = Sprite()


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
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 0:
                #get current pen mode
                (mouseX, mouseY) = pygame.mouse.get_pos()
                self.model.sprite.coords = (mouseX, mouseY)
                #draw that sprite at the current point

        return

class Sprite():
    """
    holds onto a little fragment of image
    """

    def __init__(selt, type):
        self.type = 0
        self.coords = (0, 0)

    def get_type():
        return self.type

    def draw():
        if self.type == 0:
            pygame.draw.circle

if __name__ == '__main__':
    pygame.init()
    size = SCREEN_SIZE

    model = Model(500, 500)
    view = PyGameView(model, size)
    controller = PyGameController(model)
    running = True
li
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                # handle event can end pygame loop
                if not controller.handle_event(event):
                    running = False
        model.update()
        if model.show_gen:
            view.draw_sprite()
            time.sleep(model.sleep_time)
