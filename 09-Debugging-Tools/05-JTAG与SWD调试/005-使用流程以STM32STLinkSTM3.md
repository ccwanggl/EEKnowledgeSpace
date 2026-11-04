---
tags: [jtag, swd, debug, debugger, probe]
date-created: 2026-06-15
---

# 使用流程（以 STM32 + ST-Link + STM32CubeIDE 为例）

1. **连接硬件**：ST-Link 的 SWDIO/SWCLK/GND 连接目标板，USB 连接 PC
2. **配置调试器**：Project → Debug Configurations → 选择 ST-Link + SWD
3. **编译程序**：Build 项目，确保无错误
4. **启动调试**：Debug 按钮，程序下载到 Flash 并运行到 main()
5. **设置断点**：在代码行号旁双击，设置断点
6. **运行到断点**：Resume（F8），程序运行到断点停下
7. **单步**：Step Over（F6），逐行执行
8. **查看变量**：鼠标悬停或 Variables 窗口查看变量值
9. **查看寄存器**：Peripheral 窗口查看外设寄存器
10. **修改内存**：Memory 窗口直接修改 RAM 地址
11. **继续运行**：Resume（F8），或 Stop 结束调试

---

