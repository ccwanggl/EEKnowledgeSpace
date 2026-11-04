---
tags: [debugging, uart, logging, printf, rtt, embedded]
date-created: 2026-06-15
---

# SWO / ITM 跟踪

## 特点
- ARM Cortex-M 单线输出（SWO）
- ITM（Instrumentation Trace Macrocell）
- 不占用 UART，速度可达 Mbps
- 需要支持 SWO 的调试器

### 使用
- 在代码中调用 `ITM_SendChar(port, c)`
- 在 Keil/IAR/VS Code 中配置 SWO 时钟和分频
- 适合 printf 式调试和事件跟踪

---

