# Lab 1: Filling any Polygon

## Descripción
Esta laboratorio consistia en formar los poligonos con los puntos dados y luego investigar un algorito que rellenara estos.

## Resultado
Polígonos formados y rellenados de acuerdo al color decidido.

## Características Implementadas

### Motor Gráfico (`gl.py`)
- Rasterización de píxeles con sistema de coordenadas invertido
- Algoritmo de Bresenham para dibujo de líneas suaves
- Algoritmo de conexión de vértices** para contornos de polígonos
- Algoritmo Scanline Fill para relleno de polígonos
- Sistema de colores normalizado (0-1) con conversión automática
- Framebuffer personalizado para manipulación directa de píxeles

### Funciones Principales
- `glPoint(x, y, color)` - Dibujo de píxeles individuales
- `glLine(p0, p1, color)` - Dibujo de líneas con Bresenham
- `glPolygon(puntos, color)` - Dibujo de contornos conectando vértices
- `glFillPolygon(puntos, color)` - Relleno completo usando Scanline Fill

### Algoritmo de Contorno (`glPolygon`)
1. Recorrer vértices secuencialmente del polígono
2. Conectar puntos actual con siguiente usando `glLine`
3. Cierre automático con operador módulo `(i + 1) % len(puntos)`
4. Resultado contorno cerrado perfecto sin código adicional

### Algoritmo Scanline Fill
1. Normalización de aristas (orden de abajo hacia arriba)
2. Cálculo de intersecciones usando interpolación lineal
3. Ordenamiento de intersecciones por coordenada X
4. Relleno por pares (entrada-salida del polígono)

## Polígonos de Prueba
- Estrella (10 vértices) - En color amarillo
- Cuadrilátero - En color rojo
- Triángulo - En color verde
- Forma compleja - En color azul
- Triángulo pequeño - En color blanco

## Archivos del Proyecto

### `lab1_polygon_filling.py`
Programa principal que:
- Configura la ventana de Pygame (960x540)
- Define 5 polígonos de prueba con diferentes complejidades
- Renderiza contornos y rellenos con colores únicos
- Exporta resultado como archivo BMP

### `gl.py`
Motor gráfico custom que implementa:
- Clase `Renderer` 
- Algoritmos fundamentales de rasterización
- Manejo de framebuffer y sistema de coordenadas

### `BMP_Writer.py`
Utilidad para exportación:
- Generación de archivos BMP sin dependencias externas
- Manejo correcto de headers y estructura de archivos
- Conversión de framebuffer a formato de imagen estándar

## Instalaciones necesarias
pip install pygame

## Ejecucion
python lab1_polygon_filling.py

## Hecho por:
Joel Antonio Jaquez Lopez #23369

