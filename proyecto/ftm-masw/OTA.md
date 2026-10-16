# Preparación OTA para trabajar con el maestro por USB

Estado al 16/10/2026: compilaciones ESP-IDF 5.5.1 correctas para maestro y tres esclavos; 43 pruebas OTA en PC y 45 pruebas existentes aprobadas. El maestro ESP32-S3 con flash de 16 MiB fue identificado en COM3, respaldado y actualizado por USB; `ota hello` confirma `fts1.master`. La preparación de esclavos y la validación por radio siguen en curso.

Alcance confirmado: cuatro ESP32-S3, un maestro actualizado por USB y tres esclavos actualizados por OTA. El maestro actúa como puente USB/Wi-Fi.

OTA significa actualizar el firmware por radio. El objetivo operativo es dejar los esclavos alimentados y acceder desde la PC conectada al maestro.

## Flujo propuesto

```text
PC: compila y conserva la imagen y su manifiesto
   │ USB: orden y transferencia con control de flujo
   ▼
Maestro: consulta inventario y coordina mantenimiento
   │ Wi-Fi: actualiza un esclavo identificado
   ▼
Esclavo: escribe la partición inactiva, verifica y reinicia
   │ autocomprobación y confirmación
   ▼
PC: registra versión, resultado y posibilidad de recuperación
```

El transporte nativo OTA de ESP-IDF no impone un servidor en Internet. Las APIs aceptan bloques recibidos por el transporte implementado.

La implementación aprovecha la red del maestro y añade un puente USB/Wi-Fi con bloques acotados y autenticación por sesión. La prueba de rendimiento y recuperación en placas sigue pendiente. El procedimiento operativo está en `src/firmware/ftm-test/docs/ota-prototipos.md`, dentro de Tesis.

Como alternativa de desarrollo, la PC podría conectarse también a la red Wi-Fi y servir imágenes directamente. Esa alternativa agrega conectividad en la PC.

## Antes de fijar las particiones

Se necesitan la identificación de flash por placa y los tamaños reales de bootloader y aplicación. También deben inspeccionarse las particiones instaladas.

La configuración histórica de un notebook no reemplaza una lectura del equipo actual. Para los prototipos se preparó una tabla que requiere al menos 4 MiB: NVS en `0x9000` (24 KiB), metadatos OTA en `0xf000` (8 KiB), y ranuras de 1920 KiB en `0x20000` y `0x200000`. El script de carga inicial comprueba la capacidad real antes de escribir un esclavo. Los offsets instalados y NVS todavía deben leerse y respaldarse por placa antes de la primera carga.

La base propuesta contiene NVS, metadatos OTA y dos particiones de aplicación. La necesidad de otras particiones depende de la configuración actual.

Cambiar la tabla instalada no se tratará como una actualización ordinaria de aplicación. La preparación inicial se hará por USB, con respaldo de identidad y configuración.

El alcance inicial evita cambios de eFuses. La selección de mecanismos irreversibles de seguridad requiere un diseño separado.

## Identidad y compatibilidad

Se debe consultar y registrar MAC, identificador físico, rol, revisión de placa, chip, versión, hash y partición activa.

La imagen debe acompañarse de un manifiesto que identifique proyecto, chip, rol, versión de protocolo, tamaño y SHA-256.

`esp_app_desc` por sí solo no identifica necesariamente el rol maestro/esclavo. Los builds del mismo proyecto pueden compartir nombre de proyecto.

Las órdenes de actualización deben estar autenticadas. SHA-256 detecta diferencias respecto del hash esperado, pero no identifica quién autorizó la imagen.

La implementación deberá elegir entre transporte autenticado o manifiesto autenticado y clave aprovisionada. Las credenciales se mantendrán fuera de Git.

Se propone conservar la identidad en NVS y respaldarla en la PC. Las migraciones de NVS deben permitir volver al firmware anterior.

Un retorno de aplicación no deshace automáticamente una migración incompatible de datos. Por eso las migraciones destructivas quedan fuera del primer incremento.

