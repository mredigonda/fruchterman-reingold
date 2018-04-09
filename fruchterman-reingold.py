#!/usr/bin/python3

import argparse
import random
import time

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
            x = random.randrange(1, 800)
            y = random.randrange(1, 600)
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
        self.randomize_node_positions()
    
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
