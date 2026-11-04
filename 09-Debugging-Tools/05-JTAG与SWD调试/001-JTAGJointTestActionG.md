---
tags: [jtag, swd, debug, debugger, probe]
date-created: 2026-06-15
---

# JTAG（Joint Test Action Group）

## 起源
- 最初用于边界扫描测试（Boundary Scan），测试 PCB 制造缺陷
- 后来扩展为通用调试接口

### 信号线（标准 5 线）
- **TMS**：测试模式选择，状态机控制
- **TCK**：测试时钟，所有操作同步于 TCK
- **TDI**：测试数据输入，串行输入指令/数据
- **TDO**：测试数据输出，串行输出数据
- **TRST**：可选，测试复位，异步复位 JTAG 状态机

### 特点
- **标准通用**：IEEE 1149.1，几乎所有芯片支持
- **多设备链**：多个芯片可串联在一条 JTAG 链上
- **功能全**：调试 + 边界扫描 + 编程 Flash
- **引脚多**：至少 4 线（TMS/TCK/TDI/TDO），占用 PCB 空间

---

