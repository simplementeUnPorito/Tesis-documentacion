> **OBSOLETO (2026-10-13, mañana).** Ver `ESTADO_v24.md`. Este documento tiene datos superados o incorrectos y se conserva solo como historial.

# README: Presentación v22 — Primera defensa de tesis

## 🎯 ¿Qué tienes?

Dos archivos PowerPoint listos para la defensa:

1. **`Presentacion_v22_COMPRIMIDA_INLINE_29_slides.pptx`**
   - Para la defensa de 30 minutos
   - 29 slides con ~119 pasos animados
   - Tiempo por slide: ~1 min (15 s/paso)

2. **`Presentacion_v22_LARGA_INLINE_116_slides.pptx`**
   - Respaldo completo sin animaciones
   - Todas las 116 slides lineal
   - Para referencia durante la defensa

## ✅ Checklist antes de defender

### Paso 1: Abrir en PowerPoint (AHORA)
```
1. Abre Presentacion_v22_COMPRIMIDA_INLINE_29_slides.pptx
2. Si PowerPoint pide "reparar"... ALTO. Lee "Si PowerPoint falla" abajo.
3. Si abre OK: continúa.
```

### Paso 2: Recorrer todos los clics (~30 min)
```
1. Slide 1: portada
2. Slides 2–29: recorre TODOS los clics con las flechas de animación
3. Revisa:
   - Objetos no superpuestos
   - Texto legible (no desbordado)
   - Imágenes cargan correctamente
   - Transiciones suave
   - Voces en las notas (si aplica)
4. Anota cualquier problema
```

### Paso 3: Verificar fuentes (IMPORTANTE)
```
Abre PENDIENTES_DEFENSA.md:

Para cada punto "⚠ Por confirmar":
1. Revisa el PDF citado (Foti, Ma et al., etc.)
2. Marca si VERIFICADO o RETIRAR
3. Si RETIRAR: borra o marca "por confirmar" en el slide

Criterio: No afirmar nada sin fuente escrita.
```

### Paso 4: Humanizador (OPCIONAL)
```
Si el texto de los slides o notas suena rígido:
1. Abre el skill /humanizer de Claude Code
2. Copia el texto de cada slide
3. Pasa por humanizador
4. Reemplaza en PowerPoint
5. Regenera si cambió mucho el largo
```

### Paso 5: Figuras en español (OPCIONAL)
```
Si hay figuras con etiquetas en inglés (marcadas en rojo):
- Slides larga 70, 71, 74, 94

Opción A: Regenerar con los scripts en fig/
- fig/fig_comp_curvas.py → slide 59
- fig/fig_recorte.py → slide 68
- fig/fig_geometria.py → slide 98
- fig/fig_cuna.py → slide 99

Opción B: Editar en PowerPoint directamente (más rápido)
```

### Paso 6: Ensayo con tutor + tribunal
```
1. Abre Presentacion_v22_COMPRIMIDA_INLINE_29_slides.pptx (comprimida es para la defensa)
2. Recorre todo en ~30 min
3. Anota preguntas del tribunal:
   - Brunetti: sincronización, jitter real, escalabilidad
   - Vicente: ¿señal o ruido bajo 10 Hz?, límites de apertura
   - Enrique: ruido del AFE, evidencia (modelo/simulación/medición/caracterización)
4. Revisa notas del orador en cada slide para respuestas
```

---

## 🔧 Si PowerPoint falla

### Síntoma 1: "PowerPoint found a problem and recovered..."
**Causa**: Posible conflict en IDs o animaciones complejas (zoom de matriz, build por párrafo).

**Solución**:
1. Cierra PowerPoint
2. Usa la versión LARGA en su lugar (sin animaciones complejas): `Presentacion_v22_LARGA_INLINE_116_slides.pptx`
3. Si esa tampoco funciona → error en ecuaciones OMML (ver síntoma 2)

### Síntoma 2: Fracciones o ecuaciones muestran como texto (§E_xxx§)
**Causa**: Las ecuaciones OMML no se inyectaron bien, o PowerPoint no las renderiza.

**Solución**:
1. Las ecuaciones se mostraron como texto de respaldo (eso es OK para la defensa, se entiende)
2. O: regenera con `SCALE_EQ=0` si quieres fracciones más chicas
3. O: usa la versión v17 INLINE (última que se sabe que funciona)

