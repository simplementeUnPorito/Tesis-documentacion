# Plan de la Primera Presentación (30 min) — esqueleto aprobado

Estado: esqueleto 2 aprobado por Elías el 2026-10-12. Se construye por grupos de slides altamente acoplados; no se avanza al siguiente grupo sin visto bueno.

## 1. Reglas de trabajo acordadas

- Fuente narrativa: `docs/Primera Presentación/Resumen_1ra_fimado.pdf` (15 págs., VoBo 29/09/2026). Toda cifra sale de ese resumen o de una fuente citada; nada del apéndice del v10 se reutiliza sin verificar.
- Objetivo: primera defensa; foco en estado del arte, ideas generales y resultados parciales (la final es en diciembre 2026).
- Duración: 30 min; meta 28:30 (1:30 de margen). La skill academic-pptx recomienda como máximo ~1 slide/min; este esqueleto va a ~46 s por slide, así que las slides teóricas deben ser livianas (una figura y una frase).
- Estilo (skill academic-pptx): fondo blanco, una sola tipografía (Arial), navy 1F4E79 / azul 2E75B6 / alerta C55A11, títulos de acción, un exhibit por slide, ≤ 40 palabras de cuerpo, cuerpo ≥ 20 pt, cita en cada figura prestada, slide de Referencias, la última slide principal son las conclusiones.
- Texto y notas del orador: pasar siempre la skill `humanizer` antes de construir.
- Figuras en inglés: se redibujan en español (con atribución "Adaptada de ...").
- Herramienta: PPTX con pptxgenjs (no Canva); el .pptx se puede importar a Canva al final.
- Fotos: Wikimedia Commons (CC0 / PD / CC BY / CC BY-SA) con atribución en la slide. Las "fotos" del v10 en `PPT/placeholder_images` NO sirven: `spt.jpg` es una flor, `foundation.jpg` es el zócalo de un edificio, `landslide.jpg` es una caída de rocas en blanco y negro. `cpt_truck.jpg` sirve pero tiene marca comercial y licencia desconocida.

## 2. Esqueleto (37 slides)

