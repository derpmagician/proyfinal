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

class Sistema:
    def __init__(self):
        self.inventario = Inventario()
        self.ventas = []

    def registrar_venta(self):
        id = input("Ingrese ID del producto: ")
        producto = self.inventario.buscar_por_id(id)
        if not producto:
            print("Producto no encontrado.")
            return
        try:
            cantidad = int(input("Cantidad a vender: "))
        except ValueError:
            print("Cantidad inválida.")
            return
        if producto.stock < cantidad:
            print("Stock insuficiente.")
        else:
            producto.stock -= cantidad
            venta = Venta(producto, cantidad)
            self.ventas.append(venta)
            print("Venta registrada con éxito.")
            print(venta)

    def mostrar_reporte_ventas(self):
        print("\n--- Reporte de Ventas ---")
        for venta in self.ventas:
            print(venta)
        total = sum(v.total for v in self.ventas)
        print(f"Total de ingresos: S/. {total:.2f}")

# Menú principal
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
