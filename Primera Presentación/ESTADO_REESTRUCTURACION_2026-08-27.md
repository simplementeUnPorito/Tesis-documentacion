# Estado de la reestructuración de la Primera Presentación

**Fecha:** 2026-08-27
**Para qué sirve este archivo:** retomar el trabajo en una sesión nueva sin releer toda la conversación anterior. Contiene qué se hizo, qué se decidió, qué quedó abierto y cómo reconstruir el PDF.

---

## 1. Qué se hizo

Se reescribió por completo `BORRADOR_PRELIMINAR_15_PAGINAS.md` y se generó a partir de él una versión LaTeX compilable en `latex-reestructurado/`.

El borrador anterior no seguía la estructura que pide el tutor y tenía prosa cortada. Ahora el documento reproduce **exactamente las doce secciones** de la *Estructura revisada recomendada* de `Revision_estructura_trabajo_caracterizacion_suelos_v2.pdf`, en su orden, sin agregar secciones fuera de esa lista.

Estado del PDF: **20 páginas, compila con cero errores, cero overfull, ninguna imagen faltante.** El límite reglamentario es 15.

---

## 2. Archivos

| Ruta | Rol |
|---|---|
| `BORRADOR_PRELIMINAR_15_PAGINAS.md` | **Fuente de verdad del contenido.** Todo cambio de texto se hace acá primero. |
| `latex-reestructurado/main.tex` | Preámbulo, portada y `\graphicspath`. |
| `latex-reestructurado/secciones/01_contexto.tex` | Secciones 1 a 7 |
| `latex-reestructurado/secciones/02_requerimientos.tex` | Sección 8 |
| `latex-reestructurado/secciones/03_diseno.tex` | Sección 9 |
| `latex-reestructurado/secciones/04_validacion.tex` | Secciones 10, 11 y 12 |
| `latex-reestructurado/referencias.bib` | Copia del `.bib` de `latex-15p-review` + `LinAshlock2016` y `Barbier1976` |
| `CONOCIMIENTO_REESTRUCTURACION_PRIMERA_PRESENTACION.md` | Base de conocimiento previa. Sigue vigente salvo lo corregido en §5 de este archivo. |

**No tocar `latex-15p-review/`**: es el entregable anterior y sigue siendo la referencia del estado previo.

### Reconstruir el PDF

