# Traduce al español la copia del diagrama de calibración (el original del repo no se toca).
import re, html, sys
T = {
 'Boot, PGA-gain change,\nor calibration command': 'Arranque, cambio de\nganancia o comando',
 'Load EEPROM record for\nselected PGA gain': 'Cargar la EEPROM\nde la ganancia actual',
 'Yes': 'Sí', 'No': 'No', 'No: recalibrate': 'No: recalibrar',
 'Valid record\nand CRC?': '¿Registro y\nCRC válidos?',
 'Apply stored four-DAC code set': 'Aplicar los cuatro códigos guardados',
 'Invalid record: apply safe\nnominal DAC seeds': 'Registro inválido: aplicar\nsemillas nominales seguras',
 'Configure AMux + ADC + DFB for\nrapid offset verification': 'Configurar AMux + ADC + DFB para\nverificar rápido el offset',
 'All four stages\nwithin tolerance?': '¿Las cuatro etapas\nen tolerancia?',
 'Sequentially calibrate PGA → BP → SUM → LP:\nmeasure stage → estimate DC level → control update → write DAC,\nper stage until in-deadband and stable, or timeout\n(Section III-B)':
   'Calibrar en orden PGA → BP → SUM → LP:\nmedir etapa → estimar continua → actualizar control → escribir DAC,\nhasta quedar en banda muerta y estable, o hasta el tiempo límite',
 'If all stages are valid: save codes and CRC.\nOtherwise retain the prior EEPROM record': 'Si todas las etapas son válidas: guardar códigos y CRC.\nSi no, conservar el registro EEPROM anterior',
 'Restore acquisition routing and DFB coefficients;\nfreeze all DAC codes': 'Restaurar el ruteo de adquisición y el DFB;\ncongelar los códigos de los DAC',
 'Acquire geophone signal\n(calibration feedback inactive)': 'Adquirir la señal\n(calibración inactiva)',
 '<font style="font-size: 12px;">Orange: PSoC hardware   Blue: firmware/control<br>Red: DAC actuation/failure   Yellow: decision</font>':
   '<font style="font-size: 12px;">Naranja: hardware   Azul: firmware<br>Rojo: DAC o falla   Amarillo: decisión</font>',
 '<font style="font-size: 12px;">Orange: PSoC hardware   Blue: firmware/control Red: DAC actuation/failure   Yellow: decision</font>':
   '<font style="font-size: 12px;">Naranja: hardware   Azul: firmware   Rojo: DAC o falla   Amarillo: decisión</font>',
}
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf8').read()
miss = set()
def rep(m):
    v = html.unescape(m.group(1))
    if not v.strip(): return m.group(0)
    if v not in T: miss.add(v); return m.group(0)
    return 'value="' + html.escape(T[v], quote=True).replace('\n', '&#xa;') + '"'
out = re.sub(r'value="([^"]*)"', rep, t)
if miss: sys.exit('sin traducir: ' + repr(miss))
open(dst, 'w', encoding='utf8').write(out); print('ok')
