class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cadena:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.ultimos_pasos = 0

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def __len__(self):
        total = 0
        actual = self.cabeza
        while actual is not None:
            total += 1
            actual = actual.siguiente
        return total

    def a_lista(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

    def medio_dos_pasadas(self):
        self.ultimos_pasos = 0
        total = 0
        actual = self.cabeza

        # Primera pasada: contar nodos, incluyendo el avance final a None.
        while actual is not None:
            total += 1
            actual = actual.siguiente
            self.ultimos_pasos += 1

        if total == 0:
            return None

        # Segunda pasada: llegar al primero de los dos centrales si hay par.
        posicion = (total - 1) // 2
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente
            self.ultimos_pasos += 1
        return actual.dato

    def medio(self):
        self.ultimos_pasos = 0
        if self.cabeza is None:
            return None

        lento = self.cabeza
        rapido = self.cabeza

        # El rápido avanza dos enlaces y el lento uno.
        # La condición deja el lento en el primer centro cuando hay cantidad par.
        while rapido.siguiente is not None and rapido.siguiente.siguiente is not None:
            lento = lento.siguiente
            rapido = rapido.siguiente.siguiente
            self.ultimos_pasos += 3

        return lento.dato

    def invertir(self):
        anterior = None
        actual = self.cabeza
        self.cola = self.cabeza

        while actual is not None:
            siguiente = actual.siguiente
            actual.siguiente = anterior
            anterior = actual
            actual = siguiente

        self.cabeza = anterior


class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class Doble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar(self, dato):
        nuevo = NodoDoble(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def __len__(self):
        total = 0
        actual = self.cabeza
        while actual is not None:
            total += 1
            actual = actual.siguiente
        return total

    def a_lista(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

    def a_lista_al_reves(self):
        datos = []
        actual = self.cola
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.anterior
        return datos

    def invertir(self):
        actual = self.cabeza
        while actual is not None:
            # Se intercambian los enlaces de cada nodo.
            actual.anterior, actual.siguiente = actual.siguiente, actual.anterior
            actual = actual.anterior

        self.cabeza, self.cola = self.cola, self.cabeza


if __name__ == "__main__":
    print("Medición de búsqueda del nodo central")
    print("nodos | dos pasadas | liebre y tortuga")

    for cantidad in (1001, 10001, 100001):
        cadena = Cadena()
        for numero in range(cantidad):
            cadena.agregar(numero)

        cadena.medio_dos_pasadas()
        dos_pasadas = cadena.ultimos_pasos
        cadena.medio()
        liebre_tortuga = cadena.ultimos_pasos
        print(f"{cantidad} | {dos_pasadas} | {liebre_tortuga}")
