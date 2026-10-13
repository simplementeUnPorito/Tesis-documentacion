# Prompt para ChatGPT: corregir y completar imágenes (pegar tal cual)

Estoy preparando la primera defensa de una tesis de ingeniería electrónica (MASW con geófonos SM-24). Necesito imágenes verificables para diapositivas. Reglas estrictas, valen para TODO lo que sigue:

1. NO regeneres, NO redibujes y NO «recrees» ninguna figura. Si no podés descargar el archivo original, decímelo y dame solo el enlace. No lo reemplaces por una versión tuya.
2. NO me entregues imágenes generadas por IA como si fueran fotos o figuras de una fuente.
3. Por cada imagen entregá: (a) el archivo ORIGINAL sin modificar, en la mejor resolución disponible; (b) URL de la página y URL directa del archivo; (c) autor, año, título del libro/artículo/informe, número de figura y página; (d) licencia exacta y si permite redistribuir/modificar; (e) resolución en píxeles.
4. Si traducís etiquetas al español, hacelo SOBRE el original, cambiando solo el texto de los rótulos. Los números, valores, ejes, curvas y geometría deben quedar idénticos. Dame también una lista de cada texto cambiado (antes → después) y confirmá explícitamente que no tocaste ningún número.
5. Si algo no se puede verificar, escribilo como «NO VERIFICADO». No rellenes datos.
6. Prefiero fuentes con licencia abierta (dominio público, CC BY, CC BY-SA). Si una imagen tiene derechos reservados, avisame y dame alternativas abiertas.

## A. Imágenes a CORREGIR

1. **Configuración MASW fuente-receptor** (Park Seismic): original en https://www.masw.com/images/ActiveMASW_FieldSetup_.JPG (alta resolución). La traducción anterior cambió el recuadro del shot gather («Registro #1053», estaciones 1003/1023…, offsets 4/84/164/244/324). El original dice «RECORD # 1015 (Source Station = 1001)», estaciones 1015/1020/1025/1030, offsets 14/19/24/29, canales 5/10/15/20. Traducí solo los rótulos sobre el original y no cambies esos números.
2. **Refracción, diagrama de rayos (USGS)**: extraé del PDF del informe USGS Open-File Report 87-0103-A (https://pubs.usgs.gov/of/1987/0103a/report.pdf) la figura real «Raypaths of refracted and reflected sound energy in a two-layer Earth», con número de figura y página. Recortala del PDF (no la recrees) y traducí los rótulos sobre ese recorte. Si no está en ese informe, buscá en OFR 84-0746 e indicá cuál.
3. **Dromocrónica de refracción**: descargá el original de Wikimedia Commons «File:Refraction_dia.jpg» (autor lore.trango, 794×665) y traducí los rótulos sobre él. Confirmá la licencia en la ficha.
4. **Curva de dispersión Rayleigh con 4 modos** (vR1=189,45; vR2=312,50; vR3=385,10; vR4=491,32 m/s a 50 Hz): identificá de qué libro o artículo viene (título, autores, figura, página). Dame el original en mayor resolución. No la redibujes.
5. **Esquema SASW vs MASW** (diapositiva «Surface Wave Methods», fondo negro, de una presentación «Vs30 measurements for seismic site classification» en SlideShare): identificá el artículo o libro de origen de cada esquema (SASW y MASW) y dame las figuras originales en alta resolución.
6. **Corte interno de un geófono** (carcasa de acero, resorte superior/inferior, imán, bobinas): mi documento lo cita como Breslin (2020). Confirmá la referencia completa, la figura y la licencia, y dame el original.
7. **Fotos de campo**: descartá las dos imágenes con camión y operarios con casco naranja (son generadas por IA). Sí sirve la foto real de USGS «Seismic Survey» (2006), dominio público: https://www.usgs.gov/media/images/seismic-survey (dame el archivo original, no una versión «mejorada»). Para las fotos de IIT Gandhinagar (derechos reservados) buscá alternativas abiertas.
8. **Ondas Love y Rayleigh (movimiento de partículas)**: busco una figura con licencia abierta donde la órbita de Rayleigh sea elíptica, retrógrada en superficie y progresiva en profundidad, y el movimiento de Love sea horizontal transversal. Dame candidatos con fuente (Wikimedia Commons, USGS, libros abiertos), sin crearlos.
9. **Figura SV/SH**: busco una imagen real, con fuente, que muestre la diferencia entre polarización SV (en el plano de incidencia) y SH (perpendicular). Si no existe con licencia abierta, decímelo y no la inventes.

## B. Imágenes que FALTAN

1. **Curva de dispersión experimental REAL**, con datos medidos (idealmente MASW activo), con fuente y figura. Por ejemplo la Fig. 1.1D de USGS OFR 2024-1016 (https://pubs.usgs.gov/publication/ofr20241016/full), si podés extraerla del PDF.
2. **Imagen de espectro frecuencia–velocidad de fase** (el «overtone image» o mapa de energía del MASW con la curva picada), real y con fuente.
3. **Perfil Vs(z) resultante de una inversión MASW real**, con fuente.
4. **Registro (shot gather) real** de un ensayo MASW con ondas Rayleigh dispersivas, con fuente.
5. **Fotos reales de un ensayo MASW** (martillo, placa, geófonos en línea, sismógrafo) con licencia abierta.
6. **Registradores sísmicos abiertos de bajo costo**: Geophonino (Llorens et al., 2016) y MicDAC (Kafadar, 2020): fotos o esquemas del propio artículo con su licencia.
7. **Sismógrafo comercial de 24 canales** (por ejemplo Geometrics o PASI): foto o ficha técnica oficial, con enlace a la lista de precios que usé (PASI srl, 2022; Geometrics, 2023).
8. **Figura de P y S** (deformación de partículas) de Kearey et al. (2002), a partir de Bolt: si hay versión abierta equivalente, con fuente.
9. **Figura de reflexión/transmisión/conversión P–SV** de Bangash et al. (2017): confirmá si hay versión abierta o una equivalente.
10. **Geófono SM-24**: foto oficial de Sensor Nederland / Input-Output y su hoja de datos con enlace, para citar.

Al final, dame una tabla con una fila por imagen: archivo, estado (original / traducida sobre original / NO VERIFICADO), fuente, licencia, resolución.
