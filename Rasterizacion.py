import pygame
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import vertexShader, gouradShader, crystalDinoShader, bacteriaWaveShader, hologramShader, ghostShader
from Obj_Loader import OBJLoader

width = 960
height = 540
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()
rend = Renderer(screen)
rend.glLoadBackground("paisaje1.bmp")

# Modelo 1 - Tiranosaurio Rex
obj_filename = "T-Rex Model.obj"  
print(f"Cargando modelo: {obj_filename}")
obj_loader = OBJLoader(obj_filename)
obj_loader.getInfo()

objModel = Model()
objModel.vertices = obj_loader.getVertices()
objModel.normals = obj_loader.getNormals()
objModel.texcoords = obj_loader.getTextureCoords()
objModel.vertexShader = vertexShader
objModel.fragmentShader = hologramShader
objModel.LoadTexture("T-RexTexture.bmp")

bounds = obj_loader.getBounds()

if bounds:
    center = bounds['center']
    objModel.translation = [-center[0], -center[1], -center[2]]
    
    max_size = max(bounds['size'])
    if max_size > 0:
        scale_factor = 3.0 / max_size
        objModel.scale = [scale_factor, scale_factor, scale_factor]
    
    # Valores modificados
    objModel.translation[0] = -2.4
    objModel.translation[1] = -2.1
    objModel.translation[2] = -5
    objModel.rotation[1] = -165

rend.models.append(objModel)
print(f"T-Rex cargado exitosamente con {len(objModel.vertices)//3} vértices")

# Modelo 2 - Quetzalcoatlus
obj_filename2 = "13623_Quetzalcoatlus_v1_L2.obj"  
print(f"Cargando segundo modelo: {obj_filename2}")
obj_loader2 = OBJLoader(obj_filename2)
obj_loader2.getInfo()

objModel2 = Model()
objModel2.vertices = obj_loader2.getVertices()
objModel2.normals = obj_loader2.getNormals()
objModel2.texcoords = obj_loader2.getTextureCoords()
objModel2.vertexShader = vertexShader
objModel2.fragmentShader = ghostShader
objModel2.LoadTexture("QuetzacoatlusTexture.bmp")

bounds2 = obj_loader2.getBounds()
if bounds2:
    center2 = bounds2['center']
    objModel2.translation = [-center2[0], -center2[1], -center2[2]]
    
    max_size2 = max(bounds2['size'])
    if max_size2 > 0:
        scale_factor2 = 3.0 / max_size2
        objModel2.scale = [scale_factor2, scale_factor2, scale_factor2]
    
    # Valores modificados
    objModel2.translation[0] = 0      
    objModel2.translation[1] = 1.5      
    objModel2.translation[2] = -5     
    objModel2.rotation[0] = -90        
    objModel2.rotation[1] = 30     

rend.models.append(objModel2)
print(f"Segundo dinosaurio cargado exitosamente con {len(objModel2.vertices)//3} vértices")

# Modelo 3 - Mosasaurus
obj_filename3 = "13621_Mosasaurus_v1_L2.obj"  
print(f"Cargando tercer modelo: {obj_filename3}")
obj_loader3 = OBJLoader(obj_filename3)
obj_loader3.getInfo()

objModel3 = Model()
objModel3.vertices = obj_loader3.getVertices()
objModel3.normals = obj_loader3.getNormals()
objModel3.texcoords = obj_loader3.getTextureCoords()
objModel3.vertexShader = vertexShader
objModel3.fragmentShader = bacteriaWaveShader
objModel3.LoadTexture("MosasaurioTexture.bmp")

bounds3 = obj_loader3.getBounds()
if bounds3:
    center3 = bounds3['center']
    objModel3.translation = [-center3[0], -center3[1], -center3[2]]
    
    max_size3 = max(bounds3['size'])
    if max_size3 > 0:
        scale_factor3 = 6.0 / max_size3
        objModel3.scale = [scale_factor3, scale_factor3, scale_factor3]
    
    # Valores modificados
    objModel3.translation[0] = 1.7      
    objModel3.translation[1] = -2.3       
    objModel3.translation[2] = -9.5     
    objModel3.rotation[0] = -90         
    objModel3.rotation[1] = 0         
    objModel3.rotation[2] = -40

