# Lab 2: Rasterizador de Archivos .OBJ

## Descripción
Esta tarea implementa un rasterizador 3D que puede cargar archivos .OBJ y renderizarlos con diferentes modos de visualización (puntos, líneas, triángulos rellenos). Incluye transformaciones en tiempo real y exportación automática a formato BMP.

## Archivos del Proyecto

### **Rasterizacion.py** - EL RASTERIZADOR PRINCIPAL
- Cerebro del sistema
- Maneja la ventana, controles de teclado y loop principal
- Coordina todos los demás archivos para funcionar juntos

### **gl.py** - Motor Gráfico  
- Contiene las funciones de rasterización (dibujar puntos, líneas, triángulos)
- Implementa algoritmo de Bresenham para líneas
- Maneja colores aleatorios por triángulo

### **Obj_Loader.py** - Cargador de Modelos
- Lee archivos .OBJ y extrae vértices y caras
- Convierte el formato OBJ al formato que entiende el rasterizador
- Calcula dimensiones para centrar el modelo automáticamente

### **model.py** - Manejo de Modelos 3D
- Almacena vértices del modelo y sus transformaciones
- Conecta con las matrices matemáticas para aplicar cambios

### **MathLib.py** - Matemáticas 3D
- Crea matrices de transformación (mover, rotar, escalar)
- Funciones matemáticas necesarias para el 3D

### **shaders.py** - Transformaciones
- Aplica las transformaciones a cada vértice del modelo
- Convierte coordenadas 3D según las matrices

### **BMP_Writer.py** - Exportador de Imágenes
- Convierte el resultado final en un archivo .bmp
- Se ejecuta automáticamente al cerrar el programa

### **obj file.obj** - Modelo 3D
- Archivo del modelo 3D que se va a renderizar
- Contiene 9,097 vértices y 13,995 triángulos

## Dependencias a instalar
- pip install pygame 
- pip install numpy

## Clonar y Ejecutar
- git clone https://github.com/jaq23369/Modulo1-Rasterizacion.git
- cd Modulo1-Rasterizacion
- git checkout Lab2-obj-loader
- cd Lab2_Obj_Models
- python Rasterizacion.py

## Hecho por
Joel Antonio Jaquez López #23369





