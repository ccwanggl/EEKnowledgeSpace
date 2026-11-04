---
tags: [jtag, swd, debug, debugger, probe]
date-created: 2026-06-15
---

# 调试器（Debugger/Probe）

## 软件接口
调试器硬件连接 PC 和目标芯片，PC 端通过软件控制：
- **OpenOCD**：开源调试服务器，支持几乎所有调试器和芯片
- **GDB**：GNU 调试器，配合 OpenOCD 使用
- **IDE 内置**：Keil、STM32CubeIDE、PlatformIO 集成调试器驱动

### 常见调试器

| 调试器 | 接口 | 支持芯片 | 价格 | 特点 |
|--------|------|----------|------|------|
| **ST-Link V2** | SWD/JTAG | STM8/STM32 | ~$3 | 最便宜的 STM32 调试器 |
| **ST-Link V3** | SWD/JTAG | STM32 | ~$15 | 更快，支持虚拟串口 |
| **J-Link EDU** | SWD/JTAG | ARM/RISC-V | ~$60 | SEGGER，业界标准 |
| **J-Link Plus** | SWD/JTAG | ARM/RISC-V | ~$400 | 商业授权，无限制 |
| **DAPLink** | SWD | ARM Cortex-M | ~$5 | 开源，CMSIS-DAP |
| **Black Magic Probe** | SWD/JTAG | ARM | ~$30 | 开源，GDB 直连，无需 OpenOCD |
| **WCH-Link** | SWD/RISC-V | CH32V/GD32V | ~$3 | 沁恒/RISC-V 专用 |
| **J-Link OB** | SWD | 集成在开发板上 | 免费 | 开发板自带（如 Nucleo） |

---

