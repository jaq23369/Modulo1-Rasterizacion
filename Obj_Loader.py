#Constructor de un cargador de archivos OBJ, creando una clase llamada OBJLoader
class OBJLoader:
    def __init__(self, filename):
        #Crea una lista vacía para almacenar los vértices (Puntos)
        self.vertices = []
        #Lista para almacenar las normales
        self.normals = []
        # Lista para almacenar las coordenadas de textura
        self.texcoords = []  
        #Crea una lista vacía para almacenar las caras (Triángulos)
        self.faces = []
        # Lista para almacenar los indices de las normales
        self.face_normals = []
        # Lista para almacenar los indices de las coordenadas de textura
        self.face_texcoords = []  
        #Llamada a función que va a leer el archivo OBJ
        self.loadOBJ(filename)
    
    # Función que se encarga de cargar el archivo OBJ, la cual recibe el nombre del archivo como parámetro
    def loadOBJ(self, filename):
        # Intenta abrir el archivo para leer su contenido
        try:
            with open(filename, 'r') as file:
                #Va leyendo el archivo línea por línea
                for line in file:
                    #Aquí se asegura de eliminar espacios en blanco al inicio, al final y los saltos de línea
                    line = line.strip()
                    
                    #Verificacion de que la linea este vacia o que comience con un comentario
                    if not line or line.startswith('#'):
                        #Si cualquiera de las condiciones se cumple, se salta la linea siguiente
                        continue
                    
                    #Esta parte se encarga de dividir cada linea en trozos, para identificar que es cada dato
                    parts = line.split()
                    
                    # Con este ciclo if permite ir revisando la lista y si en dado caso es un vertice
                    # va tomando cada valor y lo va conviertiendo a número decimal
                    #Luego lo almacena en la lista de vértices
                    if parts[0] == 'v':
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3]) if len(parts) > 3 else 0.0
                        self.vertices.append([x, y, z])
                    
                    elif parts[0] == 'vn':
                        nx = float(parts[1])
                        ny = float(parts[2])
                        nz = float(parts[3])
                        self.normals.append([nx, ny, nz])
                    
                    elif parts[0] == 'vt':
                        u = float(parts[1])
                        v = float(parts[2]) if len(parts) > 2 else 0.0
                        self.texcoords.append([u, v])
                    
                    # Si en dado caso no es un vértice, revisa si es una cara
                    elif parts[0] == 'f':
                        # Se crea una lista para almacenar los vertices de las caras
                        # porque se necesita ver la posicion 3D, por eso solo almacena esto
                        face_vertices = []
                        # Para guardar índices de normales
                        face_normal_indices = []
                        # Para guardar índices de coordenadas de textura
                        face_uv_indices = []

                        # Este ciclo for se encarga de omitir la palabra f y tomar los datos de los vértices
                        for vertex_data in parts[1:]:
                            # Separar v/vt/vn
                            indices = vertex_data.split('/')
                            vertex_index = int(indices[0]) - 1
                            face_vertices.append(vertex_index)

                            # Obtener índice de normal si existe
                            if len(indices) == 3:
                                normal_index = int(indices[2]) - 1
                                face_normal_indices.append(normal_index)

                            # Obtener índice de textura si existe
                            if len(indices) >= 2 and indices[1]:
                                uv_index = int(indices[1]) - 1
                                face_uv_indices.append(uv_index)

                        
                        # En dado caso haya 3 vertices se crea un triángulo
                        # pero si hay más de 3 vertices, se divide en triángulos de 3 vertices y se agrega a la lista
                        if len(face_vertices) >= 3:
                            for i in range(1, len(face_vertices) - 1):
                                triangle = [face_vertices[0], face_vertices[i], face_vertices[i + 1]]
                                self.faces.append(triangle)

                                if face_normal_indices:
                                    normal_triangle = [
                                        face_normal_indices[0],
                                        face_normal_indices[i],
                                        face_normal_indices[i + 1]
                                    ]
                                    self.face_normals.append(normal_triangle)
                                
                                if face_uv_indices:
                                    uv_triangle = [
                                        face_uv_indices[0],
                                        face_uv_indices[i],
                                        face_uv_indices[i + 1]
                                    ]
                                    self.face_texcoords.append(uv_triangle)
        
        # Si el archivo no se encuentra, se captura la excepción y se imprime un mensaje de error
        # De la misma forma si ocurre cualquier otro error al cargar el archivo   
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo {filename}")
        except Exception as e:
            print(f"Error al cargar el archivo OBJ: {e}")
    
    # Funcion para convertir los datos del obj en algo que entienda el rasterizador
    def getVertices(self):
        # Crea una lista vacía para almacenar los vértices en orden
        vertex_list = []
        # Con este ciclo for recorre cada triangulo guardado en la lista de caras
        for face in self.faces:
            # Con este otro ciclo for recorre cada índice de vértice en la cara
            for vertex_index in face:
                # Con esto va a buscar las coordenadas del vértice
                vertex = self.vertices[vertex_index]
                # Con esto agrega las coordenadas a la lista final
                vertex_list.extend(vertex)
        #De vuelve la lista completa  
        return vertex_list
    
    def getNormals(self):
        normal_list = []
        if not self.face_normals:
            return None
        
        for face_normal in self.face_normals:
            for normal_index in face_normal:
                normal = self.normals[normal_index]
                normal_list.extend(normal)
        return normal_list
    
    def getTextureCoords(self):
        texcoords_list = []
        if not self.face_texcoords:
            return None
        
        for face_uv in self.face_texcoords:
            for uv_index in face_uv:
                uv = self.texcoords[uv_index]
                texcoords_list.extend(uv)
        return texcoords_list
    
    #Con esta función se puede obtener el conteo de las caras
    def getFaceCount(self):
        #De vuelve el numero de triangulos que tiene el modelo
        return len(self.faces)
    
    #Con esta función se puede centrar y escalar el modelo 3D automáticamente
    def getBounds(self):
        #Si no hay vértices, no devuelve nada
        if not self.vertices:
            return None
        #Pero como si los hay, va sacando el mínimo y máximo de las coordenadas X, Y, Z
        min_x = min(v[0] for v in self.vertices)
        max_x = max(v[0] for v in self.vertices)
        min_y = min(v[1] for v in self.vertices)
        max_y = max(v[1] for v in self.vertices)
        min_z = min(v[2] for v in self.vertices)
        max_z = max(v[2] for v in self.vertices)
        #Para luego devolver un diccionario con los valores mínimos, máximos, centro y tamaño del modelo
        return {
            'min': [min_x, min_y, min_z],
            'max': [max_x, max_y, max_z],
            'center': [(min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2],
            'size': [max_x - min_x, max_y - min_y, max_z - min_z]
        }
    # Función para imprimir información del modelo cargado
    def getInfo(self):
        bounds = self.getBounds()
        print(f"Modelo cargado:")
        print(f"  Vértices: {len(self.vertices)}")
        print(f"  Triángulos: {len(self.faces)}")
        print(f"  Normales: {len(self.normals)}")
        print(f"  Coords UV: {len(self.texcoords)}")
        if bounds:
            print(f"  Tamaño: {bounds['size']}")
            print(f"  Centro: {bounds['center']}")