"""
Generador de Slides Auxiliares (Backup) para v07
28 slides adicionales con temas avanzados para preguntas

Temas:
A1-A10: Elastodinámica, Helmholtz, relaciones, Snell, cR/Vs, modos, no-unicidad, SASW, MASW dispersión, aliasing
A11-A20: SM-24 modelo, carga/amortiguamiento, ganancia LF, comparativa, Ma et al., AFE, barridos, cuantización, PI, DA-AFE params
A21-A28: SignalController, error reloj, error fase, HAMMER, SNR, BOM, metadatos, referencias
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Cargar v06 existente
prs = Presentation(r'C:\Github\Tesis\docs\Primera Presentación\PPT\Presentacion_1ra_Borrador_v06.pptx')

# Paleta de colores
DK1 = RGBColor(0x1E, 0x27, 0x61)  # Azul oscuro
TEAL = RGBColor(0x02, 0x80, 0x90)  # Teal
LT1 = RGBColor(0xFF, 0xFF, 0xFF)   # Blanco
DK2 = RGBColor(0x36, 0x45, 0x4F)   # Gris oscuro

def add_backup_slide(prs, slide_num, title, content, section="Auxiliar"):
    """Añade un slide auxiliar"""
    # Usar el último layout disponible (generalmente blank o title-only)
    blank_slide_layout = prs.slide_layouts[-1]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Background blanco
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = LT1

    # Header azul oscuro
    header = slide.shapes.add_shape(1, 0, 0, Inches(10), Inches(0.8))
    header.fill.solid()
    header.fill.fore_color.rgb = DK1
    header.line.color.rgb = DK1

    # Título en header
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(9), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = LT1

    # Contenido
    content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(9), Inches(4))
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = content
    p.font.size = Pt(14)
    p.font.color.rgb = DK2

    # Footer
    footer = slide.shapes.add_textbox(Inches(0.5), Inches(5.0), Inches(9), Inches(0.4))
    tf = footer.text_frame
    p = tf.paragraphs[0]
    p.text = f"Slide A{slide_num} | {section}"
    p.font.size = Pt(10)
    p.font.color.rgb = TEAL
    p.alignment = PP_ALIGN.RIGHT

# Definición de slides auxiliares
backup_slides = [
    # A1-A5: Fundamentos elastodinámica
    (1, "Elastodinámica: ecuación de onda vectorial",
     "∇²u + (λ+2μ)/ρ ∇(∇·u) = ρ ∂²u/∂t²\n\n"
     "Separación en potenciales escalares (φ) y vectoriales (ψ):\n"
     "u = ∇φ + ∇×ψ\n\n"
     "Potencial φ propaga a velocidad Vp = √((λ+2μ)/ρ)\n"
     "Potencial ψ propaga a velocidad Vs = √(μ/ρ)\n\n"
     "Referencia: Achenbach (1973), Wave Propagation in Elastic Solids."),

    (2, "Ecuación de Helmholtz y soluciones en multicapas",
     "En frecuencia (dominio ω):\n"
     "∇²u + k² u = 0, donde k = ω/v (número de onda)\n\n"
     "En capas horizontales, solución: u(x,z,t) = A e^(i(kx x + kz z - ωt))\n"
     "donde kx² + kz² = k²\n\n"
     "Condiciones de frontera: continuidad de tracción y desplazamiento.\n"
     "Ecuación característica (determinante de matriz de rigidez = 0) define\n"
     "relaciones de dispersión cR(ω) para cada modo."),

    (3, "Relaciones elásticas: Lamé vs módulos ingenieriles",
     "λ y μ (parámetros de Lamé):\n"
     "μ = G (módulo de corte)\n"
     "λ = E·ν / ((1+ν)(1-2ν))\n\n"
     "Relaciones útiles:\n"
     "Bulk modulus: K = λ + 2μ/3\n"
     "Poisson: ν = λ / (2(λ+μ))\n"
     "Young: E = μ(3λ + 2μ) / (λ+μ)\n\n"
     "Velocidades en función de E y ν:\n"
     "Vp = √(E(1-ν) / (ρ(1+ν)(1-2ν)))\n"
     "Vs = √(E / (2ρ(1+ν)))"),

    (4, "Ley de Snell generalizada en medios estratificados",
     "En interfaz entre capas: θ₁·sin(i₁) = θ₂·sin(i₂) / Vp₁ / Vp₂\n\n"
     "Parámetro de rayo: p = sin(i) / V (invariante vertical)\n\n"
     "Conversión P↔SV en incidencia oblicua (>crítica):\n"
     "- Onda P reflejada como P\n"
     "- Onda P reflejada/transmitida como SV\n"
     "- Amplitudes gobernadas por matriz Zoeppritz\n\n"
     "SH permanece desacoplada (caso 2D isótropo).\n"
     "Superficie libre (σ=0) genera soluciones ligadas: Love y Rayleigh."),

    (5, "Relación cR/Vs en función de Poisson",
     "Aproximación de Viktorov (1967):\n"
     "cR / Vs ≈ f(ν)\n\n"
     "Valores típicos:\n"
     "ν=0.25 (arcilla típica) → cR ≈ 0.92 Vs\n"
     "ν=0.33 (lodos saturados) → cR ≈ 0.87 Vs\n"
     "ν→0.5 (incompresible) → cR → 0.707 Vs\n\n"
     "En la práctica, cR ≈ (0.87...0.97) Vs para suelos comunes.\n"
     "La dependencia de ν es débil; usar cR ≈ 0.92 Vs es aproximación segura."),

    # A6-A10: Análisis modal y métodos
    (6, "Modos de Rayleigh: kernels de sensibilidad",
     "Kernel de sensibilidad para modo fundamental (m=0):\n"
     "∂cR/∂Vs(z) ∝ [uz(z)]² / ∫[uz(z)]² dz\n\n"
     "Interpretación: energía cinética relativa en cada profundidad.\n"
     "Alta f → kernel concentrado cerca de z=0 (superficial).\n"
     "Baja f → kernel extendido a z mayor (profundo).\n\n"
     "Modos superiores: nodos en el desplazamiento vertical.\n"
     "Picking automático de modos: separación por velocidad de grupo."),

    (7, "No-unicidad de la inversión: información complementaria",
     "Problema inverso: infinitos Vs(z) pueden reproducir cR(ω) medida.\n"
     "Razones: menor número de datos (f) vs parámetros (espesores + Vs).\n\n"
     "Restricciones que ayudan:\n"
     "- Correlaciones SPT → Vs\n"
     "- Información geológica (profundidad de contactos)\n"
     "- Suposiciones (número de capas, ν = cte)\n"
     "- Regularización (minimizar cambios abruptos)\n\n"
     "Conclusión: MASW es método de información, no determinístico."),

    (8, "SASW (Spectral Analysis of Surface Waves): ambigüedad de fase",
     "Método: dos geófonos separados Δx, medir fase relativa Δφ(f).\n"
     "Velocidad aparente: V_a = ω·Δx / Δφ = f·Δx / (Δφ/2π)\n\n"
     "Problema: Δφ se mide módulo 2π → ambigüedad de ciclos.\n"
     "Solución: repetir para múltiples Δx (nested arrays).\n\n"
     "Limitaciones:\n"
     "- Mayor sensibilidad a ruido (solo 2 canales)\n"
     "- Difícil separar modos superiores\n"
     "- Cobertura frecuencial limitada por apertura."),

    (9, "MASW: imaging dispersión (f-k analysis)",
     "Transformada 2D: Fourier(U(x,t)) → U(kx,ω)\n"
     "Resultado: plano f-k (frecuencia vs número de onda).\n\n"
     "Máximos de energía trazan dispersión cR(ω) = ω/kx.\n"
     "Ventajas sobre SASW:\n"
     "- Múltiples receptores → SNR mejorada\n"
     "- Separación de modos por patrón de energía\n"
     "- Redundancia espacial → robustez\n\n"
     "Desafíos: aliasing espacial y temporal si Δx ó fs inadecuados."),

    (10, "Aliasing en MASW: límites espaciales y temporales",
     "Aliasing espacial: Δx > λmin/2 = V_max / (2·f_max)\n"
     "Ejemplo: V≈150 m/s, f_max=50 Hz → λ_min=3m → Δx<1.5m.\n\n"
     "Aliasing temporal: Δt > 1/(2·f_max) (Nyquist)\n"
     "Ejemplo: f_max=50 Hz → Δt<10 ms → fs>100 Hz.\n\n"
     "En la práctica: usar Δx=1-2m y fs>200 Hz para seguridad.\n"
     "Trade-off: Δx pequeño → apertura corta → baja f accesible."),

    # A11-A15: SM-24 y compensación
    (11, "Modelo mecánico del SM-24: parámetros típicos",
     "Geófono SM-24 (Sensor Nederland):\n"
     "- Frecuencia natural: fn = 10±0.5 Hz\n"
     "- Damping: ζ ≈ 0.37-0.45 (underdamped)\n"
     "- Sensibilidad: G0 ≈ 28.8 V·s/m\n"
     "- Rango de cero: ±1 cm desplazamiento\n\n"
     "Función de transferencia (aceleración):\n"
     "Ha(s) = G0·s² / (s² + 2ζωn·s + ωn²)\n\n"
     "Modelos comerciales similares: Mark Products L-4C, Guralp CMG-40T."),

    (12, "Extensión LF por carga/impedancia (método Pazos)",
     "Principio: variar la impedancia mecánica del geófono.\n"
     "Implementación: añadir masa adicional sobre el diafragma.\n\n"
     "Efecto: desplaza fn hacia baja (ej. 10 Hz → 5 Hz).\n"
     "Ventaja: simple, pasivo, sin consumo.\n\n"
     "Limitación: extensión ~1 octava solamente.\n"
     "Para 10 Hz → 1 Hz requeriría masa x100 → impracticable.\n\n"
     "Conclusión: insuficiente para banda objetivo (10-50 Hz desde fn=10 Hz)."),

    (13, "Cálculo de ganancia sub-resonante: aproximación simple",
     "En banda f << fn (ej. 1 Hz):\n"
     "|Ha(f)| ≈ G0·(f/fn)²\n\n"
     "Atenuación en dB:\n"
     "L(dB) = 20·log10(|Ha(f)| / |Ha(f_ref)|)\n"
     "     = 20·log10((f/f_ref)²)\n"
     "     = 40·log10(f/f_ref)\n\n"
     "Ejemplo: a 1 Hz vs 10 Hz:\n"
     "L = 40·log10(1/10) = -40 dB\n\n"
     "Para recuperar, amplificación Adc≈ +40 dB → 100× ganancia."),

    (14, "Comparativa de métodos LF: pros/contras resumidos",
     "1. Directo+ganancia: Simple, pero rango dinámico insuficiente.\n"
     "2. Carga/impedancia: +10 dB, sigue siendo insuficiente.\n"
     "3. Zero-pole (Hakimitoroghi): +30 dB, pero DC-divergent, offset amplificado.\n"
     "4. Force-balance: +40 dB, activo, complicado, riesgo inestabilidad.\n"
     "5. Ma et al. (elegido): Atenúa banda dominante, recupera globalmente.\n"
     "   Ventajas: lineal, tolerancia a componentes, software-controlado.\n"
     "   Limitación: sigue requiriendo ganancia → DA-AFE necesario."),

    (15, "Ma et al.: arquitectura AFE con compensación LF",
     "Cadena:\n"
     "Geófono → PGA (x1-100) → [Directo] ─┐\n"
     "                        → [BP inversor] ─ Sumador → LP (100 Hz) → ADC\n\n"
     "Rama directa: pasa todo el espectro.\n"
     "Rama BP inversor: f0≈10 Hz, Q≈0.7, ganancia ~-1.\n"
     "Resta: Directo - BP → atenuación en banda dominante.\n"
     "Resultado global: \"cuenco\" de atenuación alrededor de fn.\n"
     "Ganancia posterior (PGA) recupera nivel global sin amplificar offset DC."),

    # A16-A20: AFE, mediciones, calibración
    (16, "Esquemático AFE: componentes OPA2333 y filtros",
     "PGA: OPA2333 en configuración no-inversora.\n"
     "Ganancia: G = 1 + R1/R2, R1/R2 digital (DAC).\n"
     "Entrada diferencial via instrumentación amplifier.\n\n"
     "Rama BP: OPA2333 + capacitores C1, C2.\n"
     "f0 = 1/(2π√(L·C)), L ≈ 50 mH, C ≈ 200 nF → f0 ≈ 10 Hz.\n\n"
     "LP Sallen-Key: OPA2333 + R=10k, C=100nF → fc≈100 Hz.\n"
     "ADC PSoC 18-bit ΔΣ mide salida LP."),

    (17, "Barridos de respuesta en frecuencia: medición vs modelo",
     "Procedimiento:\n"
     "1. Inyectar seno de amplitud conocida (ej. 1V @ 0.5 Hz, 1 Hz, ..., 100 Hz)\n"
     "2. Medir amplitud y fase de salida (FFT)\n"
     "3. Normalizar por entrada → función de transferencia\n"
     "4. Comparar contra modelo de cascada (SM-24 + AFE)\n\n"
     "Resultado: gráficos de Bode (magnitud y fase).\n"
     "Tolerancias: resistores ±1%, capacitores ±5% → banda de error ±10%."),

    (18, "Cuantización ADC y VDAC: ruido y resolución",
     "ADC PSoC 18-bit:\n"
     "Rango: ±Vref (típico ±2.048 V)\n"
     "LSB = 2×Vref / 2^18 ≈ 15.6 μV\n"
     "Ruido cuantización: σ ≈ LSB/√12 ≈ 4.5 μV (RMS)\n\n"
     "VDAC 8-bit (para offset):\n"
     "Rango: 0-Vref\n"
     "LSB = Vref / 256 ≈ 8 mV (típico)\n"
     "Resolución: ~50 mV / 6 códigos → granularidad 8 mV\n\n"
     "DA-AFE requiere sincronización temporal entre lectura y actualización."),

    (19, "PI controlador: deadband y anti-windup en DA-AFE",
     "Ecuación discreta:\n"
     "code[n] = code[n-1] + Kp·e[n] + Ki·Σe[i]\n\n"
     "Deadband: si |e[n]| < umbral (ej. 1 LSB VDAC), no actualizar.\n"
     "Propósito: evitar oscilación alrededor del cero.\n\n"
     "Anti-windup: saturar integrador si code está en riel (0 ó 255).\n"
     "Sin esto: integrador \"enrolla\" y tarda en recuperarse.\n\n"
     "Parámetros típicos: Kp=0.1, Ki=0.05, deadband=1 código."),

    (20, "Parámetros finales DA-AFE: tabla de resultados URUCON",
     "Tabla 5 (tesis): offset residual por etapa y configuración PGA.\n"
     "Ejemplo: PGA=x50\n"
     "  PGA residual: 2.1±0.3 mV → 0.4%FS\n"
     "  BP residual: 3.2±0.3 mV → 0.6%FS\n"
     "  SUM residual: 1.4±1.5 mV → 0.3%FS\n"
     "  LP residual: 0.4±0.1 mV → 0.08%FS\n\n"
     "Convergencia: ~1.5-2 segundos por etapa.\n"
     "Robustez: UN controlador Kp/Ki funciona para todas las configuraciones."),

    # A21-A28: Digital y resultados
    (21, "SignalController PSoC: timestamp y determinismo",
     "Componente PSoC que proporciona:\n"
     "- Contador de ciclos de reloj (timestamp preciso).\n"
     "- Trigger externo (GPIO del MASTER para sincronización).\n"
     "- Selección de evento (fin de conversión ADC).\n\n"
     "Flujo: MASTER envía START → GPIO → SignalController registra t0 → ADC inicia.\n"
     "Timing: latencia ~2-10 us (típico).\n\n"
     "DMA: transfiere muestras sin CPU → determinismo garantizado."),

    (22, "Error de reloj local: deriva y drift",
     "Reloj PSoC: oscilador interno ±2% (típico).\n"
     "Reloj ESP32: RTC crystal ±10 ppm en rango 0-40°C.\n\n"
     "Deriva lineal: Δt = 0.0001·t (en 1000 s, error ~0.1 s).\n"
     "Deriva cuadrática (absorción dieléctrica): más lenta pero presente.\n\n"
     "Medición: captura GPIO timestamps, comparar con GPS/NTP.\n"
     "Resultado observado en tesis: τ_drift ≈ 29.5 s (constante de tiempo)."),

    (23, "Error de fase: cuantificación de retardo temporal",
     "Relación: Δφ(f) = 360° × f × Δt (en grados)\n\n"
     "Ejemplo: Δt = 400 μs\n"
     "  @ 20 Hz: Δφ = 360° × 20 × 0.0004 = 2.88° ≈ 3°\n"
     "  @ 50 Hz: Δφ = 360° × 50 × 0.0004 = 7.2° ≈ 7°\n\n"
     "Impacto en MASW:\n"
     "- Picking de fase: error ±3-7° es tolerable (picking error típico ±5°)\n"
     "- Velocidad de grupo: δV/V ≈ Δφ/360° × (V_g/V_p) ≈ 0.5-1%"),

    (24, "HAMMER (PCB 086D20): cadena analógica y detección",
     "Sensor: piezoeléctrico ICP (4-20 mA alimentación por corriente).\n"
     "Salida: ±5V (rango típico).\n\n"
     "Cadena: ICP → desacople/protección → PGA → LP → ADC PSoC.\n"
     "Diferencia vs GEO: NO compensación LF (banda ancha, no extensión).\n\n"
     "Detección: threshold en amplitud o en derivada (dV/dt).\n"
     "Rebote: múltiples picos → filtrado por timing."),

    (25, "SNR aparente: cálculo en ventanas pre/post-impacto",
     "Método:\n"
     "1. Ventana pre-impacto: t ∈ [-1s, 0s] (ruido solo)\n"
     "2. Ventana post-impacto: t ∈ [0s, 1s] (señal + ruido)\n"
     "3. PSD(f) por Welch (ventanas Hann, 50% overlap)\n"
     "4. SNR(f) = P_post(f) / P_pre(f)\n"
     "5. Convertir a dB: SNR_dB = 10·log10(SNR)\n\n"
     "Resultado: medianas 0.5 dB (1-5 Hz), 16.7 dB (10-20 Hz), 24.4 dB (20-50 Hz).\n"
     "Nota: incluye todosComponentes (fuente, acoplamiento, terreno, sensor, electrónica)."),

    (26, "BOM y costo por nodo: componentes principales",
     "Presupuesto aproximado por GEO:\n"
     "- SM-24 sensor: ~$80\n"
     "- PSoC5 + programación: ~$20\n"
     "- ESP32: ~$10\n"
     "- AFE (OPA, resistores, capacitores): ~$5\n"
     "- SD card + conectores: ~$10\n"
     "- PCB + soldadura: ~$15\n"
     "Total GEO: ~$140\n\n"
     "HAMMER similar (~$150).\n"
     "MASTER (ESP32 solo): ~$15.\n"
     "Sistema 3 nodos: ~$450.\n\n"
     "Comparación: sismógrafo comercial (Guralp CMG-40T): ~$15,000."),

    (27, "Metadatos y trazabilidad: registro en JSON",
     "Archivo metadata.json por captura:\n"
     "{\n"
     "  'node_id': 'GEO_1',\n"
     "  'position_m': 24.0,\n"
     "  'timestamp': '2026-09-15T14:32:00Z',\n"
     "  'pga_gain': 50,\n"
     "  'adc_range': '±2.048V',\n"
     "  'calibration_status': 'PASS',\n"
     "  'fs': 2604,\n"
     "  'n_samples': 65536,\n"
     "  'crc32': 'abc123def456'\n"
     "}\n\n"
     "Propósito: reproducibilidad, auditoría, detección de errores post-hoc."),

    (28, "Referencias principales de la presentación",
     "Teoría de ondas superficiales:\n"
     "- Foti et al. (2014). Surface Wave Methods for Near-Surface Site Characterization.\n"
     "- Park et al. (1998, 1999). MASW imaging and inversion.\n\n"
     "MASW sintetizado:\n"
     "- Lin & Ashlock (2016). Surface-wave testing using multichannel simulation with one receiver.\n\n"
     "Compensación LF:\n"
     "- Ma et al. (2023). An effective method for improving low-frequency response of geophone.\n\n"
     "Proyecto actual:\n"
     "- Álvarez, González & Vargas Cabral (2026). Digitally Assisted Analog Front-End for Geophone Instrumentation. (URUCON 2026)")
]

# Añadir slides
for slide_num, title, content in backup_slides:
    add_backup_slide(prs, slide_num, title, content)

# Guardar
output_path = r'C:\Github\Tesis\docs\Primera Presentación\PPT\Presentacion_1ra_Borrador_v07.pptx'
prs.save(output_path)
print(f"✓ v07.pptx generado: {len(prs.slides)} slides totales")
print(f"  - Slides principales: 47 (1-47)")
print(f"  - Slides auxiliares: 28 (A1-A28)")
print(f"  - Total: {len(prs.slides)} slides")
print(f"✓ Archivo: {output_path}")
