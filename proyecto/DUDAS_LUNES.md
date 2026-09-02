# Dudas y bloqueos del porteo automático

Escrito por el loop (`scripts/autonomia/port_loop.py`) y por los modelos que
corrieron sin supervisión. Se lee el lunes, en orden. Las entradas nuevas se
agregan al final con su fecha.

---

## 2026-07-24 — sembrado a mano antes de largar el loop

### 1. El canal del maestro cambió de 1 a 7 (esclavos ESP-NOW)

El maestro quedó asociado a `Flia. Martinez` (IP `192.168.100.219`) y su radio se
movió al canal del router: **canal 7**. El AP `GeoNetwork` sigue vivo en
192.168.4.1 porque corre `WIFI_AP_STA`, pero **los esclavos ESP-NOW tienen que
adoptar el canal nuevo** (el esclavo escanea el SSID del maestro y adopta su
canal, `link_mode.h:612`). No lo pude verificar: no probé una captura con
esclavos en esta sesión.

**Para el lunes**: encender un esclavo y confirmar que aparece en el maestro con
el canal 7. Si el router salta de canal solo (muy común en 2.4 GHz), esto se va a
repetir; habría que decidir si vale fijar el canal en el router.

### 2. `/enlace/scan` se auto-bloquea y tira al cliente del AP

Dos cosas distintas, las dos reales:

- El escaneo **desconecta a la PC del AP** (una sola radio: para escanear la saca
  del canal). Se ve como `WinError 10053/10060` y parece un problema de red. No lo
  es. `link_config.py` ya lo tolera reconectando.
- Con un SSID guardado que no existe, `linkScanPoll` (`link_mode.h:719`) entra en
  **livelock**: `scanComplete()` devuelve FAILED porque el `WiFi.begin()` de
  reintento está en curso, y el handler arranca otro escaneo, para siempre. El
  endpoint contesta 202 indefinidamente y nunca lista una red.

**Duda que no me corresponde decidir**: arreglarlo pide tocar firmware del
maestro (por ejemplo, no re-disparar el escaneo si hay un intento de STA en
curso, o suspender el retry de STA mientras se escanea). No lo toqué porque
reflashear el maestro corta el WiFi y vos no estabas para reconectar. Queda
anotado como fix chico y bien delimitado.

Mientras tanto no molesta: la verificación buena del SSID no es el escaneo, es
que la STA se asocie (`sta=up` + IP), y eso es lo que `link_config.py` exige.

### 3. Hardware que NO se tocó, a propósito

- **PSoC**: no se programó nada. La rama está sin terminar. `device_reset.py psoc`
  sólo hace `ToggleReset` por KitProg (no programa), y no lo ejecuté en esta
  sesión: sin un esclavo hablándole no hay forma de verificar que el reset salió
  bien, y un reset a ciegas dispara una auto-calibración de varios minutos.
- **Esclavo (COM12)**: no reseteado. Resetear el esclavo puede colgar el PSoC, y
  ahí sí haría falta el ToggleReset encadenado (`--and-psoc`).
- **Maestro (COM8)**: reseteado y verificado (arranca, el AP vuelve, `/health`
  responde). La cola del enlace sobrevivió: 1 archivo, 26684 B.

**Para el lunes**: probar `python scripts/autonomia/device_reset.py psoc
--wait-autocal` con el esclavo conectado, que es la única forma de ver si el PSoC
volvió sano (`psoc=1`, `IDLE`).

### 4. El servidor sigue siendo `http.server`, no FastAPI

Es el ítem `refactor` del loop (PORT_PLAN §1). Si el loop quedó bloqueado ahí,
esta es la razón por la que nada más avanzó: el loop **para** en el primer ítem
bloqueado en vez de arrastrar un refactor torcido a los siguientes.

### 5. Cómo leer el log si el loop pasó la noche esperando

