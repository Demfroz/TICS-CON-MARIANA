"""Punto de entrada del sistema de planillas."""

from src.planilla import cargar_trabajadores, generar_planilla, mostrar_planilla


def main():
    trabajadores = cargar_trabajadores()
    planilla = generar_planilla(trabajadores)
    mostrar_planilla(planilla)


if __name__ == "__main__":
    main()
