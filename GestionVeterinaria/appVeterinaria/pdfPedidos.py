from fpdf import FPDF
import os
import random
import datetime
def codigo():
    codigo = random.randint(0, 99999)
    return codigo

def fecha():
    now = datetime.datetime.now()
    # Formatea la fecha y hora en el formato deseado: mm/dd/yyyy hh:mm:ss
    formatted_date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    return formatted_date_time

class PDFPedido(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 40, 'Factura de pedido', 0, 1, 'C')
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
        self.image(f'{logo_path}', 10, 10, 40)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', size=10)
        self.cell(0, 10, f'Fecha y Hora: {fecha()}', 0, 0, 'R')
        self.set_font('Arial', size=10)
        self.cell(0, 20, f'Código pdf: {codigo()}', 0, 1, 'R')
    
    def mostrar(self, detPedido, pe, di):
        
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Detalle del Pedido', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(50, 10, 'Codigo de pedido', 1, 0, 'C', 1)
        self.cell(50, 10, 'Estado', 1, 0, 'C', 1)
        self.cell(50, 10, 'Fecha', 1, 0, 'C', 1)
        self.cell(40, 10, 'Descuento', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        self.cell(50, 10, f"{pe.peCodigoPedido}", 1)
        self.cell(50, 10, f"{pe.peEstado}", 1)
        self.cell(50, 10, f"{pe.peFecha}", 1)
        self.cell(40, 10, f"{pe.peDescuento}", 1)

        self.ln()

        # Tabla 2: Descripción de la Mascota
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Detalle de la compra', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(50, 10, 'Producto', 1, 0, 'C', 1)
        self.cell(40, 10, 'Cantidad', 1, 0, 'C', 1)
        self.cell(40, 10, 'Precio por unidad', 1, 0, 'C', 1)
        self.cell(60, 10, 'Valor', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        for l in detPedido:
            self.cell(50, 10, f"{l.detProducto.proNombre}", 1)
            self.cell(40, 10, f"{l.detCantida}", 1)
            self.cell(40, 10, f"{l.detProducto.proPrecio}", 1)
            self.cell(60, 10, f"{l.detPrecio}", 1,1)
        self.cell(90, 10, '', )
        self.cell(40, 10, 'Total:', 1, 0, 'C', 1)
        self.cell(60, 10, f'{pe.peTotalPedido }', 1)

        self.ln()

        # Tabla 3: Descripción del Servicio
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Detalle del envio', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(55, 10, 'Nombre del destinatario', 1, 0, 'C', 1)
        self.cell(55, 10, 'Número de Identificación', 1, 0, 'C', 1)
        self.cell(30, 10, 'Direccion', 1, 0, 'C', 1)
        self.cell(50, 10, 'Correo Electrónico', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        self.cell(55, 10, f"{pe.peDetEnvio.detNombreDestinatario}", 1)
        self.cell(55, 10, f"{pe.peDetEnvio.detNitDestinatario}", 1)
        self.cell(30, 10, f"{di}", 1)
        self.cell(50, 10, f"{pe.peDetEnvio.detCorreoDestinatario }", 1)
        self.ln()

        # Tabla 4: informacion detalle de metodo de pago
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Detalle metodo de pago', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(95, 10, 'Tipo metodo de pago', 1, 0, 'C', 1)
        self.cell(95, 10, 'Descripcion', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        urlNequi = os.path.join(os.path.dirname(__file__), 'static/image/NEQUI.jpg')
        # self.image(95, 10, f'{urlNequi}', 1)
        self.cell(95, 10, 'Nequi', 1)
        self.cell(95, 10, 'Cuenta No Tel: 311492310', 1)
        self.ln()
        urlPse = os.path.join(os.path.dirname(__file__), 'static/image/PSE.jpg')
        self.cell(95, 10, 'PSE - Pagos Seguros en Línea', 1)
        self.cell(95, 10, f'Cuenta: 801921892981',1)
        self.ln()
        urlBanco = os.path.join(os.path.dirname(__file__), 'static/image/Bancolombia.png')
        # self.image(urlBanco, x=10, y=self.get_y() + 2, w=95, h=10)
        self.cell(95, 10, 'Bancolombia', 1)
        self.cell(95, 10, f'Cuenta tipo nomina, Nit 81921111',1)
        self.ln()
