---
tags: [jtag, swd, debug, debugger, probe]
date-created: 2026-06-15
---

# JTAG 与 SWD 调试

> JTAG 和 SWD 是嵌入式系统中最常用的硬件调试接口。它们允许开发者在目标芯片上设置断点、单步执行、查看寄存器和内存，是调试固件 bug 的最强工具。

---


---

本笔记为**总索引**，各章节的详细内容已拆分为独立笔记。点击下方链接直达具体章节。

---

## 分类导航

- **JTAG（Joint Test Action Group）** — [[001-JTAGJointTestActionG]]
- **SWD（Serial Wire Debug）** — [[002-SWDSerialWireDebug]]
- **调试器（Debugger/Probe）** — [[003-调试器DebuggerProbe]]
- **调试功能** — [[004-调试功能]]
- **使用流程（以 STM32 + ST-Link + STM32CubeIDE 为例）** — [[005-使用流程以STM32STLinkSTM3]]
- **常见问题** — [[006-常见问题]]
- **推荐资源** — [[09-Debugging-Tools/05-JTAG与SWD调试/007-推荐资源|007-推荐资源]]
- **可视化：JTAG vs SWD** — [[008-可视化JTAGvsSWD]]
- **相关主题** — [[09-Debugging-Tools/05-JTAG与SWD调试/009-相关主题|009-相关主题]]

## 相关主题
- [[01-调试工具概述]] — 调试器在工具体系中的位置
- [[01-Foundations/08-嵌入式C编程/000-嵌入式C编程|08-嵌入式C编程]] — 调试的对象
- [[02-示波器使用]] — 硬件调试互补工具
- [[03-逻辑分析仪]] — 协议调试工具
- [[02-工具清单]] — 推荐调试器型号
