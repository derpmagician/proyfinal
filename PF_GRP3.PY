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
        self.id = id if id else ''.join(random.choices('0123456789', k=8))
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
    
    def obtener_categorias(self):
        """Retorna una lista única de categorías disponibles."""
        return list(set(p.categoria for p in self.productos))
    
    def buscar_por_categoria(self, categoria):
        """Retorna una lista de productos que pertenecen a la categoría especificada."""
        return [p for p in self.productos if p.categoria == categoria]
    
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
    def __init__(self, fecha, id_venta, categoria, productos, total):
        self.fecha = fecha
        self.id_venta = id_venta
        self.categoria = categoria
        self.productos = productos  # Lista de tuplas (nombre, id, precio, cantidad, categoria)
        self.total = total
    
    def __str__(self):
        fecha_str = self.fecha.strftime('%d/%m/%Y %H:%M')
        productos_str = '\n'.join(
            f"{nombre} / {id_prod} / S/. {precio:.2f} x {cant}"
            for nombre, id_prod, precio, cant, _ in self.productos  # Agregamos _ para ignorar la categoría
        )
        return f"""
Fecha: {fecha_str}
ID: {self.id_venta}
Categoria: {self.categoria}
{productos_str}
Precio total: S/. {self.total:.2f}
"""

class PDFVentas(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(75, 10, 'VENTAS REGISTRADAS', 1, 0, 'C')
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def add_venta(self, venta):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, str(venta))
        self.ln(10)

