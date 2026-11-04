---
tags: [debugging, uart, logging, printf, rtt, embedded]
date-created: 2026-06-15
---

# SEGGER RTT

## 优点
- 通过 J-Link 调试器传输，无需额外 UART
- 速度极快，不影响 UART 外设
- 支持多个 Up/Down 通道

### 使用
```c
#include "SEGGER_RTT.h"

SEGGER_RTT_printf(0, "Temperature: %d\r\n", temp);
```

### 适用场景
- 有 J-Link 调试器时首选
- 需要高速日志输出
- 产品保留 SWD 接口的调试

---

