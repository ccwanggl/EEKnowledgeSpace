---
tags: [analog, filter, signal-processing]
date-created: 2026-06-15
---

# 无源滤波器（RC/RL/LC）

> 🎬 **配套视频**（B 站《手搓电脑》· [墓中巫人](https://space.bilibili.com/1632504085/lists)，第八季）：

<details>
<summary>0086 容抗与感抗</summary>
<iframe src="https://player.bilibili.com/player.html?bvid=BV1Ugah6UE2K&amp;autoplay=0&amp;danmaku=0" title="0086 容抗与感抗" width="100%" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
<p><a href="https://www.bilibili.com/video/BV1Ugah6UE2K">在 B 站打开</a></p>
</details>

<details>
<summary>0088 低通与高通滤波器</summary>
<iframe src="https://player.bilibili.com/player.html?bvid=BV1i7J96FEt6&amp;autoplay=0&amp;danmaku=0" title="0088 低通与高通滤波器" width="100%" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
<p><a href="https://www.bilibili.com/video/BV1i7J96FEt6">在 B 站打开</a></p>
</details>

<details>
<summary>0089 幅频与相频特性</summary>
<iframe src="https://player.bilibili.com/player.html?bvid=BV1VyHc6mEyv&amp;autoplay=0&amp;danmaku=0" title="0089 幅频与相频特性" width="100%" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
<p><a href="https://www.bilibili.com/video/BV1VyHc6mEyv">在 B 站打开</a></p>
</details>


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
