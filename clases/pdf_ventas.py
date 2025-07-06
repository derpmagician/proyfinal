from fpdf import FPDF

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