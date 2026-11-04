from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon


OUTPUT_DIR = Path(__file__).resolve().parent


def find_chinese_font() -> str:
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "PingFang SC", "SimHei", "WenQuanYi Micro Hei"]
    for family in candidates:
        try:
            fm.findfont(fm.FontProperties(family=family), fallback_to_default=False)
            return family
        except ValueError:
            continue
    return "sans-serif"


FONT_FAMILY = find_chinese_font()

plt.rcParams.update(
    {
        "font.family": FONT_FAMILY,
        "axes.unicode_minus": False,
        "mathtext.fontset": "stix",
        "font.size": 12,
        "axes.titlesize": 15,
        "axes.labelsize": 13,
        "legend.fontsize": 10,
        "figure.dpi": 140,
        "savefig.dpi": 180,
    }
)

BLUE = "#2563EB"
RED = "#DC2626"
GREEN = "#15803D"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"
GRAY = "#4B5563"
LIGHT_BLUE = "#DBEAFE"
LIGHT_RED = "#FEE2E2"
LIGHT_GREEN = "#DCFCE7"
LIGHT_ORANGE = "#FFEDD5"


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUTPUT_DIR / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def style_axis(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)


def draw_box(ax: plt.Axes, xy, width, height, color, title, detail) -> None:
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=2,
        edgecolor=color,
        facecolor=color + "18",
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height * 0.64, title, ha="center", va="center", fontsize=18, color=color, weight="bold")
    ax.text(xy[0] + width / 2, xy[1] + height * 0.30, detail, ha="center", va="center", fontsize=12, color=GRAY)


def generate_framework() -> None:
    fig, ax = plt.subplots(figsize=(13, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("时域分析：输入、初始状态与输出", fontsize=22, weight="bold", pad=18)

    draw_box(ax, (0.03, 0.48), 0.20, 0.28, BLUE, r"输入 $x(t)$", "外部激励")
    draw_box(ax, (0.32, 0.48), 0.24, 0.28, ORANGE, r"LTI 系统 $h(t)$", "零状态输入—输出算子")
    draw_box(ax, (0.65, 0.48), 0.20, 0.28, GREEN, r"$y_{zs}(t)$", r"$x(t)*h(t)$")
    draw_box(ax, (0.32, 0.08), 0.24, 0.22, PURPLE, r"初始状态 $\mathbf{x}(0^-)$", "电容电压、电感电流等")
    draw_box(ax, (0.65, 0.08), 0.20, 0.22, RED, r"$y_{zi}(t)$", "零输入响应")

    arrows = [
        ((0.23, 0.62), (0.32, 0.62), GRAY),
        ((0.56, 0.62), (0.65, 0.62), GRAY),
        ((0.56, 0.19), (0.65, 0.19), GRAY),
        ((0.85, 0.62), (0.94, 0.46), GREEN),
        ((0.85, 0.19), (0.94, 0.38), RED),
    ]
    for start, end, color in arrows:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=18, linewidth=2.2, color=color))
    ax.text(0.965, 0.42, r"总响应" "\n" r"$y(t)=y_{zs}(t)+y_{zi}(t)$", ha="center", va="center", fontsize=15, weight="bold")
    ax.text(0.44, 0.40, r"$h(t)$ 完全描述零状态输入—输出关系；非零初始状态另由 $y_{zi}(t)$ 描述", ha="center", va="center", color=GRAY)
    save(fig, "01_framework.png")


