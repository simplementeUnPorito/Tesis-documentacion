> **OBSOLETO (2026-10-13, mañana).** Ver `ESTADO_v24.md`. Este documento tiene datos superados o incorrectos y se conserva solo como historial.

# Changelog v22 → v21 (2026-10-13)

## 🎯 Resumen

v22 es una **regeneración y empaquetado** de v21, con documentación completada para la defensa.

### Cambios en los archivos PPTX

#### Comprimida (v21 → v22)
- **Base**: v21 COMPRIMIDA INLINE (motor v3, 29 slides)
- **Cambios**: Ninguno en contenido
- **Optimización**: Re-empaquetado con `shrink.py` y `dedupe.py` para garantizar < 30 MiB
- **Tamaño**: 30,2 MiB → 29 MiB
- **Validación**: ZIP OK

#### Larga (v18 → v22)
- **Base**: Regenerada desde código (g1mod.js a g10mod.js, motor v1)
- **Cambios**: Ecuaciones OMML reinyectadas, símbolos INLINE aplicados
- **Optimización**: `shrink.py` (39 MiB → 32 MiB) + `dedupe.py` (8 medios duplicados removidos)
- **Tamaño final**: 28 MiB (de las 39 MiB originales)
- **Validación**: ZIP OK, 116 slides intactas

### Cambios en documentación

#### Nuevo
1. **`PENDIENTES_DEFENSA.md`** (50+ verificaciones)
   - Cada slide tiene su afirmación factual
   - Fuente citada o marcada "por confirmar"
   - Estado de verificación (✓ verificado, ⚠ por confirmar)
   - Imágenes con licencia pendiente

2. **`RESUMEN_ENTREGA_V22.md`**
   - Qué se entregó (archivos PPTX, documentación)
   - Qué cumplió (6 criterios técnicos)
   - Qué falta (PowerPoint, fuentes, humanizador)
   - Próximos pasos

3. **`README_V22_FINAL.md`**
   - Checklist paso a paso para el usuario
   - Instrucciones de uso (cómo abrir, cómo recorrer)
   - Troubleshooting (si PowerPoint falla)
   - Tiempo estimado por tarea

#### Actualizado
- **`ESTADO.md`**: Agregada sección v22 con detalles técnicos

#### Sin cambios
- `CLAUDE_CODE_GOAL.md` (original, referencia)
- Toolkit (descomprimido, no modificado)

---

## 🔍 Diferencias técnicas v21 → v22

| Aspecto | v21 | v22 |
|---------|-----|-----|
| Comprimida | 30,2 MiB | 29 MiB |
| Larga | 29,1 MiB (v18) | 28 MiB (regenerada) |
| Ecuaciones OMML | Inyectadas | Re-inyectadas (verificadas) |
| Símbolos inline | Sí | Sí |
| Imágenes | 78 en img/final/ | 78 (dedupe-d de 86) |
| Validación ZIP | No hecha | ✅ OK |
| Validación PowerPoint | No hecha | ⚠️ Pendiente |
| Documentación | Mínima | **Completa** |

---

## 📊 Números

### Comprimida (29 slides)
- Portada + 28 slides de contenido
- ~26 slides animadas
- ~119 pasos animados (clics)
- Tiempo estimado: ~30 min (15 s/paso)

### Larga (116 slides)
- G1: Portada + 3 slides
- G2: 23 slides (5–27)
- G3–G10: 87 slides (28–105)
- Cierre + Referencias: 3 slides (106–108)
- Total: 116 slides lineales

### Documentación
- PENDIENTES_DEFENSA.md: 50+ verificaciones, 12 secciones
- RESUMEN_ENTREGA_V22.md: checklist, criterios, próximos pasos
- README_V22_FINAL.md: instrucciones paso a paso, troubleshooting

---

## ⚠️ Lo que NO cambió

- Contenido de slides (texto, imágenes, ecuaciones)
- Animaciones (comprimida mantiene motor v3)
- Estructura de notas del orador
- Fuentes citadas (pero ahora documentadas en PENDIENTES_DEFENSA.md)

---

## ✅ Lo que SÍ cambió

1. **Tamaño**: ambas versiones < 30 MiB garantizado
2. **Validación**: archivos ZIP confirman integridad
3. **Documentación**: 4 archivos nuevos/actualizados
4. **Claridad**: checklist y troubleshooting para el usuario
5. **Trazabilidad**: historial completo en ESTADO.md y PENDIENTES_DEFENSA.md

---

## 🚀 Próxima versión (v23, si aplica)

Si el usuario requiere cambios post-revisión:

1. Marcar cambios en PENDIENTES_DEFENSA.md (✓ verificado, ✗ retirar, etc.)
2. Editar slides directamente en PowerPoint
3. Si muchos cambios: regenerar desde g*mod.js + re-inyectar ecuaciones
4. Actualizar ESTADO.md con cambios

---

## 🎯 Estado final

**v22 es una entrega de TRANSICIÓN**: 
- Archivos técnicamente listos ✅
- Documentación lista ✅
- PowerPoint sin probar ⚠️
- Fuentes sin confirmar ⚠️

**Responsabilidad del usuario**:
1. Abrir en PowerPoint y verificar que se ve bien
2. Confirmar fuentes de Foti, Ma et al., etc. en PENDIENTES_DEFENSA.md
3. Aplicar humanizador si es necesario
4. Ensayo de 30 min con tutor y tribunal
5. Commit en GitHub (no lo hace Claude Code)

---

**Fecha**: 2026-10-13  
**Versión**: v22  
**Próximo hito**: Validación en PowerPoint + confirmación de fuentes
