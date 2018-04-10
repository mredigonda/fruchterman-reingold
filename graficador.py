import pygame
import math
from vector import Vector

class Graficador:
    
    def __init__(self, width = 480, height = 320):
        '''
        Inicializa el graficador recibiéndo como parámetros el tamaño
        de la pantalla.
        '''
        pygame.init()
        
        self.width = width
        self.height = height    
        self.screen_size = Vector(width, height)
        self.screen = pygame.display.set_mode(self.screen_size.toIntegerPair())
        
        # Definimos constantes
        self.background_color = 255, 255, 255
        
        self.node_color = 255, 0, 0
        self.node_border_color = 0, 0, 0
        self.node_border_thickness = 2
        self.node_radius = 10
        
        self.edge_color = 0, 0, 0
        self.edge_thickness = 2
    
    def _dibujar_nodo(self, pos):
        '''Dibuja un nodo en la pantalla, en la posición indicada'''
        pos = pos.toIntegerPair()
        pygame.draw.circle(self.screen, self.node_color, 
            pos, self.node_radius)
        pygame.draw.circle(self.screen, self.node_border_color, 
            pos, self.node_radius, self.node_border_thickness)
    
    def _dibujar_arista(self, a, b):
        '''Dibuja una arista, desde y hasta las posiciones indicadas'''
        pygame.draw.line(self.screen, self.edge_color,
            a.toIntegerPair(), b.toIntegerPair(), self.edge_thickness)

    def dibujar_grafo(self, grafo, posiciones):
        '''
        Recibe la descripción de un grafo, junto con un diccionario
        con la posición de cada nodo (expresado como un vector) y 
        dibuja el grafo en pantalla.
        '''
        nodes = grafo[0]
        edges = grafo[1]
        self.screen.fill(self.background_color)
        
        for edge in edges:
            a = posiciones[edge[0]] * self.screen_size
            b = posiciones[edge[1]] * self.screen_size
            self._dibujar_arista(a, b)
        
        for node in nodes:
            where = posiciones[node] * self.screen_size
            self._dibujar_nodo(where)
        
        pygame.display.flip()