| # | Título de acción | Exhibit / fuente | Dur. | Acum. |
|---|---|---|---|---|
| **A. Necesidad** | | | | |
| 1 | Portada | Título, autor, tutor, carrera | 0:30 | 0:30 |
| 2 | Toda obra parte de conocer el suelo que la sostiene | Foto de fundación; Samtani & Nowatzki 2006; dato BCP de construcción | 0:50 | 1:20 |
| 3 | El control del terreno no termina cuando la obra se levanta | Fotos: grietas/asentamientos, rutas/rellenos, taludes; Park et al. 2018 | 0:50 | 2:10 |
| 4 | Se necesita un método que mida y, con procesamiento analógico y digital, extraiga información útil del terreno | Diagrama medir → acondicionar → digitalizar → procesar → información; hoja de ruta. No menciona ondas superficiales | 0:40 | 2:50 |
| **B. Métodos** | | | | |
| 5 | Dos familias: medir resistencia a la penetración o medir propagación de ondas | `fig_mapa_metodos_es.png` | 0:40 | 3:30 |
| 6 | SPT y CPT son estándar de diseño, pero intervienen el terreno y son puntuales | Fotos SPT y CPT; ventajas y límites; Samtani & Nowatzki 2006 | 0:50 | 4:20 |
| 7 | Ondas de cuerpo: el terreno transmite compresión (P) y corte (S) | `fig_ondas_ps_es.png`; Vp, Vs | 0:50 | 5:10 |
| 8 | Vs conecta la propagación con la rigidez: Gmax = ρVs² | Ecuación y caso de pequeñas deformaciones; Foti et al. 2014; Kramer 1996 | 0:50 | 6:00 |
| 9 | Downhole y crosshole miden Vs directo, a costa de pozos | `fig_crosshole_es.png` | 0:40 | 6:40 |
| 10 | Refracción y reflexión evitan pozos, pero exigen configuraciones específicas para Vs | `fig_refraccion_es.png` (verificar en Foti cap. 1) | 0:40 | 7:20 |
| **C. Ondas desde la superficie** | | | | |
| 11 | Una interfaz refleja, transmite y convierte ondas; SH queda desacoplada | `fig02_conversion_interfaz_es.png` (revisar nitidez); Snell | 0:50 | 8:10 |
| 12 | Love: movimiento SH horizontal que requiere capas y una fuente horizontal | Esquema de movimiento de partícula | 0:40 | 8:50 |
| 13 | Rayleigh: acoplamiento P–SV con movimiento elíptico en el plano vertical | Esquema de movimiento elíptico | 0:40 | 9:30 |
| 14 | Rayleigh es la más atractiva: concentra la energía y decae como 1/√r | Barras 67/26/7 (Miller & Pursey 1955; semiespacio ideal, ν = 0.25) | 0:50 | 10:20 |
| 15 | En suelo homogéneo cR ≈ 0.9 Vs, sin depender de f | cR vs ν; Viktorov | 0:40 | 11:00 |
| **D. Estratificación, dispersión, inversión** | | | | |
| 16 | Con capas, cada longitud de onda "ve" una profundidad distinta | Foti et al. 2014 Fig. 3 redibujada; λ = c/f | 0:50 | 11:50 |
| 17 | La curva cR(f) codifica la estructura vertical | `dispersion_profundidad.png` | 0:40 | 12:30 |
| 18 | Invertir da Vs(z), pero la solución no es única | Modelo directo / problema inverso | 0:50 | 13:20 |
| **E. MASW** | | | | |
| 19 | MASW agrega a SASW la redundancia espacial | Comparación SASW / MASW; Park et al. 1998, 1999 | 0:50 | 14:10 |
| 20 | Un receptor y excitaciones sucesivas sintetizan el arreglo | Lin & Ashlock 2016; U[m,n] = uz(xm, tn) | 0:50 | 15:00 |
| 21 | MASW impone siete requisitos a la electrónica (una página) | Banda y fase; rango dinámico; antialias y fs; geometría; referencia temporal; excitación; operación de campo | 0:40 | 15:40 |
| **F. Sistema** | | | | |
| 22 | GEO mide el suelo, HAMMER la excitación, MASTER coordina | `d_arquitectura_nodos.png`; sólo los tres roles | 0:40 | 16:20 |
| 23 | Bajo su resonancia el SM-24 pierde ~40 dB a 1 Hz | Hv(s), `fig07_respuesta_sm24_modelo.png` | 0:50 | 17:10 |
| 24 | Ganancia directa y carga pasiva son simples, pero extienden poco | Tabla/diagrama; Pazos | 0:40 | 17:50 |
| 25 | Invertir la dinámica extiende la banda a costa de ruido y offset | Zero-pole; alta ganancia LF/DC | 0:40 | 18:30 |
| 26 | Force balance extiende la banda con un lazo activo y más complejidad | I_coil → F_Lorentz | 0:40 | 19:10 |
| 27 | Ma et al. atenúa la resonancia y recupera ganancia, sin levantar el fondo | Hcomp ≈ 1 − Hbp; matiz: también necesita mucha ganancia y amplifica offsets | 0:55 | 20:05 |
| 28 | El AFE implementado: PGA, directo + BP, SUM, LP, ADC | `fig08_f_frente_analogico_crop.png` | 0:40 | 20:45 |
| 29 | La respuesta medida del AFE sigue al modelo (es predicción, no calibración mecánica) | `fig12_f_cadena_geo_adc_magcoh.png` | 0:55 | 21:40 |
| 30 | La calibración de offset baja el residuo de 2.9–45.8 % a 0.4–3.9 % FS | Flujo CALIBRAR → CONGELAR → MEDIR; paper URUCOM (8 configuraciones, un controlador) | 1:10 | 22:50 |
| 31 | Disparada la captura, el tiempo crítico queda en hardware local | TopDesign PSoC 5LP; ADC ΔΣ 18 bit, ~2604 Sa/s, DMA | 0:40 | 23:30 |
| 32 | MASTER coordina por ESP-NOW; la red no transporta muestras | `secuencia_start_multinodo.png`; ARM/PRESTART/START; sync GPIO ~200–400 µs; Δφ = 360° f Δt (≈3° @ 20 Hz, ≈7° @ 50 Hz con 400 µs) | 1:00 | 24:30 |
| 33 | HAMMER mide cada impacto para alinear y rechazar capturas | `fig14_acondicionamiento_martillo_psoc.png`; PCB 086D20 | 0:40 | 25:10 |
| 34 | El flujo de campo cierra el lazo | `d_flujo_operativo` + interfaz web | 0:40 | 25:50 |
| **G. Resultados** | | | | |
| 35 | Bajo 10 Hz la SNR aparente es de apenas 0.5–2 dB | Medianas: 1–5 Hz 0.5 dB; 5–10 Hz 2.1 dB; 10–20 Hz 16.7 dB; 20–50 Hz 24.4 dB (265 impactos, 15 distancias). No atribuir sólo al sensor | 0:40 | 26:30 |
| 36 | Se obtuvo el registro espacio-tiempo de 21 posiciones | `fig19_waterfall_4s_v2.png`; 10–50 m, Δx = 2 m, alineado con HAMMER | 1:00 | 27:30 |
| 37 | Conclusiones: lo demostrado y lo que falta para diciembre | Dos columnas (demostrado / pendiente) | 1:00 | 28:30 |

Después: slide de Referencias y apéndice (ecuaciones del DA-AFE, Helmholtz y Snell, Viktorov, aliasing, cuantización q_ADC ≈ 19.1 µV y q_DAC = 16 mV, deriva de reloj fs(1+ε), cálculo de SNR aparente).

Recortes de menor costo si no se llega a tiempo: fusionar 24–26; fusionar 12 y 13; fusionar 17 y 18; fusionar 33 y 34.

## 3. Grupos de construcción (visto bueno por grupo)

