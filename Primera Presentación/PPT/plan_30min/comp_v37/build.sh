set -e
cd "/c/Github/Tesis/docs/Primera Presentación/PPT/plan_30min"
python comp_v37/compose.py Presentacion_v29_COMPRIMIDA_INLINE_29_slides.pptx /c/Users/elias/AppData/Local/Temp/claude/C--Github-Tesis/45c8af74-faf3-403b-9070-3e975279fe68/scratchpad/tk/build/choreo.json Presentacion_v37_LARGA_INLINE_126_slides.pptx comp_v37/textmap.json comp_v37/spec.py Presentacion_v41_COMPRIMIDA_INLINE_32_slides.pptx /c/Users/elias/AppData/Local/Temp/claude/C--Github-Tesis/45c8af74-faf3-403b-9070-3e975279fe68/scratchpad/tk/build | tail -1
python fix_content_types.py Presentacion_v41_COMPRIMIDA_INLINE_32_slides.pptx | tail -1
python /c/Users/elias/.claude/skills/synced/c0e92010-952e-46de-9a07-99b57b496ab1_4913805d-2bfd-4a99-8793-b4fff2563a7c/pptx/scripts/office/validate.py Presentacion_v41_COMPRIMIDA_INLINE_32_slides.pptx | tail -1
python check_anim_todas.py Presentacion_v41_COMPRIMIDA_INLINE_32_slides.pptx | tail -1
