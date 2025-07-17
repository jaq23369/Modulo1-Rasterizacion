import pygame
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import *
from Obj_Loader import OBJLoader

width = 512
height = 512
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()
rend = Renderer(screen)


obj_filename = "obj file.obj"  

try:
    # Cargar el modelo OBJ
    print(f"Cargando modelo: {obj_filename}")
    obj_loader = OBJLoader(obj_filename)
    obj_loader.getInfo()  # Mostrar información del modelo
    
    # Crear modelo para el renderer
    objModel = Model()
    objModel.vertices = obj_loader.getVertices()
    objModel.vertexShader = vertexShader
    
    # Calcular transformaciones para centrar y escalar el modelo
    bounds = obj_loader.getBounds()
    if bounds:
        # Centrar el modelo
        center = bounds['center']
        objModel.translation = [-center[0], -center[1], -center[2]]
        
        # Escalar para que quepa en pantalla (ajustar según necesidad)
        max_size = max(bounds['size'])
        if max_size > 0:
            # Escalar para que el modelo ocupe aproximadamente 60% de la pantalla
            scale_factor = (min(width, height) * 0.6) / max_size
            objModel.scale = [scale_factor, scale_factor, scale_factor]
        
        # Ajustar posición para centrar en pantalla
        objModel.translation[0] += width // 2
        objModel.translation[1] += height // 2
    
    # Agregar modelo al renderer
    rend.models.append(objModel)
    print(f"Modelo cargado exitosamente con {len(objModel.vertices)//3} vértices")
    
    # Usar el modelo OBJ como modelo principal
    currentModel = objModel
    
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    print("Creando un triángulo de ejemplo...")
    
    # Usar el triángulo original como fallback
    triangleModel = Model()
    triangleModel.vertices = [ 110, 70, 0,
                              150, 160, 0,
                              170, 80, 0 ]
    triangleModel.vertexShader = vertexShader
    rend.models.append(triangleModel)
    currentModel = triangleModel

print("\n=== CONTROLES ===")
print("Flechas: Mover modelo")
print("A/D: Rotar en Z")
print("W/S: Escalar")
print("Q/E: Rotar en Y")
print("R/F: Rotar en X")
print("ESPACIO: Toggle auto-rotación")
print("1/2/3: Cambiar tipo de primitiva")
print("ESC: Salir")
print("================\n")

# Variables de control
auto_rotate = False
rotation_speed = 30  # grados por segundo

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE:
                auto_rotate = not auto_rotate
                print(f"Auto-rotación: {'ON' if auto_rotate else 'OFF'}")
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
                print("Modo: PUNTOS")
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
                print("Modo: LÍNEAS")
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES
                print("Modo: TRIÁNGULOS")
    
    # Controles de teclado
    keys = pygame.key.get_pressed()
    
    # Movimiento
    if keys[pygame.K_RIGHT]:
        currentModel.translation[0] += 100 * deltaTime
    if keys[pygame.K_LEFT]:
        currentModel.translation[0] -= 100 * deltaTime
    if keys[pygame.K_UP]:
        currentModel.translation[1] += 100 * deltaTime
    if keys[pygame.K_DOWN]:
        currentModel.translation[1] -= 100 * deltaTime
    
    # Rotación manual 
    if keys[pygame.K_d]:
        currentModel.rotation[2] += rotation_speed * deltaTime
    if keys[pygame.K_a]:
        currentModel.rotation[2] -= rotation_speed * deltaTime
    
    # Rotación adicional en otros ejes
    if keys[pygame.K_e]:
        currentModel.rotation[1] += rotation_speed * deltaTime
    if keys[pygame.K_q]:
        currentModel.rotation[1] -= rotation_speed * deltaTime
    if keys[pygame.K_r]:
        currentModel.rotation[0] += rotation_speed * deltaTime
    if keys[pygame.K_f]:
        currentModel.rotation[0] -= rotation_speed * deltaTime
    
    # Escalado
    if keys[pygame.K_w]:
        currentModel.scale = [max(0.1, i + deltaTime) for i in currentModel.scale]
    if keys[pygame.K_s]:
        currentModel.scale = [max(0.1, i - deltaTime) for i in currentModel.scale]
    
    # Auto-rotación (opcional)
    if auto_rotate:
        currentModel.rotation[1] += 20 * deltaTime  # Rotar en Y
    
    rend.glClear()
    # Escribir lo que se va a dibujar aqui
    rend.glRender()
    #########################################
    
    
    pygame.display.flip()

# Generar BMP final
print("Generando archivo BMP...")
GenerateBMP("modelo_3d_output.bmp", width, height, 3, rend.frameBuffer)
print("Archivo 'modelo_3d_output.bmp' generado exitosamente!")

pygame.quit()

