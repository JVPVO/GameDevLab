from pplay.window import Window
from pplay.sprite import Sprite
import pplay
import time
import random

class Bola:
    def __init__(self, v1, v2):
        self.sprite = Sprite(image_file='Pong/bola.png')
        self.v1, self.v2 = v1, v2        
        self.drawn = False
    def desenhar(self):
        if not self.drawn:
            x,y = self.sprite.image.get_size()
            self.sprite.set_position(janela.width/2-x/2,janela.height/2-y/2)
        self.sprite.draw()
        self.drawn = True
    def colisao(self,x1,y1):
        if x1 > 770 or x1 < 0: 
            self.v1 = -self.v1
            return True
        elif y1 > 570 or y1 < 0: 
            self.v2 = -self.v2
            return True
    def move(self):
        self.sprite.x += self.v1
        self.sprite.y += self.v2    


janela = Window(800,600)
janela.set_title("Pong - João Vitor Pires")
cores = [random.randint(0,155),random.randint(0,155),random.randint(0,255)]

objetos, num = [], 3

for bolinha in range(num):
    bolinha = Bola(random.randint(-5,5), random.randint(-5,5))
    objetos.append(bolinha)


while True:
    janela.set_background_color(cores)
    for objeto in objetos:
        objeto.desenhar()
        pos = objeto.colisao(objeto.sprite.x, objeto.sprite.y)
        if pos:
            cores = [random.randint(0,155),random.randint(0,155),255]
            janela.set_background_color(cores)
        objeto.move()
        janela.update() 
    time.sleep(0.008)