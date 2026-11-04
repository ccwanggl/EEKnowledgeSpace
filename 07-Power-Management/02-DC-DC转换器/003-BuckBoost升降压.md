---
tags: [dc-dc, buck, boost, converter, power]
date-created: 2026-06-15
---

# Buck-Boost（升降压）

## 应用场景
- 电池电压随放电从高于输出变为低于输出
- 单节锂电（4.2V→3.0V）输出稳定 3.3V

### 拓扑
- **反相 Buck-Boost**：输出负压，简单但噪声大
- **四开关 Buck-Boost**：$V_{in}$ > $V_{out}$ 时 Buck 模式，$V_{in}$ < $V_{out}$ 时 Boost 模式
- **SEPIC**：正压升降压，无反向问题，需耦合电容
- **Cuk**：输出负压，连续输入输出电流

### 常用 IC
- **TPS63000**：96% 效率，Buck-Boost，1.5A，适合锂电
- **LTC3780**：10A，四开关，大功率
- **MAX77827**：Buck-Boost，超低功耗，适合可穿戴

---

