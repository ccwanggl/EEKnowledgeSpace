---
tags: [analog, filter, signal-processing]
date-created: 2026-06-15
---

# 无源滤波器（RC/RL/LC）

> 🎬 **配套视频**（B 站《手搓电脑》· [墓中巫人](https://space.bilibili.com/1632504085/lists)，第八季）：
> - [0086 容抗与感抗](https://www.bilibili.com/video/BV1Ugah6UE2K) · [0088 低通与高通滤波器](https://www.bilibili.com/video/BV1i7J96FEt6) · [0089 幅频与相频特性](https://www.bilibili.com/video/BV1VyHc6mEyv)

## 一阶 RC 低通
- 截止频率：$f_c = 1/(2\pi RC)$
- 衰减斜率：-20 dB/decade（十倍频程幅值降至 1/10）
- 相位偏移：-45° 在 $f_c$，趋近 -90° 在高频
- 用途：简单去耦、信号调理、PWM 滤波为模拟电压

### 一阶 RC 高通
- 截止频率：$f_c = 1/(2\pi RC)$
- 用途：隔直流、音频耦合、消除传感器偏移

### LC 谐振电路
- 谐振频率：$f_0 = 1/(2\pi\sqrt{LC})$
- 高品质因数 Q = $f_0 / BW$
- 用途：RF 选频、开关电源谐振、无线能量传输

---

