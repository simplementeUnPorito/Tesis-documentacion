# Ensayo exploratorio de impactos aproximadamente periódicos

## Propósito

Registro exploratorio que motivó la idea de acumular energía coherente mediante una fuente periódica o de cadencia controlada. No constituye todavía una validación Mini-Sosie ni una caracterización cuantitativa de la fuente.

## Contexto informado por Elías

- **Lugar:** frente al Laboratorio LED, en la zona comprendida entre el camino y el estacionamiento.
- **Distancia fuente–GEO:** estimada inicialmente en unos 20 m; una medición aproximada en Google Maps dio 26,8 m. Debe reportarse como aproximadamente 20–27 m mientras no exista relevamiento preciso.
- **Fuente:** mazo utilizado en los ensayos previos.
- **Cadencia buscada:** aproximadamente un golpe por segundo, producida manualmente y con variación apreciable.
- **Duración mostrada:** 60 s.
- **Canales:** HAMMER y `Geo1` fueron adquiridos juntos. El sistema trata al generador/HAMMER como otro esclavo y sincroniza el inicio de muestreo de los nodos.
- **Datos conservados:** sólo estas capturas de pantalla; no se localizó el registro crudo asociado.
- **Observación separada:** los picos cercanos a 0,5, 1 y 2 Hz mencionados por Elías provienen de otra medición, no necesariamente de las capturas conservadas aquí.

## Archivos

1. `01_senal_geo1_60s_impactos_aprox_1Hz.png`: señal cruda `Geo1 (S1)` durante la ventana de 60 s.
2. `02_espectro_geo1_60s_impactos_aprox_1Hz.png`: vista espectral conservada junto con la señal.

## Interpretación permitida

Las capturas documentan que se realizó una excitación manual repetida y que la señal observada presenta una distribución espectral de banda limitada, una caída en alta frecuencia y estructura compatible con impactos repetidos. El ensayo constituye una motivación experimental cualitativa para diseñar una fuente periódica controlada.

## Lo que no demuestran

- ganancia de SNR frente a igual número de golpes no periódicos;
- generación o propagación confirmada de ondas en 0,5, 1 o 2 Hz;
- función de transferencia pasa-bajos propia de la fuente;
- firma de fuerza absoluta del mazo;
- repetibilidad temporal o energética del impacto;
- precisión metrológica de sincronización entre nodos;
- mejora de profundidad MASW.

El espectro observado combina la firma del impacto, el acoplamiento, la propagación por el suelo, el geófono, el acondicionamiento analógico, la digitalización y la visualización. Para separar estos efectos se debe repetir el ensayo conservando las señales crudas de HAMMER y GEO, tiempos de impacto, configuración de ganancia, distancia y una comparación A/B controlada.
