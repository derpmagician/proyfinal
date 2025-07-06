
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