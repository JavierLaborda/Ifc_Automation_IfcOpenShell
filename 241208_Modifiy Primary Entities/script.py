# -*- coding: utf-8 -*-
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# INFORMACIÓN SCRIPT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
__autor__ = Jose Javier Laborda / jj.laborda.lopez@gmail.com
__version__ = 1.0
__fecha__ = 2024-12-27
__cliente__ = Abierto
___doc__ = Este script permite seleccionar un archivo IFC y modificar las
           entidades principales como IfcProject, IfcSite e IfcBuilding.
           Además, admite entidades de infraestructura como IfcBridge,
           IfcRoad, entre otros.

__software__ = Python 3.12
__bibliotecas__ = tkinter, ifcopenshell
"""

# .............................................................................
# IMPORTACIÓN DE BIBLIOTECAS
# .............................................................................
import os
import ifcopenshell
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# .............................................................................
# CLASES
# .............................................................................
class AplicacionIFC:
    """
    Clase principal para gestionar la selección del archivo IFC.
    """
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("IFC Automatizaciones")
        self.ventana.geometry("500x300")
        self.ventana.resizable(False, False)

        # Variable para recoger el archivo IFC
        self.archivo_ifc_ruta = tk.StringVar()

        # Crear la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal
        marco_titulo = ttk.Frame(self.ventana, padding=(10, 10))
        marco_titulo.pack(fill="x", pady=5)
        ttk.Label(
            marco_titulo,
            text="Modificar Entidades IFC",
            font=("Roboto", 14, "bold"),
            anchor="center"
        ).pack()

        # Descripción breve
        marco_descripcion = ttk.Frame(self.ventana, padding=(10, 10))
        marco_descripcion.pack(fill="x", pady=5)
        ttk.Label(
            marco_descripcion,
            text=(
                "Este desarrollo permite seleccionar un archivo IFC y modificar "
                "el contenido de sus entidades base, como IfcProject, IfcSite, "
                "e IfcBuilding o infraestructuras como IfcRoad, IfcBridge, entre otros."
            ),
            wraplength=480,
            font=("Roboto", 10),
            anchor="center",
            justify="left"
        ).pack()

        # Selector de archivo IFC
        marco_archivo = ttk.Frame(self.ventana, padding=(10, 10))
        marco_archivo.pack(fill="x", pady=5)
        ttk.Label(
            marco_archivo, text="Seleccionar archivo IFC de origen:", 
            font=("Roboto", 11)).pack(anchor="w", pady=2)
        marco_entrada = ttk.Frame(marco_archivo)
        marco_entrada.pack(fill="x")
        entrada_ruta = ttk.Entry(
            marco_entrada, textvariable=self.archivo_ifc_ruta, 
            font=("Roboto", 11))
        entrada_ruta.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(
            marco_entrada,
            text="...",
            command=self.seleccionar_archivo,
            width=3
        ).pack(side="right", padx=5)

        # Botones Aceptar y Cancelar
        marco_botones = ttk.Frame(self.ventana, padding=(10, 5))
        marco_botones.pack(fill="x", pady=10)
        ttk.Button(
            marco_botones, text="Cancelar", command=self.cancelar_accion, 
            width=12).pack(side="left", padx=5)
        ttk.Button(
            marco_botones, text="Aceptar", command=self.aceptar_accion, 
            width=12).pack(side="right", padx=5)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos IFC", "*.ifc")])
        if archivo:
            self.archivo_ifc_ruta.set(archivo)

    def aceptar_accion(self):
        self.ventana.destroy()

    def cancelar_accion(self):
        print("Operación cancelada.")
        self.ventana.quit()


class FormularioSecundario:
    """
    Clase para gestionar el formulario secundario donde se modifican los nombres.
    """
    def __init__(self, ventana, nombre_entidad):
        self.ventana = ventana
        self.ventana.title("Modificar Entidades IFC")
        self.ventana.geometry("500x420")
        self.ventana.resizable(False, False)

        # Variables para recoger datos
        self.nombre_proyecto_ifc = tk.StringVar()
        self.nombre_emplazamiento_ifc = tk.StringVar()
        self.nombre_entidad_ifc = tk.StringVar()
        self.ruta_guardado_ifc = tk.StringVar()
        self.nombre_archivo_ifc = tk.StringVar()
        self.nombre_entidad = nombre_entidad

        # Crear la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal
        marco_titulo = ttk.Frame(self.ventana, padding=(10, 10))
        marco_titulo.pack(fill="x", pady=5)
        ttk.Label(
            marco_titulo,
            text="Modificar Entidades IFC",
            font=("Roboto", 14, "bold"),
            anchor="center"
        ).pack()

        # Campos
        self.crear_campo(
            "Introducir nombre del IfcProject:", "Por Ejemplo: Proyecto Construcción 1", 
            self.nombre_proyecto_ifc)
        self.crear_campo(
            "Introducir nombre del IfcSite:", "Por Ejemplo: Emplazamiento 1", 
            self.nombre_emplazamiento_ifc)
        self.crear_campo(
            f"Introducir nombre del {self.nombre_entidad}:", "Por Ejemplo: Edificación 1", 
            self.nombre_entidad_ifc)
        self.crear_campo_con_boton(
            "Seleccionar ruta archivo destino:", self.ruta_guardado_ifc)
        self.crear_campo(
            "Seleccionar nombre de archivo IFC destino:", "Por Ejemplo: archivo_final.ifc", 
            self.nombre_archivo_ifc)

        # Botones Aceptar y Cancelar
        marco_botones = ttk.Frame(self.ventana, padding=(10, 5))
        marco_botones.pack(fill="x", pady=10)
        ttk.Button(
            marco_botones, text="Cancelar", command=self.cancelar_accion, 
            width=12).pack(side="left", padx=5)
        ttk.Button(
            marco_botones, text="Continuar", command=self.aceptar_accion, 
            width=12).pack(side="right", padx=5)

    def crear_campo(self, texto_label, placeholder, variable):
        marco = ttk.Frame(self.ventana, padding=(10, 5))
        marco.pack(fill="x")
        ttk.Label(marco, text=texto_label, font=("Roboto", 11)).pack(anchor="w", pady=2)
        entrada = ttk.Entry(marco, textvariable=variable, font=("Roboto", 11))
        entrada.insert(0, placeholder)
        entrada.configure(foreground="grey")
        entrada.bind("<FocusIn>", lambda e: self.limpiar_placeholder(
            e, placeholder, variable))
        entrada.bind("<FocusOut>", lambda e: self.agregar_placeholder(
            e, placeholder, variable))
        entrada.pack(fill="x", padx=5)

    def crear_campo_con_boton(self, texto_label, variable):
        marco = ttk.Frame(self.ventana, padding=(10, 5))
        marco.pack(fill="x")
        ttk.Label(marco, text=texto_label, font=("Roboto", 11)).pack(anchor="w", pady=2)
        marco_entrada = ttk.Frame(marco)
        marco_entrada.pack(fill="x")
        entrada = ttk.Entry(marco_entrada, textvariable=variable, font=("Roboto", 11))
        entrada.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(
            marco_entrada, text="...", command=lambda: self.seleccionar_carpeta(variable),
            width=3).pack(side="right", padx=5)

    def limpiar_placeholder(self, evento, placeholder, variable):
        if evento.widget.get() == placeholder:
            evento.widget.delete(0, tk.END)
            evento.widget.configure(foreground="black")
            variable.set("")

    def agregar_placeholder(self, evento, placeholder, variable):
        if not evento.widget.get():
            evento.widget.insert(0, placeholder)
            evento.widget.configure(foreground="grey")
            variable.set("")

    def seleccionar_carpeta(self, variable):
        carpeta = filedialog.askdirectory()
        if carpeta:
            variable.set(carpeta)

    def aceptar_accion(self):
        self.ventana.quit()

    def cancelar_accion(self):
        print("Operación cancelada en el segundo formulario.")
        self.ventana.quit()


class PantallaCarga:
    """
    Clase para mostrar una barra de carga entre procesos.
    """
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Cargando...")
        self.ventana.geometry("300x100")
        self.ventana.resizable(False, False)

        # Crear barra de progreso
        self.progreso = ttk.Progressbar(
            self.ventana, orient="horizontal", length=280, mode="indeterminate")
        self.progreso.pack(pady=20)
        self.progreso.start()

    def cerrar(self):
        self.progreso.stop()
        self.ventana.destroy()

# .............................................................................
# FUNCIONES
# .............................................................................
def buscar_entidad_ifc(archivo_ifc):
    """
    Busca una entidad de nivel 3 en el archivo IFC.
    """
    try:
        ifc_archivo = ifcopenshell.open(archivo_ifc)
        tipos_entidades = [
            "IfcBuilding", "IfcBridge", "IfcRoad", "IfcRailway",
            "IfcMarineFacility", "IfcTunnel", "IfcDam", "IfcAirport", 
            "IfcHarbor"
        ]
        for tipo in tipos_entidades:
            entidades = ifc_archivo.by_type(tipo)
            if entidades:
                return entidades
        return None
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo IFC: {e}")
        return None

# .............................................................................
# SCRIPT PRINCIPAL
# .............................................................................
# ---------------------------------------------------------------- Formulario 1
if __name__ == "__main__":
    try:
        # Formulario principal
        root = tk.Tk()
        app = AplicacionIFC(root)
        root.mainloop()
        ruta_archivo = app.archivo_ifc_ruta.get()
        if not ruta_archivo:
            raise ValueError("No se seleccionó ningún archivo IFC.")

        # Pantalla de carga
        root_carga = tk.Tk()
        pantalla_carga = PantallaCarga(root_carga)
        root_carga.after(2000, pantalla_carga.cerrar)
        root_carga.mainloop()

        # Buscar entidad nivel 3
        entidad = buscar_entidad_ifc(ruta_archivo)
        if not entidad:
            raise ValueError(
                "No se encontraron entidades válidas en el archivo IFC.")
        tipo_entidad = entidad[0].is_a()
        
# ---------------------------------------------------------------- Formulario 2
        # Formulario secundario
        root2 = tk.Tk()
        formulario = FormularioSecundario(root2, tipo_entidad)
        root2.mainloop()

        nombre_proyecto = formulario.nombre_proyecto_ifc.get()
        nombre_emplazamiento = formulario.nombre_emplazamiento_ifc.get()
        nombre_entidad = formulario.nombre_entidad_ifc.get()
        ruta_guardado = formulario.ruta_guardado_ifc.get()
        nombre_archivo = formulario.nombre_archivo_ifc.get()

        if not all([nombre_proyecto, nombre_emplazamiento, 
                    nombre_entidad, ruta_guardado, nombre_archivo]):
            raise ValueError("No se completaron todos los campos del formulario.")

# --------------------------------------------------------------- Modificar Ifc
        # Modificar archivo IFC
        ruta_salida = os.path.join(ruta_guardado, f"{nombre_archivo}.ifc")
        archivo_ifc = ifcopenshell.open(ruta_archivo)
        # Modificar IfcProject
        proyecto = archivo_ifc.by_type("IfcProject")[0]
        proyecto.Name = nombre_proyecto
        # Modificar IfcSite
        emplazamientos = archivo_ifc.by_type("IfcSite")
        for emplazamiento in emplazamientos:
            emplazamiento.Name = nombre_emplazamiento
        # Modificar entidad nivel 3
        entidades_nivel3 = archivo_ifc.by_type(tipo_entidad)
        for entidad in entidades_nivel3:
            entidad.Name = nombre_entidad

# ------------------------------------------------------------------ Output Ifc
        # Guardar archivo modificado
        archivo_ifc.write(ruta_salida)
        messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_salida}")

# --------------------------------------------------------------- Mensaje error
    except Exception as e:
        messagebox.showerror("Error", str(e))
