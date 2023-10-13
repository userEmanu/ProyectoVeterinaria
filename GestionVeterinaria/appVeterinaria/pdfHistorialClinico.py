from fpdf import FPDF
import random
import datetime
import os
def codigo():
    codigo = random.randint(0, 99999)
    return codigo

def fecha():
    now = datetime.datetime.now()
    # Formatea la fecha y hora en el formato deseado: mm/dd/yyyy hh:mm:ss
    formatted_date_time = now.strftime("%m/%d/%Y %H:%M:%S")
    return formatted_date_time
    
class PDF(FPDF):
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Historial Clínico', 0, 1, 'C')
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
        self.image(f'{logo_path}', 10, 10, 40)
        self.set_font('Arial', size=10)
        self.cell(0, 10, f'Fecha y Hora: {fecha()}', 0, 0, 'R')
        self.set_font('Arial', size=10)
        self.cell(0, 20, f'Código de Cita: {codigo()} ', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Veterinaria Animalagro', 0, 0, 'C')
        self.cell(0, 10, f'Fecha y Hora: {fecha()}', 0, 0, 'R')  # Añadir la fecha y hora aquí


    def mostrar(self, cita):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Información del Usuario', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(50, 10, 'Nombre y Apellido', 1, 0, 'C', 1)
        self.cell(40, 10, 'Tipo de Ide', 1, 0, 'C', 1)
        self.cell(40, 10, 'No. Identificación', 1, 0, 'C', 1)
        self.cell(60, 10, 'Correo Electrónico', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        self.cell(50, 10, f'{cita.ciUsuario.first_name} {cita.ciUsuario.last_name}', 1)
        self.cell(40, 10, f'{cita.ciUsuario.userTipoDoc}', 1)
        self.cell(40, 10, f'{cita.ciUsuario.userNoDoc}', 1)
        self.cell(60, 10, f'{cita.ciUsuario.email}', 1)
        self.ln()

        # Tabla 2: Descripción de la Mascota
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Información de la Mascota', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(50, 10, 'Nombre', 1, 0, 'C', 1)
        self.cell(40, 10, 'Raza', 1, 0, 'C', 1)
        self.cell(50, 10, 'Tipo de Animal', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        if cita.ciMascota != None:
            self.cell(50, 10, f'{cita.ciMascota.masNombre}', 1)
            self.cell(40, 10, f'{cita.ciMascota.masRaza}', 1)
            self.cell(50, 10, f'{cita.ciMascota.masTipoAnimal}', 1)
        else:
            self.cell(50, 10, f'Animales De Granja', 1)
            self.cell(40, 10, f'Animales De Granja', 1)
            self.cell(50, 10, f'Animales De Granja', 1)
        self.ln()


        # Tabla 3: Descripción del Servicio
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Información del Servicio', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(50, 10, 'Nombre ', 1, 0, 'C', 1)
        self.cell(40, 10, 'Tipo ', 1, 0, 'C', 1)
        self.cell(40, 10, 'Precio', 1, 0, 'C', 1)
        self.cell(60, 10, 'Empleado', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        self.cell(50, 10, f'{cita.ciServicio.serNombre}', 1)
        self.cell(40, 10, f'{cita.ciServicio.serTipo}', 1)
        self.cell(40, 10, f'{cita.ciServicio.serPrecio}', 1)
        if cita.ciServicio.serEmpleado != None:
            self.cell(60, 10, f'{cita.ciServicio.serEmpleado.emNombre} {cita.ciServicio.serEmpleado.emApellido}', 1)
        else: 
            self.cell(60, 10, f'Sin Empleado Asignado', 1)
        self.ln()

        # Tabla 4: Descripción de la Cita
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Información de la Cita', 0, 1)
        self.set_fill_color(200, 220, 255)
        self.cell(50, 10, 'Fecha y Hora', 1, 0, 'C', 1)
        self.cell(40, 10, 'Estado', 1, 0, 'C', 1)
        self.cell(90, 10, 'Síntomas o Motivo', 1, 1, 'C', 1)
        self.set_font("Arial", '', 12)
        self.cell(50, 10, f'{cita.ciFecha} {cita.ciHora}', 1)
        self.cell(40, 10, f'{cita.ciEstado}', 1)
        self.cell(90, 10, f'{cita.ciSintomas}', 1)
        self.ln()

       
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Descripción de la Cita', 0, 1)
        self.set_fill_color(200, 220, 255)

        # Añadir celda para "Descripción"
        self.cell(50, 10, f'Descripcion', 1, 0, 'C', 1)

        # Cambiar a la fuente regular
        self.set_font("Arial", '', 12)

        # Obtener la posición Y después de la celda "Descripción"
        y = self.get_y()

        # Añadir celda para "Mucho texto" debajo de la celda "Descripción"
        self.set_xy(50, y)
        self.multi_cell(0, 10, f'{cita.ciDescripcion}', 1, 'C', 1)

        # Alinear la siguiente celda a la izquierda
        self.ln()


# Guardar el PDF en un archivo

