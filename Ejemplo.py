"""
06/04/2019
@FelipedelosH

Programo un grafo a mi gusto (segun wikipedia)...
    >>Conjunto de nodos
    >>Conjunto de aristas con peso. 
    >>Dirijido


Programa Dijsktra a mi gusto..
    >>llenando tablita
    Se llama self.tablaDisjtra

"""

# Importo para representar el infinito
from math import inf


class Grafo():
    def __init__(self):
        # Cada nodo sera almacenado aqui
        self.nodos = []
        # Las Aristas son almacenadas aqui
        # origen: (destino1, peso), (destono2, peso) .... (destinon, peso)
        self.aristas = {}
        # Aqui se guarda Dijstra
        self.tablaDisjtra = []
        # temporal para controlar los nodos ya visitados
        self.procesadosDJ = []

    # Este metodo agrega un nodo 
    def addNodo(self, x):
        if x not in self.nodos:
            self.nodos.append(x)

    # Si el origen y el destino existe se vinculan por el peso
    # 1 ro verifico que el peso sea positivo
    # 2do verifico que origen y destino existan
    # 3ro esto se guarda en un vector... pero al inicio el vector nisiquiera existe
    # por eso construyo el vector y luego puedo guardar en el.
    def addCamino(self, origen, destino, peso):
        try:
            if peso >= 0:
                if origen in self.nodos and destino in self.nodos:
                    if origen in self.aristas:
                        self.aristas[origen].append((destino, peso))
                    else:
                        self.aristas[origen] = []
                        self.aristas[origen].append((destino, peso))
                else:
                    print('Error en nodos')
            else:
                print('Peso no permitido')
        except:
            print('Error Fatal agregando el camino')

    # Este metodo me retorna la distancia entre origen y destino si estan interconectados
    # 1 ro verifico que los puntos existan, si no retorna -99
    # -99 la cual es una distancia no permitida
    # Si a y b son el mismo punto sin definir una conexion al mismo punto
    # Si a y b no estan interconectados retorno infinito
    def distanciaAB(self, a, b):
        if a in self.nodos and b in self.nodos:
            if a in self.aristas:
                for i in self.aristas[a]:
                    if i[0] == b:
                        return i[1]

            if a == b:
                return 0

            return inf

        else:
            return -99

    # Compruebo que el origen exista
    # Dijsktra empieza en una tabla de nodosxnodos
    # Luego llama al metodo llenarTablaDJ
    def dijsktra(self, origen):
        if origen in self.nodos:
            # Creo la tabla:
            # Ojo depende de el orden de los nodos
            # la tabla en la pos0 corresponde a nodos[0]
            dijsktra = []

            for i in range(0, len(self.nodos)):
                dijsktra.append([])
                for j in range(0, len(self.nodos)):
                    dijsktra[i].append(())

            # Se procede a llenar el primer paso de la tabla
            self.llenarTablaDJ(origen, dijsktra, 0, 0)

            # Se procede a llenar el resto de la tabla
            self.mejorCandidatoTabla(dijsktra, 0)


                
        else:
            print('Ese origen no existe')


    # Este metodo actualiza la tabla de Dijsktra
    # Esta tabla es un objeto de la clase
    # 1ro lleno las dimenciones de la tabla
    # 2do se llenan los valores iniciales
    def actualizarDijstra(self, origen):
        if origen in self.nodos:
            # Reinicio la tabla
            self.tablaDisjtra = []
            longitudTabla = len(self.nodos)

            # Preparo los espacios necesarios en la tabla
            for i in range(0, longitudTabla):
                self.tablaDisjtra.append([])
                for j in range(0, longitudTabla):
                    self.tablaDisjtra[i].append(0)

            """======================================="""
            #lleno el primer paso (Por defecto)
            self.nextPasoTablaDJ(origen, 0, 0)
            """======================================="""

            #Relleno el resto de la tabla
            for dj in range(1, len(self.tablaDisjtra)):
                # Se procede a escojer mejor_candidato y peso minimo de lo que va la tabla
                pesoycand = self.mejorCandidato(dj-1)

                # Se dispone a actualizar la tabla con el candidato y el peso actualizado
                self.nextPasoTablaDJ(self.nodos[pesoycand[1]], dj, pesoycand[0], pesoycand[1])

        else:
            print("Error: ", origen)


    # Privote se refiere al nodo en que estoy parado
    # iteracion es el paso de la tabla en el que estoy
    # Peso acululado es el peso anterior
    # Pos en la tabla es en que posicion de la tabla dijsktra esta el pivote
    def nextPasoTablaDJ(self, pivote, iteracion, peso_acumulado, pos_tabla=0):
        # Lo marco como procesado
        self.procesadosDJ.append(pivote)
        # Si es la primera la lleno por defector
        if iteracion == 0:
            # Auxiliar para la iteracion (saber que nodo en la tabla estoy parado)
            aux = 0
            for i in self.tablaDisjtra:
                # Relleno la tabla 
                i[iteracion] = (self.distanciaAB(pivote, self.nodos[aux]), pivote)
                # Ojo el 0, origen ... anulo sus consecuentes
                if self.nodos[aux] == pivote:
                    for x in range(1, len(i)):
                        i[x] = "x"
                aux = aux + 1
        else:
            # Este fue marcado como el mejor candidato procedo a eliminar sus consecuentes
            for x in range(iteracion+1, len(self.tablaDisjtra)):
                self.tablaDisjtra[pos_tabla][x] = "x"
            # Auxiliar para la iteracion (saber que nodo en la tabla estoy parado)
            aux = 0
            for i in self.tablaDisjtra:
                # No calculo los varoles marcados
                if i[iteracion] != "x":
                    pesoAB = self.distanciaAB(pivote, self.nodos[aux])+peso_acumulado
                    # Si el peso nuevo, es mejor que el antiguo actualizo, si no pasa el anterior
                    if pesoAB < i[iteracion-1][0]:
                        i[iteracion] = (pesoAB, pivote)
                    else:
                        i[iteracion] = i[iteracion-1]
                
                aux = aux + 1



    
    # Este metodo busca en la iteracion x de la tablaDJ cual es el mejor candidato
    def mejorCandidato(self, iteracion):
        peso_minimo = inf
        objetivo = 0
        
        aux = 0
        for i in self.tablaDisjtra:
            if i[iteracion] != "x":
                if i[iteracion][0] < peso_minimo and self.nodos[aux] not in self.procesadosDJ:
                    peso_minimo = i[iteracion][0]
                    objetivo = aux
            aux = aux + 1

        return peso_minimo, objetivo

   
# Procedo a instanciar el grafo
g = Grafo()
g.addNodo("a")
g.addNodo("b")
g.addNodo("c")
g.addNodo("d")
g.addNodo("e")
g.addNodo("f")


g.addCamino("a", "b", 5)
g.addCamino("b", "a", 5)

g.addCamino("a", "f", 3)
g.addCamino("f", "a", 5)

g.addCamino("b", "c", 2)
g.addCamino("c", "b", 5)

g.addCamino("b", "e", 7)
g.addCamino("e", "b", 5)

g.addCamino("c", "e", 4)
g.addCamino("e", "c", 4)

g.addCamino("c", "d", 1)
g.addCamino("d", "c", 1)

g.addCamino("e", "d", 8)
g.addCamino("d", "e", 8)

g.addCamino("f", "d", 6)
g.addCamino("d", "f", 6)


g.actualizarDijstra("a")
# Muestro el dijstra
for i in g.tablaDisjtra:
    print(i)






