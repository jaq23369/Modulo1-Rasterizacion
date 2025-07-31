#Constructor de un cargador de archivos OBJ, creando una clase llamada OBJLoader
class OBJLoader:
    def __init__(self, filename):
        #Crea una lista vacía para almacenar los vértices (Puntos)
        self.vertices = []
        #Crea una lista vacía para almacenar las normales
        self.normals = []
        #Crea una lista vacía para almacenar las coordenadas de textura
        self.texCoords = []
        #Crea una lista vacía para almacenar las caras (Triángulos)
        self.faces = []
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
                    
                    # Leer vértices
                    if parts[0] == 'v':
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3]) if len(parts) > 3 else 0.0
                        self.vertices.append([x, y, z])
                    
                    # Leer normales
                    elif parts[0] == 'vn':
                        nx = float(parts[1])
                        ny = float(parts[2])
                        nz = float(parts[3]) if len(parts) > 3 else 0.0
                        self.normals.append([nx, ny, nz])
                    
                    # Leer coordenadas de textura
                    elif parts[0] == 'vt':
                        u = float(parts[1])
                        v = float(parts[2]) if len(parts) > 2 else 0.0
                        self.texCoords.append([u, v])
                    
                    # Leer caras
                    elif parts[0] == 'f':
                        # Se crea una lista para almacenar los vertices de las caras
                        face_vertices = []
                        face_normals = []
                        face_texcoords = []
                        
                        # Este ciclo for se encarga de omitir la palabra f y tomar los datos de los vértices
                        for vertex_data in parts[1:]:
                            # Dividir por '/' para obtener vertex/texture/normal
                            indices = vertex_data.split('/')
                            
                            # Índice del vértice (siempre presente)
                            vertex_index = int(indices[0]) - 1
                            face_vertices.append(vertex_index)
                            
                            # Índice de coordenada de textura (opcional)
                            if len(indices) > 1 and indices[1]:
                                tex_index = int(indices[1]) - 1
                                face_texcoords.append(tex_index)
                            
                            # Índice de normal (opcional)
                            if len(indices) > 2 and indices[2]:
                                normal_index = int(indices[2]) - 1
                                face_normals.append(normal_index)
                        
                        # En dado caso haya 3 vertices se crea un triángulo
                        # pero si hay más de 3 vertices, se divide en triángulos de 3 vertices y se agrega a la lista
                        if len(face_vertices) >= 3:
                            for i in range(1, len(face_vertices) - 1):
                                triangle = {
                                    'vertices': [face_vertices[0], face_vertices[i], face_vertices[i + 1]],
                                    'normals': [face_normals[0], face_normals[i], face_normals[i + 1]] if face_normals else [],
                                    'texcoords': [face_texcoords[0], face_texcoords[i], face_texcoords[i + 1]] if face_texcoords else []
                                }
                                self.faces.append(triangle)
        
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
            for vertex_index in face['vertices']:
                # Con esto va a buscar las coordenadas del vértice
                vertex = self.vertices[vertex_index]
                # Con esto agrega las coordenadas a la lista final
                vertex_list.extend(vertex)
        #De vuelve la lista completa  
        return vertex_list
    
    # Función para obtener las normales en el mismo orden que los vértices
    def getNormals(self):
        normal_list = []
        for face in self.faces:
            if face['normals']:  # Si la cara tiene normales
                for normal_index in face['normals']:
                    normal = self.normals[normal_index]
                    normal_list.extend(normal)
            else:
                # Si no hay normales, agregar normales por defecto (0,0,1)
                for _ in range(3):  # 3 vértices por triángulo
                    normal_list.extend([0.0, 0.0, 1.0])
        return normal_list
    
    # Función para obtener coordenadas de textura
    def getTexCoords(self):
        texcoord_list = []
        for face in self.faces:
            if face['texcoords']:  # Si la cara tiene coordenadas de textura
                for texcoord_index in face['texcoords']:
                    texcoord = self.texCoords[texcoord_index]
                    texcoord_list.extend(texcoord)
            else:
                # Si no hay coordenadas de textura, agregar coordenadas por defecto
                for _ in range(3):  # 3 vértices por triángulo
                    texcoord_list.extend([0.0, 0.0])
        return texcoord_list
    
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
        print(f"  Normales: {len(self.normals)}")
        print(f"  Coordenadas de textura: {len(self.texCoords)}")
        print(f"  Triángulos: {len(self.faces)}")
        if bounds:
            print(f"  Tamaño: {bounds['size']}")
            print(f"  Centro: {bounds['center']}")