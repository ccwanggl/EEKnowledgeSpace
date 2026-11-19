---
tags: [index, readme, 04-microcontrollers]
date-created: 2026-06-17
---

# 微控制器（04-Microcontrollers）

> STM32、ESP32、Arduino 等主流 MCU 的架构、外设与编程。

---

## 从一个任务开始

[[00-Index/03-AI自学任务索引#微控制器：生成和验证 PWM|微控制器：生成和验证 PWM]]。先试做，根据卡点回正文或找 AI 提示，再用变式独立验收。

## 模块导航

- [[04-Microcontrollers/01-微控制器概述/001-MCU核心组成|微控制器概述]]
- [[04-Microcontrollers/02-STM32系列/000-STM32系列|STM32 系列]]
- [[04-Microcontrollers/03-ESP32系列/001-产品线|ESP32系列]]
- [[04-Microcontrollers/04-Arduino与Raspberry-Pi-Pico/001-Arduino生态系统|Arduino与Raspberry-Pi-Pico]]
- [[04-Microcontrollers/05-RISC-V与国产MCU/001-RISCV核心概念|RISC-V与国产MCU]]
- [[04-Microcontrollers/06-中断与DMA深入/001-中断系统|中断与DMA深入]]
- [[04-Microcontrollers/07-MCU启动与链接脚本/001-上电启动流程|MCU启动与链接脚本]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "04-Microcontrollers"
WHERE file.name != "00-README"
SORT file.name ASC
```

---

## 推荐学习路径

1. 先浏览本目录下的核心概念文件。
2. 完成相关 [[00-Index/04-练习与复习#按主题找练习和测验|测验题]] 检验理解。
3. 结合 [[01-项目总览]] 中的项目动手实践。
4. 遇到问题时查阅 [[01-调试工具概述|调试工具]] 和 [[02-工具清单|工具清单]]。

---

## 推荐资源

> 以下资源按相关性和学习阶段推荐，与 [[12-Resources/00-README|12-Resources]] 中的完整资源列表互为补充。

### 推荐书籍

| 书籍 | 作者 | 级别 | 适用内容 | 获取方式 |
|------|------|------|----------|----------|
| 《Making Embedded Systems》 | Elecia White | 中级 | 嵌入式系统整体设计方法（需求→架构→实现→测试），适用于 **01-微控制器概述** | 纸质书 |
| 《Programming Embedded Systems in C and C++》 | Michael Barr & Anthony Massa | 中级 | 固件编程核心技能，中断、DMA、外设驱动，适用于 **06-中断与DMA深入**、**02-STM32系列** | 纸质书 |
| 《Embedded C》 | Michael J. Pont | 中级 | 嵌入式 C 编程与代码结构，适用于 **01-微控制器概述**、**07-MCU启动与链接脚本** | 纸质书 |
| 《The Definitive Guide to ARM Cortex-M3/M4》 | Joseph Yiu | 高级 | ARM Cortex-M 架构深入（NVIC、SysTick、MPU、FPU），适用于 **02-STM32系列**、**06-中断与DMA深入** | 纸质书 |
| 《Mastering STM32》 | Carmine Noviello | 中级~高级 | STM32 最全面的参考手册（HAL/LL、FreeRTOS、USB、以太网），适用于 **02-STM32系列** | [免费在线](https://github.com/cnovak/mstm32) |
| 《Mastering the ESP32》 | Neil Kolban | 中级~高级 | ESP32 芯片深入（WiFi/Bluetooth、RTOS、外设），适用于 **03-ESP32系列** | [免费 PDF](https://leanpub.com/masteringtheesp32) |
| 《RISC-V Reader》 | David Patterson | 入门 | RISC-V 架构精简导论，适用于 **05-RISC-V与国产MCU** | [免费 PDF](https://riscv.org) |
| 《FreeRTOS 书籍》 | Richard Barry | 中级 | 实时操作系统任务调度、信号量、队列，适用于 **10-RTOS与系统** | [免费 PDF](https://freertos.org) |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| **FastBit Embedded Brain Academy** | YouTube | STM32 嵌入式最系统的课程（从寄存器到 HAL） | **02-STM32系列**、**06-中断与DMA深入** |
| **Paul McWhorter** | YouTube | Arduino 和 Raspberry Pi Pico 最系统的教程 | **04-Arduino与Raspberry-Pi-Pico** |
| **Andreas Spiess** | YouTube | 物联网、ESP32、LoRa、Matter 实战 | **03-ESP32系列**、**05-无线通信-BLE-WiFi-Matter** |
| **Ben Eater** | YouTube | 计算机架构、数字逻辑、8-bit CPU 面包板系列 | **01-微控制器概述**、**05-RISC-V与国产MCU** |
| **江协科技** | Bilibili | STM32 标准库 + HAL 最系统的中文教程（中文） | **02-STM32系列**、**06-中断与DMA深入** |
| **正点原子** | Bilibili | STM32 教程、开发板配套（中文） | **02-STM32系列** |
| **爱上半导体** | Bilibili/YouTube | 硬件原理可视化极好（CAN、I2C、LCD、MOS管）（中文） | **01-微控制器概述**、外设原理 |
| **Coursera: Embedded Systems** | Coursera | ARM Cortex-M 系列（UC Boulder） | **02-STM32系列**、**06-中断与DMA深入** |
| **Microchip University** | 官网 | CAN、USB、以太网、电源等官方课程 | **05-Communication** 相关外设 |
| **Bootlin Training** | 官网 | 免费嵌入式 Linux 培训视频 | **05-嵌入式Linux入门** |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| **DeepBlue Embedded** | 英文 | 嵌入式教程质量极高，STM32/ESP32 实例丰富 | **02-STM32系列**、**03-ESP32系列** |
| **Adafruit Learning System** | 英文 | 传感器、项目、库教程，Arduino/CircuitPython 生态 | **04-Arduino与Raspberry-Pi-Pico** |
| **SparkFun Tutorials** | 英文 | 教育友好，从基础到传感器、通信协议 | **01-微控制器概述**、入门项目 |
| **Hackaday** | 英文 | 每日硬件项目、新闻、教程，灵感来源 | 全模块项目参考 |
| **AllAboutCircuits** | 英文 | 最全面的免费电路与嵌入式教程 | **01-微控制器概述**、基础原理 |

---

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[02-MOC-主题索引|主题索引]]
- [[01-学习路线图|学习路线图]]
