# Estado de la presentación (actualizado 2026-10-13, G3 corregido + G4 + G5)

## Hecho
- **G1 (slides 1–4)**: aprobado.
- **G2 (slides 5–27)**: aprobado. Incluye mapa de métodos, SPT, CPT/CPTu, ventajas/limitaciones, intro de propagación (slide 10, figura de Foti), simplificación, ecuaciones nativas (Navier, Helmholtz, Vp, Vs), Gmax, downhole, crosshole, refracción, reflexión.
- **G3 (slides 28–38)**: corregido según tu feedback (28 modelo en capas más realista · 29 superficie libre sin «caso particular» · 30 SV/SH referido al plano de la superficie libre · 31 Snell antes · 32 acoplamiento como conclusión · 33 Love condición · 34 Love · 35 Rayleigh · 36 energía · 37 atenuación · 38 cR). Dijiste que quedaba bien tras esos cambios.
- **G4 (slides 39–43)**: pendiente de visto bueno (estratificación, dispersión calculada con disba, inversión).
- **G5 (slides 44–50, SASW→MASW)**: construido, **pendiente de visto bueno**: 44 SASW · 45 límites de SASW · 46 MASW · 47 matriz U[m,n] (registro sintético ilustrativo) · 48 dimensión espacial sintetizada (Lin y Ashlock 2016) · 49 tres requerimientos de la medición · 50 cuatro condiciones de diseño.
- Slides 23–24 (refracción): imágenes reemplazadas (USGS recreada y dromocrónica de Commons, dominio público).
- Archivo vigente: `Presentacion_v7_slides_1_a_50.pptx` (ecuaciones nativas). Fuentes para reconstruir: `fuentes_deck_G1-G5_v7.zip`.
- Decisión: contenido progresivo con slides duplicadas (no animaciones). Ecuaciones solo nativas.

## Pendiente
0c. Auditoría de imágenes y lista de correcciones/faltantes: `PROMPT_CHATGPT_IMAGENES.md`. Cita de la figura de la slide 10 corregida a fig. 1.1 (cap. 1, por confirmar); cita de la slide 24 ahora dice «recreación a partir de».
0b. Imágenes recibidas para G4–G6 indexadas en `IMAGENES_RECIBIDAS.md` (con avisos de licencia y errores en la versión traducida de MASW).
0. Imágenes del SM-24 recibidas (foto y corte en español, `img/final/sm24_*.png`), para G6; origen/licencia sin especificar: pedir fuente.
1. Visto bueno de G3 → luego G4 (estratificación, dispersión, inversión), G5 (SASW→MASW, Lin & Ashlock), G6–G9 (sistema), G10 (resultados), Referencias, Anexo.
2. **Slide 30**: reemplazar la figura propia SV/SH por la mejorada con ChatGPT. Slide 23: confirmar que la figura USGS (recreada por ChatGPT) corresponde al informe 87-0103-A. La figura UW (`refr_uw_es.png`, sin licencia) quedó sin usar.
3. **Verificar en Foti** (cap. 1–2): limitaciones de refracción y reflexión; umbral de pequeña deformación (~1e-5); cita de Helmholtz; n.º de figura de crosshole y de la figura de Rayleigh (slide 10); fórmula de Viktorov para cR/Vs.
4. **Discrepancias a resolver**:
   - Reparto 67/26/7: tus apuntes citan Lamb (1904); la referencia habitual es Miller y Pursey (1955). Confirmar en Foti.
   - Atenuación de ondas de cuerpo: el resumen firmado dice 1/r; en el interior es 1/r, pero a lo largo de la superficie es 1/r² (Richart, Hall y Woods, 1970). Ajustar el resumen o matizar en la slide 33.
5. Licencias/autoría: figura SLB de Snell (slide 28) sin licencia abierta explícita; autor de «Basics of Seismic Reflection» (Commons) sin confirmar; imágenes de talud y zapata generadas con IA (slides 2–3).
6. Slide 2: usar cifra BCP verificada en `Informe_CNT_IV-2025.pdf` (6,2 % en 2025; no decir «auge» sin matices).
7. Fecha de la presentación para la portada.
8. **Tiempo**: 50 slides ya y se proyectan ~60; decidiste comprimir después convirtiendo slides en animaciones. Para 30 min (≈1,5–2 min/slide) sobra. Hay que fundir/recortar al final (p. ej. ventajas/limitaciones de downhole+crosshole, SPT/CPT, refracción/reflexión) o pasar parte al anexo.
9. Las ecuaciones nativas no se pudieron verificar visualmente en mi visor (LibreOffice muestra el texto de respaldo); revisar en PowerPoint.

