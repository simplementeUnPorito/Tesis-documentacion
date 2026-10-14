> **Superado por `ESTADO_v26.md`** (2026-10-13, 14:00); se conserva por el detalle de las verificaciones.

# Estado v25 (2026-10-13, mañana): entrega vigente

**Usar estos archivos:**
- `Presentacion_v25_COMPRIMIDA_INLINE_29_slides.pptx` (28,7 MiB): 29 slides, 94 clics. (Última regeneración: 13:46.)
- `Presentacion_v25_LARGA_INLINE_117_slides.pptx` (27,7 MiB): 117 slides. Ahora son 117 porque las referencias pasaron a tres slides; con dos se desbordaban.
- `Presentacion_v24_ANEXO_VIDEOS_ondas_4_slides.pptx` (14,9 MiB): animaciones de P, S, Rayleigh y Love; sin cambios.
- `figuras_es_v25/`: las figuras nuevas en español, con sus fuentes y scripts.
- `toolkit/tesis_toolkit_codigo_v25.zip` y `toolkit/tesis_toolkit_imagenes_v25_nuevas.zip`: para regenerar todo.
- `04_arquitectura_CORREGIDO.tex`: el capítulo con la corrección ya aplicada (ver más abajo).

Todo lo anterior (v22, v23, v24 y sus documentos) queda superado; no se borró nada.

## Validación
- `validate.py` PASA en las dos. `check_anim.py`: 26 slides animadas, 0 problemas.
- Las dos **abren en PowerPoint** sin pedido de reparación (verificado sobre los archivos entregados).
- **Larga:** las 117 slides exportadas con PowerPoint y revisadas.
- **Comprimida:** los 94 clics recorridos en presentación, con captura del estado final de cada uno. Además capturé **cuadros intermedios** (cada 80–140 ms) de los pasos de animación más delicados: zoom de entrada y de salida de la matriz en las slides 3 y 6, y cierre de la 7. Las animaciones se mueven sin saltos y duran unos 0,4 s.

## Cambios de esta tanda (v24 → v25)
**Fuentes cerradas:**
- **67/26/7 (larga 36):** Brown, Diehl y Nigbor (2000), 12.ª WCEE, art. 0677, p. 7, citan textualmente 67 % Rayleigh, 26 % S y 7 % P a Miller y Pursey (1955), Proc. R. Soc. A 233:55–69. El original de 1955 sigue sin consultar, y la cita lo dice.
- **Imagen de crosshole (20–22):** es un esquema propio (`fig/build_figs.py`).
- **Ma et al. (59):** +1,5 dB a 1 Hz, +17,5 dB a 10 Hz y +21,3 dB a 20 Hz, verificados en el artículo (sec. 5, fig. 13).
- **Clasificación de técnicas (56):** según Ma et al., cero-polo = Song et al. (2016) y resistencia negativa = Besedina et al. (2020).
- **Comina et al. (2011) (99):** λmáx > 60 m como requisito para Vs,30 (pp. 581 y 585). Criterio de campo cercano: distancia de la fuente al centro del arreglo > λmáx/2 (p. 580); la campaña lo cumple (30 m frente a ≈13 m).
- **Densidad (39):** Foti, cap. 7, p. 361, usa 1800 y 2100 kg/m³ en su ejemplo; cap. 6, p. 279: sensibilidad débil.
- **Referencias:** agregadas Besedina 2020, Brown 2000, Comina 2011, Miller y Pursey 1955, Pazos 2005 y Song 2016; ahora en tres slides, en orden alfabético.