rend.models.append(objModel3)
print(f"Tercer dinosaurio cargado exitosamente con {len(objModel3.vertices)//3} vértices")


# Modelo 4 - Gallimimus
obj_filename4 = "21539_Gallimimus_v2.obj"  
print(f"Cargando cuarto modelo: {obj_filename4}")
obj_loader4 = OBJLoader(obj_filename4)
obj_loader4.getInfo()

objModel4 = Model()
objModel4.vertices = obj_loader4.getVertices()
objModel4.normals = obj_loader4.getNormals()
objModel4.texcoords = obj_loader4.getTextureCoords()
objModel4.vertexShader = vertexShader
objModel4.fragmentShader = crystalDinoShader

bounds4 = obj_loader4.getBounds()
if bounds4:
    center4 = bounds4['center']
    objModel4.translation = [-center4[0], -center4[1], -center4[2]]
    
    max_size4 = max(bounds4['size'])
    if max_size4 > 0:
        scale_factor4 = 2.0 / max_size4
        objModel4.scale = [scale_factor4, scale_factor4, scale_factor4]
    
    # Valores modificados
    objModel4.translation[0] = 4.0      
    objModel4.translation[1] = -2.0      
    objModel4.translation[2] = -5     
    objModel4.rotation[0] = 0        
    objModel4.rotation[1] = 45          

rend.models.append(objModel4)
print(f"Cuarto dinosaurio cargado exitosamente con {len(objModel4.vertices)//3} vértices")

# Usar el primer modelo para controles
currentModel = objModel

print("\n=== CONTROLES ===")
print("Flechas: Mover modelo")
print("A/D: Rotar en Z")
print("W/S: Escalar")
print("Q/E: Rotar en Y")
print("R/F: Rotar en X")
print("ESPACIO: Toggle auto-rotación")

print("ESC: Salir")
print("================\n")

# Variables de control
auto_rotate = False
rotation_speed = 30

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
            
    
    # Controles de teclado
    keys = pygame.key.get_pressed()
    
    # Movimiento de cámara con IJKL
    camera_speed = 0.1
    if keys[pygame.K_i]:
        rend.camera.translation[1] += camera_speed * deltaTime
    if keys[pygame.K_k]:
        rend.camera.translation[1] -= camera_speed * deltaTime
    if keys[pygame.K_j]:
        rend.camera.translation[0] -= camera_speed * deltaTime
    if keys[pygame.K_l]:
        rend.camera.translation[0] += camera_speed * deltaTime

    # Movimiento del modelo
    model_speed = 2.0
    if keys[pygame.K_RIGHT]:
        currentModel.translation[0] += model_speed * deltaTime
    if keys[pygame.K_LEFT]:
        currentModel.translation[0] -= model_speed * deltaTime
    if keys[pygame.K_UP]:
        currentModel.translation[1] += model_speed * deltaTime
    if keys[pygame.K_DOWN]:
        currentModel.translation[1] -= model_speed * deltaTime
    
    # Rotación manual 
    if keys[pygame.K_d]:
        currentModel.rotation[2] += rotation_speed * deltaTime
    if keys[pygame.K_a]:
        currentModel.rotation[2] -= rotation_speed * deltaTime
    if keys[pygame.K_e]:
        currentModel.rotation[1] += rotation_speed * deltaTime
    if keys[pygame.K_q]:
        currentModel.rotation[1] -= rotation_speed * deltaTime
    if keys[pygame.K_r]:
        currentModel.rotation[0] += rotation_speed * deltaTime
    if keys[pygame.K_f]:
        currentModel.rotation[0] -= rotation_speed * deltaTime
    
    # Auto-rotación
    if auto_rotate:
        currentModel.rotation[1] += 20 * deltaTime

    rend.glClearBackground()
    rend.glRender()
    pygame.display.flip()

# Generar BMP final
print("Generando archivo BMP...")
GenerateBMP("modelo_3d_output.bmp", width, height, 3, rend.frameBuffer)
print("Archivo 'modelo_3d_output.bmp' generado exitosamente!")

pygame.quit()

