# -*- coding: utf-8 -*-
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# INFORMACIÓN SCRIPT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
__autor__ = Jose Javier Laborda / jj.laborda.lopez@gmail.com
__version__ = 1.1
__fecha__ = 2025-01-10
__cliente__ = Abierto
__doc__ = Este script permite generar un archivo IDS basado en un archivo Excel
           con estructuras definidas para metadatos, especificaciones,
           aplicabilidad y requisitos.
           Incluye interfaz Tkinter para seleccionar los archivos y parámetros
           necesarios. Gestión de errores mejorada y explicación detallada.

__software__ = Python 3.12
__bibliotecas__ = pandas, ifctester, tkinter
"""

# .............................................................................
# IMPORTACIÓN DE BIBLIOTECAS
# .............................................................................
import os
import pandas as pd
import ifctester as ids
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# .............................................................................
# CLASES
# .............................................................................
class AplicacionIDS:
    """
    Clase principal para gestionar la interfaz de selección de rutas y archivos.

    Métodos:
        - crear_interfaz: Configura los widgets principales de la ventana.
        - seleccionar_archivo: Abre un diálogo para seleccionar el archivo Excel.
        - seleccionar_carpeta: Abre un diálogo para seleccionar una carpeta.
        - generar_ids: Verifica los campos y cierra la ventana para continuar.
        - cancelar_accion: Cierra la ventana sin procesar.
    """

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generador de IDS")
        self.ventana.geometry("500x300")
        self.ventana.resizable(False, False)

        # Variables para almacenar rutas y nombres
        self.ruta_excel = tk.StringVar()
        self.ruta_guardado = tk.StringVar()
        self.nombre_archivo_ids = tk.StringVar()

        self.crear_interfaz()

    def crear_interfaz(self):
        """
        Configura y añade los elementos de la ventana principal.
        """
        marco_titulo = ttk.Frame(self.ventana, padding=(10, 10))
        marco_titulo.pack(fill="x", pady=5)
        ttk.Label(
            marco_titulo,
            text="Generador de IDS",
            font=("Roboto", 14, "bold"),
            anchor="center",
        ).pack()

        # Campos de entrada
        self.crear_campo(
            "Seleccionar archivo Excel de origen:", "Archivo Excel", self.ruta_excel, self.seleccionar_archivo
        )
        self.crear_campo(
            "Seleccionar ruta de guardado:", "Ruta de guardado", self.ruta_guardado, self.seleccionar_carpeta
        )
        self.crear_campo(
            "Nombre del archivo IDS:", "Ejemplo: archivo.ids", self.nombre_archivo_ids
        )

        # Botones
        marco_botones = ttk.Frame(self.ventana, padding=(10, 5))
        marco_botones.pack(fill="x", pady=10)
        ttk.Button(marco_botones, text="Cancelar", command=self.cancelar_accion, width=12).pack(side="left", padx=5)
        ttk.Button(marco_botones, text="Continuar", command=self.generar_ids, width=12).pack(side="right", padx=5)

    def crear_campo(self, texto_label, placeholder, variable, comando=None):
        """
        Crea un campo de entrada con etiqueta y botón (opcional).

        Argumentos:
            - texto_label: Texto descriptivo del campo.
            - placeholder: Texto predeterminado.
            - variable: Variable para enlazar con el campo.
            - comando: Función a ejecutar si se incluye un botón.
        """
        marco = ttk.Frame(self.ventana, padding=(10, 5))
        marco.pack(fill="x")
        ttk.Label(marco, text=texto_label, font=("Roboto", 11)).pack(anchor="w", pady=2)
        marco_entrada = ttk.Frame(marco)
        marco_entrada.pack(fill="x")
        entrada = ttk.Entry(marco_entrada, textvariable=variable, font=("Roboto", 11))
        entrada.pack(side="left", fill="x", expand=True, padx=5)
        if comando:
            ttk.Button(marco_entrada, text="...", command=comando, width=3).pack(side="right", padx=5)

    def seleccionar_archivo(self):
        """
        Abre un diálogo para seleccionar un archivo Excel y guarda la ruta.
        """
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if archivo:
            self.ruta_excel.set(archivo)

    def seleccionar_carpeta(self):
        """
        Abre un diálogo para seleccionar una carpeta y guarda la ruta.
        """
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_guardado.set(carpeta)

    def generar_ids(self):
        """
        Verifica que todos los campos estén completos y cierra la ventana.
        """
        try:
            # Validar que todos los campos están completos
            self.ruta_excel_archivo = texto_convertir(self.ruta_excel.get())
            self.ruta_salida_ids = os.path.join(texto_convertir(self.ruta_guardado.get()), 
                                                texto_convertir(self.nombre_archivo_ids.get()) + ".ids")

            if not all([self.ruta_excel_archivo, self.ruta_salida_ids]):
                raise ValueError("Todos los campos deben estar completos.")

            self.ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar los datos:\n{str(e)}")

    def cancelar_accion(self):
        """
        Cancela la acción y cierra la ventana.
        """
        self.ventana.quit()


# .............................................................................
# FUNCIONES
# .............................................................................
def procesar_restriccion(valor):
    """
    Uso:
      Procesa los valores con patrones (e.g., /.*pattern.*/).
      Devuelve una restricción IDS válida si el valor incluye un patrón.
    Entrada:
        Valor con patron regex.
    Salida:
       Restricción IDS valida
    """
    if not valor:
        return None

    if valor.startswith("/") and valor.endswith("/"):  # Si es un patrón (entre / /)
        valor = valor[1:-1]
        return ids.ids.Restriction(base="string", options={"pattern": valor})

    # Para valores exactos, crear una restricción simple
    return ids.ids.Restriction(base="string", options={"pattern": f"^{valor}$"})

def texto_convertir(arg):
    """
    Uso:
        Convierte a texto válido el argumento si no lo era.
    Entrada:
        Argumento: Puede ser una cadena o un valor nulo.
    Salida:
        Cadena válida o una excepción si es inválido.
    """
    if not arg or not isinstance(arg, str):
        raise ValueError("El argumento no es válido o está vacío.")
    return arg.strip()

def cargar_rutas():
    """
    Abre la ventana principal de la aplicación para obtener rutas necesarias.

    Salida:
        - ruta_excel: Ruta del archivo Excel seleccionado.
        - ruta_salida_ids: Ruta de salida para el archivo IDS.
    """
    root = tk.Tk()
    app = AplicacionIDS(root)
    root.mainloop()
    return app.ruta_excel_archivo, app.ruta_salida_ids


# .............................................................................
# SCRIPT
# .............................................................................

# ------------------------------------------------------ TKINTER - FORMULARIO 1
# Se inicia la ejecucion
if __name__ == "__main__":
    try:
        # Obtener rutas desde la interfaz de seleccion
        ruta_excel, ruta_ids = cargar_rutas()

        # Gestion de errores - ver rutas
        if not ruta_excel or not ruta_ids:
            # Mostrar el error al usuario
            messagebox.showerror("Error", "No se seleccionaron rutas válidas.")
            # Lanzar la excepción para detener el flujo del programa
            raise ValueError("No se seleccionaron rutas válidas.")

# --------------------------------------------------------- PANDAS - LEER EXCEL
        # Leer las hojas del archivo Excel
        metadata_df = pd.read_excel(
          ruta_excel, sheet_name="METADATA", header=None, dtype=str)
        specifications_df = pd.read_excel(
          ruta_excel, sheet_name="SPECIFICATIONS", skiprows=1, dtype=str).fillna("")
        applicability_df = pd.read_excel(
          ruta_excel, sheet_name="APPLICABILITY", skiprows=2, dtype=str).fillna("")
        requirements_df = pd.read_excel(
          ruta_excel, sheet_name="REQUIREMENTS", skiprows=2, dtype=str).fillna("")
        # Crear diccionario de metadatos
        metadata_dict = metadata_df.set_index(0).iloc[:, 0].to_dict()

# ---------------------------------------------------- IFCTESTER - IDS METADATA
        # Crear el archivo IDS con los valores del diccionario
        archivo_ids = ids.ids.Ids(
            title=metadata_dict.get("Title", "Sin título"),
            description=metadata_dict.get("Description", ""),
            author=metadata_dict.get("Author", ""),
            milestone=metadata_dict.get("Milestone", ""),
            date=metadata_dict.get("Date (dd/mm/aaaa)", ""),
            purpose=metadata_dict.get("Purpose", ""),
            version=metadata_dict.get("Version", ""),
            copyright=metadata_dict.get("Copyright", ""),
        )

# ---------------------------------------------- IFCTESTER - IDS SPECIFICATIONS
        # Procesar las especificaciones
        for _, spec_row in specifications_df.iterrows():
            # Obtener el valor de "specification optionality" y asignar minOccurs y maxOccurs
            optionality = spec_row.get("specification optionality", "required")
            minOccurs = 0 if optionality in ['optional', 'prohibited'] else 1
            maxOccurs = "unbounded" if optionality in ['required', 'optional'] else 0

            # Crear especificación
            especificacion = ids.ids.Specification(
                name=spec_row["specification"],
                description=spec_row["description"],
                instructions=spec_row["instructions"] or None,
                identifier=spec_row["identifier"] or None,
                minOccurs=minOccurs,
                maxOccurs=maxOccurs,
                ifcVersion=spec_row["IFC version"],
            )

# ------------------------------------------------ IFCTESTER - IDS APLICABILITY
            # Procesar applicability
            df_app_spec = (
              applicability_df[applicability_df["specification"] == spec_row["specification"]].fillna(""))

            for _, row in df_app_spec.iterrows():
                # Agregar entidad
                if row["entity name"]:
                    entity = ids.ids.Entity(
                        name=row["entity name"],
                        predefinedType=row["predefined type"] or None,
                    )
                    especificacion.applicability.append(entity)

                # Agregar atributo
                if row["attribute name"]:
                    attribute = ids.ids.Attribute(
                        name=row["attribute name"],
                        value=procesar_restriccion(row["attribute value"]) or None,
                    )
                    especificacion.applicability.append(attribute)

                # Agregar propiedad
                if row["property name"]:
                    property_ = ids.ids.Property(
                        baseName=row["property name"],
                        propertySet=row["property set"] or None,
                        value=procesar_restriccion(row["property value"]) or None,
                        dataType=row["data type"] or None,
                    )
                    especificacion.applicability.append(property_)

                # Agregar clasificación
                if row["classification reference"] and row["classification system"]:
                    classification = ids.ids.Classification(
                        value=row["classification reference"],
                        system=row["classification system"],
                    )
                    especificacion.applicability.append(classification)

                # Agregar material
                if row["material name"]:
                    material = ids.ids.Material(
                        value=procesar_restriccion(row["material name"]),
                    )
                    especificacion.applicability.append(material)

                # Agregar partes
                if row["part of entity"]:
                    parts = ids.ids.PartOf(
                        name=row["part of entity"],
                        relation=row["relation"] or None,
                    )
                    especificacion.applicability.append(parts)

# ------------------------------------------------ IFCTESTER - IDS REQUIREMENTS
            # Procesar requirements
            df_req_spec = (
              requirements_df[requirements_df["specification"] == spec_row["specification"]].fillna(""))

            for _, row in df_req_spec.iterrows():
                # Agregar entidad
                if row["entity name"]:
                    entity = ids.ids.Entity(
                        name=row["entity name"],
                        predefinedType=row["predefined type"] or None,
                        instructions=row["instructions"] or None,
                    )
                    especificacion.requirements.append(entity)

                # Agregar atributo
                if row["attribute name"]:
                    attribute = ids.ids.Attribute(
                        name=row["attribute name"],
                        value=procesar_restriccion(row["attribute value"]),
                        cardinality=row["cardinality"] or "required",
                        instructions=row["instructions"] or None,
                    )
                    especificacion.requirements.append(attribute)

                # Agregar propiedad
                if row["property name"]:
                    property_ = ids.ids.Property(
                        baseName=row["property name"],
                        propertySet=row["property set"] or None,
                        value=procesar_restriccion(row["property value"]),
                        dataType=row["data type"] or None,
                        cardinality=row["cardinality"] or "required",
                        instructions=row["instructions"] or None,
                    )
                    especificacion.requirements.append(property_)

                # Agregar clasificación
                if row["classification reference"] and row["classification system"]:
                    classification = ids.ids.Classification(
                        value=row["classification reference"],
                        system=row["classification system"],
                        cardinality=row["cardinality"] or "required",
                        instructions=row["instructions"] or None,
                    )
                    especificacion.requirements.append(classification)

                # Agregar material
                if row["material name"]:
                    material = ids.ids.Material(
                        value=procesar_restriccion(row["material name"]),
                        cardinality=row["cardinality"] or "required",
                        instructions=row["instructions"] or None,
                    )
                    especificacion.requirements.append(material)

                # Agregar partes
                if row["part of entity"]:
                    parts = ids.ids.PartOf(
                        name=row["part of entity"],
                        relation=row["relation"] or None,
                        cardinality=row["cardinality"] or "required",
                        instructions=row["instructions"] or None,
                    )
                    especificacion.requirements.append(parts)

            # Agregar especificación al archivo IDS
            archivo_ids.specifications.append(especificacion)

# ---------------------------------------------------- IFCTESTER - EXPORTAR IDS
        # Guardar el archivo IDS
        archivo_ids.to_xml(ruta_ids)

# ------------------------------------------------------- TKINTER - MENSAJE INFO
        messagebox.showinfo("Éxito", f"Archivo IDS generado exitosamente en:\n{ruta_ids}")

# ------------------------------------------------------- TKINTER - MENSAJE ERROR
    except Exception as e:
        messagebox.showerror("Error", f"Error crítico:\n{str(e)}")