def generate_convolution_flip() -> None:
    tau = np.linspace(-2.2, 3.2, 1600)
    h = np.where((tau >= 0) & (tau <= 1), tau, 0.0)
    h_flip = np.where((tau >= -1) & (tau <= 0), -tau, 0.0)
    t0 = 1.6
    h_shift = np.where((tau >= t0 - 1) & (tau <= t0), t0 - tau, 0.0)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    data = [
        (h, BLUE, r"原函数 $h(\tau)$", r"支撑区间 $[0,1]$"),
        (h_flip, RED, r"翻转 $h(-\tau)$", r"关于 $\tau=0$ 镜像"),
        (h_shift, GREEN, rf"平移 $h(t-\tau)$，取 $t={t0}$", rf"支撑区间 $[{t0 - 1:.1f},{t0:.1f}]$"),
    ]
    for ax, (values, color, title, note) in zip(axes, data):
        ax.plot(tau, values, color=color, linewidth=3)
        ax.fill_between(tau, 0, values, where=values > 0, color=color, alpha=0.18)
        ax.axhline(0, color="#111827", linewidth=1)
        ax.axvline(0, color="#111827", linewidth=1, alpha=0.45)
        ax.set_xlim(-2, 3)
        ax.set_ylim(-0.08, 1.15)
        ax.set_title(title, weight="bold")
        ax.text(0.5, 0.92, note, transform=ax.transAxes, ha="center", color=GRAY)
        style_axis(ax, r"积分变量 $\tau$", "幅值")
    fig.suptitle(r"卷积中的翻转和平移：$h(\tau)\rightarrow h(-\tau)\rightarrow h(t-\tau)$", fontsize=20, weight="bold", y=1.04)
    save(fig, "02a_convolution_flip.png")


def rectangle(values: np.ndarray, start: float, stop: float, amplitude: float) -> np.ndarray:
    return np.where((values >= start) & (values <= stop), amplitude, 0.0)


def generate_convolution_overlap() -> None:
    tau = np.linspace(-1.5, 4.2, 2200)
    x_tau = rectangle(tau, 0, 2, 1.5)
    sample_times = [-0.3, 0.6, 1.5, 2.4, 3.3]
    stage_titles = ["尚未进入", "进入重叠", "完全重叠", "离开重叠", "完全离开"]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10.5))
    axes = axes.ravel()
    for ax, t_value, stage in zip(axes[:5], sample_times, stage_titles):
        h_shift = rectangle(tau, t_value - 1, t_value, 2.0)
        product = x_tau * h_shift
        overlap_left = max(0.0, t_value - 1)
        overlap_right = min(2.0, t_value)
        overlap = max(0.0, overlap_right - overlap_left)
        y_value = 3.0 * overlap

        ax.plot(tau, x_tau, color=BLUE, linewidth=2.5, label=r"$x(\tau)$")
        ax.plot(tau, h_shift, color=RED, linewidth=2.5, linestyle="--", label=r"$h(t-\tau)$")
        ax.fill_between(tau, 0, product, where=product > 0, color=GREEN, alpha=0.30, label=r"乘积 $x(\tau)h(t-\tau)$")
        ax.axhline(0, color="#111827", linewidth=1)
        ax.set_xlim(-1.2, 3.6)
        ax.set_ylim(-0.15, 3.45)
        ax.set_title(rf"{stage}：$t={t_value}$，$y(t)={y_value:.1f}$", weight="bold")
        style_axis(ax, r"$\tau$", "幅值")

    axes[0].legend(loc="upper right", framealpha=0.95)
    t = np.linspace(-1, 4, 1200)
    y = np.piecewise(
        t,
        [t < 0, (t >= 0) & (t < 1), (t >= 1) & (t < 2), (t >= 2) & (t < 3), t >= 3],
        [0, lambda z: 3 * z, 3, lambda z: 3 * (3 - z), 0],
    )
    ax = axes[5]
    ax.plot(t, y, color=GREEN, linewidth=3)
    ax.fill_between(t, 0, y, color=GREEN, alpha=0.14)
    for t_value in sample_times:
        y_value = np.interp(t_value, t, y)
        ax.plot(t_value, y_value, "o", color=PURPLE, markersize=6)
        ax.vlines(t_value, 0, y_value, color=PURPLE, linestyle=":", alpha=0.55)
    ax.set_xlim(-1, 4)
    ax.set_ylim(-0.15, 3.45)
    ax.set_title(r"滑动全过程得到 $y(t)$", weight="bold")
    ax.text(0.46, 1.20, r"$3t$", color=GREEN, fontsize=13, weight="bold")
    ax.text(1.48, 3.13, r"$3$", color=GREEN, fontsize=13, weight="bold")
    ax.text(2.28, 1.20, r"$3(3-t)$", color=GREEN, fontsize=13, weight="bold")
    style_axis(ax, r"观测时刻 $t$", r"$y(t)$")
    fig.suptitle("矩形脉冲卷积：重叠长度如何变成输出", fontsize=21, weight="bold", y=1.01)
    fig.tight_layout()
    save(fig, "02b_convolution_overlap.png")


