# Lab 3: Cameras y Textures - Renderizador 3D

## Descripción

Laboratorio que implementa un renderizador 3D completo capaz de cargar archivos .obj y renderizarlos con texturas, utilizando el pipeline completo de gráficas por computadora con las 4 matrices de transformación fundamentales.

## Características Implementadas

### Pipeline de Transformaciones Matriciales
- **Model Matrix**: Transformaciones del objeto (traslación, rotación, escalado)
- **View Matrix**: Posicionamiento y orientación de cámara (Look-at)
- **Projection Matrix**: Proyección perspectiva 3D → 2D
- **Viewport Matrix**: Transformación final a coordenadas de pantalla

### Sistema de Cámara Cinematográfica
- **Medium Shot**: Vista frontal balanceada del modelo
- **Low Angle**: Cámara desde abajo mirando hacia arriba (efecto heroico)
- **High Angle**: Cámara desde arriba mirando hacia abajo
- **Dutch Angle**: Cámara inclinada para efecto dramático

### Renderizado Avanzado
- **Z-Buffer**: Depth testing para oclusión correcta
- **Fragment Shaders**: Múltiples tipos de shading
 - Flat Shader (iluminación básica)
 - Textured Shader (solo textura)
 - Textured + Lighting Shader (textura con iluminación)
- **Coordenadas Baricéntricas**: Interpolación suave de atributos
- **Soporte de Texturas**: Carga y mapeo de texturas BMP

## Instrucciones de Ejecución

### Prerrequisitos
Asegúrate de tener instalado Python o un entorno del mismo y las siguientes librerías:
- numpy
- pygame

### Al clonar el repositorio
- cd ruta/a/Lab3_Cameras_ Textures
- para correr el programa: python Rasterizacion.py

### Controles del programa
- 1: Medium Shot - Vista frontal balanceada
- 2: Low Angle Shot - Cámara desde abajo
- 3: High Angle Shot - Cámara desde arriba
- 4: Dutch Angle Shot - Cámara inclinada
- S: Guardar Screenshot de la toma actual
- G: Generar todas las tomas automáticamente
- T: Cambiar Shader (textura/iluminación/combinado)
- P: Cambiar Primitiva (puntos/líneas/triángulos)
- ESPACIO: Toggle Auto-rotación del modelo
- ESC: Salir del programa

### Imagenes de las tomas

- Medium: ![Image](https://github.com/user-attachments/assets/c4900046-d442-4d3b-96c3-6f312338b25b)
- Low: ![Image](https://github.com/user-attachments/assets/9a16acad-3af5-46fd-952e-3d0dd2b76c64)
- High: ![Image](https://github.com/user-attachments/assets/5a0657cc-67e3-4275-acea-23baa2c0e1c3)
- Dutch: ![Image](https://github.com/user-attachments/assets/dfdb84ae-c6d5-4ac8-a54d-af2ca004ebb4)

### Reflexión
Para cualquiera de los 2 auxiliares, solamente decirles que no logré implementar lo de la textura del obj y que talvez las matrices están algo regadas, pero logré hacer las cámaras y sacar las tomas.
De verdad me esforzé en hacerlo y pase días haciendolo, incluso falte a unas clases por hacer este laboratorio y vi las clases 2 veces pero al final me frustré y pues no logré meter la textura del obj, pero lo arreglaré y
me seguiré esforzando para mejorar y así entregar mejores resultados. Gracias por su comprensión.

### Hecho por:
- Joel Antonio Jaquez López #23369














