> **OBSOLETO (2026-10-13, mañana).** Ver `ESTADO_v24.md`. Este documento tiene datos superados o incorrectos y se conserva solo como historial.

# Resumen de entrega v22 — Presentación de la primera defensa de tesis

**Fecha**: 2026-10-13  
**Solicitante**: Elías David Álvarez  
**Objetivo**: Presentación lista para defender en 30 minutos (diciembre de 2026)

---

## 📋 Archivos entregados

### Versiones principales
1. **`Presentacion_v22_COMPRIMIDA_INLINE_29_slides.pptx`** (29 MiB)
   - 29 slides + portada
   - Motor v3 (instancias, un movimiento por objeto, zoom de matriz)
   - 26 slides animadas con ~119 pasos totales
   - Tiempo estimado: 15 s/paso = 30 min

2. **`Presentacion_v22_LARGA_INLINE_116_slides.pptx`** (28 MiB)
   - 116 slides (respaldo completo)
   - Motor v1 (slides lineales)
   - Cobertura total: G1–G10, cierre y referencias

### Documentación
3. **`ESTADO.md`** (actualizado)
   - Historial completo v1–v22
   - Cambios, correcciones y decisiones en cada versión
   - Supuestos no verificados en PowerPoint

4. **`PENDIENTES_DEFENSA.md`** (nuevo)
   - 50+ afirmaciones factual requieren confirmación
   - Organizadas por slide y estado (✓ verificado, ⚠ por confirmar)
   - Referencias completas a Foti, Ma et al., Pazos, etc.
   - Criterios de cierre y notas para la defensa

### Recursos
5. **`toolkit/`** (descomprimido, no borrado)
   - Código fuente: g1mod.js – g10mod.js, comp3_build.js, anim3.py, etc.
   - Imágenes: img/final/ (78 imágenes optimizadas)
   - Scripts: fig/ (figuras propias en matplotlib)

---

## ✅ Cumplido

- [x] Versión comprimida 20–50 slides (entregado: 29)
- [x] Versión larga respaldo (entregado: 116)
- [x] Ambas en INLINE (símbolos de ecuaciones en línea como OMML)
- [x] Tamaño < 30 MiB (29 y 28 MiB después de `shrink.py` + `dedupe.py`)
- [x] Archivos PPTX válidos (verificado ZIP)
- [x] Todas las imágenes incluidas (img/final/)
- [x] Ecuaciones nativas inyectadas (49 en larga, ~50 en comprimida)
- [x] Portada, motivación, métodos, teoría, sistema, resultados, referencias
- [x] Notas del orador en cada slide

---

## ⚠️ Pendiente de verificación en PowerPoint

**CRÍTICO: No se ha probado en PowerPoint.** Se validó con:
- ZIP structure (OK)
- XSD schema vía `validate.py` (pendiente)
- Render en LibreOffice por slide (parcial en v18–v21)

Necesita abrir en PowerPoint y verificar:

### Comprimida (v22): 26 slides animadas
- **Slides 3, 6, 7, 8**: Zooms de matriz 2×2 (imágenes dentro de grupo)
- **Slide 15**: Riel con esquemas propios (sin Sallen-Key, sin Ma et al.)
- **Slide 18**: Caja de t_max, D ≤ 10
- **Slide 19**: Texto naranja sobre tabla
- Todos los clics: objetos no detrás de otros, sin superposiciones

### Larga (v22): 116 slides
- Todas las fracciones OMML nativas (especialmente slides 15, 64, 67–69, etc.)
- Ecuaciones en línea sin desborde (ζ, Δφ, ×1800, etc.)
- Z-order correcto (matriz primero, imágenes encima)
- Text boxes no desbordados

### Ambas
- Abrir sin reparación ("PowerPoint found a problem and recovered...")
- Todas las imágenes cargan (sin referencia rota)
- Especificaciones de CLAUDE_CODE_GOAL.md, sección 3.4

---

## 📚 Verificación de fuentes

