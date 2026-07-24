# Revisión del paper URUCOM — Notas para reunión con el tutor
**Fecha:** 2026-07-23
**Paper:** *Automatic DC-Offset Calibration for a Geophone Front End*
**Restricción dura:** 5 páginas incluyendo referencias, A4. No hay páginas extra (ni en submission inicial ni final). Hoy el PDF está en **5 páginas exactas**.

---

## 1. Qué se arregló hoy (ya está en el `.tex`, compila en 5 páginas)

| # | Cambio | Dónde |
|---|--------|-------|
| 1 | **Bug de compilación:** se imprimía `` ```latex `` al final de la Sección III (marca de Markdown pegada). Eliminado. | `04_experimental_validation.tex` |
| 2 | Frase de ganancias reescrita (estaba forzada, mezclaba `2·Gain_PGA` con `K_i`). Ahora ata los `\|K_i\|` a la Tabla I y explica `K_PGA=1`. | `03_...tex` |
| 3 | "three-pair Board B ×4 diagnostic in Table II" → reformulado como **experimento externo** (no está en la Tabla II) y con **números reales** (LP 2.98→0.84 %FS, N=3). | `05_discussion.tex` |
| 4 | Conclusión generalizada: de "LP-output offset" a **"residual DC offsets across the conditioning stages — most consequentially at the LP output"**. | `06_conclusion.tex` |
| 5 | **Orden de referencias IEEE corregido** (aparición ascendente): [14]/[15] y [16]/[17]/[18] estaban desordenadas. | `references/references.tex` |
| 6 | **12 DOIs agregados** (los 10 artículos + conferencia [12] + libro [2]). Datasheets/app-notes/brochure/manual quedan sin DOI (correcto). | `references/references.tex` |
| 7 | Calificador **"shared"** en todas las comparaciones (incluido caption de Tabla II) para no exagerar la magnitud de la mejora. | varios |
| 8 | **Test estadístico (nuevo):** sign test pareado una cola en §IV-C → LP menor en 10/10 restarts en las 8 celdas, **p≈10⁻³**. | `04_...tex` |

**Auditoría de citas:** 18 citas, 18 referencias, **cero huérfanas**, cero errores de formato tras el reordenamiento.

---

## 2. Veredicto del panel de revisión simulado (5 revisores)

**Decisión: Minor Revision** para congreso (nivel URUCOM). Subiría a **Major Revision** si fuera a una revista completa. **No hay problemas CRÍTICOS.** Puntaje ponderado ≈ 65/100.

**Fortalezas reconocidas:** encuadre honesto y bien acotado, escritura limpia, sistema real funcionando + demo de campo, reuso ingenioso de recursos del PSoC (sin hardware extra).

---

## 3. Lo que FALTA — para discutir con el tutor

### 3.A. Cabe en 5 páginas (texto/análisis, sin experimentos nuevos)

| Ítem | Qué es | Estado | Costo |
|------|--------|--------|-------|
| **P3 — Piso de residuo teórico** | Derivar el residuo mínimo esperado del LP = paso del DAC (16 mV ≈ 0.32 %FS) + ancho de banda muerta, y compararlo con los 0.4–3.9 %FS medidos. Es la petición de consenso de 2 revisores. | **PENDIENTE** (no lo metí: requiere derivación cuidadosa; meter un número mal es peor. **Hacerla con el tutor.**) | ~2–3 frases |
| **P7 — Nota de banda** | Aclarar que el límite de coherencia (~0.84 kHz) de la Fig. 2 está **por encima** de la banda de ondas superficiales de interés (<100 Hz), o sea que la limitación de medición no afecta la aplicación. | Opcional | ~1 frase |

> **Nota sobre P3 (para no equivocarnos):** la banda muerta `Δ_i` está en *códigos DAC equivalentes* (mapeados desde el ADC, Ec. 2). Para el LP: `Δ_LP = 8` códigos y `\|K_LP\|=6`. Hay que decidir con cuidado cómo se traduce eso a %FS en el nodo medido antes de escribir el número. El paso del DAC solo (16 mV / 5000 mV) ya da un piso de **0.32 %FS**, consistente con que los mejores LP calibrados rondan 0.4–0.7 %FS. **Confirmar la derivación completa juntos.**

### 3.B. Requiere experimentos nuevos (esto es lo de "revista", NO cabe en 5 pág.)

| Ítem | Por qué lo piden | Esfuerzo |
|------|------------------|----------|
| **Más placas** | N=10 son *reinicios de la misma placa*, solo 2 placas → no se puede separar variación entre dispositivos de la intra-dispositivo. Es la limitación de validez externa #1. | Semanas |
| **Orden de medición contrabalanceado** | Hoy el baseline se mide **siempre primero** y el calibrado segundo → el drift de calentamiento se confunde con el efecto de calibración (validez interna). Bastaría medir la mitad de los restarts en orden invertido (B/A) para acotar el drift. | Días |
| **Caracterización de ruido / deriva térmica de los códigos congelados** | Un paper de *calibración* que no mide si el punto recentrado **se mantiene** (temperatura, ruido, resolución DAC) deja abierta la pregunta central. | Días–semanas |

---

## 4. El golpe fuerte del "Devil's Advocate" (discutir sí o sí)

**Argumento:** las reducciones espectaculares del LP (p. ej. 45.8→3.2 %FS en A×1) son **en parte** artefacto de un baseline deliberadamente desfavorable. El `c_base` se eligió en **Board B a ×50** y se aplicó *sin cambios* a todas las placas y ganancias → a A×1 está garantizado que esté mal ajustado. O sea, la mejora mezcla dos efectos: (i) la calibración funcionando, y (ii) el baseline compartido siendo un mal punto fijo.

**Por qué NO es fatal:** el paper es transparente en que ese "shared fixed reference" **es** el modo real sin-calibración, y el diseño pareado dentro de cada celda igual muestra una caída real (ahora respaldada por el sign test p≈10⁻³).

**Mitigación ya aplicada:** se mantiene el calificador **"shared"** en todas las comparaciones para no dar a entender que la magnitud es solo mérito de la calibración.

**Para pensar con el tutor:** ¿vale la pena una frase que contraste explícitamente contra la alternativa realista (*un trim manual único por placa*), aunque sea cualitativa? Reforzaría la motivación de "no escala" de la introducción. (Cuesta ~1 frase, entra si sacamos algo.)

---

## 5. Distinción clave para la charla

- **Para URUCOM (congreso, 5 pág.):** el paper está **listo/casi listo**. Los ítems 3.A son mejoras finas opcionales; los 3.B **no aplican** (no hay espacio ni tiempo).
- **Si después se quiere mandar a revista:** ahí sí hay que hacer 3.B (más placas, orden contrabalanceado, ruido/térmica, tests inferenciales por celda más completos) → sería Major Revision.

---

## 6. Checklist rápido antes de mandar (de `URUCON_REQUIREMENTS.md`)

- [ ] ≤ 5 páginas incluyendo referencias — **OK (5)**
- [x] Tamaño A4 (no US Letter) — **OK** (`\documentclass[conference,a4paper]{IEEEtran}`)
- [ ] Todos los autores en la primera página — OK
- [ ] PDF abre bien con todas las figuras/tablas/ecuaciones/referencias — OK
- [ ] Afirmaciones de máximo/mínimo/típico/repetible/convergente respaldadas por evidencia — revisar con el nuevo sign test agregado
- [ ] Las limitaciones del discussion concuerdan con el alcance experimental — OK (muy cuidado)

---

*Generado como apoyo a la revisión. Los cambios del punto 1 ya están commit-eables; los del punto 3 quedan a criterio tuyo y del tutor.*
