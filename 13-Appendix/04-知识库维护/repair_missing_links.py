from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import re


VAULT = Path(__file__).resolve().parents[2]
EXCLUDED = {".obsidian", ".trash", "copilot", "Clippings", "Excalidraw"}
EXCLUDED_FILES = {"99-历史总索引归档.md", "修改摘要.md", "000-修改摘要.md"}
WIKI = re.compile(r"(?<!!)\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]")

TARGETS = {
    "01-Foundations/01-数学与物理基础/README": "01-Foundations/01-数学与物理基础/000-README",
    "001-数学基础": "01-Foundations/01-数学与物理基础/000-README",
    "002-物理基础": "01-Foundations/01-数学与物理基础/000-README",
    "003-数字信号处理基础": "01-Foundations/05-信号与系统/000-信号与系统",
    "04-ADC与DAC基础": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "06-ADC与DAC基础": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "08-ADC与DAC基础": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "08-数据转换器": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "ADC": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "DAC": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "ADC 与 DAC 设计": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "001-ADC核心概念与架构": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "002-ADC驱动与代码示例": "01-Foundations/06-ADC与DAC基础/009-采集软件、校准与数据处理",
    "06-测量与仪器基础": "01-Foundations/07-测量与仪器基础/000-测量与仪器基础",
    "07-控制理论": "15-双控（控制理论与控制工程）/00-README",
    "控制理论": "15-双控（控制理论与控制工程）/00-README",
    "04-常微分方程基础": "01-Foundations/01-数学与物理基础/004-常微分方程与状态模型",
    "06-数字信号处理": "01-Foundations/05-信号与系统/000-信号与系统",
    "03-模拟电路": "02-Analog-Electronics/00-README",
    "02-模拟电路基础": "02-Analog-Electronics/01-模拟电路基础/001-核心概念",
    "模拟电路": "02-Analog-Electronics/00-README",
    "09-电磁兼容": "06-PCB-Design/04-信号完整性与EMC/003-EMC电磁兼容",
    "10-通信原理": "05-Communication/00-README",
    "通信系统": "05-Communication/00-README",
    "电路基础理论": "01-Foundations/02-电路基础理论/000-README",
    "半导体器件": "01-Foundations/04-电子元器件/000-README",
    "RLC谐振": "01-Foundations/03-电路分析方法/011-交流功率、谐振与阻抗匹配",
    "压电传感器": "08-Sensors-Actuators/01-传感器接口/01-传感器接口",
    "电容": "01-Foundations/04-电子元器件/002-电容",
    "电容器": "01-Foundations/04-电子元器件/002-电容",
    "电感": "01-Foundations/04-电子元器件/003-电感",
    "二极管": "01-Foundations/04-电子元器件/004-二极管",
    "晶体管": "01-Foundations/04-电子元器件/005-BJT晶体管",
    "稳压器": "01-Foundations/04-电子元器件/008-稳压器",
    "去耦设计": "06-PCB-Design/02-信号完整性基础/004-去耦设计",
    "节点电压法": "01-Foundations/03-电路分析方法/003-节点电压法与改进节点法",
    "PCB": "06-PCB-Design/00-README",
    "PCB传输线": "06-PCB-Design/02-信号完整性基础/002-高速信号基础",
    "传输线": "06-PCB-Design/02-信号完整性基础/002-高速信号基础",
    "传输线理论": "06-PCB-Design/02-信号完整性基础/002-高速信号基础",
    "眼图": "06-PCB-Design/02-信号完整性基础/001-核心问题",
    "电源完整性": "06-PCB-Design/02-信号完整性基础/001-核心问题",
    "高速设计": "06-PCB-Design/04-信号完整性与EMC/002-高速设计规则",
    "Buck/Boost变换器": "07-Power-Management/02-DC-DC转换器/02-DC-DC转换器",
    "开关电源": "07-Power-Management/02-DC-DC转换器/02-DC-DC转换器",
    "滤波器": "02-Analog-Electronics/03-滤波器设计/001-滤波器类型",
    "模拟滤波器设计": "02-Analog-Electronics/03-滤波器设计/001-滤波器类型",
    "数字滤波器设计": "15-双控（控制理论与控制工程）/05-数字控制与离散系统/004-数字滤波器设计",
    "IIR 滤波器设计": "15-双控（控制理论与控制工程）/05-数字控制与离散系统/004-数字滤波器设计",
    "FIR 滤波器设计": "15-双控（控制理论与控制工程）/05-数字控制与离散系统/004-数字滤波器设计",
    "传感器": "08-Sensors-Actuators/00-README",
    "传感器接口设计": "08-Sensors-Actuators/01-传感器接口/01-传感器接口",
    "无线通信": "05-Communication/07-无线通信-BLE-WiFi-Matter/000-无线通信",
    "图像处理": "11-Machine-Vision/000-README",
    "图像频域处理": "11-Machine-Vision/000-README",
    "实时操作系统": "10-RTOS与系统/00-README",
    "嵌入式软件开发": "01-Foundations/08-嵌入式C编程/000-嵌入式C编程",
    "嵌入式 DSP 实现": "01-Foundations/08-嵌入式C编程/000-嵌入式C编程",
    "嵌入式 DSP 开发": "01-Foundations/08-嵌入式C编程/000-嵌入式C编程",
    "信号与系统": "01-Foundations/05-信号与系统/000-信号与系统",
    "单位阶跃函数": "01-Foundations/05-信号与系统/001-信号、系统与LTI基础",
    "Nyquist 采样定理": "01-Foundations/05-信号与系统/010-采样、混叠与重建",
    "Z 变换": "01-Foundations/05-信号与系统/011-Z变换与离散时间系统",
    "离散时间傅里叶变换": "01-Foundations/05-信号与系统/011-Z变换与离散时间系统",
    "05-信号与系统/02-采样定理": "01-Foundations/05-信号与系统/010-采样、混叠与重建",
    "06-正弦稳态相量分析": "01-Foundations/03-电路分析方法/010-正弦稳态相量分析",
    "001-分析流程与方法论": "01-Foundations/03-电路分析方法/001-分析流程、参考方向与结果校验",
    "002-核心分析方法详解": "01-Foundations/03-电路分析方法/000-电路分析方法",
    "003-分析陷阱与学习方法": "01-Foundations/03-电路分析方法/012-方法选择、错误诊断与仿真验证",
    "004-电路定理": "01-Foundations/03-电路分析方法/000-电路分析方法",
    "005-动态电路时域分析": "01-Foundations/03-电路分析方法/008-一阶动态电路分析",
    "006-正弦稳态相量分析": "01-Foundations/03-电路分析方法/010-正弦稳态相量分析",
    "007-分析方法综合选择": "01-Foundations/03-电路分析方法/012-方法选择、错误诊断与仿真验证",
    "005-信号与系统概述": "01-Foundations/05-信号与系统/001-信号、系统与LTI基础",
    "08-ADC与DAC基础": "01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础",
    "05-通信协议概述": "05-Communication/01-通信协议概述/000-通信协议概述",
    "003-电容": "01-Foundations/04-电子元器件/002-电容",
    "001-核心概念与基本定律": "01-Foundations/02-电路基础理论/000-README",
    "002-电路分析流程与交流": "01-Foundations/02-电路基础理论/000-README",
    "003-RC电路时域与拓扑": "01-Foundations/02-电路基础理论/008-一阶RC与RL电路",
    "004-RC电路时域与拓扑": "01-Foundations/02-电路基础理论/008-一阶RC与RL电路",
    "003-滤波器设计": "02-Analog-Electronics/03-滤波器设计/001-滤波器类型",
    "machine_vision_learning": "11-Machine-Vision/000-README",
}