## Notas técnicas
- Push a GitHub no es posible desde la sesión; los archivos se dejan en esta carpeta y se commitean localmente.
- Estilo: Arial, navy 1F4E79, azul 2E75B6, alerta C55A11, fondo blanco; títulos 24 pt, etiquetas ≥ 16 pt, cuerpo 18–20 pt, cita 12 pt.
- Humanizer aplicado a textos y notas del orador.

## v8 (correcciones de G4/G5)
- Slide 39: rigidez → Vs cambia con z; Vs creciente es común pero no siempre; ecuación nativa Gmax(z) = ρ(z)·Vs²(z). Se quitó "ejemplo: tres capas".
- Slide 40: figura nueva con desplazamiento vertical vs profundidad a 5 y 15 Hz (disba, EigenFunction), inspirada en Foti fig. 2.13 (la imagen enviada es de 378×266 px, muy chica). Se quitó la regla λ/3–λ/2 (sin confirmar).
- Slide 41: texto de dispersión según tu redacción; se quitaron las líneas de 0,93·Vs del gráfico.
- Slide 42: título nuevo (reconstruir modelo compatible con los registros).
- Slide 43: capas profundas / supuestos / no unicidad / otras mediciones (extrapolación de información localizada).
- Slide 49: tercera tarjeta = forma de onda (fase); sin amplitud. OJO: el resumen firmado sec. 3 dice "amplitud y fase": corregir.
- Slide 50: cinco condiciones (se agregó sincronización temporal; geometría separada); sin aliasing; operación de campo = infraestructura mínima, registro local, transmisión fiable. El resumen sec. 4.1 lista cuatro condiciones.

## v9
- Slide 39: se agrega "ρ suele variar poco frente a Vs". SIN VERIFICAR en Foti: no pude abrir el PDF (punteros LFS en el repo clonado, acceso a la carpeta sources denegado). Tu borrador (BORRADOR_PRELIMINAR §2) lo afirma con Kramer 1996 y Foti 2014 (ρ ≈ 1,4–2,2 t/m³), pero sin página. Falta página exacta.
- Slide 40: curvas a 15 Hz (λ≈12 m) y 9,5 Hz (λ≈25 m); a 25 m el desplazamiento de 9,5 Hz es ~2 % del máximo. «ve» solo en el título.
- Slide 49: tercera tarjeta = "Preservar la forma de la onda".
- Slide 50: "Cubrir las frecuencias de interés sin distorsiones dispares entre trazas". Se quitaron notas internas de las citas.

## v10 (G6: slides 51–63, cadena analógica)
51 arquitectura (esquema nativo) · 52 SM-24 · 53 equilibrio mecánico · 54 amortiguamiento y carga · 55 respuesta nominal (−40 dB a 1 Hz, modelo) · 56 por qué importa (4,5 Hz: 92–154 USD vs SM-24 ≈70 USD) · 57 compensación (Ma et al. 2023) · 58 AFE implementado · 59 problema del offset · 60 procedimiento VDAC/PI · 61 resultado 2,9–45,8 % → 0,4–3,9 % FS · 62 respuesta del frente (fig. 9a) · 63 cadena completa (fig. 9b: PREDICCIÓN, no medición extremo a extremo).
- Ecuaciones nativas nuevas: Gmax(z), u=xm−xg, mecánica, Vo=G0·u̇, ζ, Ha(s), Hcomp(s). Sin verificar en PowerPoint.
- Las cifras 2,9–45,8 / 0,4–3,9 % salen de latex/secciones/00_resumen.tex, NO del resumen firmado.
- Precios (SparkFun 2026, R. T. Clark 2026): tomados del resumen; sin reverificar.
- Fig. 9a/9b y foto/corte del SM-24: figuras propias o de origen por confirmar (corte).
- Ref. de ρ: Kramer (1996) provisional, sin página. Xia et al. (1999), pp. 693–694: ρ influye menos que Vs (razones de sensibilidad 1,56 / 0,64 / 0,4 / 0,13 para Vs, espesor, ρ, Vp); ρ se supone conocida (p. 694). Verificado por lectura del PDF en línea.
- Pendiente: G7 (captura digital), G8 (ESP-NOW, sincronización, HAMMER), G9 (flujo de campo), G10 (resultados), Referencias.

