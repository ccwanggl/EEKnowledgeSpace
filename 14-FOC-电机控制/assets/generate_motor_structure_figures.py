"""生成《电机结构、绕组与磁路基础》中的可复现示意图。

只依赖 Pillow，运行后会覆盖同目录下的三张教学图片。图中所有相轴、
机械角和电角均按文档中的约定绘制，避免把电角误画成机械角。
"""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASSET_DIR = Path(__file__).resolve().parent
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

COLORS = {
    "ink": "#20242b",
    "grey": "#d9dde3",
    "dark_grey": "#7c8794",
    "a": "#2878b5",
    "b": "#e7831a",
    "c": "#2f9c58",
    "north": "#d94444",
    "south": "#6550a6",
    "d": "#c93636",
    "q": "#e28a13",
    "path": "#8155a7",
    "note": "#5d6672",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    index = 1 if bold else 0
    return ImageFont.truetype(FONT_PATH, size=size, index=index)


def polar(center: tuple[float, float], radius: float, degree: float) -> tuple[float, float]:
    angle = degree * pi / 180
    return center[0] + radius * cos(angle), center[1] - radius * sin(angle)


def centered_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fnt, fill: str = COLORS["ink"]):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=fnt, fill=fill)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill: str, width: int = 7):
    draw.line((start, end), fill=fill, width=width)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    left = (end[0] - 22 * ux + 10 * uy, end[1] - 22 * uy - 10 * ux)
    right = (end[0] - 22 * ux - 10 * uy, end[1] - 22 * uy + 10 * ux)
    draw.polygon([end, left, right], fill=fill)


def ring_sector(draw: ImageDraw.ImageDraw, center, outer: int, inner: int, start: float, end: float, fill: str):
    box_outer = (center[0] - outer, center[1] - outer, center[0] + outer, center[1] + outer)
    box_inner = (center[0] - inner, center[1] - inner, center[0] + inner, center[1] + inner)
    draw.pieslice(box_outer, start=-end, end=-start, fill=fill, outline=COLORS["ink"], width=2)
    draw.pieslice(box_inner, start=-end, end=-start, fill="white", outline="white")


def draw_cross_section() -> None:
    image = Image.new("RGB", (1500, 1120), "white")
    draw = ImageDraw.Draw(image)
    center = (590, 590)

    # Stator core and twelve neutral slots. The phase axes are explained separately,
    # so this drawing never pretends that colored blocks alone specify a winding table.
    draw.ellipse((70, 70, 1110, 1110), fill=COLORS["grey"], outline=COLORS["ink"], width=6)
    draw.ellipse((210, 210, 970, 970), fill="white", outline=COLORS["ink"], width=5)
    for slot in range(12):
        a0 = slot * 30 + 3
        ring_sector(draw, center, 520, 385, a0, a0 + 21, "#f4f5f6")
    centered_text(draw, (270, 180), "定子铁心、齿与 12 个槽", font(23), COLORS["note"])

    # Rotor and four alternating surface magnets.
    draw.ellipse((300, 300, 880, 880), fill="#c8ccd1", outline=COLORS["ink"], width=5)
    for degree, pole, color in [(90, "N", COLORS["north"]), (0, "S", COLORS["south"]), (-90, "N", COLORS["north"]), (180, "S", COLORS["south"])]:
        ring_sector(draw, center, 292, 228, degree - 26, degree + 26, color)
        label = polar(center, 260, degree)
        centered_text(draw, label, pole, font(29, True), "white")
    draw.ellipse((535, 535, 645, 645), fill="#777d86", outline=COLORS["ink"], width=4)

    # d axis aligns with the north-pole center. q is 90 electrical degrees later,
    # which is 45 mechanical degrees for two pole pairs.
    d_end = polar(center, 440, 90)
    q_end = polar(center, 440, 45)
    arrow(draw, center, d_end, COLORS["d"])
    arrow(draw, center, q_end, COLORS["q"])
    centered_text(draw, (720, 210), "d 轴：永磁体磁链轴", font(27, True), COLORS["d"])
    centered_text(draw, (880, 270), "q 轴：d 轴 + 90° 电角", font(26, True), COLORS["q"])

    # Reference phase axis, mechanical position, and the conversion needed by Park.
    a_end = polar(center, 360, 0)
    draw.line((center, a_end), fill=COLORS["dark_grey"], width=4)
    centered_text(draw, (790, 625), "固定机械参考线", font(22), COLORS["dark_grey"])
    draw.arc((410, 410, 770, 770), start=-90, end=0, fill="#4a5564", width=5)
    centered_text(draw, (760, 435), "θm", font(27, True), "#4a5564")

    draw.rounded_rectangle((1030, 360, 1450, 700), radius=18, fill="#f9f6df", outline="#99916b", width=3)
    centered_text(draw, (1240, 418), "Park 变换使用的角度", font(25, True))
    centered_text(draw, (1240, 485), "θe = p · θm + θoffset", font(31, True), COLORS["ink"])
    centered_text(draw, (1240, 545), "p = 2；方向与零位须校准", font(24), COLORS["note"])
    centered_text(draw, (1240, 606), "实际实现中按 2π 取模", font(24), COLORS["note"])
    centered_text(draw, (1240, 903), "槽内实际绕组还需要槽号、相别和 +/− 极性表", font(24), COLORS["note"])
    centered_text(draw, (1240, 946), "本图只说明结构与坐标轴，不替代绕组展开图", font(24), COLORS["note"])
    image.save(ASSET_DIR / "pmsm_cross_section.png", optimize=True)


