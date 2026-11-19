---
tags: [analog, electronics, op-amp, filter]
date-created: 2026-06-15
---

# ADC/DAC 前端

> 🎬 **配套视频**（B 站《手搓电脑》· [墓中巫人](https://space.bilibili.com/1632504085/lists)，第一季）：

<details>
<summary>0011 权电阻网络 D/A 变换</summary>
<iframe src="https://player.bilibili.com/player.html?bvid=BV1ar4y1o76i&amp;autoplay=0&amp;danmaku=0" title="0011 权电阻网络 D/A 变换" width="100%" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
<p><a href="https://www.bilibili.com/video/BV1ar4y1o76i">在 B 站打开</a></p>
</details>

<details>
<summary>0012 R-2R 梯形电阻网络 D/A 变换</summary>
<iframe src="https://player.bilibili.com/player.html?bvid=BV15h4y1k7fA&amp;autoplay=0&amp;danmaku=0" title="0012 R-2R 梯形电阻网络 D/A 变换" width="100%" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
<p><a href="https://www.bilibili.com/video/BV15h4y1k7fA">在 B 站打开</a></p>
</details>

两集用分立电阻网络亲手搭出 DAC，是理解"数字到模拟"物理本质的极佳材料。


## 传感器信号调理
- 电桥放大（如应变片、压力传感器）
- 电流-电压转换（如光电二极管）
- 电平偏移（双极性信号转单极性）

### 抗混叠滤波
- ADC 前必须加低通滤波器，防止高频混叠
- 截止频率 ≤ $f_s/2$（奈奎斯特频率）

---
