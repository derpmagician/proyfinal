import string
import os
import random
import pandas as pd
import jinja2
import uuid
from fpdf import FPDF
from datetime import datetime


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

class Producto:
    def __init__(self, id=None, nombre="", categoria="", precio=0.0, stock=0):
        self.id = id if id else str(uuid.uuid4())[:8]  # ID aleatorio de 8 caracteres
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
    
    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.categoria}) - S/. {self.precio:.2f} - Stock: {self.stock}"

class Inventario:
    def __init__(self):
        self.productos = []
        
    def agregar_producto(self, producto):
        if not producto.id or not producto.id.strip():
            print("Error: El producto debe tener un ID válido.")
            return False
        
        if not producto.nombre or not producto.nombre.strip():
            print("Error: El producto debe tener un nombre válido.")
            return False
            
        if not producto.categoria or not producto.categoria.strip():
            print("Error: El producto debe tener una categoría válida.")
            return False
            
        if producto.precio < 0:
            print("Error: El precio no puede ser negativo.")
            return False
            
        if producto.stock < 0:
            print("Error: El stock no puede ser negativo.")
            return False
            
        if any(p.id == producto.id for p in self.productos):
            print("Error: ID duplicado. No se puede agregar el producto.")
            return False
            
        self.productos.append(producto)
        print("Producto agregado con éxito.")
        return True
    
    def listar_productos(self):
        if not self.productos:  
            print("No hay productos en inventario.")
            return
    
    # Crear DataFrame con los productos 
        df = pd.DataFrame({
            'ID': [p.id for p in self   .productos],
            'Categoria': [p.categoria for p in self.productos],
            'Producto': [p.nombre for p in self.productos],
            'Precio': [p.precio for p in self.productos],
            'Stock': [p.stock for p in self.productos]
        })
    
    # Crear archivo Excel
        ListaProductos = f"lista_productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        df.style.format({
        'Precio': 'S/. {0:,.2f}',
        'Stock': '{0:,.0f}'
        }).to_excel(ListaProductos, index=False)

        print(f"Archivo generado exitosamente: {ListaProductos}")
    
    def buscar_por_id(self, id):
        for producto in self.productos:
            if producto.id == id:
                return producto
        return None
    
    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos if nombre.lower() in p.nombre.lower()]
    
    def buscar_por_categoria(self, categoria):
        return [p for p in self.productos if p.categoria.lower() == categoria.lower()]
    
    def obtener_categorias(self):
        return list(set(p.categoria for p in self.productos))
    
    def eliminar_producto(self, id):
        producto = self.buscar_por_id(id)
        if producto:
            self.productos.remove(producto)
            print("Producto eliminado.")
            return True
        print("Producto no encontrado.")
        return False
    
    def editar_producto(self, id, nuevo_nombre=None, nueva_categoria=None, 
                       nuevo_precio=None, nuevo_stock=None):
        producto = self.buscar_por_id(id)
        if not producto:
            print("Producto no encontrado.")
            return False
            
        if nuevo_nombre and nuevo_nombre.strip():
            producto.nombre = nuevo_nombre.strip()
            
        if nueva_categoria and nueva_categoria.strip():
            producto.categoria = nueva_categoria.strip()
            
        if nuevo_precio is not None:
            if nuevo_precio >= 0:
                producto.precio = nuevo_precio
            else:
                print("Error: El precio no puede ser negativo.")
                return False
                
        if nuevo_stock is not None:
            if nuevo_stock >= 0:
                producto.stock = nuevo_stock
            else:
                print("Error: El stock no puede ser negativo.")
                return False
                
        print("Producto actualizado.")
        return True

class Venta:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.fecha = datetime.now()
        self.total = producto.precio * cantidad
    
    def __str__(self):
        return f"{self.fecha.strftime('%Y-%m-%d %H:%M')} - {self.producto.nombre} x{self.cantidad} - Total: S/. {self.total:.2f}"