## v11 (G6 rehecho: slides 51–67)
51 arquitectura (imagen diseñada) · 52 SM-24 + ζ≈0,25 abierto / 0,60 con 1339 Ω + ec. ζ · 53 mecánica · 54 respuesta nominal · 55 por qué importa · 56 cuatro técnicas · 57 por qué Ma et al. · 58 compensador 1−H_BP(s) · 59 implementación (dif. + PGA, BP inversor, sumador, antialias) · 60 cinco decisiones de diseño · 61 AFE en PSoC Creator · 62 offset acumulado (nodo PGA→Σ; sin desacople DC) · 63 ilustración de recorte + 21,8 %FS · 64 modelo yi(DC) · 65 flujo de calibración (FIR 128, VDAC 16 mV, PI, EEPROM+CRC, 7–10 s) · 66 gráfico nativo 2,9–45,8 → 0,4–3,9 % · 67 ruta PGA–ADC + disclaimer sin excitador (62 y 63 viejas fusionadas).
- Ecuación nueva: E_off. 26 ecuaciones nativas, sin verificar en PowerPoint.
- ABIERTO: (a) "BP inversor menos sensible a tolerancias" sin evidencia documentada: tené datos o análisis de sensibilidad (Vicente y Enrique son coautores del DA-AFE). (b) Taxonomía de 4 técnicas (slide 56) sigue la intro de Ma, distinta de la lista que hablamos; descripciones propias. (c) "Estable / no amplifica ruido" (57) es inferencia mía a confirmar en Ma. (d) 17,52 dB de Ma es para su JF-20DX; no usado en slides, confirmar si se agrega. (e) Notación de E_off y cifras de 66 a verificar contra el paper URUCON. (f) Corte del SM-24 sin fuente. (g) Slide 63 es ilustración, no dato.

## v12 (G6 rehecho otra vez: slides 51–73)
56 cuatro familias (Pazos / cero–polo Hakimitoroghi / resistencia negativa–balance de fuerza / Ma) · 57 por qué no invertir (+40 dB a 1 Hz) · 58 por qué no lazo activo (ζ = ζ0 + G0²/(2mωn(Ri+RL))) · 59 idea de Ma (curvas del modelo, ζ1≈938) · 60 por qué Ma (estable, simple, no amplifica ruido; requiere más ganancia → se redistribuye) · 61 ecuaciones Hcomp = (…)/(…) → 1 − pasabanda → Ha·Hcomp (ζ0, ζ1, ωn; en Ma γ0, γ1, ω0) · 62 bloques + reparto de ganancia (×2, ×1–50, ×3,6, ×5 = ×1800; atenúa 2ζ1≈1876) · 63 entrada diferencial 2 operacionales · 64 BP: Sallen-Key vs inversor con f_low/f_high · 65 diferencial → sumador con Cf (≈393 Hz) · 66 antialias: polo del sumador + MFB (fa=300 Hz, ζa=0,691) = Bessel 3er orden · 67 AFE PSoC Creator · 68 offset + recorte + por qué no servo ni acople AC (62 y 63 viejas unidas en una) · 69 modelo yi(DC) · 70 algoritmo de calibración · 71 ejemplo de calibración · 72 gráfico resultados (sin p, sin test del signo) · 73 PGA–ADC con modelo nominal (sin "en la facultad", sin "razonable").
- Ecuaciones nativas: 32 (nuevas: E_hc1, E_hc2, E_tot, E_flow, E_fhigh, E_pa, E_zeta2). Sin verificar en PowerPoint.
- FIGURAS A REGENERAR EN EL REPO (marcadas en rojo en la slide): 70 (flujo de calibración, en inglés, 608×389 px) y 71 (ejemplo, eje "Time (s)"). Figura mía provisional: 59 (curvas del modelo; fig/fig_comp_curvas.py), 68 (recorte, fig/fig_recorte.py). Las imágenes 3–8 que pasaste (entrada diferencial, Sallen-Key, inversor, diferencial, sumador, MFB) están sin fuente: confirmar.
- Fuentes del repo usadas: latex-15p-review/secciones/03_acondicionamiento_digitalizacion.tex (compensador, ζ1≈938, ganancias, Bessel, MFB), latex/secciones/03b_topologias.tex (+1,51/+17,52/+21,28 dB de Ma sobre cero–polo; criterio MFB, repunte de Sallen-Key), URUCON paper (fig. 2 y fig. 4, deadband ΔPGA = 18).
- ABIERTO: (a) Pazos, Hakimitoroghi (2017) y Zhang (2025) salen de tus notas; falta año/página. (b) Imagen 3 asumida como entrada diferencial propia (×2): confirmar. (c) "Estable / no amplifica ruido" (60) es inferencia mía. (d) +40 dB a 1 Hz (57) sale del modelo (slide 54), referido a velocidad. (e) Menor sensibilidad a tolerancias del BP inversor: argumento analítico (un RC por quiebre) + observación; tené Monte Carlo listo.

