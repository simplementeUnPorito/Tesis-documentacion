> **OBSOLETO (2026-10-13, mañana).** Ver `ESTADO_v24.md`. Este documento tiene datos superados o incorrectos y se conserva solo como historial.

# Pendientes de verificación antes de la defensa

Lista de afirmaciones que necesitan confirmación contra las fuentes, organizadas por slide y estado de verificación.

Entrega: v22 (2026-10-13)  
Comprimida: 29 slides  
Larga: 116 slides

---

## Sección 1: Métodos de caracterización (slides larga 2–27, comprimida 1–4)

### ✓ Verificados
- SPT, CPT/CPTu: descripción estándar (normas ASTM, ISO)
- Downhole, crosshole: descripción estándar
- Refracción y reflexión: conceptos de física de ondas

### ⚠ Por confirmar
- **Slide larga 10**: Figura de excitación es Foti Fig. 1.1 (PDF: *Surface Wave Methods for Near-Surface Site Characterization*, capítulo y página exacta). **Estado**: pendiente de verificar en el PDF de Foti.
- **Slide larga 23**: Foto USGS de refracción es del informe 87-0103-A. **Estado**: pendiente de verificar en el repositorio.
- **Slide larga 24**: Dromocrónica de Wikimedia Commons. **Estado**: verificado dominio público.

---

## Sección 2: Teoría de ondas (slides larga 28–38, comprimida sin equivalente)

### ✓ Verificados
- Ecuación de Helmholtz: estándar en sísmica
- Vs desde Gmax: G = ρ·Vs² es estándar (Richart, Hall y Woods 1970)
- Atenuación de ondas de cuerpo: 1/r en el interior, 1/r² en superficie

### ⚠ Por confirmar
- **Slide larga 28**: Figura de Snell (SLB) — licencia abierta no explícita
- **Slide larga 33, 37, 38**: Números de figuras de Foti (crosshole, Rayleigh, atenuación). **Estado**: sin confirmar en PDF.
- **Slide larga 38**: Fórmula de Viktorov para cR/Vs (cR ≈ 0,9·Vs). **Estado**: sin fuente exacta.
- **Reparto 67/26/7 % (slide larga 36)**: Fuente propuesta Lamb (1904) vs referencia estándar Miller y Pursey (1955). **Estado**: sin confirmar en Foti.

---

## Sección 3: Estratificación e inversión (slides larga 39–43, comprimida 9)

### ⚠ Por confirmar
- **Slide larga 39**: "ρ suele variar poco frente a Vs". Fuentes: Kramer (1996), Foti (2014), Xia et al. (1999). **Estado**: página exacta de Kramer sin confirmar.
- **Slide larga 40**: Curvas de desplazamiento a 5 y 15 Hz (disba, EigenFunction). Inspirada en Foti Fig. 2.13. **Estado**: imagen de 378×266 px, muy chica; regenerar si es necesario.
- **Slide larga 41**: Texto de dispersión según redacción del autor (verificado contra "ζ=83,661" del historial técnico que contradice lo escrito).
- **Slide larga 43**: Supuestos de no unicidad de la inversión. **Estado**: inferencia propia del autor, no de fuente.

---

## Sección 4: SASW y MASW (slides larga 44–50, comprimida 10)

### ⚠ Por confirmar
- **Slide larga 48**: Geometría "dimensión espacial sintetizada" de Lin y Ashlock (2016, Soil Dynamics & Earthquake Engineering 87:82–92). **Estado**: verificar número de página exacto.
- **Slide larga 49**: Tercera tarjeta "Preservar la forma de la onda vs amplitud". Resumen firmado sec. 3 dice "amplitud y fase", no solo forma. **Estado**: necesario aclarar si incluir amplitud o no.
- **Slide larga 50**: Cinco condiciones de medición. Resumen sec. 4.1 lista cuatro. **Estado**: se añadió sincronización temporal; confirmar si el resumen se actualiza.

---

## Sección 5: Geófono SM-24 y compensación (slides larga 51–67, comprimida 11–15)

### ✓ Verificados
- Ma et al. (2023), Sensors 23(6):3082. +17,5 dB a 10 Hz verificado en abstract de MDPI.
- Pazos, Alguacil y Davila (2005), BSSA 95(5):1940–1946 (capacitor en serie).
- Precios SparkFun 2026, R. T. Clark 2026 (tomados del resumen sin reverificar).