class PDFVentas(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(60, 10, 'Reporte de Ventas', 1, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_venta(self, venta):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}", 0, 1)
        self.cell(0, 10, f"Producto: {venta.producto.nombre}", 0, 1)
        self.cell(0, 10, f"Cantidad: {venta.cantidad}", 0, 1)
        self.cell(0, 10, f"Total: S/. {venta.total:.2f}", 0, 1)
        self.ln(10)

class Sistema:
    def __init__(self):
        self.inventario = Inventario()
        # Productos pre-registrados
        productos_iniciales = [
            Producto(nombre="Laptop Gaming", categoria="Electrónica", precio=2500.0, stock=5),
            Producto(nombre="Mouse Inalámbrico", categoria="Electrónica", precio=50.0, stock=10),
            Producto(nombre="Monitor LED", categoria="Electrónica", precio=300.0, stock=3),
            Producto(nombre="Camiseta Polo", categoria="Ropa", precio=45.0, stock=15),
            Producto(nombre="Jean Clásico", categoria="Ropa", precio=70.0, stock=8),
            Producto(nombre="Zapatillas Deportivas", categoria="Calzado", precio=120.0, stock=12),
            Producto(nombre="Botas Mujer", categoria="Calzado", precio=180.0, stock=6),
        ]
        
        for producto in productos_iniciales:
            self.inventario.agregar_producto(producto)
    
    def registrar_venta(self):
        categorias = self.inventario.obtener_categorias()
        if not categorias:
            print("\n====== No hay categorías registradas ===")
            return
        
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria}")
            
        try:
            opcion_categoria = int(input("\nSeleccione el número de categoría: "))
            if opcion_categoria < 1 or opcion_categoria > len(categorias):
                print("====== Opción no válida ===")
                return
            
            categoria_seleccionada = categorias[opcion_categoria - 1]
            productos_categoria = self.inventario.buscar_por_categoria(categoria_seleccionada)
            
            if not productos_categoria:
                print("====== No hay productos en esta categoría ===")
                return
            
            print(f"\nProductos en {categoria_seleccionada}:")
            for i, producto in enumerate(productos_categoria, 1):
                print(f"{i}. ID: {producto.id} - {producto.nombre} - Stock: {producto.stock}")
            
            id_producto = input("\nIngrese el ID del producto: ")
            producto = self.inventario.buscar_por_id(id_producto)
            
            if not producto:
                print("====== Producto no encontrado ===")
                return
            
            cantidad = int(input("Cantidad a vender: "))
            
            if producto.stock < cantidad:
                print("====== Stock insuficiente para la venta ===")
                return
            
            producto.stock -= cantidad
            venta = Venta(producto, cantidad)
            print("====== Venta registrada con éxito ===")
            print(venta)
        except ValueError:
            print("Entrada inválida.")
    
    def encontrar_combinaciones_para_presupuesto(self, presupuesto):
        productos = [p for p in self.inventario.productos 
                    if p.precio <= presupuesto and p.stock > 0]
        
        soluciones = []
        
        def backtrack(index, seleccionados, total):
            if total > presupuesto:
                return
            if total == presupuesto:
                soluciones.append(list(seleccionados))
                return
            
            for i in range(index, len(productos)):
                p = productos[i]
                seleccionados.append(p)
                backtrack(i + 1, seleccionados, total + p.precio)
                seleccionados.pop()
                
            # Intentamos usar menos productos pero más caros
            if index < len(productos) - 1:
                backtrack(index + 1, seleccionados, total)
        
        backtrack(0, [], 0)
        return soluciones
    
    def mostrar_reporte_ventas(self):
        print("\n--- Reporte de Ventas ---")
        categorias = self.inventario.obtener_categorias()
        
        if categorias:
            print("\nCategorías registradas:")
            for categoria in categorias:
                print(f"- {categoria}")
        else:
            print("\nNo hay categorías registradas.")
        
        if hasattr(self, 'ventas') and self.ventas:
            print("\nIDs de ventas registradas:")
            for i, venta in enumerate(self.ventas, 1):
                print(f"{i}. ID: {venta.producto.id} - Producto: {venta.producto.nombre}")
        else:
            print("\nNo hay ventas registradas.")

def main():
    sistema = Sistema()
    
    while True:
        limpiar_pantalla()
        print("\n--- Sistema de Inventario ---")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto por ID")
        print("4. Buscar producto por nombre")
        print("5. Eliminar producto")
        print("6. Editar producto")
        print("7. Registrar venta")
        print("8. Mostrar reporte de ventas")
        print("9. Encontrar combinaciones según presupuesto")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre: ").strip()
            categoria = input("Categoría: ").strip()
            try:
                precio = float(input("Precio: ").strip())
                stock = int(input("Stock: ").strip())
                
                producto = Producto(nombre=nombre, categoria=categoria, 
                                  precio=precio, stock=stock)
                sistema.inventario.agregar_producto(producto)
            except ValueError:
                print("Error en tipo de datos.")
                
        elif opcion == "2":
            sistema.inventario.listar_productos()
            input("\nPresione Enter para volver al menú...")
            
        elif opcion == "3":
            id = input("Ingrese ID del producto: ")
            producto = sistema.inventario.buscar_por_id(id)
            print(producto if producto else "Producto no encontrado.")
            
        elif opcion == "4":
            nombre = input("Ingrese nombre o parte del nombre: ")
            resultados = sistema.inventario.buscar_por_nombre(nombre)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron coincidencias.")
                
        elif opcion == "5":
            id = input("Ingrese ID del producto a eliminar: ")
            sistema.inventario.eliminar_producto(id)
            
        elif opcion == "6":
            id = input("ID del producto a editar: ").strip()
            nuevo_nombre = input("Nuevo nombre: ").strip()
            nueva_categoria = input("Nueva categoría: ").strip()
            try:
                nuevo_precio = float(input("Nuevo precio: ").strip())
                nuevo_stock = int(input("Nuevo stock: ").strip())
                sistema.inventario.editar_producto(id, nuevo_nombre, nueva_categoria, 
                                                 nuevo_precio, nuevo_stock)
            except ValueError:
                print("Error en tipo de datos.")
                
        elif opcion == "7":
            sistema.registrar_venta()
            
        elif opcion == "8":
            sistema.mostrar_reporte_ventas()
            
        elif opcion == "9":
            try:
                presupuesto = float(input("Ingrese el presupuesto disponible: "))
                combinaciones = sistema.encontrar_combinaciones_para_presupuesto(presupuesto)
                if combinaciones:
                    print(f"\nSe encontraron {len(combinaciones)} combinaciones:")
                    for i, combo in enumerate(combinaciones, 1):
                        nombres = ', '.join(p.nombre for p in combo)
                        total = sum(p.precio for p in combo)
                        print(f"{i}. {nombres} -> Total: S/. {total:.2f}")
                else:
                    print("No se encontraron combinaciones.")
            except ValueError:
                print("Presupuesto inválido.")
                
        elif opcion == "0":
            print("Saliendo...")
            break
            
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
