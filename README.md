# Weighted Interval Scheduling — ADA Proyecto 2

Comparación de Programación Dinámica vs. Greedy para el problema de selección de intervalos con pesos.

**Integrantes:**
- Diego López (23242)
- Diego Rosales (23258)

---

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Demo + tests automáticos

```bash
python main.py
```

### Solo tests

```bash
python -m pytest tests/ -v
```

### Benchmark completo

```bash
python benchmark/runner.py
python benchmark/analysis.py
```

Los resultados quedan en la carpeta `results/`.

---

## Estructura

```
src/          → modelos y algoritmos (DP, Greedy)
benchmark/    → medición de operaciones y gráficas
tests/        → 14 pruebas automáticas
results/      → CSV, gráficas y reporte (generado)
main.py       → punto de entrada
```

## Algoritmos implementados

| Algoritmo | Complejidad | Óptimo |
|-----------|-------------|--------|
| DP        | O(n log n)  | Sí     |
| Greedy EDF | O(n log n) | No     |
| Greedy HVF | O(n²)     | No     |
| Greedy RATIO | O(n²)   | No     |
