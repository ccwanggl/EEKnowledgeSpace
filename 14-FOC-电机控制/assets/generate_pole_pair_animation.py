"""生成 3 极对电机的机械角与电角动画，只依赖 Pillow。"""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASSET_DIR = Path(__file__).resolve().parent
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
INK = "#20242b"
NORTH = "#d94444"
SOUTH = "#6550a6"
MECH = "#2878b5"
ELEC = "#e7831a"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size, index=1 if bold else 0)


def polar(center: tuple[float, float], radius: float, degree: float) -> tuple[float, float]:
    angle = degree * pi / 180
    return center[0] + radius * cos(angle), center[1] - radius * sin(angle)


def centered_text(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill: str = INK) -> None:
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=fnt, fill=fill)


def arrow(draw: ImageDraw.ImageDraw, start, end, color: str, width: int = 7) -> None:
    draw.line((start, end), fill=color, width=width)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    draw.polygon(
        [
            end,
            (end[0] - 20 * ux + 9 * uy, end[1] - 20 * uy - 9 * ux),
            (end[0] - 20 * ux - 9 * uy, end[1] - 20 * uy + 9 * ux),
        ],
        fill=color,
    )


def annular_sector(draw: ImageDraw.ImageDraw, center, outer: int, inner: int, start: float, end: float, fill: str) -> None:
    outer_box = (center[0] - outer, center[1] - outer, center[0] + outer, center[1] + outer)
    inner_box = (center[0] - inner, center[1] - inner, center[0] + inner, center[1] + inner)
    draw.pieslice(outer_box, start=-end, end=-start, fill=fill, outline=INK, width=2)
    draw.pieslice(inner_box, start=-end, end=-start, fill="#d9dde3", outline="#d9dde3")


def dial(draw: ImageDraw.ImageDraw, center, color: str, label: str, angle: float, readout: str) -> None:
    radius = 130
    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=color, width=5)
    for degree, text in [(0, "0°"), (90, "90°"), (180, "180°"), (270, "270°")]:
        p0 = polar(center, radius - 10, degree)
        p1 = polar(center, radius + 10, degree)
        draw.line((p0, p1), fill=INK, width=3)
        centered_text(draw, polar(center, radius + 28, degree), text, font(18), INK)
    arrow(draw, center, polar(center, radius - 24, angle), color, width=6)
    centered_text(draw, (center[0], center[1] - 178), label, font(25, True), color)
    centered_text(draw, (center[0], center[1] + 178), readout, font(24, True), color)


def frame(mechanical_angle: float) -> Image.Image:
    image = Image.new("RGB", (1500, 780), "white")
    draw = ImageDraw.Draw(image)
    centered_text(draw, (750, 46), "3 极对：一圈机械角对应三圈电角", font(36, True))
    centered_text(draw, (750, 92), "θe = p · θm，p = 3；电角按 360° 取模显示", font(24), "#5d6672")

    center = (360, 420)
    draw.ellipse((100, 160, 620, 680), fill="#d9dde3", outline=INK, width=5)
    draw.ellipse((195, 255, 525, 585), fill="#eef0f3", outline=INK, width=4)
    for slot in range(12):
        degree = slot * 30
        x, y = polar(center, 226, degree)
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill="#aeb6c0", outline=INK)
    draw.ellipse((240, 300, 480, 540), fill="#bfc4ca", outline=INK, width=4)
    for index in range(6):
        degree = mechanical_angle + index * 60
        color = NORTH if index % 2 == 0 else SOUTH
        pole = "N" if index % 2 == 0 else "S"
        annular_sector(draw, center, 155, 112, degree - 18, degree + 18, color)
        centered_text(draw, polar(center, 134, degree), pole, font(22, True), "white")
    arrow(draw, center, polar(center, 180, mechanical_angle), MECH, width=5)
    centered_text(draw, (360, 720), "定子固定；红/紫永磁体随转子转动", font(22), "#5d6672")

    electrical_angle = (3 * mechanical_angle) % 360
    dial(draw, (840, 400), MECH, "机械角 θm", mechanical_angle % 360, f"θm = {mechanical_angle:03.0f}°")
    dial(draw, (1280, 400), ELEC, "电角 θe", electrical_angle, f"θe = {3 * mechanical_angle:03.0f}°")
    centered_text(draw, (1050, 690), "右侧电角表盘显示取模后的指针，读数保留未取模的累计电角。", font(22), "#5d6672")
    return image


if __name__ == "__main__":
    frames = [frame(index * 10) for index in range(37)]
    frames[0].save(
        ASSET_DIR / "pole_pairs_3_angle_animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=90,
        loop=0,
        optimize=True,
    )
    print(f"Generated {ASSET_DIR / 'pole_pairs_3_angle_animation.gif'}")