def draw_phase_axes() -> None:
    image = Image.new("RGB", (1600, 960), "white")
    draw = ImageDraw.Draw(image)
    centered_text(draw, (800, 55), "三相绕组基波相轴：机械角与电角不能混用", font(39, True))
    centered_text(draw, (800, 106), "以 2 极对电机为例：120° 电角 = 60° 机械角", font(27), COLORS["note"])

    left = (410, 500)
    right = (1190, 500)
    for center, title in [(left, "机械空间中的相轴"), (right, "电角坐标中的相轴")]:
        draw.ellipse((center[0] - 275, center[1] - 275, center[0] + 275, center[1] + 275), outline=COLORS["ink"], width=5)
        centered_text(draw, (center[0], 173), title, font(31, True))

    # Mechanical axes for p=2. Choose B=-60 deg and C=+60 deg to keep a symmetrical layout.
    for name, degree, color, note in [
        ("A", 0, COLORS["a"], "0°"),
        ("B", -60, COLORS["b"], "−60°"),
        ("C", 60, COLORS["c"], "+60°"),
    ]:
        end = polar(left, 235, degree)
        arrow(draw, left, end, color)
        text_pos = polar(left, 305, degree)
        centered_text(draw, text_pos, f"{name} 相轴\n{note} 机械角", font(24, True), color)
    centered_text(draw, (410, 795), "相轴的机械夹角 = 120° / p", font(28, True), COLORS["ink"])

    # The same three axes in electrical coordinates.
    for name, degree, color, note in [
        ("A", 0, COLORS["a"], "0°"),
        ("B", -120, COLORS["b"], "−120°"),
        ("C", 120, COLORS["c"], "+120°"),
    ]:
        end = polar(right, 235, degree)
        arrow(draw, right, end, color)
        text_pos = polar(right, 305, degree)
        centered_text(draw, text_pos, f"{name} 相轴\n{note} 电角", font(24, True), color)
    centered_text(draw, (1190, 795), "三相基波相轴相差 120° 电角", font(28, True), COLORS["ink"])

    draw.rounded_rectangle((250, 855, 1350, 932), radius=16, fill="#f4f6f8", outline="#c4cad1", width=2)
    centered_text(draw, (800, 893), "12 槽、4 极、3 相时 q = Qs/(2pm) = 1；实际槽配还必须标出每个线圈边的相别与正负极性。", font(23), COLORS["note"])
    image.save(ASSET_DIR / "three_phase_winding_layout.png", optimize=True)


def draw_saliency() -> None:
    image = Image.new("RGB", (1600, 980), "white")
    draw = ImageDraw.Draw(image)
    centered_text(draw, (800, 55), "SPMSM 与 IPMSM：d/q 轴磁路和电感差异", font(40, True))
    centered_text(draw, (800, 108), "电感关系来自转子磁路各向异性，不应简单归因于物理气隙是否均匀", font(25), COLORS["note"])

    left, right = (420, 500), (1180, 500)
    for center, title in [(left, "SPMSM：近似非凸极"), (right, "IPMSM：转子磁路凸极")]:
        centered_text(draw, (center[0], 172), title, font(32, True))
        draw.ellipse((center[0] - 250, center[1] - 250, center[0] + 250, center[1] + 250), fill="#eed59f", outline=COLORS["ink"], width=5)
        draw.ellipse((center[0] - 80, center[1] - 80, center[0] + 80, center[1] + 80), fill="#8a8e94", outline=COLORS["ink"], width=4)

    # Surface magnets: magnetic path around d and q is similar in the simplified model.
    ring_sector(draw, left, 278, 226, -25, 25, COLORS["north"])
    ring_sector(draw, left, 278, 226, 155, 205, COLORS["south"])
    arrow(draw, left, polar(left, 320, 0), COLORS["d"], width=6)
    arrow(draw, left, polar(left, 320, 90), COLORS["q"], width=6)
    centered_text(draw, (420, 790), "表贴磁钢，简化模型中 Ld ≈ Lq", font(27, True), COLORS["ink"])
    centered_text(draw, (420, 835), "高速弱磁时仍需注入负 id", font(24), COLORS["note"])

    # Interior magnets and flux barriers. d-axis crosses the magnets/barriers;
    # q-axis predominantly crosses steel, hence usually Ld < Lq.
    draw.rounded_rectangle((right[0] - 180, right[1] - 75, right[0] - 45, right[1] + 75), radius=15, fill=COLORS["north"], outline=COLORS["ink"], width=4)
    draw.rounded_rectangle((right[0] + 45, right[1] - 75, right[0] + 180, right[1] + 75), radius=15, fill=COLORS["south"], outline=COLORS["ink"], width=4)
    draw.line((right[0] - 210, right[1] - 105, right[0] + 210, right[1] - 105), fill="#f0f2f5", width=22)
    draw.line((right[0] - 210, right[1] + 105, right[0] + 210, right[1] + 105), fill="#f0f2f5", width=22)
    arrow(draw, right, polar(right, 320, 0), COLORS["d"], width=6)
    arrow(draw, right, polar(right, 320, 90), COLORS["q"], width=6)
    centered_text(draw, (1180, 780), "d 轴：穿过磁钢/磁障，等效磁阻较大，Ld 较小", font(25, True), COLORS["d"])
    centered_text(draw, (1180, 825), "q 轴：主要经过硅钢铁心，等效磁阻较小，Lq 较大", font(25, True), COLORS["q"])
    centered_text(draw, (1180, 870), "通常 Ld < Lq，磁阻转矩与 (Ld − Lq) id iq 有关", font(24), COLORS["note"])

    image.save(ASSET_DIR / "spmsm_vs_ipmsm_saliency.png", optimize=True)


if __name__ == "__main__":
    draw_cross_section()
    draw_phase_axes()
    draw_saliency()
    print(f"Generated figures in {ASSET_DIR}")