## v13 (G6: slides 51–72; ajustes menores)
- 56: Pazos = capacitor en serie con la resistencia de derivación (Pazos, Alguacil y Davila 2005, BSSA 95(5):1940–1946, según la intro de Ma). El "×4" NO se pudo validar (no logré abrir el abstract): quitado.
- 59: rango 1 mHz–100 kHz (el pasabanda se ensancha y sigue siendo pasabanda); "compensador ideal"; resumen de resultados de Ma (+17,5 dB a 10 Hz verificado en el abstract de MDPI; +1,5 dB a 1 Hz y +21,3 dB a 20 Hz salen de la tesis, no los vi en el paper abierto).
- 60: agregado "más complejo que Pazos pero de complejidad razonable; control simple de hasta dónde se compensa".
- 61: sin la línea Ha·Hcomp; ecuaciones en fracción y más grandes.
- 64–66: f_low/f_high apiladas como ecuaciones; sin 393 Hz; antialias Bessel sin frecuencias ni ecuación de polos; 67 → "AFE final"; 69 con A_ij, b_i, K_i·u_i como ecuaciones.
- 71 fusiona ejemplo de calibración + gráfico de resultados (la ex-72 desaparece; PGA–ADC pasa a 72).
- Ecuaciones nativas nuevas en otras slides: 20 (Vs = Δx/Δt) y 38 (Vs ≈ cR/0,9). 35 en total.
- NO convertido: símbolos dentro de oraciones (ζ ≈ 0,25, ×1800, 2ζ1, etc.). Requiere ecuaciones en línea (OMML inline), no probado en PowerPoint.
- Zip MASW_Biblioteca_Completa_v8: corte SM-24 = Breslin (2020), crédito DESY, original sin verificar (citado en 52). Disponibles para G7–G9: Makama 2021 (Sensors 21(15):5171, red de geófonos inalámbricos), Dai 2015 (Sensors 15(10):24698, geófono sin cable de bajo costo), Kafadar 2020 MicDAC (GI 9:365–373), USGS Bronx 2007.
- Pendiente de regenerar en el repo: slide 70 (flujo en inglés), slide 71 (eje "Time (s)"), 59 y 68 (mías).

