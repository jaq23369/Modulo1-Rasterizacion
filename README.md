# Proyecto 1 - Gráficas por Computadora

## Descripción del Proyecto

Este proyecto implementa todo lo visto en clase durante el módulo 1 de Rasterización.
En sí el proyecto como tal buscaba crear una escena con 4 módelos obj, los cuales debían tener textura,
shaders y una distribución estética en la escena, además de que la escena fuera creativa.

## Características Principales

- **Renderizado 3D Completo**: Sistema de rasterización desde cero
- **4 Modelos 3D Texturizados**: Escena prehistórica con dinosaurios
- **4 Shaders Procedurales Únicos**: Efectos visuales avanzados 
- **Control simple de cámaras**: Controles manuales
- **Pipeline de Texturas**: Soporte completo para texturas BMP con coordenadas UV
- **Background Rendering**: Fondos texturizados para contexto visual

## Modelos Incluidos

1. **T-Rex** - Con shader `hologramShader` (efecto de holograma)
2. **Quetzalcoatlus** - Con shader `ghostShader` (efecto transparente)
3. **Mosasaurus** - Con shader `bacteriaWaveShader` (patrones verdes parecidos a bacterias con verdes cambiantes)
4. **Gallimimus** - Con shader `crystalDinoShader` (efecto cristalino con dispersión)

## Shaders Implementados

### 1. Crystal Dino Shader
- Efecto Fresnel para bordes brillantes según ángulo de vista
- Dispersión cromática simula separación de luz como en prisma
- Estructura cristalina con 3 capas de facetas procedurales
- Arcoíris interno con separación perfecta de 120° entre colores
- Sparkles aleatorios (inclusiones brillantes) con umbral del 5%
- Reflexión especular de alta intensidad (exponente 32)

### 2. Bacteria Wave Shader
- Ondas multicapa con 3 frecuencias diferentes combinadas
- Mapeo espectral completo a 6 rangos de colores del arcoíris
- Patrón orgánico simula crecimiento bacteriano procedural
- Transiciones suaves entre rojo → naranja → amarillo → verde → cyan → azul → violeta
- Algoritmo único de modulación por posición espacial

### 3. Hologram Shader
- Ondas triangulares para interferencia holográfica
- Efecto Fresnel cuadrático en bordes
- Líneas de escaneo con frecuencia alta para realismo
- Colores holográficos dominados por azul/cyan
- Interferencia procedural entre múltiples ondas

### 4. Ghost Shader
- Ondulación fantasmal continua en 3D
- Transparencia variable basada en coordenadas espaciales
- Niebla interna con múltiples frecuencias trigonométricas
- Rim lighting para efecto de borde etéreo
- Partículas espectrales con umbral del 10%
- Iluminación suave con alta componente ambiental

## Controles

### Modelos
- **Flechas**: Mover modelo activo
- **A/D**: Rotar en eje Z
- **W/S**: Escalar modelo
- **Q/E**: Rotar en eje Y
- **R/F**: Rotar en eje X
- **ESPACIO**: Activar/desactivar auto-rotación
### Cámara
- **IJKL**: Movimiento de cámara (Pan)
### Sistema
- **ESC**: Salir del programa

## Tecnologías Utilizadas

- **Python**
- **Pygame** - Para ventana y eventos
- **NumPy** - Para operaciones matemáticas optimizadas
- **Rasterización por Software** - Sin OpenGL/DirectX

## Estructura del Proyecto

### **Aplicación Principal**
- **`Rasterizacion.py`**
  - Configuración de ventana Pygame (960x540)
  - Carga de 4 modelos OBJ de dinosaurios
  - Asignación de shaders únicos a cada modelo
  - Sistema de controles de teclado
  - Loop principal de renderizado
  - Exportación automática de BMP final

###  **Motor de Renderizado**
- **`gl.py`**
  - Rasterización 3D por software
  - Pipeline completo: Vertex → Fragment shaders
  - Sistema de coordenadas baricéntricas
  - Z-buffer para profundidad
  - Soporte para texturas y backgrounds
  - Transformaciones de matriz 4x4

### **Sistema de Shaders**
- **`shaders.py`**
  - `vertexShader`: Transformaciones 3D básicas
  - `crystalDinoShader`: Efectos cristalinos con Fresnel
  - `bacteriaWaveShader`: Ondas procedurales multicolor
  - `hologramShader`: Interferencia holográfica
  - `ghostShader`: Efectos espectrales translúcidos
  - Funciones trigonométricas complejas

### **Sistema de Modelos**
- **`model.py`**
  - Clase Model con vértices, normales, UV
  - Matrices de transformación (escala, rotación, traslación)
  - Carga de texturas BMP
  - Asignación de vertex/fragment shaders

### **Cargador de Archivos**
- **`Obj_Loader.py`**
  - Parser de archivos OBJ estándar
  - Extracción de vértices, normales, coordenadas UV
  - Cálculo de bounding boxes
  - Información estadística de modelos

### **Sistema de Texturas**
- **`BMPTexture.py`**
  - Cargador de imágenes BMP
  - Sampling de colores con coordenadas UV
  - Conversión RGB normalizada
  - Manejo de coordenadas fuera de rango

### **Exportador de Imágenes**
- **`BMP_Writer.py`**
  - Generación de archivos BMP desde framebuffer
  - Estructura de headers BMP completa
  - Conversión de formato de pixeles
  - Guardado automático al cerrar

### **Operaciones Matemáticas**
- **`MathLib.py`**
  - Multiplicación de matrices 4x4
  - Operaciones con vectores 3D
  - Normalización y producto punto
  - Transformaciones geométricas

### **Sistema de Cámara**
- **`camera.py`**
  - Matriz de vista (view matrix)
  - Transformaciones de cámara
  - Controles de posición y rotación
  - Proyección perspectiva

### **Recursos del Proyecto**
- **Modelos 3D (.obj):**
  - T-Rex Model.obj (7,753 vértices)
  - Quetzalcoatlus (17,986 vértices)
  - Mosasaurus (93,698 vértices)
  - Gallimimus (51,746 vértices)

- **Texturas (.bmp):**
  - Texturas específicas por dinosaurio (observar detalladamente Rasterizacion.py)
  - Fondo paisajístico (paisaje1.bmp)

### **Entorno de Desarrollo**
- **`venv/`**: Entorno virtual con pygame y numpy
- **`__pycache__/`**: Cache compilado de Python
- **`modelo_3d_output.bmp`**: Imagen

## Imágenes del proyecto:
- Con Texturas: (El único que no tenía textura es el Gallimimus que es el del lado derecho, por ello se compensó su textura con un shader de colores similares a los de él): <img width="961" height="542" alt="Image" src="https://github.com/user-attachments/assets/764efa37-63ee-4372-9c9e-f951e9c0ff72" />
- Con Shaders: <img width="960" height="541" alt="Image" src="https://github.com/user-attachments/assets/0c664bc7-0833-49fc-8201-a55d9333eb57" />
- Moviendo la cámara: (No logré hacer una toma porque los modelos son tan pesados que no se mueve y a puras penas logré mover la cámara para demostrar que si hay profundidad,
  de igual forma si existe profundidad porque al implementar la cámara la posiciones cambian, por lo tanto todos los modelos estan en objModel.translation[2] = -5 o parecidos para poder ser apreciados): <img width="959" height="541" alt="Image" src="https://github.com/user-attachments/assets/a4dc8351-b206-48ee-b838-636d896a7543" />


  ## Proyecto hecho por:
  - Joel Antonio Jaquez López #23369


