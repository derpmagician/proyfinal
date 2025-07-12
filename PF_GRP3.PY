import string
import os
import random
import jinja2
import uuid
from datetime import datetime

from clases.producto import Producto  
from clases.inventario import Inventario  
from clases.venta import Venta 
from clases.pdf_ventas import PDFVentas

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


class Sistema:
    def __init__(self):
        self.inventario = Inventario()
        self.ventas = []
        # Productos pre-registrados
        productos_iniciales = [
            Producto(nombre="Laptop Gaming", categoria="Electrónica", precio=2500.0, stock=5),
            Producto(nombre="Mouse Inalámbrico", categoria="Electrónica", precio=50.0, stock=10),
            Producto(nombre="Monitor LED", categoria="Electrónica", precio=300.0, stock=3),
            Producto(nombre="Tablet Android", categoria="Electrónica", precio=400.0, stock=4),
            Producto(nombre="Smartphone", categoria="Electrónica", precio=800.0, stock=5),
            Producto(nombre="Cargador USB-C", categoria="Electrónica", precio=25.0, stock=15),
            Producto(nombre="Parlante Bluetooth", categoria="Electrónica", precio=180.0, stock=8),
            Producto(nombre="Camiseta Polo", categoria="Ropa", precio=45.0, stock=15),
            Producto(nombre="Jean Clásico", categoria="Ropa", precio=70.0, stock=8),
            Producto(nombre="Sudadera con Capucha", categoria="Ropa", precio=65.0, stock=10),
            Producto(nombre="Pantalón Deportivo", categoria="Ropa", precio=55.0, stock=14),
            Producto(nombre="Vestido Casual", categoria="Ropa", precio=85.0, stock=9),
            Producto(nombre="Zapatillas Deportivas", categoria="Calzado", precio=120.0, stock=12),
            Producto(nombre="Botas Mujer", categoria="Calzado", precio=180.0, stock=6),
            Producto(nombre="Sandalias Verano", categoria="Calzado", precio=60.0, stock=15),
            Producto(nombre="Botines Cuero", categoria="Calzado", precio=200.0, stock=5),
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
        
            # Filtrar productos que cumplan las condiciones:
            # 1. Pertenezcan a la categoría seleccionada
            # 2. Su precio individual no exceda el presupuesto
            # 3. Tengan stock disponible
            productos = [p for p in self.inventario.productos 
                        if p.categoria == categoria_seleccionada and 
                        p.precio <= presupuesto and 
                        p.stock > 0]
        
            if not productos:
                print(f"No hay productos disponibles en la categoría {categoria_seleccionada}")
                return []
            
            soluciones = []
        
            def backtrack(index, seleccionados, total):
                """
                Función recursiva que implementa el algoritmo de backtracking
                para encontrar combinaciones que sumen exactamente el presupuesto.
                
                Args:
                    index (int): Índice actual en la lista de productos
                    seleccionados (list): Lista de productos seleccionados hasta ahora
                    total (float): Suma acumulada de precios de productos seleccionados
                """
                # Caso base 1: Si el total excede el presupuesto, podar esta rama
                if total > presupuesto:
                    return
                # Caso base 2: Si encontramos una combinación exacta, guardarla
                if total == presupuesto:
                    soluciones.append(list(seleccionados)) # Crear copia de la lista
                    return
                # Explorar todas las posibles combinaciones desde el índice actual
                for i in range(index, len(productos)):
                    p = productos[i]
                    # Solo considerar productos con stock disponible
                    if p.stock > 0:
                        # Agregar producto a la selección actual
                        seleccionados.append(p)
                        # Reducir stock temporalmente para evitar duplicados
                        p.stock -= 1
                        # Llamada recursiva: seguir explorando desde el mismo índice
                        # (permite múltiples unidades del mismo producto)
                        backtrack(i, seleccionados, total + p.precio)
                        # Backtrack: deshacer los cambios para explorar otras opciones
                        seleccionados.pop() # Quitar producto de la selección
                        p.stock += 1 # Restaurar stock original
            # Iniciar el algoritmo de backtracking    
            backtrack(0, [], 0)
        
            # Limitar a máximo 3 combinaciones
            soluciones = soluciones[:3]
        
            if not soluciones:
                print("No se encontraron combinaciones.")
                return []
            
            print(f"\nSe encontraron {len(soluciones)} combinaciones:")
            for i, combo in enumerate(soluciones, 1):
                # Crear string con nombres de productos separados por comas
                nombres = ', '.join(p.nombre for p in combo)
                # Calcular total de la combinación
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
            categoria = input("Categoría (Electrónica, Ropa, Calzado): ").strip()
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
                # if combinaciones:
                #     print(f"\nSe encontraron {len(combinaciones)} combinaciones:")
                #     for i, combo in enumerate(combinaciones, 1):
                #         nombres = ', '.join(p.nombre for p in combo)
                #         total = sum(p.precio for p in combo)
                #         print(f"{i}. {nombres} -> Total: S/. {total:.2f}")
                # else:
                #     print("No se encontraron combinaciones.")
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