## v14 (G6 reordenado + G7 nuevo: slides 1–79)
- G6 ahora: 67 AFE final → 68 ruta PGA–ADC (resultado primero) → 69 offset/recorte (el problema) → 70 modelo yi(DC) → 71 algoritmo → 72 ejemplo + resultado.
- G7 (73–79): 73 camino digital en PSoC Creator (etiquetas en inglés, marcado) · 74 ADC ΔΣ 18 bits, 4 rangos, q=V_span/2^18 (13,8 dB = 20·log10(5/1,024), cálculo propio; el repo dice 13,7) · 75 diezmado fs′=2604/D, filtro sinc (figura propia fig/fig_sinc.py) · 76 hardware vs software + criterio · 77 SignalController (IDLE/ARMED/SAMPLING/DONE/ERROR) · 78 memoria RAM ESP32 512 lotes (5,9 s) → RAM PSoC encadenada → SD 60 000 lotes (11,5 min) · 79 metadatos e integridad.
- Ecuaciones nuevas en bloque: E_lsb, E_fsp, E_sinc, E_tlot (39 en total).
- Variante INLINE (inline_eq.py): 78 símbolos en línea como a14:m dentro de a:p (Vs, ζ0, cR, Gmax = ρ·Vs², Δφ…). Valida con validate.py pero NO probado en PowerPoint. Si falla, usar la segura.
- ABIERTO G7: (a) ENOB / ruido referido a la entrada sin medir (señalado en 74). (b) Sinc da solo −3,9 dB en Nyquist; un alias de 150 Hz con D=13 cae sobre 50 Hz atenuado ~10 dB (cálculo mío, en notas de 75): verificar rechazo por configuración. (c) EEPROM indexada por ganancia (resumen) vs ganancia y rango (repo). (d) Qué lleva a ERROR y la transición DONE→IDLE no están documentadas: no dibujadas. (e) Regla "más de 512 lotes exige SD habilitada" (repo l. 602): confirmar vigencia.
- Zip v11 (ChatGPT): nuevas = traducciones ES de ondas P/S/Love/Rayleigh (14_), fotos de campo IIT (sin fuente en los CSV), y "alternativas" 15_ que son gráficos generados (K, L, Love) o MicDAC repetido. A_electronic_compensation_geophone.png es en realidad MicDAC Fig. 1, no una figura de compensación electrónica.

## v15 (G7 rehecho: slides 73–81)
73 intro + reparto HW/SW (Δφ = 360°·f·Δt) · 74 vista del PSoC (drawio p. 18, reemplaza la captura en inglés de PSoC Creator) · 75 ΔΣ empuja el ruido fuera de banda y ΔΣ vs SAR (figura TI traducida, fuente exacta por confirmar) · 76 rangos y LSB (sin "invalida la calibración", sin pendiente) · 77 diezmado con media móvil (fs′ = 2604/D, curva genérica sin ejemplos de D) · 78 superMaquina (drawio p. 17) · 79 PRESTART: SD o arena RAM (drawio p. 11) · 80 duración máxima sin SD vs D (5,9 s·D; Nyquist 1302/D Hz) · 81 metadatos e integridad.
- Resuelto con el diagrama: ERROR = STOP o estado inválido; CLEAR_FLAGS vuelve a IDLE; START_NOW salta de IDLE a SAMPLING.
- Corregir en el repo: 04_arquitectura.tex (l. 251 y 296) dice que cambiar de rango invalida la calibración y que la EEPROM se indexa por ganancia y rango; el autor dice que es falso.
- ABIERTO: supuesto de slide 80 (el límite de 512 lotes cuenta muestras ya diezmadas); fuente TI de la figura de 75; el filtro del PSoC no es necesariamente Sinc3; nivel intermedio "RAM del PSoC encadenada" (repo) no aparece en el diagrama; ENOB sin medir (en notas de 76).
- Inline: 79 símbolos, sin probar en PowerPoint.

## v16 (G7 ajustado + G8 nuevo: slides 1–94)
- G7 (73–82): 73 "Reparto de tareas digitales entre la máquina de estados y el procesador" · 74 captura PSoC Creator (etiquetas en inglés, marcada) · 75 camino lógico (drawio p. 18) · 76 "Selección del tipo de ADC: por qué delta-sigma" · 77 rangos · 78 diezmado · 79 FSM · 80 backend (SD/RAM) · 81 duración vs D con la frecuencia efectiva fs′ bajo cada D · 82 metadatos.
- G8 (83–94): 83 topología maestro/esclavos (drawio p. 5) · 84 alternativas de sincronización (cable, Wi-Fi AP, LoRa, GPS/PPS, ESP-NOW, UWB) · 85 error de fase Δφ = 360°·f·Δt (278/139 µs; 400 µs → 7,2°/14,4°; 5° hasta ~35 Hz, cálculo propio) · 86 error de velocidad Δc/c = c·Δt/Δx (derivación propia) · 87 secuencia ARM→PRESTART→START (p. 10) · 88 broadcast vs unicast · 89 jitter 200–400 µs (3 nodos, 128 órdenes) · 90 límites de la medición · 91 reloj local y deriva (tabla ILUSTRATIVA, ε no medido) · 92 descarga en lotes (p. 12) · 93 escalabilidad (ESP-IDF v5.5) · 94 nodo HAMMER (ICP + esquema PSoC Creator).
- ABIERTO G8: (a) comparación unicast vs broadcast sin medición publicada (88, marcado). (b) Sin distribución/percentiles de jitter. (c) Reloj del ADC: ¿cristal u oscilador interno? Verificar en el proyecto del PSoC. (d) Versión de ESP-NOW usada (v1.0 250 B / v2.0 1470 B) y si el peer broadcast cuenta para el límite de 20. (e) Afirmaciones sobre Wi-Fi/LoRa/GPS en 84 son conocimiento general, sin fuente numérica. (f) El inicio efectivo del ADC (retardo de grupo fijo, común) nunca se calibró. (g) Fig. 94 izquierda es PCB (inglés, marcada). (h) 88: "cambia fiabilidad por determinismo" es argumento de diseño, no resultado medido.
- Inline: 88 símbolos, sin probar en PowerPoint.

