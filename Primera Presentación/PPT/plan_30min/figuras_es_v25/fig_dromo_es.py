# Dromocrónica de dos capas (esquema propio, valores ilustrativos), con la onda de cabeza
# punteada antes de la distancia crítica, como en Haeni et al. (1987), fig. 2.
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

V1, V2, z = 500.0, 1500.0, 3.0                      # m/s, m/s, m (ilustrativos)
ic = np.arcsin(V1 / V2)
ti = 2 * z * np.cos(ic) / V1                        # tiempo de intercepto (s)
xcr = 2 * z * np.tan(ic)                            # distancia crítica (m)
xc = 2 * z * np.sqrt((V2 + V1) / (V2 - V1))         # distancia de cruce (m)
X = 20.0
ms = 1e3
plt.rcParams.update({'font.family': 'Calibri', 'font.size': 15, 'mathtext.fontset': 'cm'})
fig, ax = plt.subplots(figsize=(2.628 * 4.2, 4.2), dpi=150)
R, B = '#D62728', '#1F3FBF'
xd = np.linspace(0, 12.5, 2); ax.plot(xd, xd / V1 * ms, color=R, lw=2.4, zorder=2)
ax.plot([0, xcr], [ti * ms, (ti + xcr / V2) * ms], color=B, lw=2, ls=':', zorder=2)
xh = np.linspace(xcr, X, 2); ax.plot(xh, (ti + xh / V2) * ms, color=B, lw=2.4, zorder=2)
g = np.arange(1, X + 0.1, 1.0)
gd = g[g <= 12]; ax.plot(gd, gd / V1 * ms, 'o', color=R, ms=6, zorder=3)
gh = g[g >= xcr]; ax.plot(gh, (ti + gh / V2) * ms, 'o', color=B, ms=6, zorder=3)
yc = xc / V1 * ms
ax.plot([xc], [yc], 'o', color='k', ms=8, zorder=4)
ax.plot([xc, xc], [0, yc], 'k--', lw=1.2); ax.plot([xcr, xcr], [0, (ti + xcr / V2) * ms], color='0.4', ls='--', lw=1.0)
ax.annotate('', xy=(0.15, ti * ms), xytext=(0.15, 0), arrowprops=dict(arrowstyle='<->', lw=1.3))
ax.text(0.32, 6.2, 'tiempo de\nintercepto\n$t_i$', fontsize=13, va='bottom')
ax.text(xcr + 0.15, 0.5, 'distancia\ncrítica', fontsize=13, color='0.3', va='bottom')
ax.text(xc + 0.25, 5.5, 'distancia de cruce\n$x_c$', fontsize=14)
ax.text(9.6, 20.5, 'Onda directa\n$(t = x/V_1)$', color=R, fontsize=15, fontweight='bold', ha='right')
ax.text(16.5, 18.2, 'Onda refractada\n$(t = t_i + x/V_2)$', color=B, fontsize=15, fontweight='bold', ha='center')
ax.text(xcr * 0.5, ti * ms + 1.9, 'no se registra', color=B, fontsize=11, ha='center', style='italic')
ax.set_xlim(0, X + 0.6); ax.set_ylim(0, 26)
ax.set_xlabel('Distancia ($x$)', fontsize=17); ax.set_ylabel('Tiempo ($t$)', fontsize=17)
ax.set_xticks([]); ax.set_yticks([])
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig('../img/final/refr_dromo_c.png', dpi=150, facecolor='white')
print('ti=%.1f ms xcr=%.2f m xc=%.2f m' % (ti * ms, xcr, xc))
