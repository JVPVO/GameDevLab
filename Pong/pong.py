from pplay.window import Window
from pplay.sprite import Sprite
from pplay.keyboard import Keyboard
from pplay.gameimage import GameImage
import pygame
import pplay
import time
import random

class Fundo:
    def __init__(self):
        self.sprite = GameImage(image_file='fundo.png')
        self.drawn = False
    def desenhar(self):
        if not self.drawn:
            x,y = self.sprite.image.get_size()
            self.sprite.set_position(janela.width/2-x/2,janela.height/2-y/2)
        self.sprite.draw()
        self.drawn = True

class Raquete:
    def __init__(self, side:int):
        self.sprite = Sprite("raquete.png")
        self.side = side
        self.drawn = False
        self.v1 = 500
    def desenhar(self):
        if not self.drawn:
            x,y = self.sprite.image.get_size()
            self.sprite.set_position(janela.width/2-x/2+janela.width*0.45*self.side,janela.height/2-y/2)
        self.sprite.draw()
        self.drawn = True
    def movement(self, side):
        x,y = self.sprite.image.get_size()
        if side == -1:
            if teclado.key_pressed('w') and self.sprite.y > 0:
                raquete.sprite.y -= self.v1 * janela.delta_time()
            elif teclado.key_pressed('s') and self.sprite.y < janela.height-y:
                raquete.sprite.y += self.v1 * janela.delta_time()
        elif side == 1:
            if teclado.key_pressed('up') and self.sprite.y > 0:
                raquete.sprite.y -= self.v1 * janela.delta_time()
            elif teclado.key_pressed('down') and self.sprite.y < janela.height-y:
                raquete.sprite.y += self.v1 * janela.delta_time()
class Bola:
    def __init__(self, v1, v2):
        self.sprite = Sprite(image_file='bola.png')
        self.v1, self.v2 = v1, v2    
        self.drawn = False
        self.reset = False
        self.ultima = 0
        self.ultimaBorda = 0
    def desenhar(self):
        if not self.drawn:
            x,y = self.sprite.image.get_size()
            self.sprite.set_position(janela.width/2-x/2,janela.height/2-y/2)
        self.sprite.draw()
        self.drawn = True
    def colisao(self,x1,y1):
        if x1 > janela.width-40 or x1 < 0: 
            self.drawn = False
            self.v1 = 0
            self.v2 = 0
            self.reset = True
            if x1 > 0:
                pontos[1] += 1
            else:
                pontos[0] += 1
            return True
        elif y1 > janela.height-30 or y1 < 0: 
            #pygame.time.get_ticks retorna o tempo do jogo em milisegundos, essencialmente botei um cooldown na colisão da bola
            #isso evita que haja colisões contínuas no mesmo eixo
            agora = pygame.time.get_ticks()
            if agora - self.ultimaBorda > 350:
                self.v2 = -self.v2
                return True
        elif self.sprite.collided(raquetes[0].sprite) or self.sprite.collided(raquetes[1].sprite):
            #garante que a bolinha não vai colidir muitas vezes com a raquete, tirando a patinação
            agora = pygame.time.get_ticks()
            if agora - self.ultima > 350:
                self.ultima = pygame.time.get_ticks()
                self.sprite.x += -self.v1 * janela.delta_time()
                self.v1 = -self.v1
                return True
    def move(self):
        self.sprite.x += self.v1 * janela.delta_time()
        self.sprite.y += self.v2 * janela.delta_time()
    def mudarVel(self, speed: list):
        self.v1, self.v2 = speed

teclado = Keyboard()
janela = Window(800,600)
janela.set_title("Pong - João Vitor Pires")
cores = [55,148,110]

pontos = [0,0]
objetos, num = [], 1
velocidade = [350, 350]

for bolinha in range(num):
    bolinha = Bola(*velocidade)
    objetos.append(bolinha)

raquetes = [Raquete(1), Raquete(-1)]
fundo = Fundo()


while True:
    janela.set_background_color(cores)
    fundo.desenhar()
    janela.draw_text(f'{pontos[0]} x {pontos[1]}',janela.width/2-40, janela.height - 0.9*janela.windowed_height,size=36)
    for raquete in raquetes:
        raquete.desenhar()
        raquete.movement(raquete.side)
    for objeto in objetos:
        objeto.desenhar()
        pos = objeto.colisao(objeto.sprite.x, objeto.sprite.y)
        objeto.move()
    #Invoca muitas bolinhas
    if teclado.key_pressed(key='f'):
        novasVelocidades = [random.choice([i*100 for i in range(-3,3) if i != 0]),random.choice([i*100 for i in range(-3,3) if i != 0])]
        objetos.append(Bola(*novasVelocidades))
    if teclado.key_pressed(key='space'):
        for objeto in objetos:
            if objeto.reset:
                objeto.mudarVel(velocidade)
                objeto.reset = False
    janela.update() 