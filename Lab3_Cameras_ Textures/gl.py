from MathLib import *
from math import pi, sin, cos, isclose

POINTS = 0
LINES = 1
TRIANGLES = 2


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = self.screen.get_rect()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)

        self.glClear()

        self.primitiveType = TRIANGLES

        # Matrices
        self.activeModelMatrix = None
        self.activeViewMatrix = None
        self.activeProjectionMatrix = None
        self.activeViewportMatrix = None

        self.activeTextureList = None

        # Shaders
        self.activeVertexShader = None
        self.activeFragmentShader = None

        self.dirLight = [1,0,0]
        
        self.camera = Camera()

        # Crear matriz de viewport
        self.activeViewportMatrix = ViewportMatrix(0, 0, self.width, self.height)
        
        # Crear matriz de proyección (se puede actualizar)
        aspect = self.width / self.height
        self.activeProjectionMatrix = self.camera.getProjectionMatrix(aspect)
        
        # Matriz de vista inicial
        self.activeViewMatrix = self.camera.getViewMatrix()


        self.models = []

    def setupCamera(self, position, target, up=[0, 1, 0], fov=60):
        """Configurar la cámara manualmente"""
        self.camera.position = position
        self.camera.target = target
        self.camera.up = up
        self.camera.fov = fov
        self.updateViewMatrix()
        self.updateProjectionMatrix()
    
    def updateViewMatrix(self):
        """Actualizar matriz de vista"""
        self.activeViewMatrix = self.camera.getViewMatrix()
    
    def updateProjectionMatrix(self):
        """Actualizar matriz de proyección"""
        aspect = self.width / self.height
        self.activeProjectionMatrix = self.camera.getProjectionMatrix(aspect)
    
    def setCameraShot(self, shotType, modelCenter=[0, 0, 0], modelSize=[2, 2, 2]):
        """
        Configurar la cámara para las diferentes tomas fotográficas
        shotType: 'medium', 'low', 'high', 'dutch'
        """
        if shotType == 'medium':
            self.camera.setMediumShot(modelCenter, modelSize)
        elif shotType == 'low':
            self.camera.setLowAngle(modelCenter, modelSize)
        elif shotType == 'high':
            self.camera.setHighAngle(modelCenter, modelSize)
        elif shotType == 'dutch':
            self.camera.setDutchAngle(modelCenter, modelSize)
        
        self.updateViewMatrix()
        self.updateProjectionMatrix()
        
        print(f"Cámara configurada para: {shotType} shot")
        print(f"Posición: {self.camera.position}")
        print(f"Target: {self.camera.target}")
        
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
        
        #Buffer donde se guardan los valores de profundidad de cada pixel
        self.zBuffer = [[float('inf') for y in range(self.height)]
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


    #Funcion para rellenado con triangulos
    #El punto A esta hasta arriba, el punto B esta a la izquierda y el punto C esta a la derecha
    #A hasta arriba y C siempre hasta abajo
    #Tenemos 3 casos de triangulos, 1 normal, 1 volteado y 1 irregular
    #El triangulo irregular se puede partir en 2 y asi formar 2 triangulos planos (1 de arriba y 1 de abajo)
    def glTriangle(self, A, B, C):
        #Asegurarse de que los vertices entren en orden
        #A.y > B.y > C.y
        if A[1] < B[1]:
            A, B = B, A
        
        if A[1] < C[1]:
            A, C = C, A
        
        if B[1] < C[1]:
            B, C = C, B
        
        #Triangulo plano hacia abajo
        def flatBottom(vA, vB, vC):
            try:
                mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
            except:
                pass

            else:

                if vB[0] > vC[0]:
                    vB, vC = vC, vB
                    mBA, mCA = mCA, mBA

                x0 = vB[0]
                x1 = vC[0]

                for y in range(round(vB[1]), round(vA[1] + 1)):
                    for x in range(round(x0), round(x1) + 1):
                        vP = [x,y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)
                        
                    #Calcular el valor de x para cada y
                    x0 += mBA
                    x1 += mCA

         #Triangulo con el plano arriba
        def flatTop(vA, vB, vC):
            try:
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
                mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
            except:
                pass

            else:

                if vA[0] > vB[0]:
                    vA, vB = vB, vA
                    mCA, mCB = mCB, mCA

                x0 = vA[0]
                x1 = vB[0]

                for y in range(round(vA[1]), round(vC[1] - 1), - 1):
                    for x in range(round(x0), round(x1 + 1)):
                        vP = [x,y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)

                    #Calcular el valor de x para cada y
                    x0 -= mCA
                    x1 -= mCB
        
        if B[1] == C[1]:
            #Si el punto A es el de arriba, entonces tenemos un triangulo plano abajo
            flatBottom(A, B, C)

        #Triangulo con el plano arriba
        elif A[1] == B[1]:
            #Si el punto A es el de arriba, entonces tenemos un triangulo plano
            flatTop(A, B, C)

        #Triangulo irregular
        #Hay que dibujar los 2 casos anteriores de triangulos
        else:
            #Teorema del intercepto
            D = [ A[0] + ((B[1] - A[1])/ (C[1] - A[1])) * (C[0] - A[0]), B[1],]
            u, v, w = barycentricCoords(A, B, C, D)
            D.append(u * A[2] + v * B[2] + w * C[2])

            flatBottom(A, B, D)
            flatTop(B, D, C)

    
    def glRender(self):
        for model in self.models:
            # Por cada modelo en la lista, los dibujo
            # Agarrar su matriz modelo y vertexshader
            self.activeModelMatrix = model.GetModelMatrix()
            self.activeVertexShader = model.vertexShader
            self.activeFragmentShader = model.fragmentShader
            self.activeTextureList = model.textureList
        
            # CAMBIO IMPORTANTE: Usar textureList en vez de texture
            if hasattr(model, 'textureList') and len(model.textureList) > 0:
                self.activeTexture = model.textureList[0]
            else:
                self.activeTexture = None

            # Aqui vamos a guardar todos los vertices y su info correspondiente
            vertexBuffer = []
        
            # CAMBIO IMPORTANTE: Iterar sobre las caras del modelo
            for face in model.faces:
                # Para cada vértice del triángulo
                faceVerts = []
            
                for i in range(3):  # Triángulos tienen 3 vértices
                    vert = []
                
                    # Agregamos los valores de posición al contenedor del vértice
                    pos_idx = face['vertices'][i]
                    pos = model.vertices[pos_idx]
                    vert.extend(pos)  # x, y, z
                
                    # Agregamos las normales
                    if face['normals'] and i < len(face['normals']):
                        normal_idx = face['normals'][i]
                        normal = model.normals[normal_idx]
                        vert.extend(normal)  # nx, ny, nz
                    else:
                        vert.extend([0.0, 0.0, 1.0])
                
                    # Agregamos las coordenadas de textura
                    if face['texcoords'] and i < len(face['texcoords']):
                        texcoord_idx = face['texcoords'][i]
                        texCoord = model.texCoords[texcoord_idx]
                        vert.extend(texCoord)  # u, v
                    else:
                        vert.extend([0.0, 0.0])
                
                    # Agregamos la información de este vértice a la lista de vértices de esta cara
                    faceVerts.append(vert)
            
                # Si contamos con un Vertex Shader, se manda cada vertice
                # para transformalos. Recordar pasar las matrices necesarias
                # para usarlas dentro del shader
                for vert in faceVerts:
                    x, y, z = vert[0], vert[1], vert[2]
                
                    if self.activeVertexShader:
                        x, y, z = self.activeVertexShader([x,y,z],
                                                        modelMatrix = self.activeModelMatrix,
                                                        viewMatrix = self.activeViewMatrix,
                                                        projectionMatrix = self.activeProjectionMatrix,
                                                        viewportMatrix = self.activeViewportMatrix)
                
                    # Agregar al vertexBuffer con las coordenadas transformadas
                    vertexBuffer.extend([x, y, z] + vert[3:8])
        
            self.glDrawPrimitives(vertexBuffer, 8)

        
    def glDrawPrimitives(self, buffer, vertexOffset):
        
        # El buffer es un listado de valores que representan
		# toda la informacion de un vertice (posicion, coordenadas
		# de textura, normales, color, etc.). El VertexOffset se
		# refiere a cada cuantos valores empieza la informacion
		# de un vertice individual
		# Se asume que los primeros tres valores de un vertice
		# corresponden a Posicion.

        if self.primitiveType == POINTS:
            # Si son puntos, revisamos el buffer en saltos igual
			# al Vertex Offset. El valor X y Y de cada vertice
			# corresponden a los dos primeros valores.
                for i in range(0, len(buffer), vertexOffset):
                    x = buffer[i]
                    y = buffer[i + 1]
                    self.glPoint(x,y)

        elif self.primitiveType == LINES:
            # Si son lineas, revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo. 
            for i in range(0, len(buffer), vertexOffset * 3):
                 for j in range(3):
					# Hay que dibujar la linea de un vertice al siguiente
                    x0 = buffer[i + vertexOffset * j + 0]
                    y0 = buffer[i + vertexOffset * j + 1]

					# En caso de que sea el ultimo vertices, el siguiente
					# seria el primero
                    x1 = buffer[i + vertexOffset * ((j + 1) % 3) + 0]
                    y1 = buffer[i + vertexOffset * ((j + 1) % 3) + 1]
                    
                    self.glLine((x0,y0), (x1,y1) )
        
        elif self.primitiveType == TRIANGLES:
			# Si son triangulos revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo. 
            for i in range(0, len(buffer), vertexOffset * 3):
                
				# Necesitamos tres vertices para mandar a dibujar el triangulo.
				# Cada vertice necesita todos sus datos, la cantidad de estos
				# datos es igual a VertexOffset
                A = [ buffer[i + j + vertexOffset * 0] for j in range(vertexOffset) ]
                B = [ buffer[i + j + vertexOffset * 1] for j in range(vertexOffset) ]
                C = [ buffer[i + j + vertexOffset * 2] for j in range(vertexOffset) ]
                
                self.glTriangle(A,B,C)
                

    def glDrawTrianglePoint(self, A, B, C, P):
        
        x = P[0]
        y = P[1]

        # Si el punto no está dentro de la ventana, lo descartamos
        if not(0 <= x < self.width) or not(0 <= y < self.height):
            return
        
        # Obtenemos las coordenadas baricentricas para el punto p
        bCoords = barycentricCoords(A, B, C, P)

        # Si son coordenadas invalidas, descarto el pixel
        if bCoords == None:
            return
        
        u, v, w = bCoords

        if not isclose(u+v+w, 1.0):
            return

        z = u * A[2] + v * B[2] + w * C[2]

        # Si el valor de Z para este punto es mayor que 
        # el valor guardado en Zbuffer, el pixel esta mas lejos
        # entonces descarto el pixel

        if z >= self.zBuffer[x][y]:
            return
        
        self.zBuffer[x][y] = z

        color = None  # Color base
    
        if self.activeFragmentShader:
            color = self.activeFragmentShader(verts = [A, B, C],
                                        bCoords = [u, v, w],
                                        pixelColor = self.currColor,
                                        dirLight = self.dirLight,
                                        textureList = self.activeTextureList)
    
    
        self.glPoint(x,y, color)
         




            
    

    

    
    