La primera corrida se chocó con el límite de sesión a los 4 minutos
(`api_error_status=429`, *"You've hit your session limit · resets 11:20pm"*), ya
con el spec del refactor escrito y **$1.71 gastados**. El loop ahora:

- espera hasta la hora que anuncia el mensaje (no un backoff a ciegas), en tramos
  de 6 h como máximo para poder re-leer el mensaje real al despertar;
- no cuenta el límite como intento fallido ni escala de modelo por eso;
- si la fase ya había dejado su entregable antes del corte, la da por hecha en vez
  de pagarla de nuevo (fue exactamente lo que pasó con ese spec).

Así que en el log es **normal** ver horas de `límite de uso: espero hasta …`
seguidas de la misma fase retomando. No es un cuelgue.

**Cota real de esta corrida**: el techo no es el plan, es la cuota. El ítem
`refactor` solo costó $1.71 sólo en escribir su spec con Opus. Si el lunes ves
pocos ítems hechos, mirá `costo` en `--status` antes de sospechar del loop.

### 6. Cosas que el loop no puede validar y vos sí

El gate verifica HTTP y datos reales, no percepción. Nada de esto está cubierto:

- que un pick arrastrado a mano **se vea** donde tiene que verse;
- que la app PyQt vea el cambio de la web y al revés (criterio §6 del plan) —
  el check `capturas.pick` verifica el ida y vuelta por `frd.load_annotations`
  en sandbox, que es lo más cerca que llega sin un humano;
- que la web responda bien con 200+ capturas en el waterfall (§3.4, fuera de
  alcance de esta corrida).

---

## 2026-07-25 — escribiendo el spec de `tabs_tema` (§2)

### 7. Los nombres de función del PORT_PLAN §3.2 no existen

El plan dice filtrar con `signal_proc.py`: `dcRemove`, `filtFilt`,
`harmonicNotch`, `hilbertEnvelope`. **Ninguno de esos cuatro existe en el repo**
(son nombres estilo MATLAB; el código Python es snake_case). Lo que hay:

- `geophone_scope/signal_proc.py:367` `dc_remove`, `:235` `harmonic_notch`,
  `:37` `fir_filter` — el camino del **scope en vivo**.
- `geophone_scope/field_review_data.py:906` `apply_bandpass_filter` y `:873`
  `design_bandpass_filter` (Butterworth SOS + `sosfiltfilt`, fase cero) — el
  camino que **realmente usa el tab Filtros de la app PyQt**
  (`field_review_app.py:1970`).
- `hilbertEnvelope` no tiene equivalente: no encontré ningún cálculo de envolvente
  de Hilbert en `field_review_*`.

**Por qué me frenó**: para §2 no bloquea nada (sólo escribí placeholders, y ahí
cité los nombres reales). Bloquea al ítem §3.2 `Filtros`, que va a arrancar
buscando funciones que no están.

**Opciones que veo**:

1. Corregir §3.2 del plan para que diga `frd.apply_bandpass_filter` — es lo que
   da paridad con la app, que es el criterio del §6 del plan. Es lo que yo haría.
2. Portar además el DC/notch de `signal_proc` como opciones extra del tab web.
   Es funcionalidad que la app de review **no** tiene, así que sería
   funcionalidad nueva, no porteo — y el plan dice explícitamente que esto es una
   mudanza.
3. Si `hilbertEnvelope` era un pedido real y no un recuerdo de otra herramienta,
   hay que decidir si entra como feature nueva. No lo asumí.

No elegí ninguna: cambiar el alcance del §3.2 no me corresponde.

---

## 2026-07-25 — escribiendo el spec de `capturas_signal` (§3.1, parte 1)

### 8. El sandbox del gate escribe en el archivo de picks REAL

`frd._procesados_dir_for` (`field_review_data.py:63-69`) resuelve la carpeta de
salida por **`raw_root.name`**, no por la ruta completa. El sandbox del gate crea
su raw en `<tmp>\raw` (`server/smoke_test.py:597-599`), así que `name == "raw"`,
igual que `data\raw`. Consecuencia:

`default_annotations_path(<tmp>\raw)` == `default_annotations_path(data\raw)` ==
`C:\Github\Tesis\data\processed\raw\field_review_annotations.json`

Hoy no hizo daño porque `reviewed_count == 0` y el ZIP que ingesta el gate no
tiene par hammer+geo (sin shots, `Pipeline._process` no llama a
`save_annotations`). **Pero el día que tengas picks validados a mano, un check de
sandbox que ingeste una captura completa te los borra todos, sin aviso.** Es lo
que el §0.3 del plan ("nada se borra solo") prohíbe explícitamente.

**Por qué me frenó**: no bloquea el ítem §3.1-parte-1 (lo escribí de sólo
lectura, y los fixtures del gate se escriben directo en el raw temporal en vez de
pasar por `/ingest`). **Sí bloquea al ítem de `POST /api/pick`**, que escribe
anotaciones por diseño.

**Opciones que veo**:

1. Pasarle `TESIS_DATA_ROOT=<tmp>` en el `env` del `subprocess.Popen` de
   `start_server` (`smoke_test.py:516`) **sólo en modo sandbox**.
   `frd._discover_data_root` (`field_review_data.py:30-42`) ya respeta esa
   variable, así que todo `data/processed` del sandbox cae en el temporal y el
   modo `read` sigue viendo las anotaciones reales. Es lo que yo haría: una línea
   y no toca la capa de datos.
2. Que `_procesados_dir_for` use algo único por dataset (hash de la ruta
   absoluta, o la ruta completa espejada). Es más correcto de fondo —dos datasets
   llamados `raw` en distintos discos hoy comparten anotaciones **también en la
   app PyQt**— pero cambia dónde vive todo lo ya generado y habría que migrar
   `data/processed/*`. No lo decido yo.
3. Hacer una copia de seguridad del JSON de picks antes de cada corrida del gate.
   Es un parche, no un arreglo.

### 9. `catalog.pickable` y `discover_dataset` no coinciden (186 vs 194)

Medido hoy contra `data\raw`: el catálogo marca **186** capturas `pickable` en
`Canchiga`, y `discover_dataset` encuentra **194** disparos en esa misma carpeta.
Al revés también pasa: las 9 capturas de `Canchita` son `pickable: true` y
**ninguna** tiene `shot_id` (quedaron afuera por el dedup por firma de señal).

La causa es que hay **dos detecciones de rol distintas**:

- `catalog.py:104` lee sólo `node["role"]`;
- `frd._node_role` (`field_review_data.py:1754`) mira además
  `type`/`hw_type`/`name`/`data_dir`/`raw_file`.

**Por qué me frenó**: para este ítem lo esquivé (la web habilita el dibujo por
`pick.shot_id`, no por `pickable`, y está escrito en el spec). Pero significa que
la columna "Estado" de la tabla de Capturas **le miente al usuario en 8
capturas**: dice "sin martillo" en capturas que sí tienen martillo.

**Opciones que veo**:

1. Que `catalog.py` importe y use `frd._node_role`. Es una función privada de
   `frd`, y el §0 del plan dice no relajar ese contrato… pero acá no lo relaja:
   lo unifica. Es lo que yo haría.
2. Copiar la lógica de roles en `catalog.py`. Queda una tercera copia que se va a
   desincronizar: en contra del §0.4 del plan.
3. Exponer `node_role()` público en `field_review_data.py` y que los dos lo usen.
   Es lo más limpio, pero toca `geophone_scope`, que es código compartido con la
   app PyQt, y eso no lo decido yo.

Aparte, `/api/dataset` **no dice por qué** una captura no tiene `shot_id`
(¿sin martillo? ¿duplicada?). La web hoy lo explica con un texto genérico. Si
querés que diga "duplicada de X", hay que exponer `duplicate_of`
(`FieldShot.duplicate_of`, `field_review_data.py:105`) en el contrato de
`/api/dataset` — es un agregado, no rompe `refactor.contrato_dataset`, pero es
alcance nuevo.