def generate_impulse_response() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.7), gridspec_kw={"width_ratios": [1.1, 0.65, 1.5]})
    t = np.linspace(-0.5, 5, 1300)
    epsilon = 0.18
    pulse = np.where((t >= 0) & (t <= epsilon), 1 / epsilon, 0.0)
    h = np.where(t >= 0, np.exp(-t), 0.0)

    axes[0].plot(t, pulse, color=BLUE, linewidth=2.5)
    axes[0].fill_between(t, 0, pulse, where=pulse > 0, color=BLUE, alpha=0.20)
    axes[0].text(0.47, 0.82, r"面积 $=1$", transform=axes[0].transAxes, color=BLUE, weight="bold")
    axes[0].set_xlim(-0.4, 1.2)
    axes[0].set_ylim(0, 6.4)
    axes[0].set_title(r"窄脉冲近似 $\delta(t)$", weight="bold")
    style_axis(axes[0], r"$t$", "幅值")

    axes[1].axis("off")
    draw_box(axes[1], (0.10, 0.32), 0.80, 0.36, ORANGE, "RC 低通", r"$h(t)$")
    axes[1].add_patch(FancyArrowPatch((0.02, 0.5), (0.10, 0.5), arrowstyle="-|>", mutation_scale=18, linewidth=2, color=GRAY))
    axes[1].add_patch(FancyArrowPatch((0.90, 0.5), (0.99, 0.5), arrowstyle="-|>", mutation_scale=18, linewidth=2, color=GRAY))

    axes[2].plot(t, h, color=RED, linewidth=3)
    axes[2].fill_between(t, 0, h, where=h > 0, color=RED, alpha=0.16)
    axes[2].axvline(1, color=GRAY, linestyle="--", alpha=0.55)
    axes[2].plot(1, np.exp(-1), "o", color=PURPLE)
    axes[2].annotate(r"$RC\,h(RC)=e^{-1}$", xy=(1, np.exp(-1)), xytext=(1.55, 0.65), arrowprops={"arrowstyle": "->", "color": GRAY})
    axes[2].set_xlim(-0.4, 5)
    axes[2].set_ylim(0, 1.1)
    axes[2].set_title(r"输出为冲激响应 $h(t)$", weight="bold")
    axes[2].text(0.48, 0.84, r"示例取 $RC=1$", transform=axes[2].transAxes, color=GRAY)
    style_axis(axes[2], r"$t/RC$", r"归一化响应 $RC\,h(t)$")

    fig.suptitle("冲激响应：系统在零状态下对单位冲激的响应", fontsize=20, weight="bold", y=1.02)
    save(fig, "03_impulse_response.png")


