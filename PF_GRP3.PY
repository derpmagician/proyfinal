import string
from fpdf import FPDF
from datetime import datetime

class Producto:
    def __init__(self, id, nombre, categoria, precio, stock):
        self.id = id
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
        if any(p.id == producto.id for p in self.productos):
            print("Error: ID duplicado. No se puede agregar el producto.")
        else:
            self.productos.append(producto)
            print("Producto agregado con éxito.")
    
    def listar_productos(self):
        if not self.productos:
            print("No hay productos en inventario.")
        for producto in self.productos:
            print(producto)
    
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
        else:
            print("Producto no encontrado.")
    
    def editar_producto(self, id, nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock):
        producto = self.buscar_por_id(id)
        if producto:
            producto.nombre = nuevo_nombre
            producto.categoria = nueva_categoria
            producto.precio = nuevo_precio
            producto.stock = nuevo_stock
            print("Producto actualizado.")
        else:
            print("Producto no encontrado.")

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
        self.cell(30, 10, 'Reporte de Ventas', 1, 0, 'C')
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
        self.ventas = []
    
    def registrar_venta(self):
        # Mostrar categorías disponibles
        categorias = self.inventario.obtener_categorias()
        if not categorias:
            print("No hay categorías registradas.")
            return
            
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria}")
            
        try:
            opcion_categoria = int(input("\nSeleccione el número de categoría: "))
            if opcion_categoria < 1 or opcion_categoria > len(categorias):
                print("Categoría no válida.")
                return
                
            categoria_seleccionada = categorias[opcion_categoria - 1]
            
            # Mostrar productos de la categoría
            productos_categoria = self.inventario.buscar_por_categoria(categoria_seleccionada)
            if not productos_categoria:
                print("No hay productos en esta categoría.")
                return
                
            print(f"\nProductos en {categoria_seleccionada}:")
            for i, producto in enumerate(productos_categoria, 1):
                print(f"{i}. ID: {producto.id} - {producto.nombre} - Stock: {producto.stock}")
                
            try:
                id_producto = input("\nIngrese el ID del producto: ")
                producto = self.inventario.buscar_por_id(id_producto)
                
                if not producto:
                    print("Producto no encontrado.")
                    return
                    
                cantidad = int(input("Cantidad a vender: "))
                
                if producto.stock < cantidad:
                    print("Stock insuficiente.")
                    return
                    
                producto.stock -= cantidad
                venta = Venta(producto, cantidad)
                self.ventas.append(venta)
                print("\nVenta registrada con éxito.")
                print(venta)
                
            except ValueError:
                print("Cantidad inválida.")
                
        except ValueError:
            print("Opción no válida.")
    
    def mostrar_reporte_ventas(self):
        print("\n--- Reporte de Ventas ---")
        
        # Mostrar categorías registradas
        categorias = self.inventario.obtener_categorias()
        if categorias:
            print("\nCategorías registradas:")
            for categoria in categorias:
                print(f"- {categoria}")
        else:
            print("\nNo hay categorías registradas.")
            
        # Mostrar IDs de ventas
        if self.ventas:
            print("\nIDs de ventas registradas:")
            for i, venta in enumerate(self.ventas, 1):
                print(f"{i}. ID: {venta.producto.id} - Producto: {venta.producto.nombre}")
        else:
            print("\nNo hay ventas registradas.")
            
        # Generar PDF filtrado
        self.generar_pdf_ventas_filtrado()
    
    def generar_pdf_ventas_filtrado(self):
        # Solicitar filtros
        print("\nFiltros para el reporte:")
        print("1. Por categoría")
        print("2. Por mes")
        print("3. Por día")
        print("4. Sin filtros")
        
        try:
            opcion_filtro = int(input("Seleccione el filtro (1-4): "))
            
            ventas_filtradas = self.ventas
            nombre_archivo = "reporte_ventas"
            
            if opcion_filtro == 1:
                categorias = self.inventario.obtener_categorias()
                print("\nCategorías disponibles:")
                for i, categoria in enumerate(categorias, 1):
                    print(f"{i}. {categoria}")
                categoria_idx = int(input("Seleccione el número de categoría: ")) - 1
                categoria_seleccionada = categorias[categoria_idx]
                ventas_filtradas = [v for v in self.ventas if v.producto.categoria == categoria_seleccionada]
                nombre_archivo += f"_{categoria_seleccionada}"
                
            elif opcion_filtro == 2:
                mes = int(input("Ingrese el mes (1-12): "))
                ventas_filtradas = [v for v in self.ventas if v.fecha.month == mes]
                nombre_archivo += f"_mes_{mes}"
                
            elif opcion_filtro == 3:
                dia = int(input("Ingrese el día (1-31): "))
                ventas_filtradas = [v for v in self.ventas if v.fecha.day == dia]
                nombre_archivo += f"_dia_{dia}"
                
            # Generar PDF
            pdf = PDFVentas()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f"Reporte de Ventas - {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
            pdf.ln(10)
            
            for venta in ventas_filtradas:
                pdf.add_venta(venta)
            
            pdf.output(f"{nombre_archivo}.pdf")
            print(f"\nPDF generado exitosamente: {nombre_archivo}.pdf")
            
        except ValueError:
            print("Opción no válida.")

def main():
    sistema = Sistema()
    while True:
        print("\n--- Sistema de Inventario ---")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto por ID")
        print("4. Buscar producto por nombre")
        print("5. Eliminar producto")
        print("6. Editar producto")
        print("7. Registrar venta")
        print("8. Reporte de ventas")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            categoria = input("Categoría: ")
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
            except ValueError:
                print("Error en tipo de datos.")
                continue
            producto = Producto(id, nombre, categoria, precio, stock)
            sistema.inventario.agregar_producto(producto)
            
        elif opcion == "2":
            sistema.inventario.listar_productos()
            
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
            id = input("ID del producto a editar: ")
            nuevo_nombre = input("Nuevo nombre: ")
            nueva_categoria = input("Nueva categoría: ")
            try:
                nuevo_precio = float(input("Nuevo precio: "))
                nuevo_stock = int(input("Nuevo stock: "))
            except ValueError:
                print("Error en tipo de datos.")
                continue
            sistema.inventario.editar_producto(id, nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock)
            
        elif opcion == "7":
            sistema.registrar_venta()
            
        elif opcion == "8":
            sistema.mostrar_reporte_ventas()
            
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
