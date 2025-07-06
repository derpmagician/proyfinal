# Sistema de Inventario y Ventas

Un sistema de gestión de inventario y ventas desarrollado en Python que permite administrar productos, registrar ventas y generar reportes en PDF.

## 🚀 Características

- **Gestión de Inventario**: Agregar, editar, eliminar y buscar productos
- **Sistema de Ventas**: Registro de ventas por categorías múltiples
- **Reportes en PDF**: Generación automática de reportes de ventas
- **Algoritmo de Backtracking**: Encuentra combinaciones de productos según presupuesto
- **Interfaz de Consola**: Menú interactivo fácil de usar

## 📋 Requisitos

- Python 3.7+
- Dependencias listadas en `requirements.txt`

## 🛠️ Instalación

1. Clona o descarga el proyecto:
   ```bash
   git clone <url-del-repositorio>
   cd proyfinal
   ```

2. Instala las dependencias desde requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el programa:
   ```bash
   python PF_GRP3.PY
   ```

## 📁 Estructura del Proyecto

```
proyfinal/
├── PF_GRP3.PY              # Archivo principal del sistema
├── requirements.txt        # Dependencias del proyecto
├── clases/
│   ├── __init__.py         # Inicializador del paquete
│   ├── producto.py         # Clase Producto
│   ├── inventario.py       # Clase Inventario
│   ├── venta.py           # Clase Venta
│   └── pdf_ventas.py      # Clase PDFVentas
└── README.md              # Este archivo
```

## 🎯 Funcionalidades

### 1. Gestión de Productos
- **Agregar**: Crear nuevos productos con ID único autogenerado
- **Listar**: Mostrar todos los productos disponibles
- **Buscar**: Por ID o nombre del producto
- **Editar**: Modificar información de productos existentes
- **Eliminar**: Remover productos del inventario

### 2. Sistema de Ventas
- Registro de ventas por categorías múltiples
- Control automático de stock
- Generación de ID único para cada venta
- Cálculo automático de totales

### 3. Reportes
- Reportes por día, mes o año
- Generación automática de PDF
- Formato profesional con detalles de cada venta

### 4. Algoritmo de Backtracking
- Encuentra combinaciones exactas de productos según presupuesto
- Optimización por categoría
- Máximo 3 combinaciones mostradas

## 🎮 Uso del Sistema

### Menú Principal
```
--- Sistema de Inventario ---
1. Agregar producto
2. Listar productos
3. Buscar producto por ID
4. Buscar producto por nombre
5. Eliminar producto
6. Editar producto
7. Registrar venta
8. Mostrar reporte de ventas
9. Encontrar combinaciones según presupuesto
0. Salir
```

### Ejemplo de Uso - Registrar Venta
1. Selecciona opción 7
2. Elige categoría de productos
3. Selecciona productos y cantidades
4. El sistema calcula el total automáticamente
5. Se genera un ID único para la venta

### Ejemplo de Uso - Backtracking
1. Selecciona opción 9
2. Ingresa tu presupuesto
3. Elige una categoría
4. El sistema encuentra combinaciones exactas que sumen el presupuesto

## 🧩 Algoritmos Implementados

### 1. Backtracking
```python
def backtrack(index, seleccionados, total):
    if total > presupuesto:
        return  # Poda
    if total == presupuesto:
        soluciones.append(list(seleccionados))  # Solución encontrada
        return
    # Exploración recursiva...
```

### 2. Búsqueda Lineal
- Búsqueda por ID: O(n)
- Búsqueda por nombre: O(n)
- Filtrado por categoría: O(n)

### 3. Generación de IDs Únicos
- Productos: 8 dígitos numéricos
- Ventas: 8 caracteres alfanuméricos mayúsculas

## 📊 Productos Pre-registrados

El sistema incluye productos de ejemplo:

| Categoría | Producto | Precio | Stock |
|-----------|----------|--------|-------|
| Electrónica | Laptop Gaming | S/. 2,500.00 | 5 |
| Electrónica | Mouse Inalámbrico | S/. 50.00 | 10 |
| Electrónica | Monitor LED | S/. 300.00 | 3 |
| Ropa | Camiseta Polo | S/. 45.00 | 15 |
| Ropa | Jean Clásico | S/. 70.00 | 8 |
| Calzado | Zapatillas Deportivas | S/. 120.00 | 12 |
| Calzado | Botas Mujer | S/. 180.00 | 6 |

## 📄 Generación de Reportes

Los reportes PDF incluyen:
- Fecha y hora de generación
- ID único de cada venta
- Productos vendidos con cantidades
- Totales por venta
- Formato profesional