#### RESUELTA (2026-07-25, respondida por Elías)

La premisa de la duda era equivocada: **las cuatro funciones existen**. Los nombres
están en camelCase porque vienen del **SPA del maestro**, que las tiene
implementadas en JavaScript (`master/data/js/signal_proc.js` las exporta todas:
`dcRemove:224`, `filtFilt:195`, `harmonicNotch`, `hilbertEnvelope:284`). También
hay versiones en Python y en MATLAB. O sea: no hay nada que inventar ni ningún
alcance que cambiar, y `hilbertEnvelope` tampoco es una feature nueva.

Qué hace cada una, ya escrito en el §3.2 del PORT_PLAN (que es lo que leen todas
las fases del loop, a diferencia de este archivo, que sólo se escribe):

- `dcRemove`: quita la continua.
- `filtFilt`: pasabanda Butterworth de **fase cero** — no corre los tiempos de
  arribo, que es justo lo que no se puede romper para el picking.
- `harmonicNotch`: cancela ruido de línea estimando **por RMS** las senoidales en
  los armónicos de la frecuencia de línea y restándolas. El maestro es donde está
  mejor explicado (`app.js:1298`, LS de armónicos sobre la ventana completa).
- `hilbertEnvelope`: envolvente por transformada de Hilbert.

Más el orden de la cadena, que no estaba escrito en ninguna parte del plan y sí
importa: **FIR → DC → notch**, con el notch último y sobre la ventana completa.

La instrucción para el loop quedó como "buscá la implementación que te convenga y
llamala, no la reescribas", sin atarlo a un nombre ni a un archivo.

## 2026-07-25T14:28:28-03:00

**[capturas_pick] §3.1 Pick editable (POST /api/pick) + geo_flip** — no se pudo ni escribir el spec. Ver C:\Github\Tesis\scripts\autonomia\state\raw.

---

## 2026-07-26 — porteo de la ventana Capturas, a mano y con Elías

Decisión del usuario en esta sesión: **la web reemplaza a la app PyQt**; la
referencia deja de ser "un porteo parcial" y pasa a ser "la mismísima app, en
web". Copia de referencia de la app en `docs/legacy/pyqt_field_review/`.

### 10. RESUELTA la #9 (`catalog.pickable` vs `discover_dataset`)

Se tomó la opción 3, no la 1: `field_review_data` ahora expone **`node_role()`**
público (más `discover_capture_channels()` y `zero_by_pretrigger()`), y
`catalog.py` lo llama. Antes había dos deducciones de rol y el catálogo marcaba
"sin martillo" capturas que `discover_dataset` sí tomaba (186 vs 194). Ahora
`/api/captures` da 210 filas = 194 disparos + 16 que no lo son, y cada una dice
por qué (`Duplicada` 10, `Sin geófono` 4, `Sin martillo` 1, `Sin señal` 1).

También se borró la copia de `_zero_by_pretrigger` que tenía
`field_review_app.py`: ahora delega en la de `field_review_data`, que es la que
ya usaba el servidor. Una sola implementación.

### 11. Bug encontrado y arreglado: `_save_state` perdía la cola

`Pipeline._save_state` escribía siempre en el mismo `jobs.tmp`, fuera de todo
lock. Dos ingestas simultáneas se pisaban y en Windows la segunda moría con
`PermissionError`, o sea **se perdía el registro de trabajos**. Se agregó un
lock de E/S propio y nombre de temporal único por hilo. Era preexistente; lo
destapó el check `refactor.worker_no_bloquea`, que hasta ahora venía pasando por
suerte de timing.

### 12. RESUELTA — lo que estaba frenado: todo lo que ESCRIBE anotaciones

