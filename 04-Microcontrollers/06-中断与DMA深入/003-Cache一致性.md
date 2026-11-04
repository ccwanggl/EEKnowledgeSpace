---
tags: [mcu, interrupt, dma, stm32, embedded]
date-created: 2026-06-15
---

# Cache 一致性

## 问题来源
- Cortex-M7 等带 Cache 的 MCU 中，CPU 和外设 DMA 看到的数据可能不一致
- CPU 写内存后数据可能仍在 Cache，未写回 SRAM
- DMA 从 SRAM 读取到的仍是旧数据

### 解决方案
- **Cache 维护函数**：
  - `SCB_CleanDCache()`：将 Cache 数据写回内存
  - `SCB_InvalidateDCache()`：使 Cache 行失效，强制从内存重读
- **MPU 配置**：将 DMA 缓冲区设为 Shareable 或 Non-cacheable
- **对齐要求**：DMA 缓冲区通常需要 32 字节对齐

---

