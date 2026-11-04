---
tags: [arduino, pico, rp2040, rp2350, prototyping]
date-created: 2026-06-15
---

# Arduino 生态系统

## 核心特点
- **极简**：几行代码即可点亮 LED、读取传感器
- **开源硬件**：原理图公开，可自由复制和改进
- **庞大社区**：无数库、教程、项目、论坛
- **跨平台**：Windows/Mac/Linux 均可开发

### 主流板型
| 板型 | 处理器 | 特点 |
|------|--------|------|
| **Arduino Uno** | ATmega328P | 最经典，教育标准 |
| **Arduino Nano** | ATmega328P | 小巧，面包板友好 |
| **Arduino Mega** | ATmega2560 | 更多 I/O，内存更大 |
| **Arduino Leonardo** | ATmega32U4 | 内置 USB，模拟键盘/鼠标 |
| **Arduino Due** | SAM3X8E（ARM Cortex-M3）| 32位，高性能 |
| **Arduino Giga R1** | STM32H747XI | 双核，WiFi，多接口 |
| **MKR 系列** | SAMD21/SAMD51 | 物联网，集成 WiFi/BLE/GPS |

### Arduino 语言
- C++ 封装，隐藏底层细节
- `setup()` + `loop()` 结构
- `pinMode()`、`digitalWrite()`、`analogRead()`、`Serial.print()`
- 丰富的库：`Wire`（I2C）、`SPI`、`Servo`、`WiFi` 等

### 局限
- 性能有限（8-bit AVR 主频 16MHz）
- 无调试器（无法单步断点）
- 部分库效率低
- 不适合实时性要求高的场景

---

