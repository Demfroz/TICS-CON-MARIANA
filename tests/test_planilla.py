"""Pruebas unitarias de los calculos de planilla."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.planilla import (  # noqa: E402
    Trabajador,
    calcular_descuentos,
    calcular_pago_horas_extras,
    calcular_sueldo_bruto,
    calcular_sueldo_neto,
    cargar_trabajadores,
    generar_planilla,
    procesar_trabajador,
)


# --------------------------- horas extras ---------------------------
def test_pago_horas_extras():
    # 2400 / 240 = 10 por hora -> 10 * 1.25 * 8 = 100
    assert calcular_pago_horas_extras(2400, 8) == 100.0


def test_pago_horas_extras_sin_horas():
    assert calcular_pago_horas_extras(2400, 0) == 0.0


# --------------------------- sueldo bruto ---------------------------
def test_sueldo_bruto_con_bonificacion_y_extras():
    t = Trabajador(1, "Ana Torres", "Analista", 2400, 200, 8)
    # 2400 + 200 + 100 = 2700
    assert calcular_sueldo_bruto(t) == 2700.0


def test_sueldo_bruto_sin_bonificacion_ni_extras():
    t = Trabajador(2, "Carlos Perez", "Desarrollador", 3000)
    assert calcular_sueldo_bruto(t) == 3000.0


# --------------------------- descuentos -----------------------------
def test_descuentos_sin_impuesto_a_la_renta():
    # 2000 * 13% = 260 (no supera la base afecta de 3000)
    assert calcular_descuentos(2000) == 260.0


def test_descuentos_con_impuesto_a_la_renta():
    # 4000 * 13% = 520  +  (4000 - 3000) * 8% = 80  -> 600
    assert calcular_descuentos(4000) == 600.0


# --------------------------- sueldo neto ----------------------------
def test_sueldo_neto():
    assert calcular_sueldo_neto(2000, 260) == 1740.0


def test_sueldo_neto_menor_que_bruto():
    t = Trabajador(3, "Maria Lopez", "Administradora", 2800, 150, 8)
    bruto = calcular_sueldo_bruto(t)
    neto = calcular_sueldo_neto(bruto, calcular_descuentos(bruto))
    assert 0 < neto < bruto


# --------------------------- boleta completa ------------------------
def test_procesar_trabajador():
    t = Trabajador(4, "Jose Ramirez", "Tecnico", 2400, 200, 8)
    boleta = procesar_trabajador(t)
    assert boleta["sueldo_bruto"] == 2700.0
    assert boleta["descuentos"] == 351.0   # 2700*0.13 = 351
    assert boleta["sueldo_neto"] == 2349.0
    assert boleta["nombre"] == "Jose Ramirez"


# --------------------------- planilla / CSV -------------------------
def test_cargar_trabajadores_desde_csv():
    trabajadores = cargar_trabajadores()
    assert len(trabajadores) > 0
    assert all(isinstance(t, Trabajador) for t in trabajadores)
    assert trabajadores[0].sueldo_base > 0


def test_generar_planilla_completa():
    planilla = generar_planilla(cargar_trabajadores())
    assert len(planilla) == 5
    for boleta in planilla:
        assert boleta["sueldo_neto"] == round(
            boleta["sueldo_bruto"] - boleta["descuentos"], 2
        )
