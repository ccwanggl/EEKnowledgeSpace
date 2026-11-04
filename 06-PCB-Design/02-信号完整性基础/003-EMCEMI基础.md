---
tags: [signal-integrity, analog, emc, noise]
date-created: 2026-06-15
---

# EMC/EMI 基础

## 电磁辐射
- 电流环路是天线：$E \propto I \cdot A \cdot f^2$
- 减小环路面积：电流去路和返回路径紧贴
- 高速信号必须有完整的参考平面（地或电源）

### 传导发射
- 电源线上的高频噪声通过电缆传导出去
- 解决：滤波器、 ferrite bead、屏蔽电缆

### 抗扰度
- 外部电磁干扰对电路的影响
- 解决：屏蔽、滤波、接地、合理的 PCB 布局

---

