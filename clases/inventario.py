from datetime import datetime
import pandas as pd

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
