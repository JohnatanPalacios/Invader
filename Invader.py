import pygame
import random
from libreria import *


class Jugador(pygame.sprite.Sprite):
    def __init__(self,pos): #constructor
        #pass
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("nave.png").convert_alpha()
        #self.image = pygame.Surface([50,50]) #crea un cuadrado
        #self.image.fill(BLANCO) #lo pinta de blanco
        self.rect = self.image.get_rect() #metodo para limitaciones y colisiones
        self.rect.x = pos[0] #variable de posicionamiento
        self.rect.y = (ALTO-self.rect.height) - 10 #se le suma 10 para que no este pegado al final
        self.velx = 0
        self.vely = 0 #se comenta para que el jugador no se mueva en y
        self.vida = 2

    def RetPos(self):
        x = self.rect.x
        y = self.rect.y - 30
        return [x,y]

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

class Rival(pygame.sprite.Sprite):
    def __init__(self,pos): #constructor
        #pass
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("monster.png").convert_alpha()
        #convert_alpha reduce la colusion solo a la parte con alpha
        self.rect = self.image.get_rect() #metodo para limitaciones y colisiones
        self.rect.x = pos[0] #variable de posicionamiento
        self.rect.y = pos[1] #variable de posicionamiento
        self.velx = 5
        self.vely = 0
        self.temp = random.randrange(40,220)

    def RetPos(self):
        x = self.rect.x + 5
        y = self.rect.bottom + 5
        return [x,y]

    def update(self):
        self.temp -= 1
        self.rect.x += self.velx
        if self.rect.x > (ANCHO - self.rect.width):
            self.rect.x = ANCHO - self.rect.width
            self.velx = -5
        elif self.rect.x < 0:
            self.rect.x = 0
            self.velx = 5
        #self.rect.y += self.vely

class Bala(pygame.sprite.Sprite):
    def __init__(self,pos, cl=AMARILLO): #constructor
        #pass
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5,15]) #crea un cuadrado
        self.image.fill(cl) #lo pinta de blanco
        self.rect = self.image.get_rect() #metodo para limitaciones y colisiones
        self.rect.x = pos[0]+35 #variable de posicionamiento
        self.rect.y = pos[1]+20 #variable de posicionamiento
        self.velx = 0
        self.vely = 0

    def update(self):
        self.rect.y += self.vely

if __name__ == '__main__':
    pygame.init() #crea la ventana e inicializa todo
    #Definicion de variables
    ventana = pygame.display.set_mode([ANCHO, ALTO])

    #Seccion antes del juego
    msc = pygame.mixer.Sound('Battleship.ogg')
    fuente_prev = pygame.font.Font(None,46)
    txt_titulo = fuente_prev.render('JUEGO EJEMPLO',True,BLANCO)
    msc.play(-1)
    fin = False
    fin_prev = False
    while (not fin) and (not fin_prev):
        #Gestion eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                fin_prev = True

        ventana.blit(txt_titulo,[350,300])
        pygame.display.flip()
    msc.stop()



    #Seccion del juego
    #Definicion de variables
    jugadores = pygame.sprite.Group()
    rivales = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    balas_r = pygame.sprite.Group()

    fuente_j = pygame.font.Font(None,32)
    shoot = pygame.mixer.Sound('shoot.wav')

    j = Jugador([300,200])
    jugadores.add(j)

    #creación de enemigos
    n=10
    for i in range(n):
        x = random.randrange(ANCHO)
        y = random.randrange(ALTO-180)
        #vx = random.randrange(10)
        r=Rival([x,y])
        #r.velx=vx
        rivales.add(r)

    reloj = pygame.time.Clock()
    fin_juego = False
    #fin = False
    ptos = 0

    while (not fin) and (not fin_juego):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            # Gestion de eventos (raton, teclado, etc)
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
                shoot.play()
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
        ls_col = pygame.sprite.spritecollide(j,rivales,True)

        #colision activa
        for e in ls_col:
            ptos+=1
        print (ptos)

        #colision balas
        '''for b in balas:
            ls_r = pygame.sprite.spritecollide(b,rivales,true)
            for e in ls_colision:
                ptos+=1
                balas.remove(b)
            print(ptos)'''

        #Control de rivales
        for r in rivales:
            if r.temp < 0:
                print('Disparo')
                pos = r.RetPos()
                b = Bala(pos,VERDE)
                b.vely = 10
                balas_r.add(b)
                r.temp = random.randrange(40,220)

        #limpieza de memoria
        for b in balas:
            ls_r = pygame.sprite.spritecollide(b,rivales,True)
            if b.rect.y < -30:
                balas.remove(b)
            for r in ls_r:
                balas.remove(b)

        for b in balas_r:
            ls_j = pygame.sprite.spritecollide(b,jugadores,False)
            #se elimina bala si sale de ventana
            if b.rect.y > ALTO:
                balas_r.remove(b)

            contacto = True
            for j in ls_j:
                if contacto:
                    j.vida -= 1
                    balas_r.remove(b) #elimina bala si hay contacto
                    contacto = False

        for j in jugadores:
            if j.vida < 0:
                fin_juego = True

        # Refresco de pantalla
        msj = 'Vidas: ' + str(j.vida)
        info = fuente_j.render(msj,True,BLANCO)

        jugadores.update() #actualiza los objetos o sprites
        rivales.update()
        balas.update()
        balas_r.update()

        ventana.fill(NEGRO) #borra
        ventana.blit(info,[10,10])

        jugadores.draw(ventana) #dibuja
        rivales.draw(ventana)
        balas.draw(ventana)
        balas_r.draw(ventana)
        pygame.display.flip() #refresca
        reloj.tick(40) #cuadros por segundo

    #Despues del juego
    while not fin:
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

        gameOver = pygame.image.load("GameOver.png").convert()
        ventana.blit(gameOver, (0, 0))

        #fuente = pygame.font.Font(None,50)
        #msj = fuente.render('Fin de Juego', True, BLANCO)
        #ventana.fill(NEGRO)
        #ventana.blit(msj,[300,350])
        pygame.display.flip()
