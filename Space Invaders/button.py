import pygame
from pplay.window import Window
from pplay.gameimage import GameImage
from pplay.sprite import Sprite
from pplay.keyboard import Keyboard
from pplay.mouse import Mouse
from pplay.animation import Animation
from PIL import Image
import io
import json
import random
import os
WIDTH = 1280
HEIGHT = 720
def pos_x(x):
    return round(WIDTH * (x / 1920), 2)

def pos_y(y):
    return round(HEIGHT * (y / 1080), 2)
class Button():
    def __init__(self, img, pos: tuple):
        self.image = img
        self.animated = Animation(image_file=img, total_frames=25)
        self.animated.set_sequence_time(0, 24, 30, False)
        self.animated.image.set_colorkey((0, 0, 0))
        self.animated.pause()
        self.animated.x, self.animated.y = pos_x(pos[0]), pos_y(pos[1])
    def isHovering(self, mouse: Mouse):
        if mouse.is_over_object(self.animated):
            self.animated.play()
            self.animated.update()
        else:
            self.animated.curr_frame = 0
    def clicked(self, mouse: Mouse):
        if mouse.is_button_pressed(1) and mouse.is_over_object(self.animated):
            global atual
            global janela
            if self.image == 'jogar.png':
                atual = 2
            elif self.image == 'dificuldade.png':
                atual = 1
            elif self.image == 'voltar.png':
                atual = 0
            elif self.image == 'sair.png':
                janela.close()
            elif self.image == 'ranking.png':
                atual = 3
    def desenhar(self):
        self.animated.draw()