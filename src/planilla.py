"""
Sistema simple de pago de planillas.

Contiene la logica de negocio: carga de trabajadores desde CSV,
calculo de sueldo bruto, descuentos y sueldo neto.
No usa base de datos ni librerias externas.
"""

import csv
from pathlib import Path

# ---------------------------------------------------------------------------
# Parametros del calculo (valores fijos para simplificar la demostracion)
# ---------------------------------------------------------------------------
HORAS_MES = 240          # horas trabajadas al mes (jornada referencial)
FACTOR_HORA_EXTRA = 1.25  # recargo del 25% sobre el valor de la hora
TASA_PENSION = 0.13       # descuento de pension (AFP/ONP)
TASA_RENTA = 0.08         # impuesto a la renta
BASE_AFECTA_RENTA = 3000  # solo se grava el exceso de este monto

RUTA_CSV = Path(__file__).resolve().parent.parent / "data" / "trabajadores.csv"


class Trabajador:
    """Representa a un trabajador de la planilla."""

    def __init__(self, id, nombre, cargo, sueldo_base, bonificacion=0.0, horas_extras=0.0):
        self.id = int(id)
        self.nombre = nombre
        self.cargo = cargo
        self.sueldo_base = float(sueldo_base)
        self.bonificacion = float(bonificacion)
        self.horas_extras = float(horas_extras)

    def __repr__(self):
        return f"Trabajador({self.id}, {self.nombre!r}, {self.cargo!r})"


# ---------------------------------------------------------------------------
# Calculos
# ---------------------------------------------------------------------------
def calcular_pago_horas_extras(sueldo_base, horas_extras):
    """Valor de la hora extra = (sueldo base / 240) * 1.25."""
    if sueldo_base <= 0 or horas_extras <= 0:
        return 0.0
    valor_hora = sueldo_base / HORAS_MES
    return round(valor_hora * FACTOR_HORA_EXTRA * horas_extras, 2)


def calcular_sueldo_bruto(trabajador):
    """Sueldo bruto = sueldo base + bonificacion + pago por horas extras."""
    extras = calcular_pago_horas_extras(trabajador.sueldo_base, trabajador.horas_extras)
    return round(trabajador.sueldo_base + trabajador.bonificacion + extras, 2)


def calcular_descuentos(sueldo_bruto):
    """Descuentos = pension (13%) + renta (8% sobre el exceso de 3000)."""
    pension = sueldo_bruto * TASA_PENSION
    exceso = max(0.0, sueldo_bruto - BASE_AFECTA_RENTA)
    renta = exceso * TASA_RENTA
    return round(pension + renta, 2)


def calcular_sueldo_neto(sueldo_bruto, descuentos):
    """Sueldo neto = sueldo bruto - descuentos."""
    return round(sueldo_bruto - descuentos, 2)


def procesar_trabajador(trabajador):
    """Devuelve un diccionario con el detalle de la boleta de un trabajador."""
    bruto = calcular_sueldo_bruto(trabajador)
    descuentos = calcular_descuentos(bruto)
    neto = calcular_sueldo_neto(bruto, descuentos)
    return {
        "id": trabajador.id,
        "nombre": trabajador.nombre,
        "cargo": trabajador.cargo,
        "sueldo_base": round(trabajador.sueldo_base, 2),
        "bonificacion": round(trabajador.bonificacion, 2),
        "horas_extras": trabajador.horas_extras,
        "sueldo_bruto": bruto,
        "descuentos": descuentos,
        "sueldo_neto": neto    }
qwfwf
wqfwqfwq
def generar_planilla(trabajadores):
    """Procesa la lista completa de trabajadores."""
    return [procesar_trabajador(t) for t in trabajadores]


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
def cargar_trabajadores(ruta=RUTA_CSV):
    """Lee el CSV y devuelve una lista de objetos Trabajador."""
    trabajadores = []
    with open(ruta, newline="", encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            trabajadores.append(
                Trabajador(
                    id=fila["id"],
                    nombre=fila["nombre"],
                    cargo=fila["cargo"],
                    sueldo_base=fila["sueldo_base"],
                    bonificacion=fila.get("bonificacion", 0) or 0,
                    horas_extras=fila.get("horas_extras", 0) or 0,
                )
            )
    return trabajadores


# ---------------------------------------------------------------------------
# Salida por consola
# ---------------------------------------------------------------------------
def mostrar_planilla(planilla):
    """Imprime la planilla en formato de tabla."""
    print("=" * 96)
    print("PLANILLA DE PAGOS".center(96))
    print("=" * 96)
    print(
        f"{'ID':<4}{'NOMBRE':<18}{'CARGO':<17}{'BASE':>10}{'BONIF.':>10}"
        f"{'H.EXT':>7}{'BRUTO':>11}{'DESCTOS':>10}{'NETO':>11}"
    )
    print("-" * 96)
    for b in planilla:
        print(
            f"{b['id']:<4}{b['nombre']:<18}{b['cargo']:<17}{b['sueldo_base']:>10,.2f}"
            f"{b['bonificacion']:>10,.2f}{b['horas_extras']:>7,.0f}{b['sueldo_bruto']:>11,.2f}"
            f"{b['descuentos']:>10,.2f}{b['sueldo_neto']:>11,.2f}"
        )
    print("-" * 96)
    total_bruto = sum(b["sueldo_bruto"] for b in planilla)
    total_desc = sum(b["descuentos"] for b in planilla)
    total_neto = sum(b["sueldo_neto"] for b in planilla)
    print(f"{'TOTALES':<56}{total_bruto:>18,.2f}{total_desc:>10,.2f}{total_neto:>11,.2f}")
    print("=" * 96)
    print(f"Trabajadores procesados: {len(planilla)}")
