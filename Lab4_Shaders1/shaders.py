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

def hologramShader(**kwargs):
    #Shader de holograma 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Interpolar coordenadas del mundo
    x = u * A[0] + v * B[0] + w * C[0]
    y = u * A[1] + v * B[1] + w * C[1]
    z = u * A[2] + v * B[2] + w * C[2]
    
    # Obtener normales interpoladas
    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    # Crear ondas con operaciones simples
    wave1 = abs((y * 20) % 2 - 1)  # Onda triangular
    wave2 = abs((z * 15) % 2 - 1)  # Otra onda triangular
    interference = wave1 * wave2
    
    # Efecto fresnel simple (bordes brillantes)
    fresnel = 1.0 - abs(normal[2])  # Usar componente Z de la normal
    fresnel = fresnel * fresnel  # Cuadrático para más intensidad
    
    # Colores holográficos
    r = 0.1 + interference * 0.3 + fresnel * 0.6
    g = 0.7 + interference * 0.2 + fresnel * 0.3
    b = 0.9 + interference * 0.1 + fresnel * 0.8
    
    # Líneas de escaneo
    scanline = 0.8 + 0.2 * (abs((y * 30) % 2 - 1))
    
    return [min(r * scanline, 1.0), min(g * scanline, 1.0), min(b * scanline, 1.0)]

def zebraShader(**kwargs):
    #Shader de rayas de zebra dinámicas
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Interpolar coordenadas
    x = u * A[0] + v * B[0] + w * C[0]
    y = u * A[1] + v * B[1] + w * C[1]
    z = u * A[2] + v * B[2] + w * C[2]
    
    # Crear rayas curvas usando múltiples ondas
    wave1 = (x * 8 + y * 2) % 2.0
    wave2 = (x * 6 + z * 3 + 1.5) % 2.0
    wave3 = (y * 10 + x * 1.5 + 0.7) % 2.0
    
    # Combinar ondas para crear patrones complejos
    combined_wave = (wave1 + wave2 * 0.5 + wave3 * 0.3) / 1.8
    
    # Crear variación en el ancho de las rayas
    stripe_width = 0.4 + abs(((x + z) * 5) % 2.0 - 1.0) * 0.3
    
    # Determinar si estoy en raya negra o blanca
    stripe_pattern = combined_wave % 2.0
    
    if stripe_pattern < stripe_width:
        return [0.05, 0.05, 0.05]  # Negro
    else:
        return [0.95, 0.95, 0.9]   # Blanco cremoso
    

def bacteriaWaveShader(**kwargs):
    #Shader que simula ondas de bacterias con colores verdes
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Interpolar coordenadas
    x = u * A[0] + v * B[0] + w * C[0]
    y = u * A[1] + v * B[1] + w * C[1]
    z = u * A[2] + v * B[2] + w * C[2]
    
    # Crear ondas de bacteria
    wave1 = abs(((x * 5 + y * 3) % 2.0) - 1.0)
    wave2 = abs(((y * 4 + z * 2 + 1.5) % 2.0) - 1.0)
    wave3 = abs(((z * 6 + x * 2 + 0.8) % 2.0) - 1.0)
    
    # Combinar ondas
    combined_wave = (wave1 + wave2 + wave3) / 3.0
    
    # Mapear a posición en el espectro de colores verde
    rainbow_pos = combined_wave
    
    # Colores de bacteria s
    if rainbow_pos < 0.167:  # Rojo
        r, g, b = 1.0, 0.0, 0.0
    elif rainbow_pos < 0.333:  # Naranja-Amarillo
        r, g, b = 1.0, 0.8, 0.0
    elif rainbow_pos < 0.5:  # Amarillo-Verde
        r, g, b = 0.5, 1.0, 0.0
    elif rainbow_pos < 0.667:  # Verde-Cyan
        r, g, b = 0.0, 1.0, 0.5
    elif rainbow_pos < 0.833:  # Cyan-Azul
        r, g, b = 0.0, 0.5, 1.0
    else:  # Azul-Violeta
        r, g, b = 0.5, 0.0, 1.0
    
    return [r, g, b]