def generate_step_impulse_relation() -> None:
    theta = np.linspace(0, 5, 900)
    step = 1 - np.exp(-theta)
    impulse_normalized = np.exp(-theta)
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.3))

    axes[0].plot(theta, step, color=BLUE, linewidth=3)
    axes[0].fill_between(theta, 0, step, color=BLUE, alpha=0.16)
    axes[0].axhline(1, color=GRAY, linestyle="--", alpha=0.55)
    axes[0].axvline(1, color=GRAY, linestyle="--", alpha=0.55)
    axes[0].plot(1, 1 - np.exp(-1), "o", color=PURPLE)
    axes[0].annotate("63.2%", xy=(1, 1 - np.exp(-1)), xytext=(1.45, 0.46), arrowprops={"arrowstyle": "->", "color": GRAY})
    axes[0].set_title(r"单位阶跃响应 $s(t)=1-e^{-t/RC}$", weight="bold")
    style_axis(axes[0], r"无量纲时间 $\theta=t/RC$", r"$s(t)$")

    axes[1].plot(theta, impulse_normalized, color=RED, linewidth=3)
    axes[1].fill_between(theta, 0, impulse_normalized, color=RED, alpha=0.16)
    axes[1].set_title(r"归一化冲激响应 $RC\,h(t)=e^{-t/RC}$", weight="bold")
    style_axis(axes[1], r"无量纲时间 $\theta=t/RC$", r"$RC\,h(t)$")

    fig.suptitle("阶跃响应与冲激响应互为积分、微分", fontsize=20, weight="bold", y=1.03)
    fig.text(0.5, -0.01, r"$s(t)=\int_{0}^{t}h(\lambda)\,d\lambda$　　　　$h(t)=\dfrac{ds(t)}{dt}$", ha="center", fontsize=16, bbox={"boxstyle": "round,pad=0.4", "facecolor": LIGHT_ORANGE, "edgecolor": ORANGE})
    save(fig, "04_step_impulse_relation.png")


def generate_zero_state() -> None:
    t = np.linspace(0, 5, 800)
    v0 = 5.0
    vc0 = 2.0
    y_zi = vc0 * np.exp(-t)
    y_zs = v0 * (1 - np.exp(-t))
    y = y_zi + y_zs

    fig, ax = plt.subplots(figsize=(11.5, 6.3))
    ax.plot(t, y_zi, color=RED, linestyle="--", linewidth=2.5, label=r"零输入响应 $y_{zi}(t)$")
    ax.plot(t, y_zs, color=BLUE, linestyle="--", linewidth=2.5, label=r"零状态响应 $y_{zs}(t)$")
    ax.plot(t, y, color=GREEN, linewidth=3, label=r"总响应 $y(t)=y_{zi}(t)+y_{zs}(t)$")
    ax.axhline(v0, color=GRAY, linestyle=":", linewidth=2, label=r"稳态值 $V_0=5\,\mathrm{V}$")
    ax.text(0.03, 0.92, r"示例：$V_{C0}=2\,\mathrm{V}$，$V_0=5\,\mathrm{V}$，$RC=1\,\mathrm{s}$", transform=ax.transAxes, color=GRAY)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 6.1)
    ax.set_title("RC 电路的零输入响应、零状态响应与总响应", fontsize=19, weight="bold")
    style_axis(ax, r"时间 $t$（s）", "电容电压（V）")
    ax.legend(loc="center right", framealpha=0.94)
    save(fig, "05_zero_input_zero_state.png")


def generate_first_order() -> None:
    t = np.linspace(0, 5, 900)
    taus = [0.3, 0.7, 1.0, 2.0]
    colors = [RED, ORANGE, GREEN, BLUE]
    fig, ax = plt.subplots(figsize=(11.5, 6.3))
    for tau_value, color in zip(taus, colors):
        response = 1 - np.exp(-t / tau_value)
        ax.plot(t, response, color=color, linewidth=2.8, label=rf"$\tau={tau_value}\,\mathrm{{s}}$")
        ax.plot(tau_value, 1 - np.exp(-1), "o", color=color, markersize=7)
    ax.axhline(1, color=GRAY, linestyle="--", alpha=0.55, label="稳态值 1")
    ax.axhline(1 - np.exp(-1), color=GRAY, linestyle=":", alpha=0.45)
    ax.text(2.25, 0.655, r"每条曲线在 $t=\tau$ 时达到 63.2%", color=GRAY)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.08)
    ax.set_title("一阶系统：时间常数决定响应速度", fontsize=19, weight="bold")
    style_axis(ax, r"时间 $t$（s）", r"单位阶跃响应 $s(t)$")
    ax.legend(loc="lower right", framealpha=0.94)
    save(fig, "06_first_order_response.png")


