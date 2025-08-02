import numpy as np

def vertexShader(vertex, **kwargs):
    # Se lleva a cabo por vertice

	# Recibimos las matrices
    modelMatrix = kwargs["modelMatrix"]

	# Agregamos un componente W al vertice
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

	# Transformamos el vertices por todas las matrices en el orden correcto
    vt = modelMatrix @ vt

    vt = vt.tolist()[0]

	# Dividimos x,y,z por w para regresar el vertices a un tama�o de 3
    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]

    return vt

#Corre por cada pixel renderizado
def fragmentShader(**kwargs):
    r, g, b = kwargs["pixelColor"]
    return [r, g, b]

def flatShader(**kwargs):
    A, B, C = kwargs["verts"]
    r, g, b = kwargs["pixelColor"]
    dirLight = kwargs["dirLight"]

    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]

    normal = [(nA[0] + nB[0] + nC[0]) / 3,
              (nA[1] + nB[1] + nC[1]) / 3,
              (nA[2] + nB[2] + nC[2]) / 3]
    
    # La formula de la intensidad es:
    # intensity = normal DOT -dirLight
    intensity = np.dot(normal, -np.array(dirLight))
    intensity = max(0, intensity)

    r *= intensity
    g *= intensity
    b *= intensity

    return [r, g, b]

def gouradShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    r, g, b = kwargs["pixelColor"]
    dirLight = kwargs["dirLight"]
    textureList = kwargs["textureList"]

    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]

    tA = [A[6], A[7]]
    tB = [B[6], B[7]]
    tC = [C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2] ]
    
    UVs = [u * tA[0] + v * tB[0] + w * tC[0],
           u * tA[1] + v * tB[1] + w * tC[1]]
    
    if textureList is not None:
        if len(textureList) > 0:
            texColor = textureList[0].getColor(UVs[0], UVs[1])

            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]


    # La formula de la intensidad es:
    # intensity = normal DOT -dirLight
    intensity = np.dot(normal, -np.array(dirLight))
    intensity = max(0, intensity)

    r *= intensity
    g *= intensity
    b *= intensity

    return [r, g, b]

def unlitShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    r, g, b = kwargs["pixelColor"]
    textureList = kwargs["textureList"]

    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]

    tA = [A[6], A[7]]
    tB = [B[6], B[7]]
    tC = [C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2] ]
    
    UVs = [u * tA[0] + v * tB[0] + w * tC[0],
           u * tA[1] + v * tB[1] + w * tC[1]]
    
    if textureList is not None:
        if len(textureList) > 0:
            texColor = textureList[0].getColor(UVs[0], UVs[1])

            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    return [r, g, b]


def normalMapShader(**kwargs):
    #Shader que muestra las normales como colores RGB
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    dirLight = kwargs["dirLight"]
    
    # Obtener normales de los vértices
    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]
    
    # Interpolar la normal usando coordenadas baricéntricas
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    # Convertir normales de [-1,1] a [0,1] para visualización
    r = (normal[0] + 1) * 0.5
    g = (normal[1] + 1) * 0.5
    b = (normal[2] + 1) * 0.5
    
    return [r, g, b]


def checkerboardShader(**kwargs):
    #Shader que crea un patrón de tablero de ajedrez
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Interpolar coordenadas X e Y
    x = u * A[0] + v * B[0] + w * C[0]
    y = u * A[1] + v * B[1] + w * C[1]
    
    # Crear patrón de tablero
    frequency = 8.0
    x_check = int((x + 1) * frequency) % 2
    y_check = int((y + 1) * frequency) % 2
    
    # XOR para crear patrón alternante
    if (x_check + y_check) % 2 == 0:
        return [0.9, 0.9, 0.9]  # Gris claro
    else:
        return [0.1, 0.1, 0.1]  # Gris oscuro
