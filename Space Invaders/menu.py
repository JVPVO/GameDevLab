import pygame
from pplay.window import Window
from pplay.gameimage import GameImage
from pplay.sprite import Sprite
from pplay.keyboard import Keyboard
from pplay.mouse import Mouse
from pplay.animation import Animation

# global variables
atual = 0

def pos_x(x):
    return round(WIDTH * (x / 1920), 2)

def pos_y(y):
    return round(HEIGHT * (y / 1080), 2)
def calcularScale(x, y):
    if x/1920 == y/1080:
        return round(x/1920, 2)
    else:
        print("Sua resolução não está na proporção 16:9")


class AnimatedSprite():
    def __init__(self, img, pos: tuple):
        self.animated = Animation(img, total_frames=50)
        self.animated.set_sequence_time(0, 49, 100, True)
        self.animated.x, self.animated.y = pos_x(pos[0]), pos_y(pos[1])
    def desenhar(self):
        self.animated.draw()

class Fundo:
    def __init__(self, img):
        self.sprite = GameImage(image_file=img)
        self.drawn = False
    def desenhar(self):
        if not self.drawn:
            x, y = self.sprite.image.get_size()
            self.sprite.set_position(janela.width/2 - x/2, janela.height/2 - y/2)
        self.sprite.draw()
        self.drawn = True

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
    def desenhar(self):
        self.animated.draw()

# Inicializando janela
WIDTH = 1920
HEIGHT = 1080
SCALE = calcularScale(WIDTH, HEIGHT)
janela = Window(WIDTH, HEIGHT)
janela.set_title("Space Invaders - João Vitor Pires")
# Periféricos
teclado = Keyboard()
mouse = Mouse()

fundo = Fundo(img='background.jpg')

planeta = AnimatedSprite(img='planeta10.png', pos=(-500, 50))

# TELA PRINCIPAL
jogar = Button(img='jogar.png', pos=(1100, 150))
dificuldade = Button(img='dificuldade.png', pos=(1100, 400))
ranking = Button(img='ranking.png', pos=(1100, 550))
sair = Button(img='sair.png', pos=(1475, 750))

# TELA DE DIFICULDADE
facil = Button(img='facil.png', pos=(700, 150))
medio = Button(img='medio.png', pos=(700, 350))
dificil = Button(img='dificil.png', pos=(700, 550))
voltar = Button(img='voltar.png', pos=(700, 750))

# LISTAS PRA AJUDAR A COMPRIMIR O CÓDIGO DO LOOP PRINCIPAL
screen = ['menu', 'dif', 'gameplay']
atual = 0
botoes = [jogar, dificuldade, ranking, sair]
animated = [planeta]

allbotoes = [jogar, dificuldade, ranking, sair, facil, medio, dificil, voltar]


if __name__ == "__main__":
    while True:
        fundo.desenhar()
        for botao in botoes:
            botao.desenhar()
            botao.isHovering(mouse)
            if botao.isHovering:
                botao.clicked(mouse)
        planeta.desenhar()
        planeta.animated.update()
        janela.update()

        if screen[atual] == 'menu':
            botoes = [jogar, dificuldade, ranking, sair]
            planeta.animated.x, planeta.animated.y = pos_x(-500), pos_y(50)
        elif screen[atual] == 'dif':
            botoes = [facil, medio, dificil, voltar]
            planeta.animated.x, planeta.animated.y = pos_x(1500), pos_y(50)
        elif screen[atual] == 'gameplay':
            botoes = []
            planeta.animated.hide()

        if teclado.key_pressed(key='m'):
            if atual == 0:
                atual = 1
            else:
                atual = 0
        # Ajudar a pegar as coordenadas de onde o cursor do mouse está
        if teclado.key_pressed(key='p'):
            print(f"Coordenadas do mouse: X:{mouse.get_position()[0]}, Y:{mouse.get_position()[1]}")
            planeta.scale()
        if teclado.key_pressed(key='esc'):
            atual = 0
            planeta.animated.unhide()
        # Quit Game
        if teclado.key_pressed(key='q'):
            janela.close()
