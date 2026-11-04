---
tags: [arduino, pico, rp2040, rp2350, prototyping]
date-created: 2026-06-15
---

# Raspberry Pi Pico / RP2040 / RP2350

## RP2040（Pico 1）
- **双核 Cortex-M0+**，133MHz
- **264KB SRAM**
- **可编程 I/O（PIO）**：自定义协议处理器，极其灵活
- **USB 1.1**：Device/Host
- **QSPI Flash**：外接，通常 2MB（Pico 自带）
- **低价格**：$4（Pico 开发板）

### RP2350（Pico 2）
- **双核 Cortex-M33 或 Hazard3 RISC-V**（可选）
- **520KB SRAM**
- **TrustZone** 安全扩展
- **硬件浮点单元（FPU）**
- **USB 1.1 + 改进 PIO**
- 保持引脚兼容，性能翻倍

### 开发环境
- **C/C++ SDK**：官方，完整功能，使用 CMake
- **MicroPython**：官方维护，快速原型
- **CircuitPython**：Adafruit 维护，教育友好
- **Arduino（Earle Philhower 核心）**：兼容 Arduino IDE
- **Pico W**：RP2040 + CYW43439（WiFi + BLE），Pico 2 W 同理

### 独特优势：PIO（Programmable I/O）
- 用汇编语言定义自定义协议（UART、SPI、I2C、DVI、PWM 等）
- 独立运行，不占用 CPU
- 可以实现任何时序精确的协议
- 示例：DVI 视频输出、8 通道并行 PWM、自定义传感器接口

---