METHOD_TARGETS = {
    "基尔霍夫电流定律": "01-Foundations/02-电路基础理论/003-基尔霍夫定律与电路拓扑",
    "基尔霍夫电压定律": "01-Foundations/02-电路基础理论/003-基尔霍夫定律与电路拓扑",
    "002-基尔霍夫定律": "01-Foundations/02-电路基础理论/003-基尔霍夫定律与电路拓扑",
    "003-等效变换法": "01-Foundations/03-电路分析方法/002-等效变换与源变换",
    "004-节点电压法": "01-Foundations/03-电路分析方法/003-节点电压法与改进节点法",
    "005-网孔电流法": "01-Foundations/03-电路分析方法/004-网孔电流法与支路法",
    "006-叠加定理": "01-Foundations/03-电路分析方法/005-叠加、替代与拓扑定理",
    "007-戴维南-诺顿定理": "01-Foundations/03-电路分析方法/006-戴维南、诺顿与端口等效",
    "008-最大功率传输定理": "01-Foundations/03-电路分析方法/007-最大功率传输与负载匹配",
    "009-动态电路时域分析": "01-Foundations/03-电路分析方法/008-一阶动态电路分析",
    "010-正弦稳态相量分析": "01-Foundations/03-电路分析方法/010-正弦稳态相量分析",
    "011-s域分析": "01-Foundations/05-信号与系统/007-拉普拉斯变换与系统函数",
    "012-频率响应与滤波器": "01-Foundations/05-信号与系统/009-频率响应与Bode图",
}
for name, target in list(METHOD_TARGETS.items()):
    METHOD_TARGETS[f"{name}/"] = target
