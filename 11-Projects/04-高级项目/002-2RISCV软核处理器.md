---
tags: [projects, advanced, expert, fpga, drone, sdr, 3d-printer]
date-created: 2026-06-15
---

# 2. RISC-V 软核处理器

**目标**：理解计算机架构，从门级到 CPU。

## 硬件
- FPGA 开发板（Tang Nano / ULX3S / Basys 3）
- 板载 LED、按键、串口
- 可选：外部 SRAM/PSRAM

### 项目内容
- 实现 RV32I 指令集的子集（如 10~20 条指令）
- 数据通路：PC、寄存器堆、ALU、立即数生成
- 控制单元：指令译码、控制信号生成
- 内存接口：指令存储器（ROM）+ 数据存储器（RAM）
- 串口输出：实现 UART 写，用于打印 "Hello"
- 汇编程序：写测试程序，汇编为机器码，初始化 ROM

### 技能点
- RISC-V 指令格式（R/I/S/B/U/J 型）
- 数据通路设计（单周期或流水线）
- 控制信号真值表
- 指令存储器初始化（$readmemb/$readmemh）
- 上板验证：LED 响应、串口输出

### 进阶
- 添加流水线（5 级），处理冒险
- 添加 CSR 寄存器、中断处理
- 集成到 SoC（加 GPIO、UART、定时器）
- 跑 C 程序（用 RISC-V GCC 编译）

### 参考
- **learn-fpga**（Bruno Levy）— 从 Blinky 到 RISC-V（GitHub）
- **"CPU from scratch in Verilog"**（Hackaday 项目）
- **RVfpga**（Imagination University）— 课程和教材

---

