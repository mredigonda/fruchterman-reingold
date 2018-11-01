#!/usr/bin/python3

import argparse
import math
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
        return self.c1 * self.k**2 / d
    
    def atraccion(self, d):
        '''Calcula la fuerza de atracción dada la distancia'''
        return self.c2 * d**2 / self.k
    
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
                self.posiciones[node].x = min(self.W, max(0, npos.x))
                self.posiciones[node].y = min(self.H, max(0, npos.y))
        self.t -= self.dt
    
    def create_view(self):
        '''Inicializa el graficador'''
        self.graficador = Graficador(800, 600)

    def dibujar(self):
        '''Dibuja el grafo mediante el graficador'''
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
            # Realizar un paso de la simulacion
            self.step()
            if i % 20 == 0 and self.verbose:
                print('Temperatura: ' + str(self.t))
                
            # Si es necesario, lo mostramos por pantalla
            if (self.refresh > 0 and i % self.refresh == 0):
                self.dibujar()
            
        # Ultimo dibujado al final
        self.dibujar()
        
        # Solo al final, permitimos que el usuario cierre la ventana
        self.graficador.permitir_cerrado()

def obtenerArgumentos():
    '''Procesa los argumentos de la linea de comandos'''
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
                        default=3e-3)
                        
    # Fuerza de atracción, opcional. 2.5 por defecto.
    parser.add_argument('-c2', '--atraccion', type=float, 
                        help='Constante de atracción de aristas', 
                        default=3e-2)
                        
    # Cantidad de iteraciones, opcional, 50 por defecto.
    parser.add_argument('-i', '--iters', type=int, 
                        help='Cantidad de iteraciones a efectuar', 
                        default=500)

    # Ruta al archivo conteniendo la descripción del grafo. Requerida.
    parser.add_argument('-p', '--path',
                        help='Ruta al archivo con la descripción del grafo')

    args = parser.parse_args()
    return args
    
def main():
    args = obtenerArgumentos()
    
    # Leemos el grafo del archivo indicado
    f = open(args.path, 'r')
    n, m = f.readline().split(' ')
    n = int(n)
    m = int(m)
    nodos = []
    aristas  = []
    for i in range(n):
        nodos.append(f.readline().rstrip())
    for i in range(m):
        a, b = f.readline().split(' ')
        a = a.rstrip()
        b = b.rstrip()
        aristas.append( (a, b) )
    grafo = (nodos, aristas)
    
    # Inicializamos la clase y corremos el algoritmo
    fruchterman_reingold = FruchtermanReingold(
        grafo,
        iters=args.iters,
        refresh=args.refresh,
        c1=args.repulsion,
        c2=args.atraccion,
        verbose=args.verbose
        )
    fruchterman_reingold.run()
    
if __name__ == '__main__':
    main()
