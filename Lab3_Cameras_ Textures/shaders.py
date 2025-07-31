import numpy as np

def vertexShader(vertex, **kwargs):

    # Recibir todas las matrices
    modelMatrix = kwargs.get("modelMatrix")
    viewMatrix = kwargs.get("viewMatrix") 
    projectionMatrix = kwargs.get("projectionMatrix")
    viewportMatrix = kwargs.get("viewportMatrix")
    
    # Agregar componente W al vértice
    vt = np.array([vertex[0], vertex[1], vertex[2], 1.0])
    
    # Pipeline de transformaciones
    if modelMatrix is not None:
        vt = modelMatrix @ vt
        vt = vt.A1  # Convertir matrix a array
    
    if viewMatrix is not None:
        vt = viewMatrix @ vt
        vt = vt.A1
    
    if projectionMatrix is not None:
        vt = projectionMatrix @ vt
        vt = vt.A1
    
    # Perspective divide
    if vt[3] != 0:
        vt[0] /= vt[3]
        vt[1] /= vt[3] 
        vt[2] /= vt[3]
    
    # Viewport transformation
    if viewportMatrix is not None:
        vt_viewport = viewportMatrix @ np.array([vt[0], vt[1], vt[2], 1.0])
        vt_viewport = vt_viewport.A1
        vt[0] = vt_viewport[0]
        vt[1] = vt_viewport[1]
    
    return [vt[0], vt[1], vt[2]]

def fragmentShader(**kwargs):
    """Fragment Shader básico"""
    r, g, b = kwargs["pixelColor"]
    return [r, g, b]

def flatShader(**kwargs):
    """Shader con iluminación básica"""
    A, B, C = kwargs["verts"]
    r, g, b = kwargs["pixelColor"]
    dirLight = kwargs["dirLight"]
    
    # Verificar si hay normales
    if len(A) < 6 or len(B) < 6 or len(C) < 6:
        return [r, g, b]
    
    # Extraer normales
    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]
    
    # Normal promedio
    normal = [(nA[0] + nB[0] + nC[0]) / 3,
              (nA[1] + nB[1] + nC[1]) / 3,
              (nA[2] + nB[2] + nC[2]) / 3]
    
    # Iluminación
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

    # Extraer coordenadas de textura
    tA = [A[6], A[7]]
    tB = [B[6], B[7]]
    tC = [C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    # Interpolar coordenadas UV
    UVs = [u * tA[0] + v * tB[0] + w * tC[0],
           u * tA[1] + v * tB[1] + w * tC[1]]
    
    # Aplicar textura si está disponible
    if textureList is not None:
        if len(textureList) > 0:
            texColor = textureList[0].getColor(UVs[0], UVs[1])
            
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    # intensity = normal DOT -dirLight
    intensity = np.dot(normal, -np.array(dirLight))
    intensity = max(0, intensity)
    
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [r, g, b]

def texturedShader(**kwargs):
    """Shader con textura solamente"""
    A, B, C = kwargs["verts"]
    r, g, b = kwargs["pixelColor"]
    texture = kwargs.get("texture", None)
    u, v, w = kwargs.get("barycentricCoords", (0, 0, 0))
    
    # Si no hay textura, usar color normal
    if not texture:
        return [r, g, b]
    
    # Si los vértices tienen coordenadas UV (formato: x,y,z,nx,ny,nz,u,v)
    if len(A) >= 8 and len(B) >= 8 and len(C) >= 8:
        # Coordenadas UV de cada vértice
        uvA = [A[6], A[7]]
        uvB = [B[6], B[7]]
        uvC = [C[6], C[7]]
        
        # Interpolar UV usando coordenadas baricéntricas
        texU = u * uvA[0] + v * uvB[0] + w * uvC[0]
        texV = u * uvA[1] + v * uvB[1] + w * uvC[1]
        
        # Obtener color de la textura
        textureColor = texture.getColor(texU, texV)
        if textureColor:
            return textureColor
    
    return [r, g, b]

def texturedWithLightingShader(**kwargs):
    """Shader con textura E iluminación"""
    A, B, C = kwargs["verts"]
    r, g, b = kwargs["pixelColor"]
    texture = kwargs.get("texture", None)
    dirLight = kwargs.get("dirLight", [0, 0, 1])
    u, v, w = kwargs.get("barycentricCoords", (0, 0, 0))
    
    # Obtener color base (textura o color por defecto)
    color = [r, g, b]
    
    # Aplicar textura si está disponible
    if texture and len(A) >= 8 and len(B) >= 8 and len(C) >= 8:
        uvA = [A[6], A[7]]
        uvB = [B[6], B[7]]
        uvC = [C[6], C[7]]
        
        texU = u * uvA[0] + v * uvB[0] + w * uvC[0]
        texV = u * uvA[1] + v * uvB[1] + w * uvC[1]
        
        textureColor = texture.getColor(texU, texV)
        if textureColor:
            color = textureColor
    
    # Aplicar iluminación si hay normales
    if len(A) >= 6 and len(B) >= 6 and len(C) >= 6:
        nA = [A[3], A[4], A[5]]
        nB = [B[3], B[4], B[5]]
        nC = [C[3], C[4], C[5]]
        
        # Interpolar normal
        normal = [u * nA[0] + v * nB[0] + w * nC[0],
                  u * nA[1] + v * nB[1] + w * nC[1],
                  u * nA[2] + v * nB[2] + w * nC[2]]
        
        # Normalizar la normal
        import math
        normal_length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if normal_length > 0:
            normal = [normal[0]/normal_length, normal[1]/normal_length, normal[2]/normal_length]
        
        # Calcular iluminación
        intensity = np.dot(normal, -np.array(dirLight))
        intensity = max(0.2, min(1.0, intensity))  # Entre 0.2 y 1.0
        
        # Aplicar iluminación al color
        color = [color[0] * intensity, color[1] * intensity, color[2] * intensity]
    
    return color