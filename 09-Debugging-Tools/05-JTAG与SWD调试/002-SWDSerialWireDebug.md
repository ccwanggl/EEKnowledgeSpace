---
tags: [jtag, swd, debug, debugger, probe]
date-created: 2026-06-15
---

# SWD（Serial Wire Debug）

## ARM 专有接口
- 由 ARM 定义，替代 JTAG 的简化调试接口
- 仅需 2 根信号线 + 1 根可选复位

### 信号线（2+1 线）
- **SWDIO**：双向数据，上传调试命令和下载数据
- **SWCLK**：时钟，同步所有操作
- **nRST**：可选复位，硬件复位目标芯片
- **SWO（Serial Wire Output）**：可选，单线输出，用于 ITM/printf 跟踪

### 特点
- **引脚少**：2 线（+1 可选），节省 PCB 空间
- **速度快**：与 JTAG 相当甚至更快
- **功能全**：调试 + Flash 编程
- **ARM 专用**：主要 Cortex-M 系列支持，其他架构不一定

---

