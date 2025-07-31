import pygame
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import *
from Obj_Loader import OBJLoader

width = 256
height = 256
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()
rend = Renderer(screen)

# Variables globales para el modelo
modelCenter = [0, 0, 0]
modelSize = [2, 2, 2]
screenshot_count = 0

obj_filename = "among us.obj" # Cambiar por tu archivo OBJ
texture_filename = "Plastic_4K_Diffuse.bmp"

try:
    # Cargar el modelo OBJ
    print(f"Cargando modelo: {obj_filename}")
    obj_loader = OBJLoader(obj_filename)
    obj_loader.getInfo()
    
    # Crear modelo para el renderer
    objModel = Model(obj_filename)
    objModel.vertexShader = vertexShader
    objModel.gouradShader = gouradShader

    # Cargar modelo con textura
    if objModel.LoadTexture(texture_filename):
        objModel.fragmentShader = texturedWithLightingShader
        print("✅ Con textura")
        
    else:
        objModel.fragmentShader = flatShader
        print("❌ Sin textura")
    
    # Obtener información del modelo para configurar la cámara
    bounds = obj_loader.getBounds()
    if bounds:
        modelCenter = bounds['center']
        modelSize = bounds['size']
        print(f"Centro del modelo: {modelCenter}")
        print(f"Tamaño del modelo: {modelSize}")
        
        # Configurar cámara inicial (medium shot)
        rend.setCameraShot('medium', modelCenter, modelSize)
        
        # Resetear transformaciones del modelo (ahora las maneja la cámara)
        objModel.translation = [0, 0, 0]
        objModel.rotation = [0, 0, 0]
        objModel.scale = [1, 1, 1]
    else:
        # Valores por defecto
        modelCenter = [0, 0, 0]
        modelSize = [2, 2, 2]
        rend.setCameraShot('medium', modelCenter, modelSize)
    
    # Agregar modelo al renderer
    rend.models.append(objModel)
    print(f"Modelo cargado exitosamente")

    rend.glColor(1, 0, 0)  # Blanco para ver texturas
    currentModel = objModel
    
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    print("Creando un triángulo de ejemplo...")
    
    # Usar triángulo como fallback
    triangleModel = Model()
    triangleModel.vertices = [0, 1, 0,   # Top
                             -1, -1, 0,  # Bottom left
                              1, -1, 0]  # Bottom right
    triangleModel.vertexShader = vertexShader
    triangleModel.fragmentShader = fragmentShader
    rend.models.append(triangleModel)
    currentModel = triangleModel
    
    # Configurar cámara para triángulo
    modelCenter = [0, 0, 0]
    modelSize = [2, 2, 2]
    rend.setCameraShot('medium', modelCenter, modelSize)

# Función para generar screenshot
def takeScreenshot(shot_name):
    global screenshot_count
    screenshot_count += 1
    filename = f"shot_{screenshot_count}_{shot_name}.bmp"
    GenerateBMP(filename, width, height, 3, rend.frameBuffer)
    print(f"Screenshot guardado: {filename}")
    return filename

# Función para generar todas las tomas
def generateAllShots():
    shots = ["medium", "low", "high", "dutch"]
    filenames = []
    
    for shot in shots:
        print(f"\nGenerando {shot} shot...")
        rend.setCameraShot(shot, modelCenter, modelSize)
        
        # Renderizar
        rend.glClear()
        rend.glRender()
        pygame.display.flip()
        
        # Pequeña pausa
        pygame.time.wait(500)
        
        # Guardar screenshot
        filename = takeScreenshot(shot)
        filenames.append(filename)
    
    print(f"\n¡Todas las tomas generadas exitosamente!")
    print("Archivos creados:")
    for filename in filenames:
        print(f"  - {filename}")
    
    return filenames

print("\n=== CONTROLES ===")
print("1: Medium Shot")
print("2: Low Angle Shot")
print("3: High Angle Shot")
print("4: Dutch Angle Shot")
print("S: Guardar screenshot")
print("G: Generar todas las tomas")
print("T: Cambiar shader (textura/iluminación)")
print("ESPACIO: Toggle auto-rotación")
print("P: Cambiar primitiva (puntos/líneas/triángulos)")
print("ESC: Salir")
print("================\n")

# Variables de control
auto_rotate = False
rotation_speed = 30
current_shot = "medium"

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
                current_shot = "medium"
                rend.setCameraShot('medium', modelCenter, modelSize)
                print("Configurado: Medium Shot")
            elif event.key == pygame.K_2:
                current_shot = "low"
                rend.setCameraShot('low', modelCenter, modelSize)
                print("Configurado: Low Angle Shot")
            elif event.key == pygame.K_3:
                current_shot = "high"
                rend.setCameraShot('high', modelCenter, modelSize)
                print("Configurado: High Angle Shot")
            elif event.key == pygame.K_4:
                current_shot = "dutch"
                rend.setCameraShot('dutch', modelCenter, modelSize)
                print("Configurado: Dutch Angle Shot")
            elif event.key == pygame.K_s:
                takeScreenshot(current_shot)
            elif event.key == pygame.K_g:
                generateAllShots()
            elif event.key == pygame.K_t:
                # Cambiar shader
                if hasattr(currentModel, 'texture') and currentModel.texture:
                    if currentModel.fragmentShader == texturedWithLightingShader:
                        currentModel.fragmentShader = texturedShader
                        print("🎨 Solo textura")
                    elif currentModel.fragmentShader == texturedShader:
                        currentModel.fragmentShader = flatShader
                        print("🎨 Solo iluminación")
                    else:
                        currentModel.fragmentShader = texturedWithLightingShader
                        print("🎨 Textura + iluminación")
            elif event.key == pygame.K_p:
                if rend.primitiveType == TRIANGLES:
                    rend.primitiveType = POINTS
                    print("Modo: PUNTOS")
                elif rend.primitiveType == POINTS:
                    rend.primitiveType = LINES
                    print("Modo: LÍNEAS")
                else:
                    rend.primitiveType = TRIANGLES
                    print("Modo: TRIÁNGULOS")
    
    # Auto-rotación del modelo (opcional)
    if auto_rotate:
        currentModel.rotation[1] += 20 * deltaTime
    
    # Renderizar
    rend.glClear()
    rend.glRender()
    pygame.display.flip()

# Generar archivo BMP final
print("\nGenerando archivo BMP final...")
GenerateBMP("modelo_3d_output.bmp", width, height, 3, rend.frameBuffer)
print("Archivo 'modelo_3d_output.bmp' generado exitosamente!")

print("\n=== INSTRUCCIONES PARA LAS 4 TOMAS ===")
print("1. Presiona '1' para Medium Shot, luego 'S' para guardar")
print("2. Presiona '2' para Low Angle Shot, luego 'S' para guardar")
print("3. Presiona '3' para High Angle Shot, luego 'S' para guardar")
print("4. Presiona '4' para Dutch Angle Shot, luego 'S' para guardar")
print("O presiona 'G' para generar todas automáticamente")
print("=====================================")

pygame.quit()