def second_order_step(t: np.ndarray, zeta: float, wn: float = 1.0) -> np.ndarray:
    if zeta == 0:
        return 1 - np.cos(wn * t)
    if zeta < 1:
        wd = wn * np.sqrt(1 - zeta**2)
        phi = np.arctan2(np.sqrt(1 - zeta**2), zeta)
        return 1 - np.exp(-zeta * wn * t) / np.sqrt(1 - zeta**2) * np.sin(wd * t + phi)
    if zeta == 1:
        return 1 - (1 + wn * t) * np.exp(-wn * t)
    root = np.sqrt(zeta**2 - 1)
    s1 = -wn * (zeta - root)
    s2 = -wn * (zeta + root)
    return 1 + s2 / (s1 - s2) * np.exp(s1 * t) - s1 / (s1 - s2) * np.exp(s2 * t)


def generate_second_order() -> None:
    t = np.linspace(0, 12, 1800)
    cases = [(2.0, BLUE, "过阻尼"), (1.0, GREEN, "临界阻尼"), (0.5, ORANGE, "欠阻尼"), (0.0, RED, "无阻尼")]
    fig, ax = plt.subplots(figsize=(12.5, 7.0))
    responses = {}
    for zeta, color, label in cases:
        response = second_order_step(t, zeta)
        responses[zeta] = response
        ax.plot(t, response, color=color, linewidth=2.8, label=rf"{label}，$\zeta={zeta:g}$")

    ax.axhspan(0.98, 1.02, color=GREEN, alpha=0.10, label="±2% 调节带")
    ax.axhline(1, color=GRAY, linestyle="--", linewidth=1.6)
    zeta = 0.5
    wd = np.sqrt(1 - zeta**2)
    tp = np.pi / wd
    peak = 1 + np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2))
    ax.plot(tp, peak, "o", color=PURPLE, markersize=8)
    ax.vlines(tp, 0, peak, color=PURPLE, linestyle=":", alpha=0.65)
    ax.annotate(
        rf"$t_p={tp:.2f}$，$M_p={(peak - 1) * 100:.1f}\%$",
        xy=(tp, peak),
        xytext=(4.8, 1.55),
        arrowprops={"arrowstyle": "->", "color": PURPLE, "linewidth": 1.8},
        color=PURPLE,
        fontsize=12,
    )
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.08, 2.15)
    ax.set_title(r"标准二阶系统：阻尼比 $\zeta$ 决定阶跃响应形态", fontsize=19, weight="bold")
    style_axis(ax, r"归一化时间 $\omega_n t$", r"单位阶跃响应 $s(t)$")
    ax.legend(loc="lower right", framealpha=0.94)
    save(fig, "07_second_order_response.png")