**La #8 se arregló** (2026-07-26, visto bueno de Elías) con la opción 1:
`start_server` (`smoke_test.py`) le pasa `TESIS_DATA_ROOT=<tmp>` en el `env` del
subprocess **sólo en modo sandbox**. `frd._discover_data_root` ya respetaba esa
variable, así que todo lo que escribe el gate cae en su temporal y el modo
`read` sigue viendo lo real. Verificado: el md5 de
`data/processed/Canchita/field_review_annotations.json` queda idéntico después
de una corrida completa del gate.

Con eso destrabado se implementó `POST /api/pick` (`server/picks.py`), que
escribe con `frd.save_annotations` en el mismo archivo y formato que la app.
Dos reglas de escritura que salen de cómo es el equipo:

- **El trigger es de la CAPTURA.** Un tendido de N geófonos comparte un solo
  martillo: un golpe, un tiempo cero. Mover el trigger lo escribe en los N
  disparos de esa captura. Al leer, un receptor sin marca propia hereda el
  trigger de un hermano que sí la tenga (`trigger_source: "capture"`).
- **La polaridad es de CADA geófono.** El circuito no tiene polaridad: uno pudo
  quedar conectado al revés y el otro no. `geo_flip` se escribe sólo en el
  disparo que se está mirando.

Verificado punta a punta contra un árbol sintético de 2 geófonos: trigger
compartido, `geo_flip` y estado independientes por receptor.

Texto original de la duda, para contexto:

Sigue en pie la duda #8 (el sandbox del gate resuelve la carpeta de picks por
`raw_root.name` y escribiría sobre `data/processed/raw/field_review_annotations.json`,
el archivo real). Mientras eso no se arregle, en la web están **presentes pero
deshabilitados**, con el motivo escrito en pantalla:

- `Guardar y siguiente`, `Aplicar dist. a carpeta`, `Invertir geo de carpeta`
- los campos `Distancia m`, `Usar esta muestra`, `Notas`
- la tecla `Espacio` (rotar estado sin validar → OK → rechazada)

Todo lo demás de la ventana Capturas anda y **no toca el disco**: arrastrar el
trigger, `Auto` (con o sin zona), zona auto por clicks, `Invertir esta señal`
(preview), orden, filtros, overlays, zoom, teclas de navegación.

**Para decidir**: si se aplica la opción 1 de la duda #8 (`TESIS_DATA_ROOT=<tmp>`
en el `env` del subprocess del gate, sólo en modo sandbox), se destraba todo eso
de una. Es una línea en `smoke_test.py:516`.

### 13. El `raw_root` por defecto esconde casi todos los datos

`data/raw` **no** es una raíz de datos: es un contenedor de campañas. La raíz que
`discover_dataset` espera es la campaña, porque busca `<raw_root>/<carpeta>/captures/`
y no baja más. Comparación, medida hoy:

| `raw_root` | disparos | anotaciones que matchean |
|---|---|---|
| `data/raw` (el default) | 194 | **0** |
| `data/raw/Canchita` | 607 | **607** |
| `data/raw/Canchita_2` | 242 | 242 |

O sea que arrancando el servidor como dice el PORT_PLAN §0 se ven 194 de ~1400
capturas y **ninguna** de las 606 marcas validadas a mano, aunque el archivo
está intacto en `data/processed/Canchita/field_review_annotations.json`. No hay
nada que migrar ni ningún id que reconstruir: el archivo casa 607/607 apenas se
apunta a la campaña.

Se arranca así mientras tanto:

    python -m server --port 8000 --raw-root C:\Github\Tesis\data\raw\Canchita

#### RESUELTA (2026-07-26, decisión de Elías): unir todas las campañas

Se implementó `server/campaigns.py`. Modelo:

- **Campaña** = directorio que contiene directamente una o más *carpetas* (un
  directorio con `captures/` adentro). Se busca en `raw_root` y en cada hijo, así
  que entran el layout plano (`raw/<carpeta>/captures/`) y el anidado
  (`raw/<campaña>/<carpeta>/captures/`).