class Sistema:
    def __init__(self):
        self.inventario = Inventario()
        self.ventas = []
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

    def generar_id_venta(self):
        """Genera un ID único para la venta usando números y letras mayúsculas"""
        caracteres = string.ascii_uppercase + string.digits
        return ''.join(random.choices(caracteres, k=8))
    
    def obtener_categorias(self):
        return list(set(p.categoria for p in self.inventario.productos))
    
    def buscar_por_categoria(self, categoria):
        return [p for p in self.inventario.productos if p.categoria == categoria]
    
    def registrar_venta(self):
        categorias = self.inventario.obtener_categorias()
        if not categorias:
            print("\n====== No hay categorías registradas ===")
            return
        
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria}")
            
        productos_seleccionados = []
        while True:
            try:
                opcion_categoria = input("\nSeleccione el número de categoría (0 para finalizar): ")
                if opcion_categoria == "0":
                    break
                    
                opcion_categoria = int(opcion_categoria)
                if opcion_categoria < 0 or opcion_categoria > len(categorias):
                    print("Opción no válida.")
                    continue
                    
                categoria_seleccionada = categorias[opcion_categoria - 1]
                productos_categoria = self.inventario.buscar_por_categoria(categoria_seleccionada)
                if not productos_categoria:
                    print("No hay productos en esta categoría.")
                    continue
                    
                print(f"\nProductos en {categoria_seleccionada}:")
                for i, producto in enumerate(productos_categoria, 1):
                    print(f"{i}. {producto.nombre} - Stock: {producto.stock}")
                    
                num_producto = input("\nIngrese el número del producto: ")
                if num_producto == "0":
                    continue
                    
                num_producto = int(num_producto)
                if num_producto < 1 or num_producto > len(productos_categoria):
                    print("Número de producto no válido.")
                    continue
                    
                producto = productos_categoria[num_producto - 1]
                cantidad = int(input("Cantidad a vender: "))
                if producto.stock < cantidad:
                    print("Stock insuficiente.")
                    continue
                    
                producto.stock -= cantidad
                productos_seleccionados.append((
                    producto.nombre,
                    producto.id,
                    producto.precio,
                    cantidad,
                    categoria_seleccionada  # Agregamos la categoría
                ))
                
            except ValueError:
                print("Entrada inválida.")
        
        if not productos_seleccionados:
            print("No se han seleccionado productos.")
            return
            
        total_venta = sum(precio * cantidad for _, _, precio, cantidad, _ in productos_seleccionados)
        id_venta = self.generar_id_venta()
        fecha = datetime.now()
        
        # Agrupar productos por categoría para el reporte
        productos_por_categoria = {}
        for nombre, id_prod, precio, cantidad, categoria in productos_seleccionados:
            if categoria not in productos_por_categoria:
                productos_por_categoria[categoria] = []
            productos_por_categoria[categoria].append((nombre, id_prod, precio, cantidad))
        
        venta = Venta(fecha, id_venta, "MÚLTIPLES CATEGORÍAS", productos_seleccionados, total_venta)
        self.ventas.append(venta)
        
        print("\nVenta registrada con éxito:")
        print(venta)
    
    def encontrar_combinaciones_para_presupuesto(self, presupuesto):
    # Obtener categorías disponibles
        categorias = self.inventario.obtener_categorias()
        if not categorias:
            print("No hay categorías disponibles.")
            return []
    
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria}")
    
        try:
        # Seleccionar categoría
            opcion_categoria = int(input("\nSeleccione el número de categoría: "))
            if opcion_categoria < 1 or opcion_categoria > len(categorias):
                print("Opción no válida.")
                return []
        
            categoria_seleccionada = categorias[opcion_categoria - 1]
        
        # Filtrar productos por categoría y presupuesto
            productos = [p for p in self.inventario.productos 
                        if p.categoria == categoria_seleccionada and 
                        p.precio <= presupuesto and 
                        p.stock > 0]
        
            if not productos:
                print(f"No hay productos disponibles en la categoría {categoria_seleccionada}")
                return []
            
            soluciones = []
        
            def backtrack(index, seleccionados, total):
                if total > presupuesto:
                    return
                if total == presupuesto:
                    soluciones.append(list(seleccionados))
                    return
                for i in range(index, len(productos)):
                    p = productos[i]
                    if p.stock > 0:
                        seleccionados.append(p)
                        p.stock -= 1
                        backtrack(i, seleccionados, total + p.precio)
                        seleccionados.pop()
                        p.stock += 1
                    
            backtrack(0, [], 0)
        
        # Limitar a máximo 3 combinaciones
            soluciones = soluciones[:3]
        
            if not soluciones:
                print("No se encontraron combinaciones.")
                return []
            
            print(f"\nSe encontraron {len(soluciones)} combinaciones:")
            for i, combo in enumerate(soluciones, 1):
                nombres = ', '.join(p.nombre for p in combo)
                total = sum(p.precio for p in combo)
                print(f"{i}. {nombres} -> Total: S/. {total:.2f}")
            
            return soluciones
        
        except ValueError:
            print("Entrada inválida.")
        return []
    

    def mostrar_reporte_ventas(self):
        if not hasattr(self, 'ventas') or not self.ventas:
            print("No hay ventas registradas.")
            return
            
        print("\n=== REPORTE DE VENTAS ===")
        print("1. Por día")
        print("2. Por mes")
        print("3. Por año")
        
        try:
            opcion = int(input("Seleccione el período del reporte: "))
            if opcion not in [1, 2, 3]:
                print("Opción no válida.")
                return
                
            # Filtrar ventas según el período seleccionado
            fecha_actual = datetime.now()
            ventas_filtradas = []
            
            if opcion == 1:  # Por día
                ventas_filtradas = [v for v in self.ventas 
                                 if v.fecha.date() == fecha_actual.date()]
                titulo = f"VENTAS REGISTRADAS DEL DÍA {fecha_actual.strftime('%d/%m/%Y')}"
            elif opcion == 2:  # Por mes
                ventas_filtradas = [v for v in self.ventas 
                                 if v.fecha.year == fecha_actual.year and 
                                 v.fecha.month == fecha_actual.month]
                titulo = f"VENTAS REGISTRADAS DEL MES {fecha_actual.strftime('%B %Y')}"
            else:  # Por año
                ventas_filtradas = [v for v in self.ventas 
                                 if v.fecha.year == fecha_actual.year]
                titulo = f"VENTAS REGISTRADAS DEL AÑO {fecha_actual.year}"
                
            if not ventas_filtradas:
                print("No hay ventas para el período seleccionado.")
                return
                
            # Generar PDF
            pdf = PDFVentas()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 15)
            pdf.cell(145, 10, titulo, 1, 0, 'C')
            pdf.ln(30)
            
            for venta in ventas_filtradas:
                pdf.add_venta(venta)
                
            nombre_archivo = f"reporte_ventas_{fecha_actual.strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(nombre_archivo)
            print(f"\nReporte generado exitosamente: {nombre_archivo}")
            
        except ValueError:
            print("Entrada inválida.")

    def generar_pdf_ventas(self):
        if not hasattr(self, 'ventas') or not self.ventas:
            print("No hay ventas para generar el reporte.")
            return
            
        pdf = PDFVentas()
        fecha_actual = datetime.now()
        titulo = f"VENTAS REGISTRADAS POR {fecha_actual.strftime('%B %Y')}"
        pdf.add_page()
        pdf.set_font('Arial', 'B', 15)
        pdf.cell(200, 10, titulo, 1, 0, 'C')
        pdf.ln(20)
        
        for venta in self.ventas:
            pdf.add_venta(venta)
            
        nombre_archivo = f"reporte_ventas_{fecha_actual.strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(nombre_archivo)
        print(f"\nReporte generado exitosamente: {nombre_archivo}")

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
            input("\nPresione Enter para volver al menú...")
                
        elif opcion == "2":
            sistema.inventario.listar_productos()
            input("\nPresione Enter para volver al menú...")
            
        elif opcion == "3":
            id = input("Ingrese ID del producto: ")
            producto = sistema.inventario.buscar_por_id(id)
            print(producto if producto else "Producto no encontrado.")
            input("\nPresione Enter para volver al menú...")
            
        elif opcion == "4":
            nombre = input("Ingrese nombre o parte del nombre: ")
            resultados = sistema.inventario.buscar_por_nombre(nombre)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron coincidencias.")
            input("\nPresione Enter para volver al menú...")
                
        elif opcion == "5":
            id = input("Ingrese ID del producto a eliminar: ")
            sistema.inventario.eliminar_producto(id)
            input("\nPresione Enter para volver al menú...")
            
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
            input("\nPresione Enter para volver al menú...")
                
        elif opcion == "7":
            sistema.registrar_venta()
            input("\nPresione Enter para volver al menú...")
            
        elif opcion == "8":
            sistema.mostrar_reporte_ventas()
            input("\nPresione Enter para volver al menú...")
            
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
            input("\nPresione Enter para volver al menú...")
        
                
        elif opcion == "0":
            print("Saliendo...")
            break
            
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
