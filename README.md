# Sistema de Planillas — Actividad de CI/CD con GitHub Actions

Proyecto en Python **sin base de datos** que calcula la planilla de pagos de una lista de
trabajadores y muestra el resultado por consola. Su objetivo es demostrar un pipeline de
CI/CD con tres etapas: **BUILD → TEST → DEPLOY**.

## Estructura

```text
sistema-planillas/
├── .github/workflows/ci-cd.yml   # Pipeline BUILD -> TEST -> DEPLOY
├── src/planilla.py               # Logica de negocio (calculos)
├── tests/test_planilla.py        # Pruebas unitarias con pytest
├── data/trabajadores.csv         # Lista de trabajadores
├── main.py                       # Punto de entrada
├── requirements.txt
├── .gitignore
└── README.md
```

## Datos que se registran

ID, Nombre, Cargo, Sueldo base, Bonificacion y Horas extras (archivo `data/trabajadores.csv`).

## Formulas usadas

| Concepto | Formula |
|---|---|
| Valor hora | `sueldo_base / 240` |
| Pago horas extras | `valor_hora * 1.25 * horas_extras` |
| **Sueldo bruto** | `sueldo_base + bonificacion + pago_horas_extras` |
| Pension (AFP/ONP) | `sueldo_bruto * 13%` |
| Impuesto a la renta | `8%` sobre el exceso de `S/ 3,000` |
| **Descuentos** | `pension + impuesto_renta` |
| **Sueldo neto** | `sueldo_bruto - descuentos` |

## Ejecutar localmente

```bash
pip install -r requirements.txt
python main.py        # muestra la planilla por consola
pytest -v             # ejecuta las pruebas unitarias
python -m compileall .  # valida que todo compile
```

## Pipeline CI/CD

| Etapa | Que hace |
|---|---|
| **BUILD** | Instala dependencias y valida la compilacion con `python -m compileall .` |
| **TEST** | Ejecuta las pruebas unitarias con `pytest` (solo si BUILD paso) |
| **DEPLOY** | Copia el proyecto a `staging/`, lo ejecuta e imprime `Despliegue exitoso` (solo si BUILD y TEST pasaron) |

El encadenamiento se logra con `needs:` en el archivo `ci-cd.yml`: si BUILD o TEST fallan,
DEPLOY nunca se ejecuta.

## Agregar un trabajador

Basta con agregar una fila a `data/trabajadores.csv`:

```csv
6,Pedro Diaz,Asistente,1800,80,12
```
"# TICS-CON-MARIANA" 
