import numpy as np

def vertexShader(vertex, normal, **kwargs):
    # Se lleva a cabo por vertice

	# Recibimos las matrices
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

	# Agregamos un componente W al vertice
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    nt = [normal[0],
          normal[1],
          normal[2],
          0]

	# Transformamos el vertices por todas las matrices en el orden correcto
    vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt
    vt = vt.tolist()[0]

    nt = modelMatrix @ nt
    nt = nt.tolist()[0]

	# Dividimos x,y,z por w para regresar el vertices a un tama�o de 3
    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]
    
    nt = [nt[0],
          nt[1],
          nt[2]]
    
    nt = nt / np.linalg.norm(nt)

    return vt[0], vt[1], vt[2], nt[0], nt[1], nt[2]

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

def crystalDinoShader(**kwargs):
    #Shader de color cristalizado verdoso 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    dirLight = kwargs.get("dirLight", [0, -1, -1])
    
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
    
    # Normalizar la normal
    norm_length = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    if norm_length > 0:
        normal = [n/norm_length for n in normal]
    
    # Vector de vista simulado
    view_dir = [0, 0, 1]
    
    # Efecto Fresnel para bordes brillantes
    dot_nv = abs(normal[0]*view_dir[0] + normal[1]*view_dir[1] + normal[2]*view_dir[2])
    fresnel = 1.0 - dot_nv
    fresnel = fresnel ** 2  # Intensificar el efecto
    
    # Reflexión especular
    light_dir = [-dirLight[0], -dirLight[1], -dirLight[2]]
    dot_nl = max(0, normal[0]*light_dir[0] + normal[1]*light_dir[1] + normal[2]*light_dir[2])
    
    # Dispersión cromática basada en ángulo
    dispersion_r = np.sin(x * 15 + y * 10) * 0.3
    dispersion_g = np.sin(x * 15 + y * 10 + 1.5) * 0.3
    dispersion_b = np.sin(x * 15 + y * 10 + 3.0) * 0.3
    
    # Estructura cristalina interna (facetas)
    facet1 = abs(np.sin(x * 20) * np.cos(z * 20))
    facet2 = abs(np.sin(y * 25) * np.cos(x * 25))
    facet3 = abs(np.sin(z * 18) * np.cos(y * 18))
    crystal_structure = (facet1 + facet2 + facet3) / 3.0
    
    # Arcoíris interno
    rainbow_r = abs(np.sin((x + y) * 10))
    rainbow_g = abs(np.sin((x + y) * 10 + 2.094))  # 120 grados
    rainbow_b = abs(np.sin((x + y) * 10 + 4.188))  # 240 grados
    
    # Color base del cristal (verde esmeralda con variaciones)
    base_r = 0.1
    base_g = 0.4
    base_b = 0.3
    
    # Combinar todos los efectos
    r = base_r * (1 - fresnel) + fresnel * 0.9
    g = base_g * (1 - fresnel) + fresnel * 0.95
    b = base_b * (1 - fresnel) + fresnel * 1.0
    
    # Agregar dispersión cromática
    r += dispersion_r * fresnel * 0.5 + rainbow_r * crystal_structure * 0.3
    g += dispersion_g * fresnel * 0.5 + rainbow_g * crystal_structure * 0.3
    b += dispersion_b * fresnel * 0.5 + rainbow_b * crystal_structure * 0.3
    
    # Especular fuerte para aspecto de gema
    specular = dot_nl ** 32  # Exponente alto para brillo concentrado
    r += specular * 0.8
    g += specular * 0.9
    b += specular * 1.0
    
    # Brillos internos aleatorios (inclusiones)
    sparkle = abs(np.sin(x * 100) * np.cos(y * 100) * np.sin(z * 100))
    if sparkle > 0.95:
        sparkle_intensity = (sparkle - 0.95) * 20
        r += sparkle_intensity
        g += sparkle_intensity
        b += sparkle_intensity
    
    # Modulación por iluminación
    ambient = 0.3
    diffuse = dot_nl * 0.7
    lighting = ambient + diffuse
    
    r *= lighting
    g *= lighting
    b *= lighting
    
    return [min(r, 1.0), min(g, 1.0), min(b, 1.0)]

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

def ghostShader(**kwargs):
    # Shader fantasmal 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    dirLight = kwargs.get("dirLight", [0, -1, -1])
    
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
    
    # Ondulación fantasmal
    wave = np.sin(y * 10 + x * 5 + z * 5)
    
    # Transparencia variable
    transparency = abs(np.sin(x * 8 + y * 8 + z * 8))
    
    # Niebla interna
    fog = abs(np.sin(x * 15) * np.cos(y * 15) * np.sin(z * 15))
    
    # Color base espectral (azul-blanco pálido)
    r = 0.7 + transparency * 0.2
    g = 0.8 + transparency * 0.15
    b = 0.95
    
    # Efecto de borde brillante (rim lighting)
    edge_brightness = 1.0 - abs(normal[2])
    r += edge_brightness * 0.3
    g += edge_brightness * 0.3
    b += edge_brightness * 0.4
    
    # Ondulaciones de energía
    if wave > 0.8:
        energy = (wave - 0.8) * 5
        r += energy * 0.2
        g += energy * 0.3
        b += energy * 0.5
    
    # Partículas espectrales
    if fog > 0.9:
        particle = (fog - 0.9) * 10
        r += particle * 0.4
        g += particle * 0.4
        b += particle * 0.5
    
    # Iluminación suave
    light_dir = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = np.dot(normal, light_dir)
    intensity = 0.5 + intensity * 0.3  # Más luz ambiental para efecto etéreo
    
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [min(r, 1.0), min(g, 1.0), min(b, 1.0)]
