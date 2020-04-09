import pygame
import random
from libreria import *


class Jugador(pygame.sprite.Sprite):
    def __init__(self,pos): #constructor
        #pass
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50]) #crea un cuadrado
        self.image.fill(BLANCO) #lo pinta de blanco
        self.rect = self.image.get_rect() #metodo para limitaciones y colisiones
        self.rect.x = pos[0] #variable de posicionamiento
        self.rect.y = (ALTO-self.rect.height) - 10 #se le suma 10 para que no este pegado al final
        self.velx = 0
        #self.vely = 0 #se comenta para que el jugador no se mueva en y

    def RetPos(self):
        x = self.rect.x
        y = self.rect.y - 30
        return [x,y]

    def update(self):
        self.rect.x += self.velx
        #self.rect.y += self.vely


class Rival(pygame.sprite.Sprite):
    def __init__(self,pos): #constructor
        #pass
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50]) #crea un cuadrado
        self.image.fill(VERDE) #lo pinta de blanco
        self.rect = self.image.get_rect() #metodo para limitaciones y colisiones
        self.rect.x = pos[0] #variable de posicionamiento
        self.rect.y = pos[1] #variable de posicionamiento
        self.velx = 0
        self.vely = 0

    def update(self):
        #self.rect.x += self.velx
        #self.rect.y += self.vely
        pass

class Bala(pygame.sprite.Sprite):
    def __init__(self,pos): #constructor
        #pass
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,30]) #crea un cuadrado
        self.image.fill(AMARILLO) #lo pinta de blanco
        self.rect = self.image.get_rect() #metodo para limitaciones y colisiones
        self.rect.x = pos[0] #variable de posicionamiento
        self.rect.y = pos[1] #variable de posicionamiento
        self.velx = 0
        self.vely = 0

    def update(self):
        self.rect.y += self.vely



if __name__ == '__main__':
    pygame.init()
    #Definicion de variables
    ventana = pygame.display.set_mode([ANCHO, ALTO])

    jugadores = pygame.sprite.Group()
    rivales = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    j = Jugador([300,200])
    jugadores.add(j)

    n=10
    for i in range(n):
        x = random.randrange(ANCHO)
        y = random.randrange(ALTO-180)
        vx = random.randrange(10)
        r=Rival([x,y])
        r.velx=vx
        rivales.add(r)

    fin = False
    reloj = pygame.time.Clock()

    while not fin:
        # Gestion de eventos (raton, teclado, etc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.velx = 5
                    j.vely = 0
                if event.key == pygame.K_LEFT:
                    j.velx = -5
                    j.vely = 0
                if event.key == pygame.K_UP:
                    j.vely = -5
                    j.velx = 0
                if event.key == pygame.K_DOWN:
                    j.vely = 5
                    j.velx = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                #pos jugador
                p = j.RetPos()
                b = Bala(p)
                b.vely = -10
                balas.add(b)
            if event.type == pygame.KEYUP:
                j.velx = 0
                j.vely = 0

        # Codigo de control
        '''
        if j.rect.x > (ANCHO-j.rect.width):
            j.rect.x = ANCHO-j.rect.width
        '''
        if j.rect.x > ANCHO:
            j.rect.x = 0-j.rect.width

        #Colision


        #limpieza
        for b in balas:
            if b.rect.y < -30:
                balas.remove(b)

        # Refresco de pantalla
        jugadores.update() #actualiza los objetos o sprites
        rivales.update()
        balas.update()
        ventana.fill(NEGRO) #borra
        jugadores.draw(ventana) #dibuja
        rivales.draw(ventana)
        balas.draw(ventana)
        pygame.display.flip() #refresca
        reloj.tick(40) #cuadros por segundo
        