## v17 (G9 + G10 + cierre + referencias; versión LARGA = 116 slides; versión COMPRIMIDA = 29 slides)
- G9 (95–105): flujo completo · interfaz web · sesión de campo (carriles) · geometría 21 posiciones (fig mía) · cotas Δx y L (fig mía, c = 150 m/s) · receptor móvil vs MASW simultáneo · captura real · alineación y promedio (fig. 16) · registro espacio–tiempo (fig. 17b) · error de posición (inferencia: δc/c ≈ δ(Δx)/Δx) · servidor.
- G10 (106–116): SNR aparente (método) · resultados 0,5/2,1/16,7/24,4 dB (265 impactos, 15 distancias) · causas y pruebas propuestas · tabla de evidencia · trabajo futuro · UWB · riesgo watchdog START_NOW (solo en tesis, no en resumen) · conclusiones · preguntas · referencias (incompletas, ver CLAUDE_CODE_GOAL.md).
- Discrepancias detectadas: jitter 100–200 µs (15p-review) vs 200–400 µs (resumen firmado); Comina λmáx > 60 m vs Foti 2018 L ≳ λmáx; 18,9/4,9 dB por distancia (tesis) vs bandas del resumen; fs = 2929 Hz en la figura de repetibilidad vs 2604 SPS.
- Versión COMPRIMIDA: 29 slides generadas por comp_build.js (proxy que redibuja cada slide larga como panel), animaciones de entrada/salida por clic y transición fade (comp_anim.py). Probada solo en LibreOffice por pasos y con validate.py; no probada en PowerPoint.
- Entrega a Claude Code: tesis_toolkit_*.zip + CLAUDE_CODE_GOAL.md (brief completo con pendientes, reglas y protocolo).

## v18 (compresión rehecha: motor v2 con objetos persistentes)
- Rechazo del autor a la v17 comprimida: copias de la misma imagen que aparecían, desaparecían y reaparecían; transiciones "simples y bobas".
- Motor v2 (`comp2_build.js`, `anim2.py`, `choreo.json`): una sola copia de cada imagen; las imágenes principales se achican a una riel lateral (máx. 3) y vuelven a crecer; salen textos, entran otros con zoom/wipe/fade; viñetas por párrafo en el mismo clic; la primera escena se arma sola al entrar a la slide. 29 slides (26 animadas, 113 escenas, 1 portada + 2 copias).
- Cambios de spec: se eliminaron los pares lado a lado (3: 6+7, 5: 13+14, 6: 19+20) porque a media columna la letra bajaba a ~7 pt y se desbordaba; ahora son escenas sucesivas con la imagen anterior en la riel.
- Probado: `validate.py` OK, render por escena en LibreOffice (revisión de layout). NO probado: movimiento, escala acumulada y build por párrafo en PowerPoint. Ver supuestos en CLAUDE_CODE_GOAL.md.
- Rail: las miniaturas miden como máximo 1,35 × 0,9 in; son ilegibles a propósito (solo memoria visual). Si el autor las quiere más grandes, cambiar `RAIL_*` en comp2_build.js.

