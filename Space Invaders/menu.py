import pygame
from pplay.window import Window
from pplay.gameimage import GameImage
from pplay.sprite import Sprite
from pplay.keyboard import Keyboard
from pplay.mouse import Mouse
from pplay.animation import Animation
from PIL import Image
from player import Player
from tiros import Tiros
import io
import json
import random
import os
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
def score(pontos):
    try:
        with open('rank.json', 'r') as file:
            temprank = json.load(file)
            file.close()
    except FileNotFoundError:
        temprank = {}

    with open('rank.json', 'w') as file:
        nome = input("Bote seu nome para registrar a sua pontuação: ")
        temprank[nome] = pontos
        json.dump(temprank, file, indent=4)
        file.close()
def lerScore(rankings):
    for idx, nome in enumerate(rankings):
        if idx == 5:
            return
        janela.draw_text(f'{idx+1}. {nome}:{rankings[nome]}', x=(WIDTH/2)-220, y=50+(60*idx), size=40, color=(255,255,255))

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
            elif self.image == 'ranking.png':
                atual = 3
    def desenhar(self):
        self.animated.draw()
class Inimigo():
    def __init__(self, img, velocidade):
        self.img = img
        self.sprite = Sprite(image_file=img)
        self.sprite.x = 0
        self.sprite.y = 0
        self.lastShot = 0
        self.firstDraw = True
        self.vel = velocidade
        self.cooldown = 0
        self.alive = True
        self.scale(WIDTH/1280)
    def desenhar(self, x, y):
        if self.firstDraw:
            self.sprite.x = x
            self.sprite.y = y
            self.firstDraw = False
        if self.alive:
            self.sprite.draw()
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
        global direcao
        colidiu = False
        if pygame.time.get_ticks() - self.cooldown > 1000:
            if 0+self.sprite.width > self.sprite.x or self.sprite.x > WIDTH-self.sprite.width:
                direcao *= -1
                self.cooldown = pygame.time.get_ticks()
                colidiu = True
        return colidiu
    def movimento(self, janela):
        colisao = self.colisao()
        self.sprite.x += self.vel * direcao * janela.delta_time()
        return colisao
    def atirar(self):
        global ultimoTiroDosTiras
        #Implementa um cooldown nos tiros
        if pygame.time.get_ticks() - ultimoTiroDosTiras > 600:
            self.lastShot = pygame.time.get_ticks()
            return Tiros(tipo=0, x= self.sprite.x + self.sprite.width/2, y= self.sprite.y, orientacao=-1, velocidade=400)

class Barreira():
    def __init__(self, img, idx):
        self.img = img
        self.sprite = Sprite(image_file=img)
        self.sprite.x = int((WIDTH-200-(450*(idx))))
        self.sprite.y = HEIGHT-250
        self.firstDraw = True
        self.alive = True
        self.health = 3
    def desenhar(self):
        if self.firstDraw:
            self.firstDraw = False
        if self.alive:
            self.sprite.draw()
    def scale(self, scaleFactor):
        imagem = Image.open(self.img)
        resized = imagem.resize(((int(self.sprite.width*scaleFactor)), int(self.sprite.height*scaleFactor)), resample=Image.LANCZOS)
        img_data = io.BytesIO()
        resized.save(img_data, format='PNG')
        img_data.seek(0)
        self.sprite.image = pygame.image.load_extended(img_data)
        self.sprite.width *= scaleFactor
        self.sprite.height *= scaleFactor

# Inicializando janela
WIDTH = 1280    
HEIGHT = 720
SCALE = calcularScale(WIDTH, HEIGHT)
global janela
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
screen = ['menu', 'dif', 'gameplay', 'ranking']
atual = 0
botoes = [jogar, dificuldade, ranking, sair]
animated = [planeta]
nave = Player(img = 'spaceinvaders.png')
nave.scale(0.2)
lista_tiros = []
sprites = [nave]
allbotoes = [jogar, dificuldade, ranking, sair, facil, medio, dificil, voltar]
barreiras = []
def criarMatriz(linhas, colunas, velocidade):
    matriz = []
    for _ in range(linhas):
        matriz.append([Inimigo(img='inimigo.png', velocidade=velocidade) for i in range(colunas)])
    return matriz