def generate_system_classification() -> None:
    fig = plt.figure(figsize=(16, 7.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.35], wspace=0.18)
    left = fig.add_subplot(gs[0, 0])
    right = fig.add_subplot(gs[0, 1])

    left.set_xlim(0, 2)
    left.set_ylim(0, 2)
    left.axis("off")
    left.set_title("系统性质是两条独立分类轴", fontsize=18, weight="bold", pad=16)
    cells = [
        ((0, 1), LIGHT_GREEN, GREEN, "线性、时不变", "LTI：可用普通卷积描述零状态响应"),
        ((1, 1), LIGHT_RED, RED, "非线性、时不变", r"如 $y(t)=x^2(t)$"),
        ((0, 0), LIGHT_ORANGE, ORANGE, "线性、时变", r"可用二元核 $h(t,\tau)$ 描述"),
        ((1, 0), "#F3E8FF", PURPLE, "非线性、时变", r"如 $y(t)=t\,x^2(t)$"),
    ]
    for (x0, y0), fill, edge, title, detail in cells:
        patch = FancyBboxPatch((x0 + 0.06, y0 + 0.08), 0.88, 0.82, boxstyle="round,pad=0.03", facecolor=fill, edgecolor=edge, linewidth=2.2)
        left.add_patch(patch)
        left.text(x0 + 0.5, y0 + 0.62, title, ha="center", va="center", fontsize=16, color=edge, weight="bold")
        left.text(x0 + 0.5, y0 + 0.34, detail, ha="center", va="center", fontsize=11, color=GRAY, wrap=True)
    left.text(0.5, 2.01, "线性", ha="center", va="bottom", fontsize=14, color=BLUE, weight="bold")
    left.text(1.5, 2.01, "非线性", ha="center", va="bottom", fontsize=14, color=RED, weight="bold")
    left.text(-0.03, 1.5, "时不变", ha="right", va="center", fontsize=14, color=GREEN, weight="bold", rotation=90)
    left.text(-0.03, 0.5, "时变", ha="right", va="center", fontsize=14, color=ORANGE, weight="bold", rotation=90)

    right.set_xlim(0, 1)
    right.set_ylim(0, 1)
    right.axis("off")
    right.set_title("LTI 零状态响应为何能写成普通卷积", fontsize=18, weight="bold", pad=16)
    steps = [
        (0.78, LIGHT_BLUE, BLUE, r"分解输入：$x(t)=\int x(\tau)\delta(t-\tau)\,d\tau$"),
        (0.55, LIGHT_ORANGE, ORANGE, r"时不变：$\delta(t-\tau)\rightarrow h(t-\tau)$"),
        (0.32, LIGHT_GREEN, GREEN, r"线性：缩放并叠加 $x(\tau)h(t-\tau)$"),
        (0.09, "#ECFDF5", GREEN, r"$y_{zs}(t)=\int x(\tau)h(t-\tau)\,d\tau=x(t)*h(t)$"),
    ]
    for y0, fill, edge, label in steps:
        box = FancyBboxPatch((0.05, y0), 0.90, 0.14, boxstyle="round,pad=0.025", facecolor=fill, edgecolor=edge, linewidth=2)
        right.add_patch(box)
        right.text(0.5, y0 + 0.07, label, ha="center", va="center", fontsize=14, color=edge if y0 != 0.09 else GREEN, weight="bold" if y0 == 0.09 else "normal")
    for y1, y2 in [(0.78, 0.69), (0.55, 0.46), (0.32, 0.23)]:
        right.add_patch(FancyArrowPatch((0.5, y1), (0.5, y2), arrowstyle="-|>", mutation_scale=16, linewidth=1.8, color=GRAY))
    save(fig, "08_system_classification.png")