Se creó **`PENDIENTES_DEFENSA.md`** con 50+ puntos de verificación:

### ✓ Verificados
- Ma et al. (2023): +17,5 dB a 10 Hz en abstract
- Pazos, Alguacil y Davila (2005): capacitor en serie
- Xia et al. (1999): sensibilidad de ρ vs Vs
- Estándar IEEE/ISO para SPT, CPT, downhole

### ⚠ Por confirmar
- Foti (2014): figura y capítulos exactos (limitaciones de refracción/reflexión, cross-hole, Rayleigh)
- Hakimitoroghi (2017), Zhang (2025): año y página (solo referencias de notas)
- Texas Instruments: documento exacto del delta-sigma (slide larga 75)
- Comina (2011) vs Foti (2018): criterio de apertura L ≳ λmáx vs 1,5·λmáx
- Deriva de reloj ADC: ¿cristal u oscilador interno?
- Figures SLB (Snell), drawio: licencias
- Fotos de campo IIT: fuente en CSV

---

## 🎯 Criterios de aceptación (para el usuario)

Antes de llevar a defensa:

1. [ ] Abrir en PowerPoint — debe abrir sin reparación
2. [ ] Recorrer todas las slides (29 comprimida / 116 larga) — sin errores de render
3. [ ] Recorrer todos los clics de la comprimida (~119 pasos) — objetos correctos
4. [ ] Revisar PENDIENTES_DEFENSA.md — confirmar o retirar afirmaciones
5. [ ] Regenerar figuras en español si es necesario (slides larga 70, 71, 74, 94)
6. [ ] Humanizador: revisar que el texto lea natural en español
7. [ ] Fecha de presentación y nombres en portada
8. [ ] Ensayo con el tutor y tribunal

---

## 🔧 Si PowerPoint reporta error

Si PowerPoint pide reparar:

1. **Primero**: Intentar `PARA=0` (sin párrafos automáticos). En comp3_build.js, cambiar `const PARA = 1` a `PARA = 0` y regenerar.
2. **Si falla aún**: El sospechoso es `animMotion` o `animScale` en `anim3.py`. Revisar la regla de un movimiento por objeto.
3. **Fallback**: Usar la versión larga (motor v1, sin animaciones complejas) directamente para la defensa.

---

## 🚀 Próximos pasos

1. Abrir ambas versiones en PowerPoint (usuario)
2. Completar verificación de fuentes (PENDIENTES_DEFENSA.md)
3. Humanizador aplicado al texto si es necesario
4. Regeneración de figuras en español
5. Ensayo completo de 30 min
6. Commit en GitHub (usuario, no Claude Code)

---

## 📝 Notas técnicas

- **Motor v3** (comprimida): instancias, un movimiento/objeto, riel de 4 slots, matriz 2×2 con zoom.
- **Motor v1** (larga): slides lineales sin animaciones complejas.
- **INLINE**: símbolos de ecuaciones en línea dentro de párrafos (OMML a:run). Si falla, cambiar a SIMPLE (PARA=0, AUTO=0).
- **Shrink + dedupe**: ~100s por archivo, reduce tamaño quitando medios duplicados.
- **Toolkit**: Node v24.19.0, Python 3.14.5, pptxgenjs v4.x.

---

## ⚖️ Tribunal

- Fernando Brunetti: WSN, sincronización, ESP-NOW, latencia, jitter, deriva, escalabilidad
- Vicente González Ayala: física de ondas, G = ρVs², dispersión, límites de apertura
- Enrique A. Vargas Cabral: AFE, geófono SM-24, ruido, rango dinámico, offset, ADC

**Preguntas probables**: Ver PENDIENTES_DEFENSA.md, sección "Notas para la defensa".

---

**Estado final**: ✅ Archivo listo, ⚠️ PowerPoint pendiente, ⚠️ Fuentes pendiente

Entregado por Claude Code (Claude Haiku 4.5), 2026-10-13