| Grupo | Slides | Contenido |
|---|---|---|
| G1 | 1–4 | Necesidad |
| G2 | 5–10 | Métodos: resistencia, ondas de cuerpo, Vs y Gmax, downhole/crosshole, refracción/reflexión |
| G3 | 11–15 | Ondas desde la superficie: interfaz, Love, Rayleigh, por qué Rayleigh, homogéneo |
| G4 | 16–18 | Estratificación, dispersión, inversión |
| G5 | 19–21 | SASW/MASW, prototipo sintetizado, requisitos |
| G6 | 22–23 | Arquitectura general y SM-24 |
| G7 | 24–29 | Estrategias de extensión LF, Ma et al., AFE, modelo vs medición |
| G8 | 30–31 | DA-AFE y captura digital |
| G9 | 32–34 | MASTER, HAMMER, flujo de campo |
| G10 | 35–37 + refs + apéndice | Resultados, conclusiones, referencias |

## 4. Decisiones de contenido tomadas

- Familias de métodos: "resistencia a la penetración" vs "propagación de ondas" (no "directo/indirecto": era inconsistente, downhole se llamaba indirecto pero daba Vs "bastante directo").
- Slide 4 no define ondas superficiales: sólo plantea la necesidad de un método de medición con procesamiento analógico y digital.
- Ondas de cuerpo primero (slides 7–8), luego downhole/crosshole (9), luego desde la superficie.
- Rayleigh gana por energía (67 % en el caso ideal) y por su relación con Vs.
- Decaimiento: ondas de cuerpo ~1/r, superficiales ~1/√r (campo lejano ideal), como en el resumen firmado.
- Love no existe en un semiespacio homogéneo (requiere estratificación); una fuente vertical no es la configuración natural para generarlas.
- Orden obligatorio del sistema: arquitectura general (sólo tres roles) → GEO completo → MASTER → HAMMER. Que la red no transporta muestras se explica recién en MASTER.
- La extensión SM-24 + AFE en baja frecuencia es una predicción en cascada con el modelo nominal, no una calibración mecánica extremo a extremo.
- La sincronización observada (~200–400 µs entre flancos GPIO) es preliminar y no equivale a sincronización ADC–ADC.

## 5. Temas abiertos / a verificar

1. Slide 2, "auge" en Paraguay: los datos respaldan "sector en expansión desde 2024", no "auge" sin matices. BCP vía La Nación (28/03/2026): construcción +6,2 % en 2025 (4T 2025: +4,3 %). Contexto no verificado contra BCP: −3,2 % en 2022, −7,1 % en 2023, +5,9 % en 2024 (MEF/La Nación). En 2025 creció menos que el PIB (6,6 %). CAPACO (27/04/2026) proyecta +3,5 % para 2026 y reporta menor ejecución de obra pública. Citar la versión más reciente y abrir el PDF original del BCP (`Informe_CNT_IV-2025.pdf`) para copiar página y cifra.
2. Atribución del 67/26/7: las notas de Obsidian lo atribuyen a Lamb (1904); lo clásico es Miller & Pursey (1955), zapata circular, ν = 0.25. Citar y acotar en la slide 14.
3. Decaimiento de ondas de cuerpo: el resumen dice r⁻¹; las notas de Obsidian dicen r⁻² en superficie en una nota y r⁻³ en otra. Se usa r⁻¹ vs r⁻¹ᐟ² como en el resumen firmado.
4. Fecha de la presentación (portada).
5. Verificar en Foti cap. 1 las limitaciones de refracción/reflexión (slide 10), la redacción de la taxonomía (slide 5) y el número de figura de crosshole (los PDF del repo son punteros Git LFS).
6. Atribución de fuentes de figuras: autor original de refracción, ondas P/S y conversión en interfaz no determinable; no se inventa atribución.
7. Discrepancia del v10: el apéndice daba LSB ≈ 15.6 µV (±2.048 V) y SM-24 ~$80; el resumen firmado da q_ADC ≈ 19.1 µV (5 V / 2^18) y SM-24 ~70 USD. Prevalece el resumen firmado.

## 6. Recursos

- Resumen firmado: `docs/Primera Presentación/Resumen_1ra_fimado.pdf`
- Figuras de la versión 15 págs.: `docs/Primera Presentación/latex-15p-profesor/figuras/`
- Placeholders y figuras del v10: `docs/Primera Presentación/PPT/placeholder_images/`
- Handoff previo: `docs/Primera Presentación/PPT/PRESENTACION_HANDOFF.md`
- Paper URUCOM (DA-AFE): `docs/Urucom_2026/`
- Figuras redibujadas en español: `PPT/plan_30min/figuras/`

## 7. Cómo continuar

1. Abrir una sesión nueva de Claude en el proyecto "Tesis" y pedir: "Seguimos la presentación de la primera defensa; leé `PPT/plan_30min/PLAN_PRESENTACION_30MIN.md` y `PPT/plan_30min/ESTADO.md`".
2. El siguiente paso está en `ESTADO.md`.
3. Skills a usar: `anthropic-skills:academic-pptx`, `anthropic-skills:pptx`, `anthropic-skills:humanizer`.
