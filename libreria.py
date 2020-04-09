import pygame
import math

ANCHO = 950
ALTO = 750
MIDDLE = [int(ANCHO/2),int(ALTO/2)]

VIOLETA = [243, 104, 224]
AZUL = [0,0,209]
VERDE = [0,255,0]
MANZANA = [143,210,136]
AMARILLO = [220,157,0]
NARANJA = [243,112,0]
ROJO = [255,0,0]
GRIS = [113,128,147]
NEGRO = [0,0,0]
BLANCO = [255,255,255]

#subrutina
def Plano(v, pos=MIDDLE):
    '''
    Dibuja un plano al dar click
    --------------------------------
    v: ventana donde se crea el plano
    pos: posicion del origen del plano
    '''
    posx = pos[0]
    posy = pos[1]
    v.fill(NEGRO)
    pygame.draw.line(v, ROJO, [posx, 0], [posx, ALTO],2)
    pygame.draw.line(v, ROJO, [0, posy], [ANCHO, posy],2)

    setMiddle(pos)

def setMiddle(pos):
    MIDDLE[0] = pos[0]
    MIDDLE[1] = pos[1]

def Cart_Pant(pc):
    ''' Transformación lineal de puntos cartecianos
    a puntos en pantalla
    p = punto'''
    xp = pc[0] + MIDDLE[0]
    yp = -pc[1] + MIDDLE[1]

    return [int(xp),int(yp)]

def Pant_Cart(pp):
    xc = pp[0] - MIDDLE[0]
    yc = -pp[1] + MIDDLE[1]

    return [int(xc),int(yc)]

def SumaVec(v, ls):
    '''
    V: Ventana
    ls: lista de puntos
    '''
    x=0
    y=0
    for p in ls:
        x+=p[0]
        y+=p[1]
        pygame.draw.line(v, VERDE, MIDDLE, Cart_Pant(p))
    pygame.draw.line(v, AMARILLO, MIDDLE, Cart_Pant([x,y]))
    print('El punto del vR es: ' + str(x) + ',' + str(y))
    print('La magnitud del vR es: ' + str(math.sqrt(x**2 + y**2)))

def graRecta(v, ls):
    ''' Grafica una recta dados dos puntos
    '''
    x1 = ls[0][0]
    y1 = ls[0][1]
    x2 = ls[1][0]
    y2 = ls[1][1]

    m = (y2-y1)/(x2-x1)
    b = y1-(m*x1)
    for i in range(-800,800):
        y = int((m*i)+b)
        p = Cart_Pant([i,y])
        pygame.draw.circle(v, AMARILLO, p, 1, 1)

def Escalamiento(p,s,operacion):
    '''
    Aumentar tamaño de un gráfico
    p: punto
    s: vector de escalamiento [x,y]
    operacion: aug amuentar y dis disminuir
    '''
    if operacion == "aug":
        xp = int(p[0]*s[0])
        yp = int(p[1]*s[1])
    elif operacion == "dis":
        xp = int(p[0]/s[0])
        yp = int(p[1]/s[1])

    return [int(xp),int(yp)]

def Rotacion(punto,angulo):
    '''
    Requiere un punto [x,y]
    el angulo en grados y puede ser negativo
    '''
    a = math.radians(angulo)
    x = punto[0]
    y = punto[1]

    xp = (x*math.cos(a)) + (y*math.sin(a))
    yp = (-x*math.sin(a)) + (y*math.cos(a))

    return [int(xp),int(yp)]

def Traslacion(p,t):
    '''
    p = punto [x,y]
    t = aumento en el movimiento [x,y]
    '''
    xp = p[0] + t[0]
    yp = p[1] + t[1]

    return [int(xp), int(yp)]

def EscalamientoPFijo(pFijo, punto, zoom):
    '''
    pFijo = punto fijo del movimiento
    pEsc = punto a escalar
    zoom = tamaño del aumento
    '''
    xF = pFijo[0]
    yF = pFijo[1]

    x = punto[0]
    y = punto[1]

    xp = (x * zoom[0]) + (xF * (1 - zoom[0]))
    yp = (y * zoom[1]) + (yF * (1 - zoom[1]))

    return [int(xp), int(yp)]

def RotacionPFijo(pFijo, punto, angulo):
    '''
    pFijo = punto fijo del movimiento
    punto = punto a girar
    angulo = angulo de giro en grados
    '''
    a = math.radians(angulo)
    xF = pFijo[0]
    yF = pFijo[1]

    x = punto[0]
    y = punto[1]

    xp = (xF + ((x - xF) * math.cos(a))) - ((y - yF) * math.sin(a))
    yp = (yF + ((y - yF) * math.cos(a))) + ((x - xF) * math.sin(a))

    return [int(xp), int(yp)]

def PolarCart(radio, angulo):
    '''
    radio es una distancia o tamaño
    angulo en grados
    retorna coordenadas [x,y] en cartesiano
    '''
    a = math.radians(angulo)
    x = radio * math.cos(a)
    y = radio * math.sin(a)

    return [int(x), int(y)]
