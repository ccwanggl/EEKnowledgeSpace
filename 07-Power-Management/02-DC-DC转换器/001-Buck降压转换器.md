---
tags: [dc-dc, buck, boost, converter, power]
date-created: 2026-06-15
---

# Buck（降压）转换器

## 配套视频

**TI：Buck Converter Basics**

[打开 TI 官方视频](https://www.ti.com/video/5103393152001)。画出开关导通和关断时的两条电流路径，并标出电感电压。

## 工作原理
- 开关管（高侧 MOSFET）快速导通/关断，控制占空比 $D$
- 电感储能：导通时充电，关断时通过续流二极管/同步整流放电
- 输出电压：$V_{out} = D \cdot V_{in}$（理想情况）
- 输出电流：$I_{out} = I_{in} / D$（功率守恒，忽略损耗）

### 关键元件
- **电感**：$L = (V_{in} - V_{out}) \cdot D / (\Delta I_L \cdot f_{sw})$，纹波电流通常取 20~40% 负载电流
- **输出电容**：决定输出纹波，$\Delta V_{out} = \Delta I_L / (8 \cdot f_{sw} \cdot C_{out})$（连续模式）
- **输入电容**：提供高频脉冲电流，减小输入电压纹波
- **MOSFET**：高侧开关 + 低侧同步整流（现代 Buck）
- **续流二极管**：非同步 Buck 中使用，同步 Buck 用 MOSFET 替代（效率更高）

### 常用 IC
- **LM2596**：经典，3A，150kHz，外设简单，便宜
- **MP1584**：2A，1.5MHz，小体积，适合便携设备
- **TPS5430**：3A，500kHz，集成 MOSFET
- **XL4015**：5A，180kHz，国产，超便宜
- **TPS6282x**：6A，2.2MHz，超低功耗模式，PFM/PWM 自动切换

---

