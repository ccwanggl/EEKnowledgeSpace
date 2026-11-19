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

---