- Cada campaña **sigue siendo su propia raíz de datos**: sus `shot_id` y su
  `data/processed/<campaña>/` no se tocan. Por eso las 606 marcas siguen
  valiendo sin migrar nada.
- La web las **une**: cada fila lleva `campaign` y su clave es
  `campaña|carpeta|captura`. Cada request de señal/overlays manda `campaign`
  para que el `shot_id` se busque en la raíz correcta.
- Nombre visible y tilde de "usar" se guardan en `<data_root>/campaigns.json`.

Un directorio puede ser **las dos cosas** a la vez: `data/raw/Canchiga` tiene su
propio `captures/` (210 capturas, que cuentan para la campaña raíz) y además 79
carpetas anidadas (692 capturas, que son la campaña `Canchiga`). Son capturas
distintas, así que **no se excluye** una de la otra — excluirlas tiraba 210.

Resultado con `raw_root = data/raw` (el default, sin flags):

| campaña | carpetas | capturas | validadas |
|---|---|---|---|
| `.` (raíz) | 2 | 210 | 0 |
| `Canchiga` | 79 | 692 | 0 |
| `Canchita` | 92 | 944 | 606 |
| `Canchita_2` | 13 | 252 | 0 |
| **total** | | **2098 filas / 1408 disparos** | **606** |

Contra las 194 capturas y 0 validadas de antes.

### 15. N geófonos por tendido, y el nodo que aparecía dos veces

`_discover_folder_shots` tomaba **sólo el primer geófono** de cada captura
(`_first_role`), así que un tendido de N receptores daba 1 disparo en vez de N.
Ahora emite uno por geófono (mismo golpe, distinta distancia), que es
exactamente lo que necesita MASW.

**Compatibilidad de ids**: el primer geófono conserva el `shot_id` histórico
(`sha1(ruta de la captura)`, sin sufijo); del segundo en adelante el id lleva
`#<pcb_id>`. Con un solo receptor —todo lo que hay grabado hoy— los ids no
cambian y las 606 marcas siguen valiendo. Verificado: 2098 filas / 1408
disparos / 606 validadas, idéntico a antes del cambio.

**Trampa que destapó**: al principio aparecieron 8 capturas de `Canchiga` con
"dos geófonos" (`esclavo_2_s2` y `geo1_s2`). No son dos: es **el mismo nodo S2
exportado con dos nombres de directorio** (8790 vs 10800 muestras). Su metadata
tiene todos los nodos con `role: unknown`, así que se descubren por nombre de
directorio y ahí caían los dos como geo. Se agregó `_dedupe_by_slave`: un canal
por (rol, nodo físico), donde el nodo físico sale del `_s<N>` final del nombre.
Conserva el mismo canal que elegía `_first_role` antes, así que no cambia nada
de lo ya anotado.

**Sin datos con qué validarlo de verdad**: no hay ninguna captura multi-geo real
en `data/raw`. Se probó con fixtures sintéticas (3 nodos distintos → 3 disparos;
mismo nodo con dos nombres → 1 disparo). Cuando haya un tendido real hay que
volver a mirarlo.

**Trigger compartido** (pedido de Elías, 2026-07-26): los N geófonos comparten
el golpe, así que comparten trigger y tiempo cero. Escribir el trigger lo escribe
en los N disparos de la captura; al leer, un receptor sin marca propia hereda la
de un hermano (`trigger_source: "capture"`). La polaridad y el estado **no** se
comparten: son de cada geófono. Congelado hasta que haya más placas.

---

## 2026-07-26 (tarde) — Filtros, Agrupamiento, Enfase y Promedios

### 16. Portado, y qué falta de cada una

| Tab | Estado | Archivo que persiste (el mismo que la app) |
|---|---|---|
| Filtros §3.2 | completo | `filter_settings.json` |
| Agrupamiento §3.3 | completo | `dispersion_groups.json` |
| Enfase §3.2 | **parcial** | `alignment_offsets.json`, `alignment_disabled_folders.json` |
| Promedios §3.3 | **parcial** | `field_review_average_arrivals.json` |

