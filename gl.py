class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = self.screen.get_rect()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)

        self.glClear()
    
    #Es para el color del fondo de la pantalla
    def glClearColor(self, r, g, b):
        #los valores de r, g, b deben estar entre 0 y 1
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.ClearColor = [r,g,b]
    
    #Para el color del pixel
    def glColor(self, r, g, b):
        #los valores de r, g, b deben estar entre 0 y 1
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        #curr para el color actual
        self.currColor = [r,g,b]
    
    #Para aplicar el color de fondo
    def glClear(self):
        #compresion de listas
        color = [int(i * 255) for i in self.ClearColor]
        self.screen.fill(color)

        self.frameBuffer = [[color for y in range(self.height)]
                            for x in range(self.width)]
    
    #Para dibujar un punto en la pantalla
    #pygame renderiza desde la esquina superior izquierda y hay que voltear la y
    def glPoint(self, x, y, color = None):
        
        x = round(x)
        y = round(y)

        if (0 <= x < self.width) and (0 <= y < self.height):
             color = [int(i * 255) for i in (color or self.currColor)]
             self.screen.set_at((x, self.height - y - 1), color)

             self.frameBuffer[x][y] = color
    
    #Para dibujar lineas en la pantalla
    def glLine(self, p0, p1, color = None):
        # y = mx + b

        #Algoritmo de linea de Bresenham
        x0 = p0[0]
        x1 = p1[0]
        y0 = p0[1]
        y1 = p1[1] 
        
        #Revisar si el punto es igual que el punto 1, solamente dibujar un punto. Para evitar division por cero
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return
        
        #En vez de sacar las pendientes, sacamos los deltas
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #steep corresponde a inclinación
        steep = dy > dx
        #Si la inclinación es mayor a 1, intercambiamos los puntos
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        #Cuando algo va de derecha a izquierda
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        #Volver a calcular los deltas
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Ahora ya podemos dibujar las lineas
        #Pero antes de dibujar las lineas, tenemos que calcular algunas cosas extra

        #1. el offset, el offset se refiere a cuanto eh subido en la linea
        offset = 0
        #2. el limite, se refiere a partir de que punto se va a dibujar la siguiente linea o siguiente fila de pixeles
        limit = 0
        #3. la pendiente, que es la diferencia entre los deltas
        m = dy / dx
        #4.valor en y actualmente
        y = y0

        #Asegurarse de que los valores de x que se pasan también son enteros
        for x in range(round(x0), round(x1) + 1):
            #Si la inclinación es mayor a 1, entonces tenemos que intercambiar los valores de x e y
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor) 

            #Aumentar el offset
            offset += m

            #Si el offset es mayor al limite, entonces tenemos que aumentar el valor de y
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                #Aumentar el limite, para pasar a la siguiente fila de pixeles
                limit += 1

    #Dibujar un poligono
    def glPolygon(self, puntos, color = None):
        #Recorrer los puntos y dibujar las lineas entre ellos
        for i in range(len(puntos)):
            #Tomar el punto actual en la posicion i
            punto_actual = puntos[i]
            #Calcula cual es el siguiente punto y usa el módulo para cerrar el polígono
            punto_siguiente = puntos[(i + 1) % len(puntos)]
            #Dibuja la línea entre el punto actual y el siguiente
            self.glLine(punto_actual, punto_siguiente, color or self.currColor)

    #Rellenar un polígono usando el algoritmo de scanline
    #1. Función que recibe un lista de puntos y un color de manera opcional
    def glFillPolygon(self, puntos, color = None):
        #2. Dibujamos el contorno
        self.glPolygon(puntos, color)
        
        #3. Encontrar los valores mínimos y máximos de Y para saber el rango de scanlines
        y_min = min(punto[1] for punto in puntos)
        y_max = max(punto[1] for punto in puntos)
        
        #4. Recorre cada fila horizontal desde y_min hasta y_max
        for y in range(y_min, y_max + 1):
            #5. Se crea una lista para almacenar las intersecciones al cruzar los bordes los polígonos
            intersecciones = []
            
            #6. Recorre cada lado del polígono, hasta cerrar el polígono
            for i in range(len(puntos)):
                p1 = puntos[i]
                p2 = puntos[(i + 1) % len(puntos)]
                
                #7. Extrar las coordenadas de cada punto
                x1, y1 = p1
                x2, y2 = p2
                
                #8. Normalizar los lados para que vayamos de abajo hacia arriba
                if y1 > y2:
                    x1, y1, x2, y2 = x2, y2, x1, y1
                
                #9. Verificar si la scanline intersecta con las aristas del polígono
                #No se incluye y2 para evitar contar vértices dos veces
                if y1 <= y < y2: 

                    #10. Luego de saber si las scanLines tienen intersecciones con el polígono
                    #Calcular la intersección x usando una ecuación de interpolación lineal (método para estimar un valor desconocido entre dos puntos de datos conocidos)
                    if y2 - y1 != 0: #Verificar que no sea una línea horizontal y evitar división por cero
                        x_interseccion = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                        #11. Agregar las intersecciones encontradas a la lista
                        intersecciones.append(x_interseccion)
            
            #12. Ordenar las intersecciones de izquierda a derecha
            intersecciones.sort()
            
            #13. #Se van recorriendo las intersecciones de dos en dos
            for i in range(0, len(intersecciones) - 1, 2):
                #14. Sacar las coordenadas x de inicio y fin de la línea horizontal
                x_inicio = int(intersecciones[i])
                x_fin = int(intersecciones[i + 1])
                
                #15. Dibujar línea horizontal entre las intersecciones o mejor dicho pintar los píxeles
                for x in range(x_inicio, x_fin + 1):
                    self.glPoint(x, y, color or self.currColor)
    

    

    
    