created = False
fase = 1
linhas, colunas = 5,10
direcao = 1
pontos = 0
global ultimoTiroDosTiras
ultimoTiroDosTiras = pygame.time.get_ticks()

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
        
        if screen[atual] == 'menu':
            botoes = [jogar, dificuldade, ranking, sair]
            planeta.animated.x, planeta.animated.y = pos_x(-500), pos_y(50)
            if not created:
                barreiras = [Barreira(img='barreira.png', idx=i) for i in range(3)]
                for barreira in barreiras:
                    barreira.scale(3)
                matriz = criarMatriz(linhas, colunas, velocidade=100)
                nave.health = 3
                planeta.animated.unhide()
                created = True
        elif screen[atual] == 'dif':
            botoes = [facil, medio, dificil, voltar]
            planeta.animated.x, planeta.animated.y = pos_x(1500), pos_y(50)
        elif screen[atual] == 'gameplay':
            for barreira in barreiras:
                barreira.desenhar()
            botoes = []
            planeta.animated.hide()
            nave.desenhar()
            nave.movimento(teclado, janela)
            bullet = nave.atirar(teclado=teclado)
            if bullet != False:
                lista_tiros.append(bullet)
            for tiro in lista_tiros:
                if tiro is None:
                    lista_tiros.remove(tiro)
                #A função movimento retorna True se ele está dentro da tela, então podemos desenhá-lo.
                elif tiro.movimento(janela=janela):
                    tiro.draw()
                else:
                    #Retirar o tiro da lista se ele saiu da tela.
                    lista_tiros.remove(tiro)
            for i in range(linhas):
                for j in range(colunas):
                    matriz[i][j].desenhar(x = WIDTH/2+(matriz[i][j].sprite.width*2*(j+1))-200*int(colunas/3), y=(matriz[i][j].sprite.height*2*(i+1)))
            for i in range(linhas):
                for monstro in matriz[i]:
                    if monstro.alive:
                        cld = monstro.movimento(janela=janela)
                        if cld:
                            for i in range(linhas):
                                for monstro in matriz[i]:
                                    monstro.sprite.y += 4
            for tiro in lista_tiros:
                if tiro is None:
                    break
                for i in range(linhas):
                    for j in range(colunas):
                        for barreira in barreiras:
                            if tiro.collidable:
                                if tiro.collided(barreira):
                                    tiro.collidable = False
                                    lista_tiros.remove(tiro)
                                    if tiro.orientacao == -1:
                                        barreira.health -=1
                            if barreira.health <= 0:
                                barreiras.remove(barreira)
                        if matriz[i][j].alive and tiro.collidable:
                            if tiro.collided(matriz[i][j]) and tiro.orientacao == 1:
                                tiro.collidable = False
                                lista_tiros.remove(tiro)
                                matriz[i][j].alive = False
                                pontos += 100
                        if tiro.collidable and tiro.orientacao == -1:
                            if tiro.collided(nave):
                                nave.dano()
                                lista_tiros.remove(tiro)
                                tiro.collidable = False
            if pygame.time.get_ticks() - ultimoTiroDosTiras > 600:
                if pontos != 5000:
                    alien = random.choice(random.choice(matriz))
                    while alien.alive == False:
                        alien = random.choice(random.choice(matriz))
                    lista_tiros.append(alien.atirar())
                    ultimoTiroDosTiras = pygame.time.get_ticks()
            if pontos // 5000 >= fase:
                fase += 1
                barreiras = [Barreira(img='barreira.png', idx=i) for i in range(3)]
                for barreira in barreiras:
                    barreira.scale(3)
                matriz = criarMatriz(linhas, colunas, velocidade=100+(fase*35))

            if nave.health < 1:
                atual = 0
                score(pontos=pontos)
                created = False
                pontos = 0
            janela.draw_text(f'Pontuação: {pontos}',x = WIDTH/2000, y= 0,size=50, color=(255,255,255))
            janela.draw_text(f'Vida: {nave.health}', x = WIDTH/2000, y= 100, size=50, color=(255,255,255))
        elif screen[atual] == 'ranking':
            botoes = []
            planeta.animated.hide()
            with open('rank.json', 'r') as file:
                rankings = json.load(file)
                file.close()
                rankings = dict(sorted(rankings.items(), key=lambda item: item[1], reverse=True))
            lerScore(rankings)
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
            barreiras = [Barreira(img='barreira.png', idx=i) for i in range(3)]
            for barreira in barreiras:
                barreira.scale(3)
            pontos = 0
            matriz = criarMatriz(linhas, colunas, velocidade=100+(fase*35))
            atual = 0
            planeta.animated.unhide()
        # Quit Game
        if teclado.key_pressed(key='q'):
            janela.close()
        janela.update()