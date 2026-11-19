---
tags: [riscv, mcu, china, open-source]
date-created: 2026-06-15
---

# RISC-V 核心概念

## 什么是 RISC-V
- 开放指令集架构：任何人可自由使用、修改、扩展
- 模块化设计：基础整数指令 + 可选扩展（M=乘除、A=原子、F=浮点、D=双精度、C=压缩）
- 无授权费：对比 ARM 的 IP 授权费用，大幅降低芯片成本
- 社区驱动：RISC-V International 管理标准，全球贡献

### RISC-V 与 ARM 对比
| 特性 | RISC-V | ARM |
|------|--------|-----|
| 授权 | 开源免费 | 需授权费（~$0.1-$0.5/芯片）|
| 定制 | 可自由添加自定义指令 | 受限于 ARM 许可 |
| 生态 | 快速成长，但弱于 ARM | 成熟庞大 |
| 工具链 | GCC、LLVM 支持良好 | 极其成熟 |
| 调试 | OpenOCD 支持，持续完善 | 完善（J-Link、ULINK）|

---

**可结合本节观看的案例**　中文处理器课程可参考芯来科技。对照 learn-fpga、Ben Eater 或课程中的简单 CPU，区分通用数据通路和 RISC-V 指令集。
