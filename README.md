# Lab 4: Implementación de Shaders

## Descripción del Laboratorio

Este laboratorio se enfoca en la implementación y comprensión de shaders en un motor de rasterización 3D. Los shaders son programas que se ejecutan en el pipeline de renderizado para controlar cómo se procesan los vértices y cómo se colorean los píxeles finales.

### Objetivos
- Implementar diferentes tipos de fragment shaders o vertex shaders
- Crear efectos visuales usando matemáticas y técnicas de shading
- Experimentar con coordenadas baricéntricas e interpolación

## Modelo Utilizado
**Among Us Character (.obj)** - Modelo 3D del popular personaje del videojuego Among Us

## Shaders Implementados

### 1. **normalMapShader**
**Descripción**: Visualiza las normales de superficie como colores RGB.

**Técnica**:
- Interpola normales usando coordenadas baricéntricas
- Convierte normales de [-1,1] a [0,1] para visualización
- Mapea X→Rojo, Y→Verde, Z→Azul

**Efecto Visual**: Las superficies se colorean según su orientación.

---

### 2. **hologramShader**

**Descripción**: Simula un efecto de holograma como los de Star Wars.

**Técnica**:
- Genera ondas triangulares usando operación módulo
- Implementa efecto Fresnel para bordes brillantes
- Crea líneas de escaneo horizontales
- Combina interferencia de ondas para patrones complejos

**Efecto Visual**: Aspecto holográfico con colores azul-cyan y líneas de escaneo dinámicas.

---

### 3. **zebraShader**

**Descripción**: Crea un patrón de rayas de zebra dinámicas y curvas.

**Técnica**:
- Combina múltiples ondas en diferentes direcciones
- Varía el ancho de las rayas usando funciones trigonométricas
- Alterna entre negro profundo y blanco cremoso

**Efecto Visual**: Patrón de rayas orgánico y dinámico que sigue la geometría del modelo.

---

### 4. **bacteriaWaveShader**

**Descripción**: Simula ondas de bacterias con colores vibrantes del espectro.

**Técnica**:
- Genera múltiples ondas de frecuencias diferentes
- Mapea la intensidad combinada a colores del espectro
- Transiciona suavemente entre: Rojo → Naranja → Amarillo → Verde → Cyan → Azul → Violeta

**Efecto Visual**: Patrones ondulatorios multicolor que simulan cultivos bacterianos vistos bajo microscopio.


# Imágenes de los shaders aplicados
- Normal Map Shader: <img width="280" height="352" alt="Image" src="https://github.com/user-attachments/assets/8af23ee7-6ee5-4708-a3d6-9a5f20e84a94" />

- Hologram Shader: <img width="293" height="351" alt="Image" src="https://github.com/user-attachments/assets/f3912195-30a4-4c57-8c46-0c83e4e04587" />

- Zebra Shader: <img width="277" height="390" alt="Image" src="https://github.com/user-attachments/assets/b2efd7e5-a47c-43f7-8ee3-4e304d0c1174" />

- Bacteria Wave Shader: <img width="287" height="373" alt="Image" src="https://github.com/user-attachments/assets/4a5b1b5b-1616-45d4-99d2-b30b9bf86d08" />

## Hecho por
Joel Antonio Jaquez López #23369