**Filtros**: probar y guardar quedaron separados a propósito (la app guarda en
cada tecleo). Los ajustes mandan sobre promedios, waterfall, MASW y export, y
con el autoguardado es muy fácil pisar los de una campaña sin querer — me pasó
a mí probando. El botón «Guardar y aplicar» se resalta cuando hay cambios sin
guardar. El espectro se agrupa en **bins espaciados en log**, no uniformes: con
bins uniformes dibujados en eje log las décadas bajas quedaban con cuatro puntos
sueltos y se veía como una sierra.

**Lo que NO está portado, y por qué:**

1. **Enfase — auto-enfase de dos etapas y auto-polaridad.** La app tiene
   `frd.auto_align_polarity` y un auto-enfase intra/inter punto. No lo porté
   porque no entendí bien el criterio de la segunda etapa (qué define el signo
   de referencia entre puntos cuando ninguno está validado todavía) y meterlo
   mal invierte señales buenas. La parte manual —offset por carpeta, «OK
   alineado», rechazar carpeta, resets— sí está y es la que se usa a mano.
2. **Enfase — offsets por señal** (`alignment_shot_offsets`). Se **leen** (los
   promedios los respetan, porque `get_alignment_offset` les da prioridad sobre
   el de carpeta), pero no hay UI para editarlos. En la app se editan desde otro
   lado; no encontré cuál.
3. **Promedios — sólo la anotación del arribo.** El panel de la app tiene más
   cosas alrededor (comparar grupos, disparar el export). Acá está el promedio
   por distancia, el hammer promedio, marcar el arribo con click y validar.
4. ~~**Waterfall §3.4 y MASW §3.5**: sin empezar.~~ Waterfall quedó portado y
   MASW tiene la imagen de dispersión — ver la #17.

**Nota sobre el rendimiento de Enfase**: `/api/alignment` promedia todas las
carpetas del label leyendo sus señales enteras. En `Canchita` cada label tiene
una sola carpeta y responde al instante, pero con muchas tandas del mismo punto
va a tardar. Si molesta, hay que cachear el promedio por carpeta como se hizo
con el escaneo (`datacache`).

### 14. Rendimiento: el escaneo tardaba 30 s y se pedía cada 3 s

Con 944 capturas, `scan_catalog` + `discover_dataset` (que hashea archivos para
detectar duplicados) tardan ~28 s, y `/api/captures`, `/api/signal` y
`/api/overlays` lo hacían **cada uno, en cada request**, con la tabla
refrescando cada 3 s: las peticiones se encolaban y la web quedaba en blanco.

Ahora: `server/datacache.py` cachea el escaneo estructural (TTL 60 s), el
Pipeline lo invalida al ingestar o borrar, y se calienta en un hilo al arrancar.
Las **anotaciones no se cachean nunca** — son baratas y son lo que la app PyQt
puede tocar por detrás. Medido después: `/api/captures` 334 ms, `/api/signal`
18 ms, `/api/overlays` 83 ms. El polling de la tabla pasó de 3 s a 8 s.

### 17. Sesión 2026-07-26 (tarde): sierra, zoom con mouse, Waterfall y MASW

**La "forma de sierra" era el orden de los extremos, no el decimado.** Cada
bucket min/max se dibujaba siempre `max → min`, sin mirar cuál de los dos
ocurrió antes en el tiempo. Sobre cualquier traza suave eso convierte cada
subida real en una bajada, y el salto a la columna siguiente cierra el diente:
un serrucho parejo que no está en la señal. `decimate_minmax` ahora devuelve
también `rising` (si el mínimo del bucket vino antes que el máximo) y
`drawMinMax` emite los dos puntos en ese orden. Verificado: sobre una senoide,
`rising` coincide con el signo de la pendiente real en el 100 % de los buckets.

