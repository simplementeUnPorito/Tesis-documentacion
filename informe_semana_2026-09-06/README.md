# Informe de la semana — 2026-09-06

**[`informe.pdf`](informe.pdf)** — 9 páginas con todos los resultados de la
semana: qué funciona hoy, los números vigentes, las cinco figuras, el error de
método que más costó, y **dónde está cada cosa en el repositorio** para poder ir
a buscarla.

## Para regenerarlo

```powershell
.\compilar.ps1
```

Regenera las figuras desde los JSON crudos y compila. **No hay ningún número en
el informe que esté escrito a mano**: los de la deriva y el ruido salen a
`numeros.tex` —que genera `figuras_semana.py` y no hay que editar— y el resto
está en las figuras. Si un ensayo se rehace, se corre esto y el informe queda al
día solo.

Eso importa más de lo que parece con el registro de deriva, que sigue corriendo:
un informe que dice «3,2 h» cuando ya van 5 no está desactualizado, está
equivocado.

## Dos cosas que hacen falta saber si algo falla

**MiKTeX se cae con `cannot retrieve attributes for the directory
'...\matlab.exe\'`.** No es LaTeX: hay una entrada del PATH que apunta a un
ejecutable donde MiKTeX espera una carpeta. `compilar.ps1` la saca para su
propio proceso; el PATH del sistema no se toca.

**Va con `lualatex`, no con `pdflatex`**, porque el preámbulo usa `fontspec`. Y
por eso mismo **no lleva `inputenc` ni `fontenc`**: con ellos los caracteres de
un byte alto se remapean mal y en el PDF aparece `£` donde va `¿` y `Œ` donde va
`×`. Compila limpio y sale mal, que es la peor combinación —el log no dice nada
y sólo se ve mirando el PDF.

## Qué contiene

| sección | |
|---|---|
| Resumen | Las cuatro preguntas del apartado de tesis, con su respuesta medida |
| 1 | Estado del nodo y tabla de números vigentes |
| 2 | El hallazgo principal: el firmware se detenía 63 códigos antes del codo |
| 3 | La autocalibración, con la trayectoria y las siete correcciones |
| 4 | ¿Vale lo que cuesta? Las tres mediciones que lo sostienen |
| 5 | El ADC usa el 4,8 % de su rango, y qué se ganaría |
| 6 | Un error de método, contado porque enseña más que el resultado |
| **7** | **Dónde está cada cosa en el repositorio** |
| 8 | Lo que queda |

## Las figuras

Están en `lab/planta/figuras/` y las genera
`src/interfaces/python/figuras_semana.py`:

- `adder_curva_20260906.png` — el hallazgo principal, de una mirada
- `rescate_comparado.png` — la comprobación que separó la explicación cómoda
- `calibracion_antes_despues.png` — el nodo calibrándose solo
- `sin_calibrar_20260906_0856.png` — el argumento de la tesis
- `deriva_tendencia.png` — EXP4c
- `ruido_exp4d.png` — EXP4d