**Figuras en inglés reemplazadas:**
- **71:** el diagrama de flujo de calibración, traducido desde su archivo fuente (`Urucom_2026/imagenes/psoc_foreground_calibration_flow_compressed.drawio`, obtenido de Git LFS) y exportado con draw.io.
- **72:** el panel de calibración, regenerado con MATLAB a partir de los scripts y los datos del artículo (mismo FIR de 128 coeficientes; las curvas son idénticas), con ejes en español.
- **76:** reemplacé la diapositiva de Texas Instruments (fuente y licencia nunca confirmadas) por una **figura propia ilustrativa** (modulador de 2.º orden y filtro sinc³ genéricos). La cita aclara que no son los parámetros del PSoC.
- **94:** el esquema ICP de PCB, reemplazado por un **esquema propio** con los datos de `03_excitacion.tex` (21 V, LM7805 con 1 kΩ ≈ 5 mA, 47 µF, polarización de 8–14 V).
- **74:** es una captura de PSoC Creator; sus rótulos son nombres de componentes y no se traducen. Lo dice la cita; la vista lógica en español es la slide 75.
- **98 y 99:** ya eran figuras propias a 300 dpi; saqué la etiqueta «a regenerar» y la cita nombra su script.

**Corrección de `04_arquitectura.tex`:** verificada en el firmware. Durante la calibración se fuerza la configuración de ±2,5 V del ADC (`psoc_adc.c:102`), y la EEPROM se indexa solo por ganancia (`psoc_nv.h:11`). Por eso el rango de captura no invalida la calibración. **Aplicada** en `latex/secciones/04_arquitectura.tex`: solo cambian las dos zonas, el documento compila sin errores con `pdflatex`, y el cambio queda sin commitear. Para deshacerlo: `git -C docs checkout -- "Primera Presentación/latex/secciones/04_arquitectura.tex"`. La copia `04_arquitectura_CORREGIDO.tex` es idéntica.

## Lo que sigue abierto (y por qué)
1. **Fecha de la portada:** solo consta «diciembre de 2026» como mes de la defensa, y la nota de la portada dice «la validación completa queda para diciembre», lo que sugiere que esta presentación es antes. Solo vos sabés la fecha.
2. **Hakimitoroghi y Zhang: identificados** y agregados a las referencias.
   - Hakimitoroghi, Raut, Mirshafiei y Bagchi (2017), *Compensation techniques for geophone response used as vibration sensor in seismic applications*, ICST 2017, 1–5. **Contenido verificado** en su tesis de maestría (Hakimitoroghi, 2018, Concordia University, leída desde el navegador):
   - pp. 30–31: la técnica de función de transferencia inversa usa un integrador (1/s) y un integrador con pérdidas para cancelar los ceros del geófono (ec. 5, fig. 30).
   - p. 34: «Use of integrators cause problems of the DC offset [...] to avoid saturation».
   - p. 47: tuvo que restar la vibración ambiente.

   La slide 57 decía que sus mediciones mostraban «el papel del piso de ruido»; eso no figura en la tesis. La reemplacé por lo que sí dice: offset que satura y vibración ambiente. Agregué la tesis a las referencias.
   - Zhang et al. (2025), *Chinese Journal of Electronics* 34(6):1678–1688, doi:10.23919/cje.2025.00.059: balance de fuerza, circuito de resistencia negativa e integrador aproximado. Coincide con la slide 58.
3. **Kramer (1996): resuelto quitándolo.** No hay copia legítima para confirmar la página, así que la slide 39 ahora se apoya solo en lo verificado en Foti: 1800 y 2100 kg/m³ en el cap. 7, p. 361, y la débil sensibilidad a ρ en el cap. 6, p. 279. Saqué el rango de 1,4 a 2,2 t/m³ y, como Kramer ya no se cita en ninguna slide, también su entrada en las referencias.
4. **Fórmula aproximada de la slide 38:** según fuentes secundarias, la forma (0,862 + 1,14ν)/(1 + ν) es de Freund; la de Bergmann, que suele citarse también como de Viktorov, usa 0,87 y 1,12. La cita ya dice «Freund, según fuentes secundarias (por confirmar)», porque Freund no se consultó directamente. Los valores exactos son los de Foti, fig. 2.15.
5. **Pendientes del propio trabajo, no de la presentación:** ENOB y ruido referido a la entrada sin medir, tasa real del IMO entre placas, percentiles de jitter. Están declarados en las slides.
6. Nada commiteado.

## Hallazgos que conviene tener presentes en la defensa
- El reloj del ADC sale del IMO, sin cristal (±1 %). Ver la slide 91 y la memoria del proyecto.
- Foti 2018 pide disparos desde los dos extremos del arreglo; la campaña disparó desde uno.
