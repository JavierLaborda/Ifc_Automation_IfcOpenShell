# -*- coding: utf-8 -*-
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# INFORMACIÓN SCRIPT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
__autor__ = Jose Javier Laborda / jj.laborda.lopez@gmail.com
__version__ = 1.0
__fecha__ = 2025-01-10
__cliente__ = Abierto
__doc__ = Este script valida múltiples modelos IFC contra un archivo IDS, genera
           un reporte consolidado en Excel para análisis en Power BI.

__software__ = Python 3.12
__bibliotecas__ = pandas, ifcopenshell, ifctester, openpyxl
"""

# .............................................................................
# IMPORTACIÓN DE BIBLIOTECAS
# .............................................................................
import os
import time
import pandas as pd
import ifcopenshell
import ifctester as ids
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# .............................................................................
# CLASES
# .............................................................................
class AplicacionIFCIDS:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Validación IFC-IDS")
        self.ventana.geometry("500x300")
        self.ventana.resizable(False, False)
        
        # Variables para almacenar rutas
        self.ruta_modelos = tk.StringVar()
        self.ruta_ids = tk.StringVar()
        self.ruta_reporte = tk.StringVar()
        
        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(self.ventana, text="Validación IFC-IDS", font=("Roboto", 14, "bold"), anchor="center").pack(pady=10)

        self.crear_campo("Seleccionar carpeta con modelos IFC:", self.ruta_modelos, self.seleccionar_carpeta)
        self.crear_campo("Seleccionar archivo IDS:", self.ruta_ids, self.seleccionar_archivo_ids)
        self.crear_campo("Seleccionar ruta de destino para el reporte:", self.ruta_reporte, self.seleccionar_archivo_reporte)
        
        marco_botones = ttk.Frame(self.ventana, padding=(10, 5))
        marco_botones.pack(fill="x", pady=10)
        ttk.Button(marco_botones, text="Cancelar", command=self.ventana.quit, width=12, padding=(0, 2)).pack(side="left", padx=5)
        ttk.Button(marco_botones, text="Continuar", command=self.generar_reporte, width=12, padding=(0, 2)).pack(side="right", padx=5)

    def crear_campo(self, texto_label, variable, comando):
        marco = ttk.Frame(self.ventana, padding=(10, 5))
        marco.pack(fill="x")
        ttk.Label(marco, text=texto_label, font=("Roboto", 11)).pack(anchor="w", pady=2)
        marco_entrada = ttk.Frame(marco)
        marco_entrada.pack(fill="x")
        entrada = ttk.Entry(marco_entrada, textvariable=variable, font=("Roboto", 11))
        entrada.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(marco_entrada, text="...", command=comando, width=3).pack(side="right", padx=5)
    
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_modelos.set(carpeta)
    
    def seleccionar_archivo_ids(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos IDS", "*.ids")])
        if archivo:
            self.ruta_ids.set(archivo)
    
    def seleccionar_archivo_reporte(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if archivo:
            self.ruta_reporte.set(archivo)
    
    def generar_reporte(self):
        if not all([self.ruta_modelos.get(), self.ruta_ids.get(), self.ruta_reporte.get()]):
            messagebox.showerror("Error", "Debe seleccionar todas las rutas antes de continuar.")
            return
        
        try:
            generar_reporte(self.ruta_modelos.get(), self.ruta_ids.get(), self.ruta_reporte.get())
            messagebox.showinfo("Éxito", f"El reporte se generó exitosamente en: {self.ruta_reporte.get()}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el reporte:\n{str(e)}")

# .............................................................................
# FUNCIÓN PRINCIPAL DE VALIDACIÓN IFC-IDS
# .............................................................................
def validar_modelo_ifc(ruta_ifc, archivo_ids):
    resumen = []
    detalle = []
    try:
        modelo_ifc = ifcopenshell.open(ruta_ifc)
        if not modelo_ifc:
            raise ValueError(f"No se pudo abrir el archivo IFC: {ruta_ifc}")
        archivo_ids.validate(modelo_ifc)
        
        for spec in archivo_ids.specifications:
            total_entidades = len(spec.passed_entities) + len(spec.failed_entities)
            porcentaje_cumplen = (len(spec.passed_entities) / total_entidades) * 100 if total_entidades > 0 else 0
            
            resumen.append({
                "Modelo": os.path.basename(ruta_ifc),
                "Especificación": spec.name,
                "Entidades que cumplen": len(spec.passed_entities),
                "Entidades que no cumplen": len(spec.failed_entities),
                "Total de entidades": total_entidades,
                "Porcentaje de cumplimiento": f"{porcentaje_cumplen:.2f}%"
            })
            
            for entity in spec.passed_entities:
                detalle.append({"Modelo": os.path.basename(ruta_ifc), "Especificación": spec.name, "GUID": entity.GlobalId, "Tipo de Entidad": entity.is_a(), "Cumple IDS": "Sí"})
            for entity in spec.failed_entities:
                detalle.append({"Modelo": os.path.basename(ruta_ifc), "Especificación": spec.name, "GUID": entity.GlobalId, "Tipo de Entidad": entity.is_a(), "Cumple IDS": "No"})
    except Exception as e:
        print(f"Error validando {ruta_ifc}: {e}")
    return resumen, detalle


def generar_reporte(ruta_modelos, ruta_ids, ruta_reporte):
    try:
        archivo_ids = ids.open(ruta_ids)
        resumen_total, detalle_total = [], []
        
        for archivo_ifc in os.listdir(ruta_modelos):
            if archivo_ifc.endswith(".ifc"):
                resumen, detalle = validar_modelo_ifc(os.path.join(ruta_modelos, archivo_ifc), archivo_ids)
                resumen_total.extend(resumen)
                detalle_total.extend(detalle)
        
        df_resumen = pd.DataFrame(resumen_total)
        df_detalle = pd.DataFrame(detalle_total)
        
        with pd.ExcelWriter(ruta_reporte, engine="openpyxl") as writer:
            df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
            df_detalle.to_excel(writer, sheet_name="Detalle", index=False)
        
        print(f"Reporte generado exitosamente en {ruta_reporte}")
    except Exception as e:
        print(f"Error generando el reporte: {e}")
        raise

# .............................................................................
# FUNCIONES
# .............................................................................
def validar_modelo_ifc(ruta_ifc, archivo_ids):
    """
    Valida un modelo IFC contra un archivo IDS.

    :param ruta_ifc: Ruta del archivo IFC.
    :param archivo_ids: Objeto IDS cargado.
    :return: Diccionarios con datos de resumen y detalle del modelo.
    """
    resumen = []
    detalle = []

    try:
        # Cargar el archivo IFC
        modelo_ifc = ifcopenshell.open(ruta_ifc)
        if not modelo_ifc:
            raise ValueError(f"No se pudo abrir el archivo IFC: {ruta_ifc}")

        # Validar contra el IDS
        archivo_ids.validate(modelo_ifc)

        for spec in archivo_ids.specifications:
            total_entidades = len(spec.passed_entities) + len(spec.failed_entities)
            porcentaje_cumplen = (len(spec.passed_entities) / total_entidades) * 100 if total_entidades > 0 else 0

            # Agregar al resumen
            resumen.append({
                "Modelo": os.path.basename(ruta_ifc),
                "Especificación": spec.name,
                "Entidades que cumplen": len(spec.passed_entities),
                "Entidades que no cumplen": len(spec.failed_entities),
                "Total de entidades": total_entidades,
                "Porcentaje de cumplimiento": f"{porcentaje_cumplen:.2f}%"
            })

            # Agregar al detalle
            for entity in spec.passed_entities:
                detalle.append({
                    "Modelo": os.path.basename(ruta_ifc),
                    "Especificación": spec.name,
                    "GUID": entity.GlobalId,
                    "Tipo de Entidad": entity.is_a(),
                    "Cumple IDS": "Sí",
                })

            for entity in spec.failed_entities:
                detalle.append({
                    "Modelo": os.path.basename(ruta_ifc),
                    "Especificación": spec.name,
                    "GUID": entity.GlobalId,
                    "Tipo de Entidad": entity.is_a(),
                    "Cumple IDS": "No",
                })

    except Exception as e:
        print(f"Error validando {ruta_ifc}: {e}")

    return resumen, detalle


def generar_reporte(ruta_modelos, ruta_ids, ruta_reporte):
    """
    Procesa todos los modelos en la carpeta y genera un reporte consolidado.

    :param ruta_modelos: Carpeta con los archivos IFC.
    :param ruta_ids: Ruta del archivo IDS.
    :param ruta_reporte: Ruta de salida del reporte consolidado.
    """
    try:
        # Cargar el archivo IDS
        archivo_ids = ids.open(ruta_ids)
        if not archivo_ids:
            raise ValueError("No se pudo cargar el archivo IDS.")

        resumen_total = []
        detalle_total = []

        # Validar cada modelo IFC
        for archivo_ifc in os.listdir(ruta_modelos):
            if archivo_ifc.endswith(".ifc"):
                ruta_ifc = os.path.join(ruta_modelos, archivo_ifc)

                # Registrar tiempo de validación
                inicio = time.time()
                resumen, detalle = validar_modelo_ifc(ruta_ifc, archivo_ids)
                fin = time.time()

                # Agregar tiempo al resumen
                for item in resumen:
                    item["Tiempo de validación (s)"] = round(fin - inicio, 2)

                resumen_total.extend(resumen)
                detalle_total.extend(detalle)

        # Crear DataFrames para exportar a Excel
        df_resumen = pd.DataFrame(resumen_total)
        df_detalle = pd.DataFrame(detalle_total)

        # Exportar a Excel
        with pd.ExcelWriter(ruta_reporte, engine="openpyxl") as writer:
            df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
            df_detalle.to_excel(writer, sheet_name="Detalle", index=False)

        print(f"Reporte generado exitosamente en {ruta_reporte}")

    except Exception as e:
        print(f"Error generando el reporte: {e}")

# .............................................................................
# SCRIPT PRINCIPAL
# .............................................................................
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionIFCIDS(root)
    root.mainloop()

