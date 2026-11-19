---
tags: [projects, advanced, expert, fpga, drone, sdr, 3d-printer]
date-created: 2026-06-15
---

# 1. FPGA 数字钟与数字系统

**目标**：完整 FPGA 设计流程，从 RTL 到比特流。

## 硬件
- FPGA 开发板（Basys 3 / Tang Nano 9K / iCEstick）
- 外部晶振（板载通常 100MHz/50MHz/12MHz）
- 七段数码管或板载 LED
- 可选：按键、蜂鸣器、温度传感器（1-Wire）

### 项目内容
- 分频器：从系统时钟分频到 1Hz
- 计数器：时、分、秒计数
- 状态机：设定时间模式（按键切换）
- 显示驱动：扫描七段数码管或 VGA 显示
- 闹钟功能：蜂鸣器 + 按键消抖
- 可选：RTC 芯片（I2C 接口）备用

### 技能点
- Verilog 状态机、计数器、分频器
- 按键消抖（硬件或软件延时）
- 七段译码和动态扫描
- 约束文件（XDC/PCF）和时钟约束
- 仿真测试（Testbench + GTKWave）

### 参考
- **Ben Eater** — 数字时钟项目
- **nandland** — FPGA 时钟教程

### 项目来源与详细资源

**核心来源**
- Ben Eater 面包板 8 位计算机官方项目页：<https://eater.net/8bit> — 时钟模块（555 定时器 + 单步/自动/暂停逻辑）是整个系列的第一课，后面寄存器、ALU、RAM、PC、控制单元逐模块搭建，是本项目的直接原型
- 配套汇编器/模拟器（开源）：<https://github.com/wmvanvliet/8bit> — Ben Eater 8 位机的 Python 汇编器 + 子周期精确模拟器，可先生成微码 EEPROM 二进制再上板
- nandland（FPGA 时钟、计数器、PWM 系列教程，含 Verilog 代码和仿真）

**关键实现要点**
- 时钟部分：555 无稳态振荡（频率 f = 1.44 / ((Ra+2Rb)·C)）+ 单步按钮 + 暂停（halt）信号，与 FPGA 中的分频器 + 使能计数器等价
- 建议路线：先用面包板复现 Ben Eater 时钟模块理解原理，再用 Verilog 实现同功能并对照仿真波形
- 数据手册重点：74LS00/74LS04（门电路）、74LS161（计数器）、555 定时器电气特性

---

