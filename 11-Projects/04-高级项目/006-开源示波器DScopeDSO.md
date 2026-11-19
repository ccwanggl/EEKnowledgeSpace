---
tags: [projects, advanced, expert, fpga, drone, sdr, 3d-printer]
date-created: 2026-06-15
---

# 6. 开源示波器（DScope / DSO）

**目标**：FPGA + 高速 ADC + 数字信号处理。

## 硬件
- FPGA：iCE40 / ECP5 / Artix-7（带高速 LVDS）
- ADC：ADS4249（14-bit，250MSPS）或类似
- 前端：衰减器（1×/10×/100×）+ 运放缓冲 + 抗混叠滤波
- 触发：比较器或数字触发
- 显示：TFT LCD 或 HDMI（FPGA 输出）
- 存储：外部 SRAM/SDRAM（DDR）用于波形存储

### 技能点
- FPGA 高速数据采集和存储（DDR 控制器）
- 触发系统（前触发/后触发）
- 波形显示（像素渲染、插值、缩放）
- 测量功能（Vpp、频率、上升时间）
- 通信：USB 或以太网传输波形到 PC

### 参考
- **"DScope"** 开源项目（Hackaday）
- **"Open Scope"**（Digilent）— 教育开源示波器
- **The Signal Path** — 高速 ADC 和采样理论

### 项目来源与详细资源

**核心来源**
- Digilent OpenScope MZ 开源固件仓库：<https://github.com/Digilent/openscope-mz> — 硬件/固件/软件全开源的多功能仪器（PIC32MZ2048EFG124 主控）：2 通道 12-bit 示波器（2 MHz 带宽、6.25 MS/s）、10 通道逻辑分析仪（10 MS/s）、任意波形发生器、±4 V 可编程电源；上位机 WaveForms Live 是开源 JavaScript Web 应用；固件可用 Arduino IDE 或 MPLAB X 重新编译
- OpenScope MZ 参考手册与原理图在 Digilent reference 站（reference.digilentinc.com），EEVblog #1057 有完整评测，适合看设计取舍
- DScope（Hackaday 开源示波器项目，名称提及）— 手持开源示波器路线，可对照学习前端衰减/放大链路设计
- The Signal Path（YouTube）— 高速 ADC、采样理论、示波器前端实测讲解

**关键实现要点**
- 前端是难点：1×/10×/100× 继电器/模拟开关切换衰减 + 运放缓冲（注意带宽和建立时间）
- 采样与存储：高速 ADC → FPGA 采集 → DDR/SRAM 乒乓缓存 → 触发判决（数字触发更灵活）
- 校准：直流增益/偏移用软件校准，探头补偿用可调电容

---

