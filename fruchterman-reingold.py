#!/usr/bin/python3

import argparse
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
        pass
    
    def repulsion(self, delta):
        '''Calcula la fuerza de repulsión dado el vector diferencia'''
        pass
    
    def atraccion(self, delta):
        '''Calcula la fuerza de atracción dado el vector diferencia'''
        pass
    
    def step(self, delta):
        '''
        Efectúa un paso de la simulación, actualizando posiciones 
        de los nodos
        '''
    
    def create_view(self):
        '''Inicializa el graficador'''
        pass
    
    def run(self):
        '''
        Ejecuta los pasos del algoritmo, de acuerdo a los argumentos
        con los cuales se inicializó la clase.
        '''
        pass

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