### ⚠ Por confirmar
- **Slide larga 56**: Referencias completas a Pazos, Hakimitoroghi (2017), Zhang (2025). **Estado**: año y página pendientes.
- **Slide larga 57**: "BP inversor menos sensible a tolerancias". **Estado**: argumento analítico sin análisis de sensibilidad/Monte Carlo documentado.
- **Slide larga 57**: "Estable / no amplifica ruido" para Ma. **Estado**: inferencia propia del autor; confirmar contra el abstract.
- **Slide larga 62–63**: Entrada diferencial con 2 operacionales (imagen 3). **Estado**: asumida como entrada propia ×2, confirmar.
- **Slide larga 66**: Gráfico de resultados 2,9–45,8 % → 0,4–3,9 % FS. **Estado**: números verificados contra papel URUCON (confirmar notación E_off).
- **Slide larga 67**: Corte del SM-24. **Estado**: licencia/autoría sin especificar (Breslin 2020, DESY); confirmar original.

---

## Sección 6: Cadena digital (slides larga 68–82, comprimida 16–17)

### ✓ Verificados
- ADC delta-sigma 18 bits: q = V_span / 2^18 (13,8 dB = 20·log₁₀(5/1,024)).
- PSoC 5LP, ESP32 v5.5: especificaciones.

### ⚠ Por confirmar
- **Slide larga 74**: Figura delta-sigma de Texas Instruments. **Estado**: documento exacto y licencia sin confirmar.
- **Slide larga 74**: ENOB y ruido referido a la entrada. **Estado**: sin medir.
- **Slide larga 75**: Rechazo de alias de 150 Hz sobre 50 Hz con D=13 (~10 dB). **Estado**: cálculo propio del autor, sin verificar.
- **Slide larga 78**: Límite de 512 lotes de RAM del ESP32. **Estado**: ¿cuenta muestras ya diezmadas? Confirmar en firmware.
- **Slide larga 78**: Nivel intermedio "RAM del PSoC encadenada". **Estado**: aparece en repo, no en drawio; clarificar arquitectura.
- **Slide larga 80**: Máximo D=10 (5,9 s·D, Nyquist 1302/D Hz). **Estado**: ¿es el máximo razonable? Nota para el tutor.

---

## Sección 7: Sincronización y ESP-NOW (slides larga 83–94, comprimida 18–20)

### ✓ Verificados
- Jitter 200–400 µs (3 nodos, 128 órdenes START) medido en el repo.

### ⚠ Por confirmar
- **Slide larga 85**: Error de fase Δφ = 360°·f·Δt; cálculo propio (278/139 µs para 400 µs → 7,2°/14,4°; 5° hasta ~35 Hz). **Estado**: verificación cruzada con estándar de sincronización sísmica.
- **Slide larga 86**: Error de velocidad Δc/c = c·Δt/Δx. **Estado**: derivación propia del autor.
- **Slide larga 88**: Broadcast vs unicast. **Estado**: cambio fiabilidad por determinismo es argumento de diseño, no medición.
- **Slide larga 89**: Jitter 200–400 µs sin distribución/percentiles. **Estado**: faltan estadísticos.
- **Slide larga 91**: Tabla de deriva de reloj (ILUSTRATIVA, ε = 10 y 50 ppm). **Estado**: ε no medido; reloj ADC ¿cristal u oscilador?
- **Slide larga 84**: Afirmaciones sobre Wi-Fi, LoRa, GPS. **Estado**: conocimiento general sin cifras publicadas.
- **Slide larga 94**: Figura PCB en inglés, marcada. **Estado**: regenerar en español.

---

## Sección 8: Captura y operación (slides larga 95–105, comprimida 21–23)

### ⚠ Por confirmar
- **Slide larga 99**: Sugerencia de campo cercano con offset mínimo 10 m. **Estado**: inferencia propia del autor.
- **Slide larga 104**: Error de posición δc/c ≈ δ(Δx)/Δx. **Estado**: derivación propia a partir de c = 2πf·Δx/Δφ.
- **Slide larga 101–103**: Geometría sintética de 21 posiciones (Δx=2 m, offset 10 m, apertura 40 m). **Estado**: validada en campo IIT, leer memoria [[Geometría de las campañas]].

---

## Sección 9: Resultados y evidencia (slides larga 106–112, comprimida 24–25)