TARGETS.update(METHOD_TARGETS)

DELINK_UNRESOLVED: set[str] = set()


def rel(path: Path) -> str:
    return path.relative_to(VAULT).as_posix()


def is_content(path: Path) -> bool:
    return path.name not in EXCLUDED_FILES and not any(
        part in EXCLUDED for part in path.relative_to(VAULT).parts
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    notes = [path for path in VAULT.rglob("*.md") if is_content(path)]
    invalid_targets = sorted(
        {target for target in TARGETS.values() if not (VAULT / f"{target}.md").exists()}
    )
    if invalid_targets:
        raise SystemExit("invalid mapped targets: " + ", ".join(invalid_targets))
    by_relative = {rel(path).lower(): path for path in notes}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in notes:
        by_stem[path.stem.lower()].append(path)

    changed_files: list[Path] = []
    mapped = 0
    delinked = 0

    def resolves(source: Path, raw: str) -> bool:
        lowered = raw.lower().rstrip("/")
        for key in (lowered, f"{lowered}.md"):
            if key in by_relative:
                return True
        if "/" in raw:
            candidate = source.parent / raw.rstrip("/")
            for item in (candidate, candidate.with_suffix(".md")):
                try:
                    key = item.resolve().relative_to(VAULT).as_posix().lower()
                except ValueError:
                    continue
                if key in by_relative:
                    return True
        return len(by_stem.get(lowered, [])) == 1

    for source in notes:
        old = source.read_text(encoding="utf-8-sig")
        lines = old.splitlines(keepends=True)
        in_fence = False
        changed = False

        def replace(match: re.Match[str]) -> str:
            nonlocal mapped, delinked, changed
            raw = match.group(1).strip().replace("\\", "/")
            heading = match.group(2) or ""
            alias = match.group(3)
            lookup = raw.rstrip("/")
            target = TARGETS.get(lookup)
            if target:
                mapped += 1
                changed = True
                return f"[[{target}{heading}|{alias or raw}]]"
            if rel(source) in DELINK_UNRESOLVED and not resolves(source, raw):
                delinked += 1
                changed = True
                return alias or raw.rstrip("/")
            return match.group(0)

        for index, line in enumerate(lines):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                lines[index] = WIKI.sub(replace, line)

        new = "".join(lines)
        if changed and new != old:
            changed_files.append(source)
            if args.apply:
                source.write_text(new, encoding="utf-8", newline="")

    action = "updated" if args.apply else "would update"
    print(f"{action}: {len(changed_files)} files, mapped={mapped}, delinked={delinked}")
    for path in changed_files:
        print(rel(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
