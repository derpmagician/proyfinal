import random

class Producto:
    def __init__(self, id=None, nombre="", categoria="", precio=0.0, stock=0):
        self.id = id if id else ''.join(random.choices('0123456789', k=8))
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
    
    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.categoria}) - S/. {self.precio:.2f} - Stock: {self.stock}"