### ✓ Verificados
- SNR aparente: método documentado en el código.
- Tabla de evidencia: nivel de confirmación de cada afirmación.

### ⚠ Por confirmar
- **Slide larga 106–108**: SNR 0,5 / 2,1 / 16,7 / 24,4 dB (265 impactos, 15 distancias). **Estado**: muestreo validado contra 607 candidatos y 598 procesados del repo.
- **Slide larga 112**: Riesgo de watchdog START_NOW tras captura + 2,5 s (tesis, no resumen). **Estado**: verificar vigencia en firmware actual.

---

## Sección 10: Futuro y riesgos (slides larga 113–116, comprimida 26–29)

### ✓ Verificados
- UWB como alternativa de sincronización (conocimiento general).
- Conclusiones alineadas con los hallazgos.

### ⚠ Por confirmar
- **Referencias incompletas** (slides 115–116, comprimida): 
  - Pazos 2005, Hakimitoroghi 2017, Zhang 2025
  - URUCON (paper DA-AFE)
  - Texas Instruments (documento delta-sigma)
  - Wood y Cox 2012, Comina 2011, Socco y Strobbia 2004, Xia 1999
  - Foti et al. (2018), Bull. Earthquake Eng. 16(6) — confirmar criterio L ≳ 1,5·λmáx
  - Korsimaa et al. (2025) HardwareX 24:e00713
  - Xue et al. (2021) Measurement 183:109760
  - Pérez-Solano et al. (2022) Comput. Commun. 186:80–89 (UWB)
  - Espressif ESP-IDF v5.5 official docs

---

## Multimedia

### Imágenes generadas con IA (requieren aclaración de autoría/licencia)
- **Slide larga 2–3**: Talud y zapata (generadas con ChatGPT).
- **Slide larga 23**: Refracción USGS (recreada con ChatGPT a partir de 87-0103-A).

### Imágenes propias (scripts en `fig/`)
- **Slide larga 40**: Desplazamiento vs profundidad (disba, EigenFunction).
- **Slide larga 59, 68**: Curvas y recorte (fig_comp_curvas.py, fig_recorte.py).
- **Slide larga 98, 99**: Geometría y cuna (fig_geometria.py, fig_cuna.py).
- **Slide larga 70, 71**: Flujo de calibración en inglés, eje "Time (s)" en inglés. **Estado**: regenerar en español.

### Figuras externas sin fuente confirmada
- **Slide larga 74, 94**: Imágenes del repo con etiquetas en inglés.
- **Slide larga 81, 78**: Mías pero sin regeneración reciente.

---

## Criterios de cierre (para que la presentación esté "lista")

1. ✓ Existe una versión comprimida (29 slides) y una larga (116 slides)
2. ✓ Ambas en INLINE (símbolos en línea como OMML)
3. ✓ Tamaño < 30 MiB (29 MiB y 28 MiB)
4. ⚠ **Falta**: Verificación visual en PowerPoint de todos los clics, layout y animaciones
5. ⚠ **Falta**: Validación de cada afirmación en las fuentes (en este archivo, con checkmarks)
6. ⚠ **Falta**: Humanizador aplicado al texto completo
7. ⚠ **Falta**: Regeneración de figuras en español (slides 70, 71, 74, 94)
8. ⚠ **Falta**: Confirmación de fecha de presentación y nombres en portada

---

## Notas para la defensa

- **Tribunal**: Fernando Brunetti (WSN, sincronización, jitter), Vicente González Ayala (física de ondas, límites de apertura), Enrique Vargas Cabral (AFE, ruido, calibración).
- **Preguntas probables**: 
  - Brunetti: ¿por qué ESP-NOW broadcast? Jitter real, deriva de relojes, escalabilidad.
  - Vicente: ¿señal o ruido bajo 10 Hz? Límites de apertura, incertidumbre de inversión.
  - Enrique: Ruido del AFE, estabilidad del compensador, nivel de evidencia (modelo/simulación/medición/caracterización/extremo a extremo).
- **Respuestas**: Ver notas del orador en slides larga 54–60, 85–93, 106–112 (revisar coherencia tras compresión).

---

**Última actualización**: 2026-10-13, Claude Code  
**Versión**: v22  
**Estado**: preparada para defensa pendiente de verificación en PowerPoint y confirmación de fuentes