**Segundo síntoma, misma zona: escalones al acercarse.** El servidor decimaba
la señal **entera** a un bucket por píxel, así que al hacer zoom esos buckets se
repartían entre menos tiempo y cada uno pasaba a ocupar varios píxeles. pyqtgraph
no tiene el problema porque redibuja desde los datos completos. Ahora
`maxPointsFor` pide tantos buckets como haría falta para que la **ventana
visible** tenga uno por píxel, y se re-pide (con freno de 180 ms y sólo si hace
falta 1.5× más detalle del que ya hay) al cambiar el encuadre.

**Zoom y paneo con mouse**: `attachViewControls` en `plot.js`, el equivalente al
ViewBox que pyqtgraph le da de fábrica a cada PlotWidget. Rueda = zoom sobre el
cursor; shift+rueda = sólo vertical; alt/ctrl+rueda = sólo horizontal; arrastre
= mover; doble click = reencuadrar. El estado son rangos en unidades de dato, no
un factor, así que sobrevive a que la traza cambie de escala. El teclado (↑/↓,
q/e y el nuevo `0`) usa el mismo estado, así mouse y teclas no se pelean.
Enganchado en Capturas, Filtros (original y filtrada comparten vista), Enfase,
Promedios, Waterfall y MASW. Donde el botón izquierdo ya tiene dueño —arrastrar
el trigger, marcar zona, poner el arribo— ahí se panea con el del medio o el
derecho.

**Waterfall §3.4: portado.** `server/waterfall.py` + `routers/waterfall.py` +
`static/js/tabs/waterfall.js`. Recorte de tiempo, trazas tildables, «Amplitud
real», filtro f-k (Off/Directo/Inverso), «Invertir traza», cursor con
tiempo/distancia, y el arribo dibujado sólo si está validado (igual que la app).
Los ajustes de vista se guardan en el **mismo** `masw_state.json` que la app: al
abrir la web apareció el recorte −0.05 a 2.5 s que ya estaba guardado desde PyQt.

**Bug encontrado y arreglado de paso: Promedios ignoraba los grupos.**
`build_averages` llamaba a `compute_average_groups` con el dataset completo. La
app filtra antes con `_filtered_dataset_for_group` + `_project_disabled_for_group`
(:284 y :227), porque cada grupo es un tendido distinto y sus distancias no se
promedian con las de otro aunque coincidan en metros. Ahora está en
`server/groups.py` y lo usan Promedios, Waterfall y MASW. Con eso, Canchita da
Grupo 1 = 21 promedios y Grupo 2 = 14, no 21 mezclados.

**MASW §3.5: sólo la etapa 1.** `server/masw.py` calcula la imagen de dispersión
con `masw_dispersion.phase_shift_dispersion_image` —el mismo módulo que la app—
sobre lo que el waterfall tenga a la vista (`matrix_for_masw`, calcado de
`_emit_masw` :3974). Viaja como PNG de 8 bits en base64 (la grilla son ~95 000
floats; en JSON serían ~½ MB por recálculo) y el color se aplica en el navegador
con la rampa de `_dispersion_colormap` (:4824). Medido: 21 receptores, imagen
252×376, 115 KB, ~11 s.

#### Lo que sigue faltando (§3.5 y lo de la #16)

1. **Picking de la curva de dispersión**: las regiones-polígono editables que
   dan N curvas por modo. Es lo próximo de MASW.
2. **Inversión y Perfil Vs**: los backends de `masw_backends.py` /
   `masw_inversion.py` (evodcinv+disba, ADsurf) tardan **minutos**. No pueden ir
   dentro de un request: hay que correrlos como trabajos del `Pipeline`, con
   estado y progreso, igual que el preprocesado de las capturas. Es el diseño
   que hay que decidir antes de escribir el código.
3. Sigue pendiente todo lo de la #16: auto-enfase de dos etapas /
   `auto_align_polarity`, offsets por señal editables, y el panel de Borrado
   (§4) con flags y subgrupos.
