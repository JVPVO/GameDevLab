import pygame
from pplay.window import Window
from pplay.gameimage import GameImage
from pplay.sprite import Sprite
from pplay.keyboard import Keyboard
from pplay.mouse import Mouse
from pplay.animation import Animation
from PIL import Image
import io
WIDTH = 1280
HEIGHT = 720
class Tiros():
    def __init__(self, tipo, x, y, orientacao, velocidade):
        self.tipo = tipo
        self.orientacao = orientacao
        self.tiposTiros = ['tiro.png']
        self.sprite = Sprite(image_file=self.tiposTiros[tipo])
        self.speed = velocidade * orientacao
        self.sprite.x = x
        self.sprite.y = y
        self.collidable = True
        self.img = self.tiposTiros[tipo]
        self.scale(WIDTH/25600)
        if orientacao == -1:
            self.sprite.image = pygame.transform.rotate(self.sprite.image, 180)
    def colisao(self):
        #A colisão do tiro implementada pra retirar ele da lista quando sair da tela.
        pos = {'x': self.sprite.x, 'y': self.sprite.y}
        if pos['y'] < 0 - self.sprite.rect.height:
            return False
        return True
    def movimento(self, janela):
        if self.colisao():
            self.sprite.y -= self.speed * janela.delta_time()
            return True
        else: return False
    def scale(self, scaleFactor):
        imagem = Image.open(self.img)
        resized = imagem.resize(((int(self.sprite.width*scaleFactor)), int(self.sprite.height*scaleFactor)), resample=Image.LANCZOS)
        img_data = io.BytesIO()
        resized.save(img_data, format='PNG')
        img_data.seek(0)
        self.sprite.image = pygame.image.load_extended(img_data)
        self.sprite.width *= scaleFactor
        self.sprite.height *= scaleFactor
    def draw(self):
        self.sprite.draw()
    def collided(self, alvo):
        return self.sprite.collided(alvo.sprite)