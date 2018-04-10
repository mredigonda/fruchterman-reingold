#!/usr/bin/python3

import argparse
import math
import time
from random import random

from graficador import Graficador
from vector import Vector

class FruchtermanReingold:
    
    def __init__(self, grafo, iters, refresh, c1, c2, verbose):
        '''
        Parámetros:
        * iters: cantidad de iteraciones a realizar.
        * refresh: numero de iteraciones entre actualizaciones de 
        pantalla, si vale 1, se grafica solo al final.
        * c1: constante usada para calcular la repulsión entre nodos.
        * c2: constante usada para calcular la atracción de aristas.
        * verbose: si vale true, el programa imprimirá información
        adicional a medida que corre.
        '''
        
        # Guardo grafo
        self.grafo = grafo
        
        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        
        # Inicializo estado
        self.posiciones = {}
    
    def randomize_node_positions(self):
        '''Randomiza las posiciones de los nodos'''
        nodos = self.grafo[0]
        for node in nodos:
            x = self.W*random()
            y = self.H*random()
            self.posiciones[node] = Vector(x, y)
    
    def repulsion(self, d):
        '''Calcula la fuerza de repulsión dada la distancia'''
        return self.k**2 / d
    
    def atraccion(self, d):
        '''Calcula la fuerza de atracción dada la distancia'''
        return d**2 / self.k
    
    def step(self):
        '''
        Efectúa un paso de la simulación, actualizando posiciones 
        de los nodos
        '''
        nodes = self.grafo[0]
        edges = self.grafo[1]
        despl = {}
        
        # 1: Calcular repulsiones de nodos (actualiza fuerzas)
        for u in nodes:
            despl[u] = Vector(0, 0)
            for v in nodes:
                if u == v:
                    continue
                delta = self.posiciones[u] - self.posiciones[v]
                dist = delta.longitud()
                if dist != 0:
                    d = self.repulsion(dist) / dist
                    despl[u] = (despl[u] + delta*d)

        # 2: Calcular atracciones de aristas (actualiza fuerzas)
        for u, v in edges:
            delta = self.posiciones[u] - self.posiciones[v]
            dist = delta.longitud()
            if delta != 0:
                d = self.atraccion(dist) / dist
                dd = delta*d
                despl[u] = (despl[u] - dd)
                despl[v] = (despl[v] + dd)

        # 4: En base a fuerzas, temperatura y bordes, actualizar
        # las posiciones de los nodos.
        cnt = 0
        for node in nodes:
            delta = despl[node]
            dist = delta.longitud()
            if dist != 0:
                cnt = cnt + 1
                d = min(dist, self.t) / dist
                npos = self.posiciones[node] + delta*d
                npos.x = min(self.W, max(0, npos.x)) - self.W/2
                npos.y = min(self.H, max(0, npos.y)) - self.H/2
                self.posiciones[node].x = min(math.sqrt(self.W**2/4-npos.y**2), max(-math.sqrt(self.W**2/4-npos.y**2), npos.x)) + self.W/2
                self.posiciones[node].y = min(math.sqrt(self.H**2/4-npos    .x**2), max(-math.sqrt(self.H**2/4-npos.x**2), npos.y)) + self.H/2
        self.t -= self.dt
    
    def create_view(self):
        '''Inicializa el graficador'''
        self.graficador = Graficador(800, 600)

    def dibujar(self):
        self.graficador.dibujar_grafo(self.grafo, self.posiciones)
    
    def run(self):
        '''
        Ejecuta los pasos del algoritmo, de acuerdo a los argumentos
        con los cuales se inicializó la clase.
        '''
        # Inicializamos constantes
        nodes = self.grafo[0]
        
        self.W = 1
        self.H = 1;
        self.area = self.W * self.H
        self.k = math.sqrt(self.area/len(nodes))
        
        self.t = self.W / 10
        self.dt = self.t / (self.iters + 1)
        
        # Inicializamos la 'pantalla'
        self.create_view()
        
        # Inicializamos las posiciones
        self.randomize_node_positions()
        
        # Si es necesario, lo mostramos por pantalla
        if (self.refresh > 0):
            self.dibujar()
        
        # Bucle principal
        for i in range(0, self.iters):
            # Esperamos un tiempo para hacerlo interactivo
            time.sleep(0.2)
            
            # Realizar un paso de la simulacion
            self.step()
                
            # Si es necesario, lo mostramos por pantalla
            if (self.refresh > 0 and i % self.refresh == 0):
                self.dibujar()
                
        # Ultimo dibujado al final
        self.dibujar()

def obtenerArgumentos():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()
    
    # Verbosidad, opcional, False por defecto.
    parser.add_argument('-v', '--verbose', 
                        action='store_true', 
                        help='Muestra mas informacion',
                        default=False)
                        
    # Refresh, opcional. 1 por defecto.
    parser.add_argument('-r', '--refresh', type=int, 
                        help='Cantidad de iteraciones entre \
                            actualizaciones de imagen', 
                        default=1)
                        
    # Fuerza de repulsión, opcional. 1.0 por defecto.
    parser.add_argument('-c1', '--repulsion', type=float, 
                        help='Constante de repulsión entre nodos', 
                        default=1.0)
                        
    # Fuerza de atracción, opcional. 2.5 por defecto.
    parser.add_argument('-c2', '--atraccion', type=float, 
                        help='Constante de atracción de aristas', 
                        default=2.5)
                        
    # Cantidad de iteraciones, opcional, 50 por defecto.
    parser.add_argument('-i', '--iters', type=int, 
                        help='Cantidad de iteraciones a efectuar', 
                        default=50)
    args = parser.parse_args()
    return args
    
def main():
    args = obtenerArgumentos()
    
    fruchterman_reingold = FruchtermanReingold(
        ([1, 2, 3, 4, 5, 6, 7], 
         [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)]
        ),  # TODO: Cambiar a usar grafo leido de archivo.
        iters=args.iters,
        refresh=args.refresh,
        c1=args.repulsion,
        c2=args.atraccion,
        verbose=args.verbose
        )
    fruchterman_reingold.run()
    
if __name__ == '__main__':
    main()
