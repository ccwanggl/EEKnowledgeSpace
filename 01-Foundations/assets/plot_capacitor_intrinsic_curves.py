"""Generate intrinsic characteristic curve figures for 002-电容.md.

Outputs (next to this script):
- capacitor-qv-vs-resistor-vi.png : resistor static V-I line vs capacitor static Q-V line
- capacitor-vi-ellipse.png        : sinusoidal V-I Lissajous ellipse, pure vs series ESR
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
GRAY = "#666666"

# ---------------------------------------------------------------- figure 1
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))

R = 100.0
v = np.linspace(0.0, 10.0, 200)
ax = axes[0]
ax.plot(v, v / R, color="#d62728", lw=2)
ax.set_title("Resistor: static V-I characteristic")
ax.set_xlabel("Voltage v (V)")
ax.set_ylabel("Current i (A)")
ax.grid(True, alpha=0.3)
ax.annotate(
    f"slope = 1/R = {1/R:.3g} S",
    xy=(6.0, 6.0 / R),
    xytext=(2.0, 0.075),
    arrowprops=dict(arrowstyle="->", color=GRAY),
    color=GRAY,
)
ax.text(
    0.98, 0.04, "i is fixed by v alone (static)",
    transform=ax.transAxes, ha="right", fontsize=9, color=GRAY,
)

C = 100e-6
ax = axes[1]
q_mc = C * v * 1e3  # mC
ax.plot(v, q_mc, color="#1f77b4", lw=2)
ax.fill_between(v, 0, q_mc, color="#1f77b4", alpha=0.15)
ax.set_title("Capacitor: static Q-V characteristic")
ax.set_xlabel("Voltage v (V)")
ax.set_ylabel("Charge q (mC)")
ax.grid(True, alpha=0.3)
ax.annotate(
    f"slope = C = {C * 1e6:.0f} µF",
    xy=(7.0, C * 7.0 * 1e3),
    xytext=(2.0, 0.8),
    arrowprops=dict(arrowstyle="->", color=GRAY),
    color=GRAY,
)
ax.text(
    0.98, 0.04,
    f"area under line = stored energy E = ½Cv² = {0.5 * C * 10.0**2 * 1e3:.1f} mJ at 10 V",
    transform=ax.transAxes, ha="right", fontsize=9, color=GRAY,
)

fig.tight_layout()
fig.savefig(OUT / "capacitor-qv-vs-resistor-vi.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------- figure 2
f0 = 1e3
w = 2 * np.pi * f0
C2 = 1e-6
V0 = 1.0
ESR = 80.0
t = np.linspace(0, 2 * np.pi, 600)

fig, axes = plt.subplots(1, 2, figsize=(11, 5.0))


def draw_ellipse(ax, esr, color, title, notes):
    z = esr + 1.0 / (1j * w * C2)
    i0 = V0 / abs(z)
    phi = -np.angle(z)  # current phase lead
    vv = V0 * np.sin(t)
    ii = i0 * np.sin(t + phi) * 1e3  # mA
    ax.plot(vv, ii, color=color, lw=2)
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.plot(V0, 0, "o", color=color, ms=4)
    ax.annotate("V₀", xy=(V0, 0), xytext=(V0 + 0.06, 0.3), color=color)
    ax.plot(0, i0 * 1e3, "o", color=color, ms=4)
    ax.set_xlim(-1.4, 2.8)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_ylim(-7.6, 7.6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("v (V)")
    ax.set_ylabel("i (mA)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.text(0.60, 0.96, notes, transform=ax.transAxes, va="top", fontsize=9, color=GRAY)


draw_ellipse(
    axes[0], 0.0, "#2ca02c",
    "Pure capacitor: V-I Lissajous (sinusoid)",
    "phase lead = 90°\nno static V-I curve",
)
delta = np.degrees(np.arctan(w * C2 * ESR))
draw_ellipse(
    axes[1], ESR, "#ff7f0e",
    "Capacitor + series ESR",
    f"ESR = {ESR:.0f} Ω, lead φ ≈ {90 - delta:.0f}° (< 90°)\n"
    f"loss angle δ ≈ {delta:.0f}°, tan δ = ωC·ESR ≈ {w * C2 * ESR:.2f}",
)

fig.text(
    0.5, 0.01,
    f"Example: C = {C2 * 1e6:.0f} µF, f = {f0 / 1e3:.0f} kHz, V₀ = {V0:.0f} V. "
    "Illustrative only; ellipse aspect scales with 1/ωC.",
    ha="center", fontsize=8, color=GRAY,
)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT / "capacitor-vi-ellipse.png", dpi=150)
plt.close(fig)

print("wrote", OUT / "capacitor-qv-vs-resistor-vi.png")
print("wrote", OUT / "capacitor-vi-ellipse.png")