## Estados y recuperación

La secuencia propuesta es:

```text
inventario → mantenimiento → transferencia → verificación
           → arranque pendiente → autocomprobación → confirmado
```

Al fallar una transferencia, no se selecciona la imagen incompleta para arrancar. La aplicación activa debe continuar disponible.

La API de [ESP-IDF 5.5.1](https://raw.githubusercontent.com/espressif/esp-idf/v5.5.1/components/app_update/include/esp_ota_ops.h) dispone de escritura, cancelación, selección de imagen y estados OTA.

El retorno del bootloader está habilitado en las tres configuraciones de esclavos. La nueva aplicación se confirma después de inicializar y observar comunicación de control y una sesión FTM válida; una confirmación manual autenticada permite aceptar una imagen pendiente tras revisar su estado.

La autocomprobación debe tener un plazo y distinguir fallo de firmware de ausencia del maestro. Exigir conexión eterna puede impedir confirmar una imagen válida.

Se propone comprobar arranque, NVS, inicialización Wi-Fi, comunicación de control y una operación FTM válida en un plazo definido.

Una autocomprobación aprobada no valida precisión metrológica ni sincronización sísmica. Esas propiedades requieren sus propias pruebas.

## Radio, sincronización y consola

La actualización se ejecutará en mantenimiento. La PC debe marcar como interrumpida la captura y dejar de interpretar los rangos como continuos.

El protocolo USB necesita tramas separadas de los logs y CSI, límites de tamaño, secuencia, plazo, confirmaciones y control de flujo.

La UART de aplicación documentada opera a 921600 baudios. Con 8N1, el máximo teórico es 92160 bytes/s antes de sobrecargas.

Una imagen de 1 MiB necesitaría al menos 11,38 s por ese enlace. No es una predicción del tiempo OTA total.

No se propone almacenar una imagen completa en RAM del maestro. Un puente con bloques acotados o almacenamiento explícito evita esa dependencia.

Al volver a medir, se debe verificar identidad, versión, todos los pares y recuperación del sincronismo. Se registrará una nueva etapa de captura.

## Incrementos y pruebas de aceptación

| Incremento | Resultado comprobable |
|---|---|
| O0. Inventario | Flash, particiones, firmware e identidad leídos por placa. Entorno de compilación disponible. |
| O1. Base por USB | Aplicación inicial con NVS respaldada, dos espacios de aplicación y mecanismo de recuperación. |
| O2. Un esclavo por radio | Desde USB del maestro se instala una versión distinta y se verifica el hash en destino. |
| O3. Fallos controlados | Imagen truncada, incompatible y conexión interrumpida no inutilizan el nodo. Reinicio fallido retorna a la versión válida. |
| O4. Identidad y datos | Actualización y retorno conservan identidad y configuración compatible. |
| O5. Conjunto | Se actualizan esclavos de uno en uno; un nodo ausente no bloquea los demás. |
| O6. Medición recuperada | Se registran versiones, se reinicia la etapa de captura y se comprueban pares y sincronismo. |

El maestro se actualizará por USB. No necesita recepción OTA. El protocolo deberá declarar compatibilidad entre versiones durante la transición.

La primera sesión de preparación requiere acceso USB a cada placa. Después se podrá ensayar el flujo de trabajo inalámbrico completo.

El operario confirmó disponibilidad de dos conexiones USB simultáneas. Se preparará primero el maestro junto con un esclavo; luego el maestro quedará conectado y se cambiará el esclavo por los otros dos, uno a la vez. Antes de asignar roles se leerán chip, MAC y capacidad de flash, y se registrará qué placa física corresponde a cada rol. Los puertos Bluetooth no se tratarán como placas ESP32.

IA principal: Codex, modelo no reportado.  
Delegados: GPT-5.6-sol, contraste de requisitos y correcciones; Claude Sonnet, implementación OTA.  
Fallbacks: se alternaron ejecutores tras plazos máximos de implementación.
