# Propuesta de corrección: `latex/secciones/04_arquitectura.tex`

**Aplicada el 2026-10-13, 13:50** (sin commitear; compila sin errores). Para deshacerla: `git -C docs checkout -- "Primera Presentación/latex/secciones/04_arquitectura.tex"`.

Motivo: según el autor, es falso que cambiar el rango del ADC invalide la calibración de offset, y es falso que la EEPROM se indexe por ganancia y rango (se indexa solo por ganancia). Los slides ya lo reflejan (larga 77, notas); el documento de tesis todavía dice lo contrario en dos lugares.

**Verificado en el firmware:** `src/firmware/psoc/AcondicionamientoAnalogico.cydsn/psoc_nv.h:11` («Layout EEPROM v3 (1 fila de 16 bytes por ganancia PGA 0..8)») y `psoc_nv.c:64` (`EEPROM_Write(row0, NV_ROW_FOR_GAIN(pga_code))`). La EEPROM se indexa solo por ganancia; el rango no interviene.

## 1. Párrafo de las líneas 249–255

```diff
-Un detalle de implementaci\'on que conviene registrar: el cambio de rango
-\textbf{invalida la calibraci\'on de \emph{offset} vigente}, porque el punto de operaci\'on
-\'optimo depende del fondo de escala. Por eso la persistencia en EEPROM del DA-AFE se
-indexa por c\'odigo de ganancia y de rango, y no como un \'unico valor global
-(\S\ref{sec:arq-daafe}). La verificaci\'on de que la conmutaci\'on entre rangos preserva
-la coherencia del sistema fue parte de la auditor\'ia pre-campo, con
-\textbf{49 de 49 transiciones correctas} (\S\ref{sec:resultados}).
+La calibraci\'on de \emph{offset} se guarda por c\'odigo de ganancia del PGA: la
+persistencia en EEPROM del DA-AFE se indexa s\'olo por ganancia
+(\S\ref{sec:arq-daafe}). El rango del ADC se elige despu\'es de la cadena anal\'ogica y
+no cambia el punto de operaci\'on de sus etapas, de modo que conmutarlo no invalida la
+calibraci\'on vigente. La verificaci\'on de que la conmutaci\'on entre rangos preserva
+la coherencia del sistema fue parte de la auditor\'ia pre-campo, con
+\textbf{49 de 49 transiciones correctas} (\S\ref{sec:resultados}).
```

**Actualización (verificado en el firmware):** el criterio de aceptación sí está en cuentas del ADC (`calibration.c:1095`, `cal_pi_deadband_counts`), pero durante la calibración el firmware **fuerza la configuración de ±2,5 V** (`psoc_adc.c:102`, `psoc_adc_select_calibration_config` → `psoc_adc_cal_override(1)` → `ADC_CF_2V5`). Por eso el rango de captura no afecta la calibración. El texto de arriba quedó superado por esta justificación, que es la que usa el archivo corregido:

**Archivo ya corregido (nuevo, el original no se tocó):** `04_arquitectura_CORREGIDO.tex` en esta carpeta. Para aplicarlo, reemplazá `latex/secciones/04_arquitectura.tex` por esta copia; `diff` muestra que solo cambian las dos zonas.

## 2. Tabla, línea 296

```diff
-Persistencia & Registro en EEPROM con CRC, indexado por c\'odigo de ganancia y rango \\
+Persistencia & Registro en EEPROM con CRC, indexado por c\'odigo de ganancia \\
```

## Para aplicarla
Editar a mano las dos zonas, o pedirle a Claude Code que aplique este parche y compile el LaTeX.
