import numpy as np
from math import pi, sin, cos, tan, isclose

def TranslationMatrix(x, y, z):
    return np.matrix([[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1]])

def ScaleMatrix(x, y, z):
    return np.matrix([[x, 0, 0, 0],
                      [0, y, 0, 0],
                      [0, 0, z, 0],
                      [0, 0, 0, 1]])

def RotationMatrix(pitch, yaw, roll):
    # Convertir a radianes
    pitch *= pi/180
    yaw *= pi/180
    roll *= pi/180
    
    # Creamos la matriz de rotación para cada eje
    pitchMat = np.matrix([[1,0,0,0],
                          [0,cos(pitch),-sin(pitch),0],
                          [0,sin(pitch),cos(pitch),0],
                          [0,0,0,1]])
    
    yawMat = np.matrix([[cos(yaw),0,sin(yaw),0],
                        [0,1,0,0],
                        [-sin(yaw),0,cos(yaw),0],
                        [0,0,0,1]])
    
    rollMat = np.matrix([[cos(roll),-sin(roll),0,0],
                         [sin(roll),cos(roll),0,0],
                         [0,0,1,0],
                         [0,0,0,1]])
    
    return pitchMat * yawMat * rollMat

def ViewMatrix(camPosition, camTarget, camUp):
    """
    Crea una matriz de vista (cámara) usando look-at
    """
    # Convertir a numpy arrays
    camPos = np.array(camPosition)
    target = np.array(camTarget)
    up = np.array(camUp)
    
    # Calcular vectores de la cámara
    forward = target - camPos
    forward = forward / np.linalg.norm(forward)
    
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)
    
    up = np.cross(right, forward)
    
    # Crear matriz de vista
    viewMatrix = np.matrix([
        [right[0], right[1], right[2], -np.dot(right, camPos)],
        [up[0], up[1], up[2], -np.dot(up, camPos)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, camPos)],
        [0, 0, 0, 1]
    ])
    
    return viewMatrix

def ProjectionMatrix(fov, aspect, near, far):
    """
    Crea una matriz de proyección perspectiva
    """
    fov_rad = fov * pi / 180
    f = 1.0 / tan(fov_rad / 2.0)
    
    projMatrix = np.matrix([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near)/(near - far), (2 * far * near)/(near - far)],
        [0, 0, -1, 0]
    ])
    
    return projMatrix

def ViewportMatrix(x, y, width, height):
    """
    Crea una matriz de viewport
    """
    viewportMatrix = np.matrix([
        [width/2, 0, 0, x + width/2],
        [0, height/2, 0, y + height/2],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    return viewportMatrix

def barycentricCoords(A, B, C, P):
    # Se saca el area de los subtriangulos y del triangulo
    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) -
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))
    
    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) -
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))
    
    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) -
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))
    
    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) -
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))
    
    if areaABC == 0:
        return None
    
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC
    
    if (0<=u<=1 and 0<=v<=1 and 0<=w<=1):
        return (u, v, w)
    else:
        return None

# Clase Camera para las diferentes tomas
class Camera:
    def __init__(self, position=[0, 0, 5], target=[0, 0, 0], up=[0, 1, 0]):
        self.position = position
        self.target = target
        self.up = up
        self.fov = 60
        self.near = 0.1
        self.far = 100.0
    
    def getViewMatrix(self):
        return ViewMatrix(self.position, self.target, self.up)
    
    def getProjectionMatrix(self, aspect):
        return ProjectionMatrix(self.fov, aspect, self.near, self.far)
    
    def setMediumShot(self, modelCenter, modelSize):
        """Medium shot: Vista frontal a distancia media"""
        distance = max(modelSize) * 2.5
        self.position = [modelCenter[0], modelCenter[1], modelCenter[2] + distance]
        self.target = modelCenter
        self.up = [0, 1, 0]
        self.fov = 60
    
    def setLowAngle(self, modelCenter, modelSize):
        """Low angle: Cámara desde abajo mirando hacia arriba"""
        distance = max(modelSize) * 2.0
        self.position = [modelCenter[0], modelCenter[1] - distance * 0.8, modelCenter[2] + distance * 0.6]
        self.target = [modelCenter[0], modelCenter[1] + modelSize[1] * 0.3, modelCenter[2]]
        self.up = [0, 1, 0]
        self.fov = 70
    
    def setHighAngle(self, modelCenter, modelSize):
        """High angle: Cámara desde arriba mirando hacia abajo"""
        distance = max(modelSize) * 2.0
        self.position = [modelCenter[0], modelCenter[1] + distance * 0.8, modelCenter[2] + distance * 0.6]
        self.target = [modelCenter[0], modelCenter[1] - modelSize[1] * 0.3, modelCenter[2]]
        self.up = [0, 1, 0]
        self.fov = 70
    
    def setDutchAngle(self, modelCenter, modelSize):
        """Dutch angle: Cámara inclinada"""
        distance = max(modelSize) * 2.5
        self.position = [modelCenter[0] + distance * 0.3, modelCenter[1] + distance * 0.2, modelCenter[2] + distance * 0.8]
        self.target = modelCenter
        # Vector up inclinado
        self.up = [0.3, 0.9, 0.1]
        self.fov = 65