### Síntoma 3: Imágenes faltantes o en blanco
**Causa**: Rutas de imágenes rotas en el ZIP.

**Solución**:
1. Abre RESUMEN_ENTREGA_V22.md, busca "Si PowerPoint reporta error"
2. Regresa a las versiones v21 (última confirmada que funciona)
3. Contacta a Claude Code si la estructura cambió

---

## 📋 Archivos en esta carpeta

### Presentaciones
- `Presentacion_v22_COMPRIMIDA_INLINE_29_slides.pptx` ← **PARA LA DEFENSA**
- `Presentacion_v22_LARGA_INLINE_116_slides.pptx` ← respaldo
- `Presentacion_v21_*.pptx` ← versión anterior confirmada OK (fallback)

### Documentación
- `README_V22_FINAL.md` ← **TÚ ESTÁS AQUÍ** (instrucciones)
- `RESUMEN_ENTREGA_V22.md` ← qué se entregó y qué falta
- `PENDIENTES_DEFENSA.md` ← 50+ verificaciones de fuentes
- `ESTADO.md` ← historial completo v1–v22
- `CLAUDE_CODE_GOAL.md` ← brief original

### Multimedia
- `Ondas_sismicas_REMASTER_FHD_COMPLETO/` ← videos (no tocar)
- `toolkit/` ← código fuente (no tocar)

---

## ⏰ Tiempo estimado

- Checklist paso 1–2: **45 min** (abrir + recorrer clics)
- Checklist paso 3: **1–2 h** (verificar Foti, Ma et al., etc.)
- Checklist paso 4: **30 min** (humanizador, si aplica)
- Checklist paso 5: **1 h** (regenerar figuras, si aplica)
- Checklist paso 6: **infinito** (ensayo con tutor)

**Total mínimo**: 45 min + 1.5 h = ~2.5 h

---

## 📞 Si hay problemas

1. **PowerPoint no abre**: fallback a `Presentacion_v21_COMPRIMIDA_INLINE_29_slides.pptx`
2. **Fuente no se encuentra**: ver PENDIENTES_DEFENSA.md, marcar como "por confirmar" y aclarar en la defensa
3. **Texto desbordado / ilegible**: humanizador o editar directamente en PowerPoint
4. **Figura en inglés**: regenerar o editar en PowerPoint
5. **Animaciones raras**: descarta clics innecesarios o usa versión LARGA (sin animaciones)

---

## 🎬 Para la defensa (día D)

```
1. Lleva AMBOS archivos en USB:
   - Presentacion_v22_COMPRIMIDA_INLINE_29_slides.pptx
   - Presentacion_v22_LARGA_INLINE_116_slides.pptx

2. Copia en el proyector con 10 min de anticipación
   Prueba: abre, recorre slide 1–5, cierra

3. Abre la COMPRIMIDA para la defensa
   Usa los clics para marcar el tiempo (15 s/paso ≈ 30 min)

4. Si PowerPoint se cuelga:
   - Alt+Tab a la versión LARGA
   - O abre el PDF si existe

5. Notas del orador:
   - Están en cada slide
   - Lee antes de la defensa
   - Enfatiza diferencia entre modelo/simulación/medición/caracterización
```

---

## ✏️ Últimos retoques (si tienes tiempo)

- [ ] Confirmar fecha de presentación (portada)
- [ ] Confirmar nombres del tribunal (portada)
- [ ] Revisar español en títulos y notas
- [ ] Revisar que cada figura cite su fuente
- [ ] Print en PDF como respaldo (File > Export as PDF)

---

## 🏁 ¿Está listo?

Sí. La presentación está **lista técnicamente**:
- ✅ 29 slides comprimidas
- ✅ Tiempo ~30 min
- ✅ Todas las imágenes incluidas
- ✅ Ecuaciones nativas
- ✅ Notas del orador
- ✅ Archivos < 30 MiB

Falta **validación en PowerPoint** y **confirmación de fuentes** antes de defender.

---

**Última actualización**: 2026-10-13  
**Versión**: v22  
**Estado**: Listo para defensa (pendiente de revisión final en PowerPoint)

¡Buena suerte en la defensa! 🍀