```bash
cd "docs/Primera Presentación/latex-reestructurado"
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

---

## 3. Cómo está marcado el documento

En el markdown, cada bloque modificado lleva un marcador al inicio:

- **`[C01]`–`[C25]`** — cambios de contenido. Tabla completa en el **Anexo E** del borrador.
- **`[R01]`–`[R19]`** — recortes de compresión. Tabla en el mismo Anexo E.

Los marcadores **no** pasan al LaTeX; el conversor los elimina.

---

## 4. Decisiones ya cerradas (no reabrir)

1. **Sin resumen.** La estructura del tutor no lo incluye y el documento abre directamente en §1.
2. **Sin sección de Conclusiones.** La estructura del tutor termina en §12; el cierre argumental está en §11.4.
3. **Contribución:** instrumento validado end-to-end. Es de instrumentación: integración y evaluación con datos reales de la cadena completa hasta un perfil `Vs(z)` preliminar.
4. **Registro de escritura:** el de `Primera_Presentación_Federico_Morán.pdf`. Impersonal con «se», «proyecto de fin de grado» (nunca «Proyecto Final de Carrera»), bloque Alumno/Matrícula/Carrera/Tutor en la portada.
5. **Foco:** es un PFC de Ingeniería Electrónica. La geofísica es el contexto que define requerimientos. Declarado explícitamente en §1.
6. **Datos de portada:** Alumno Elías David Álvarez Martínez, Matrícula **Y24127**, Carrera Ingeniería Electrónica, Tutor **Enrique A. Vargas Cabral, Ph.D.**
7. **ζ₁ = 938** es el valor de diseño de la rama pasabanda del compensador. El valor 83,661 que aparece en material anterior **no** es el correcto.
8. **Composición del tribunal.** En esta Facultad el tutor también evalúa, acompañado por otros dos profesores. El tribunal es entonces Enrique A. Vargas Cabral (tutor y evaluador), Fernando Brunetti y Vicente González. No es una inconsistencia.

---

## 5. Hallazgos que corrigen la base de conocimiento previa

### 5.1 La cadena analógica SÍ está caracterizada bajo 10 Hz

**Esto invalida lo que decían el borrador anterior y parte de la base de conocimiento.**

La carpeta correcta es **`resultados_tanda_calibrada`**, no `resultados_verificacion_calibracion_2026-07-21`.

| | corrida parcial (la que se citaba mal) | tanda calibrada (correcta) |
|---|---:|---:|
| Puntos PGA→ADC | 30 | **61** |
| Banda | 11,58 Hz – 863 Hz | **0,21 Hz – 1,11 kHz** |
| Error de magnitud | 0,416 dB | **0,200 dB** |
| Error de fase | 1,88° | **1,16°** |
| Coherencia | 0,9938 | **0,9946** |

Ruta: `src/calculos_modelados/matlab/AnalisisCircuito/resultados_tanda_calibrada/05_tablas_reportes/resumen_identificacion.csv`

La campaña de osciloscopio `data/raw/Osciloscopio_verificacion_calibracion_2026-07-21/` incluye bandas desde **10 mHz**.

**Consecuencia argumental, que es el mejor resultado del documento:** como el acondicionamiento preserva magnitud y fase por debajo de 10 Hz, la ausencia de señal útil en 1–10 Hz **no puede atribuirse a la electrónica**; queda en la fuente, el geófono o la propagación. Está en §11.1.

Cautelas que igual hay que mantener: la dinámica subsónica del compensador no es observable pese a haber puntos bajo 1 Hz; el compensador conserva desajuste en torno a 10 Hz (mejoró de 26,7 a 10,7 dB); la fila BP tiene error alto (6,485 dB) porque mezcla campañas históricas incompatibles, no porque el circuito empeore.

### 5.2 Sí existe un ensayo de sincronización multinodo

Se probó en laboratorio con **tres nodos simultáneos**: uno de clase HAMMER y dos de clase GEO, sobre los módulos de radio, sin PSoC asociado. Demuestra que la coordinación escala más allá de dos nodos, pero **no** aporta cifra de precisión.

§10.2 distingue ahora **cuatro** magnitudes: alineación de golpes en un nodo (1,46 ms) / coordinación multinodo funcional / sincronización medida entre placas (pendiente) / verificación con osciloscopio (no preservada).

### 5.3 Correcciones bibliográficas sobre fuentes repetitivas

- **SIST (Park et al. 1996)** fue desarrollado para reflexión de alta frecuencia y su secuencia **atenúa deliberadamente** las frecuencias inferiores a la tasa inicial de impacto. No se puede citar como antecedente de ganancia en baja frecuencia.
- **Mini-Sosie original (Barbier et al. 1976)** no usaba cadencia fija: variaba la velocidad del motor para obtener una secuencia aproximadamente aleatoria y registraba el instante real de cada golpe.
- **45 rpm** da una fundamental de 0,75 Hz y sólo doce líneas dentro de 1–10 Hz, la primera a 1,50 Hz. No excita 1,0 Hz.
- **Presupuesto de jitter:** el factor de coherencia decae como `exp[-½(2πf·σt)²]`, así que menos de 5 % de pérdida exige `σt ≲ 0,051/f`: 5,1 ms a 10 Hz y 1,02 ms a 50 Hz. El valor medido de 1,46 ms es holgado abajo (0,4 %) y marginal arriba (10 %).

---

## 6. Figuras y tablas

**17 figuras y 4 tablas.** Todas las imágenes salen de `latex-historial/figuras/`, `latex-15p-review/figuras/`, `Urucom_2026_compact/imagenes/` y `Propuesta Urucom/Imagenes/`, resueltas por `\graphicspath`.

Las que más sostienen el argumento: `respuesta_sm24_modelo` (§9.2, velocidad vs aceleración), `extension_banda` (§9.3, efecto de subir ζ₁), `sincronizacion_fase` (§8, tolerancia de 130 µs), `mosaico_normalizados` (§10.1, las cinco transferencias), `contenido_baja_frecuencia` (§11.2, reemplaza la tabla de SNR).

**Descartadas a propósito** por declararse históricas o no vigentes en sus propias leyendas: `geofono_vs_cadena_medida`, `masw_estado_actual`.

**Figuras 1 y 2 rehechas** a pedido del autor (marcadores `[C24]` y `[C25]`):
- **Figura 1 (§6)** ahora es un **diagrama TikZ** dibujado dentro del documento, no una imagen. Se descartó `fundamentos_dispersion.png` por llevar título y tipografía propios, fondos grises y datos ilustrativos.
- **Figura 2 (§7)** ahora es la **Tabla 1**, comparación de métodos. Se descartó `comparacion_metodos.png`: era contenido tabular montado como imagen.

---

## 7. Qué queda abierto

### Bloqueante para entregar

1. **20 páginas contra un límite de 15** (Art. 19 del Reglamento, incluida bibliografía). El autor decidió no recortar más por su cuenta y **dejar que el tutor elija qué sale**. Menú preparado:

| Opción | Ahorro | Qué se pierde |
|---|---:|---|
| A | ~0,6 pág | Mover el bloque de fuente repetitiva de §12 a diapositivas auxiliares |
| B | ~0,3 pág | Sacar la tabla de barrido de subarreglos a material auxiliar |
| C | ~0,3 pág | Reducir §9.3 de 5 ecuaciones a 3 |
| D | ~0,3 pág | Podar §2 y §3 al mínimo |
| E | ~2–3 pág | Reducir el número de figuras (hoy 17) |

### No bloqueante

2. **Verificar la cita de Ma et al. (2023)** antes de dar por buena la entrada del `.bib`.
3. **Verificar contra fuente primaria** las referencias que aportó el informe externo: Barbier 1976, Chen et al. 2017, Yang et al. 2020 y 2021, Lin et al. 2024. Sólo Barbier se cita en el cuerpo.
4. **Verificar el criterio `L ≥ 1,5·λmax`** contra Foti2018 (marcado en §8 con un comentario LaTeX).
5. **Fotografías del hardware:** no se localizaron fotos físicas de las placas; lo que hay son esquemáticos. Si aparecen, una lámina de la evolución placa universal → placa por transferencia → PCB fabricada reforzaría §9.

---

## 8. Cómo trabajar sobre esto

1. **Editar siempre el markdown primero.** Es la fuente de verdad.
2. **Regenerar el LaTeX** desde el markdown. La conversión la hizo `codex exec -s workspace-write` con reglas estrictas de fidelidad literal; el resultado fue bueno y se puede repetir.
3. **Delegar lo pesado y mecánico** (conversiones masivas, auditorías de longitud y redundancia, barridos de consistencia) a codex o a un subagente. Verificar siempre su salida: en la auditoría de longitud, codex propuso recortar justo lo que el autor había pedido expandir, porque no conocía esas instrucciones.
4. **Reglas de escritura que el autor exige:** declarar toda variable al presentarla, nada de meta-comentarios sobre las propias cautelas, no plantear hombres de paja, y profundidad proporcional a la importancia (la cadena analógica y el compensador son el núcleo).
5. **No editar `.cyprj/.cydwr/.cysch/.cyfit`** ni variantes históricas de LaTeX por accidente.

---

## 9. El PPTX sigue pendiente

No se empezó. Debe contener la exposición principal (~30 min) y un banco amplio de diapositivas auxiliares, porque las preguntas son posteriores y no hay demostración en vivo. El Anexo B del borrador tiene el reparto de páginas de los dos `.drawio` entre PDF, presentación principal y auxiliares.
