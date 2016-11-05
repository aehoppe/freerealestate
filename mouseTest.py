import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((300,200))
pygame.display.set_caption('Mouse Input Demonstration')
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            print event.button

pygame.display.quit()