def generate_rc_memory() -> None:
    t_ms = np.linspace(0, 500, 900)
    t = t_ms / 1000
    r = 1_000.0
    c = 100e-6
    vs = 5.0
    current_ma = vs / r * np.exp(-t / (r * c)) * 1_000
    voltage = vs * (1 - np.exp(-t / (r * c)))

    fig, axes = plt.subplots(2, 1, figsize=(14, 8.7), sharex=True)
    axes[0].plot(t_ms, current_ma, color=BLUE, linewidth=3)
    axes[0].fill_between(t_ms, 0, current_ma, color=BLUE, alpha=0.10)
    axes[0].axvline(100, color=RED, linestyle="--", alpha=0.55)
    axes[0].plot(100, 5 * np.exp(-1), "o", color=PURPLE)
    axes[0].annotate(r"$t=RC=100\,\mathrm{ms}$", xy=(100, 5 * np.exp(-1)), xytext=(145, 3.1), arrowprops={"arrowstyle": "->", "color": GRAY})
    axes[0].set_title(r"充电电流 $i(t)=\dfrac{V_s}{R}e^{-t/RC}$", weight="bold")
    style_axis(axes[0], "", "电流（mA）")

    axes[1].plot(t_ms, voltage, color=ORANGE, linewidth=3)
    axes[1].fill_between(t_ms, 0, voltage, color=ORANGE, alpha=0.08)
    axes[1].axvline(100, color=RED, linestyle="--", alpha=0.55)
    axes[1].axhline(vs * (1 - np.exp(-1)), color=RED, linestyle="--", alpha=0.45)
    axes[1].plot(100, vs * (1 - np.exp(-1)), "o", color=PURPLE)
    axes[1].annotate("达到最终值的 63.2%", xy=(100, vs * (1 - np.exp(-1))), xytext=(145, 2.25), arrowprops={"arrowstyle": "->", "color": GRAY})
    axes[1].set_title(r"电容电压 $v_C(t)=\dfrac{1}{C}\int_0^t i(\lambda)\,d\lambda=V_s(1-e^{-t/RC})$", weight="bold")
    style_axis(axes[1], "时间（ms）", "电压（V）")
    fig.suptitle(r"RC 阶跃响应：电容电压累积过去的电流　$R=1\,\mathrm{k\Omega}, C=100\,\mu\mathrm{F}, V_s=5\,\mathrm{V}$", fontsize=20, weight="bold", y=1.01)
    save(fig, "09_rc_memory.png")


def generate_rc_circuit() -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    source_center = (1.4, 3.0)
    ax.add_patch(Circle(source_center, 0.72, fill=False, linewidth=2.3, edgecolor=GRAY))
    ax.text(1.4, 3.30, "+", ha="center", va="center", fontsize=18)
    ax.text(1.4, 2.70, "−", ha="center", va="center", fontsize=18)
    ax.text(0.42, 3.0, r"$V_s u(t)$", ha="center", va="center", fontsize=15, color=BLUE)

    ax.plot([1.4, 1.4, 2.5], [3.72, 4.65, 4.65], color=GRAY, linewidth=2.3)
    x_res = np.linspace(2.5, 5.4, 10)
    y_res = np.array([4.65, 4.98, 4.32, 4.98, 4.32, 4.98, 4.32, 4.98, 4.32, 4.65])
    ax.plot(x_res, y_res, color=GRAY, linewidth=2.3)
    ax.text(3.95, 5.35, r"$R$", ha="center", va="center", fontsize=18, color=ORANGE)
    ax.add_patch(FancyArrowPatch((2.0, 5.1), (2.9, 5.1), arrowstyle="-|>", mutation_scale=16, linewidth=1.8, color=BLUE))
    ax.text(2.45, 5.45, r"$i(t)$", ha="center", va="center", color=BLUE)

    ax.plot([5.4, 7.2], [4.65, 4.65], color=GRAY, linewidth=2.3)
    ax.plot([7.2, 7.2], [4.65, 3.55], color=GRAY, linewidth=2.3)
    ax.plot([6.45, 7.95], [3.55, 3.55], color=GRAY, linewidth=3)
    ax.plot([6.45, 7.95], [3.05, 3.05], color=GRAY, linewidth=3)
    ax.plot([7.2, 7.2], [3.05, 1.35], color=GRAY, linewidth=2.3)
    ax.text(8.35, 3.30, r"$C$", ha="center", va="center", fontsize=18, color=ORANGE)

    ax.plot([7.2, 1.4, 1.4], [1.35, 1.35, 2.28], color=GRAY, linewidth=2.3)
    ax.plot([6.75, 7.65], [1.35, 1.35], color=GRAY, linewidth=2)
    ax.plot([6.90, 7.50], [1.05, 1.05], color=GRAY, linewidth=1.7)
    ax.plot([7.05, 7.35], [0.78, 0.78], color=GRAY, linewidth=1.4)

    ax.add_patch(FancyArrowPatch((8.85, 3.05), (8.85, 4.65), arrowstyle="-|>", mutation_scale=16, linewidth=1.8, color=GREEN))
    ax.text(9.35, 3.85, r"$v_C(t)=y(t)$", ha="center", va="center", fontsize=15, color=GREEN, rotation=90)
    ax.set_title("RC 低通：输出取电容两端电压", fontsize=20, weight="bold", pad=10)
    save(fig, "09_rc_circuit.png")