## v19 (arreglo del aviso "PowerPoint found a problem with content" en v18)
- Causa probable: ids de forma duplicados dentro de la misma slide (pptxgenjs asigna id de tabla = n*slide+1 y el marcador de número de slide colisionaba con otros objetos). El timing apunta por spid, así que las animaciones por párrafo (txEl/pRg) podían caer en la forma equivocada (índice de párrafo fuera de rango). validate.py (XSD) no detecta esto.
- Arreglo: `normalize_ids()` en anim2.py renumera todos los ids de forma única (Choice/Fallback de mc:AlternateContent comparten id) antes de generar el timing. Nuevo `check_anim.py`: ids únicos, spid existentes, párrafos en rango, bldP coherente, sin efectos mixtos, cTn únicos. Falló en v18 y pasa en v19.
- Archivos: v19 completa (párrafos + primera escena automática), v19 INLINE, v19 SIMPLE (`PARA=0 AUTO=0`: sin párrafos ni arranque automático, solo entradas/salidas/movimiento). Si v19 completa vuelve a pedir reparar, probar SIMPLE; si SIMPLE también falla, el sospechoso es animMotion/animScale.

## v20 (motor v3: instancias, un movimiento por objeto, zoom de matriz; solo INLINE)
- Pedido del autor: animaciones al doble de rápido; slide 3 empieza con la matriz 2×2, zoom a SPT/CPT-CPTu (imagen 1, imagen 2, luego solo cambia el texto, rótulos estáticos), zoom out y misma lógica para downhole/crosshole; tras refracción/reflexión, zoom out y zoom in a «métodos no invasivos basados en ondas»; en la riel quedan las imágenes de cada tema.
- Bugs corregidos (por diseño, sin poder probar en PowerPoint): SPT y downhole saliendo de escena; SV/SH detrás del texto «P se acoplan SV» (slide 8); dos imágenes de la riel detrás del AFE final (slide 15); caja de t_max desbordada y D limitado a 10 (slide 18, también en la larga); texto naranja sobre la tabla (slide 19).
- Motor: `comp3_build.js`, `anim3.py`, `group.py`, `check_anim.py`. Regla: un solo movimiento por objeto; copias idénticas para nuevos movimientos; riel de 4 casillas fijas.
- Entregados solo INLINE (comprimida v20, larga v18). Variantes seguras ya no se generan: si PowerPoint falla, regenerar con `PARA=0`.
- No probado en PowerPoint: zoom por `ppt_x/y/w/h` en grupos, build por párrafo, el supuesto de un movimiento por objeto.

## v21 (matriz con imágenes en las celdas, miniatura fija, riel del AFE, ecuaciones de la slide 15)
- Matriz 2×2: al terminar cada sección el texto de la celda se reemplaza por sus imágenes (SPT + CPT/CPTu en slide 3; downhole + crosshole en slide 6; refracción + reflexión en slide 7). Las imágenes se achican a la celda (un solo movimiento) y desde la slide siguiente la matriz ya trae las imágenes dentro del grupo (`p:pic` dentro de `p:grpSp`; `group.py` los envuelve). En la celda de ondas de superficie las imágenes ocupan el 36 % superior y el texto queda abajo (13 pt). Ya no se usa el riel en esas secciones.
- Slide 5: la imagen de excitación (slide larga 10, Foti fig. 1.1 por confirmar) queda fija en la casilla 0 del riel desde el primer instante y no se desaloja (`"pin"` en `comp_spec.json`). Crítica: la figura muestra ondas Rayleigh, no P y S; como miniatura de "excitación" sirve, pero conviene que el orador lo diga.
- Slide 15 (comprimida): el riel solo guarda los esquemas propios: entrada instrumental con 2 operacionales, inversor −Zf/Zin, sumador y pasabajas MFB. Se excluyen Sallen-Key y el diferencial de Ma et al. (`"railSkip"`).
- Ecuaciones f_low y f_high (slide larga 64): ahora lado a lado (2,35 × 0,85 in, 20 pt). Antes apiladas en cajas de 0,55 in: el numerador y denominador de la fracción rebasaban la caja y se solapaban. En LibreOffice se ve el texto de respaldo, que envuelve; la fracción OMML real hay que revisarla en PowerPoint.
- Las matrices se dibujan primero (z-order) para que las imágenes que llegan a las celdas queden encima.
- No probado en PowerPoint: imágenes dentro de un grupo que hace zoom, y la fidelidad de las fracciones OMML.
- Idea no implementada (para Claude Code): transición Morph entre slides para continuidad real de la matriz y del riel; hoy cada slide reinicia sus objetos. No probado y puede chocar con las animaciones.
