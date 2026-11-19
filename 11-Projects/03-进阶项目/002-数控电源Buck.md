---
tags: [projects, intermediate, diy, control, communication]
date-created: 2026-06-15
---

# 2. 数控电源（Buck）

**目标**：理解 DC-DC 控制、反馈、ADC、数字控制。

## 硬件
- STM32G4（高分辨率定时器 + ADC）或 STM32F3
- Buck 功率级（MOSFET + 电感 + 二极管 + 电容）
- 输出电压/电流采样（分压 + 采样电阻 + 运放）
- 编码器或按键 + 显示屏（设定电压/电流）

### 技能点
- Buck 拓扑与 PWM 控制
- 电压/电流闭环控制（PID 或数字补偿器）
- ADC 采样时序与 PWM 同步
- 过压/过流保护（硬件 + 软件）
- 数字控制理论（z 变换、离散 PID）

### 参考
- **Phil's Lab** — 数字电源设计
- **TI C2000** — 数字电源控制培训

### 项目来源与详细资源

- **TI C2000Ware Digital Power SDK**（官方数字电源 SDK，含 Buck 参考设计 TIDM-DC-DC-BUCK 的完整原理图与固件）：https://www.ti.com/tool/C2000WARE-DIGITALPOWER-SDK
- **ST STM32 数字电源生态**（STM32G4 高分辨率定时器 HRTimer 184ps 分辨率、5 MSPS ADC，官方数字电源页面与例程）：https://www.st.com/content/st_com/en/ecosystems/stm32-digital-power.html
- **Phil's Lab** 数字电源系列视频（数字补偿器设计、电压模式/电流模式控制，网站 phils-lab.net）
- **理论与设计**：
  - TI《Switching Power Supplies A to Z》与电源设计研讨会资料（ti.com 搜 "power supply design seminar"）
  - 数字控制：z 变换、离散 PID、2P2Z/3P3Z 补偿器；采样与 PWM 同步是关键（ADC 由定时器事件触发，避开开关噪声）
  - Buck 功率级设计：电感按 ΔI_L=30%I_out 计算，输出电容按纹波/瞬态选取，TI WEBENCH 可作初始验证
- **保护要点**：硬件过流比较器（G4 内置 DAC+COMP）做逐周期限流，软件做打嗝/锁断；MOSFET 选低 Qg 降低开关损耗
- **开源参考**：立创开源平台搜索 "数控电源" / "Buck"（大量 STM32 数字电源工程含原理图）

---