def generate_echo_convolution() -> None:
    t = np.linspace(0, 9, 1800)
    tk = np.array([0.5, 1.6, 2.9, 4.1, 5.3])
    ak = np.array([1.0, 0.6, 0.8, 0.4, 0.9])
    colors = ["#DB2777", "#9333EA", "#0284C7", "#16A34A", "#F59E0B"]

    def impulse_response(time):
        return np.where(time >= 0, np.exp(-0.95 * time) * (1 + 0.22 * np.cos(3.1 * time)), 0.0)

    echoes = np.array([a * impulse_response(t - t0) for a, t0 in zip(ak, tk)])
    output = echoes.sum(axis=0)

    fig, axes = plt.subplots(3, 1, figsize=(15.5, 10.0), sharex=True, gridspec_kw={"height_ratios": [0.9, 1.25, 1.25]})
    markerline, stemlines, baseline = axes[0].stem(tk, ak, linefmt=GRAY, markerfmt="o", basefmt="k-")
    plt.setp(stemlines, linewidth=2.1, color=GRAY)
    plt.setp(markerline, markersize=7, markerfacecolor=GRAY, markeredgecolor=GRAY)
    for index, (t0, a, color) in enumerate(zip(tk, ak, colors)):
        axes[0].annotate(rf"$a_{index}={a:.1f}$", xy=(t0, a), xytext=(t0 + 0.18, a + 0.10), color=color, weight="bold", arrowprops={"arrowstyle": "->", "color": color})
    axes[0].set_ylim(0, 1.35)
    axes[0].set_title(r"输入是连续时间加权冲激列　$x_\delta(t)=\sum_k a_k\delta(t-t_k)$", weight="bold")
    style_axis(axes[0], "", "冲激权重")

    for index, (echo, color) in enumerate(zip(echoes, colors)):
        axes[1].plot(t, echo, color=color, linewidth=2.2, label=rf"$a_{index}h(t-t_{index})$")
    axes[1].set_ylim(0, 1.35)
    axes[1].set_title(r"每个冲激产生一个缩放、平移后的响应 $a_kh(t-t_k)$", weight="bold")
    style_axis(axes[1], "", "幅值")
    axes[1].legend(ncol=3, loc="upper right", framealpha=0.94)

    axes[2].plot(t, output, color=RED, linewidth=3)
    axes[2].fill_between(t, 0, output, color=RED, alpha=0.10)
    axes[2].text(0.5, 0.83, r"$y(t)=\sum_k a_kh(t-t_k)$", transform=axes[2].transAxes, ha="center", fontsize=17, color=RED, bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": RED, "alpha": 0.9})
    axes[2].set_ylim(0, 1.65)
    axes[2].set_title("输出是所有响应的线性叠加", weight="bold")
    style_axis(axes[2], r"时间 $t$", "幅值")
    fig.suptitle("卷积的叠加视角：每个输入冲激都触发一次系统响应", fontsize=21, weight="bold", y=1.01)
    save(fig, "10_echo_convolution.png")


def main() -> None:
    generators = [
        generate_framework,
        generate_convolution_flip,
        generate_convolution_overlap,
        generate_impulse_response,
        generate_step_impulse_relation,
        generate_zero_state,
        generate_first_order,
        generate_second_order,
        generate_system_classification,
        generate_rc_memory,
        generate_rc_circuit,
        generate_echo_convolution,
    ]
    for generator in generators:
        generator()


if __name__ == "__main__":
    main()
