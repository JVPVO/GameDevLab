from pplay.sprite import Sprite
import pygame
from tiros import Tiros
from PIL import Image
import io
import json
import random
import os

WIDTH = 1280
HEIGHT = 720

class Player():
    def __init__(self, img):
        self.img = img
        self.sprite = Sprite(image_file=img)
        self.sprite.x = WIDTH/2
        self.sprite.y = HEIGHT - self.sprite.image.get_height() + 130
        self.lastShot = 0
        self.health = 3
        self.scale(WIDTH/1280)
        self.blinkando = True
        self.lasthit = 0
        self.lastBlink = 0
    def desenhar(self):
        if pygame.time.get_ticks() - self.lasthit > 2000:
            self.sprite.draw()
            if self.blinkando:
                self.sprite.unhide()
        else:
            if pygame.time.get_ticks() - self.lastBlink > 5:
                if not self.blinkando:
                    self.blinkando = True
                    self.sprite.hide()
                    self.sprite.draw()
                    self.lastBlink = pygame.time.get_ticks()
                else:
                    self.blinkando = False
                    self.sprite.unhide()
                    self.sprite.draw()
                    self.lastBlink = pygame.time.get_ticks()
    def scale(self, scaleFactor):
        imagem = Image.open(self.img)
        resized = imagem.resize(((int(self.sprite.width*scaleFactor)), int(self.sprite.height*scaleFactor)), resample=Image.LANCZOS)
        img_data = io.BytesIO()
        resized.save(img_data, format='PNG')
        img_data.seek(0)
        self.sprite.image = pygame.image.load_extended(img_data)
        self.sprite.width *= scaleFactor
        self.sprite.height *= scaleFactor
    def colisao(self):
        global janela
        janela = self.janela
        res = {'x': janela.width, 'y': janela.height}
        pos = {'x': self.sprite.x, 'y': self.sprite.y}
        pos2 = {'x': self.sprite.x+self.sprite.width, 'y': self.sprite.y + self.sprite.height}
        if pos2['x'] >= res['x']:
            self.sprite.x -= 1
            return False
        elif pos['x'] <= 0:
            self.sprite.x += 1
            return False
        return True
    def movimento(self, teclado, janela):
        self.janela = janela
        if self.colisao():
            if teclado.key_pressed('a'): self.sprite.x -= 400 * janela.delta_time()
            if teclado.key_pressed('d'): self.sprite.x += 400 * janela.delta_time()
    def atirar(self, teclado):
        #Implementa um cooldown nos tiros
        if pygame.time.get_ticks() - self.lastShot > 50:
            if teclado.key_pressed('t'):
                self.lastShot = pygame.time.get_ticks()
                return Tiros(tipo=0, x= self.sprite.x + self.sprite.width/2, y= self.sprite.y, orientacao=1, velocidade=900)
    def dano(self):
        if pygame.time.get_ticks() - self.lasthit > 2000:
            self.health -= 1
            self.lasthit = pygame.time.get_ticks()