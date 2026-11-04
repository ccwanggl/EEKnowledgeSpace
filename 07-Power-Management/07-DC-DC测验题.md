---
tags: [quiz, power, dc-dc, practice]
date-created: 2026-06-17
---

# DC-DC 转换器测验题

> 本测验覆盖 Buck、Boost、Buck-Boost 拓扑原理、参数计算和布局要点。建议先完成 [[02-DC-DC转换器]] 和 [[01-电源管理基础]] 后再做。

---

## 一、选择题

### 1. Buck 拓扑
Buck（降压）转换器的输出电压与输入电压关系是？
- A. $V_{out} = V_{in} / D$
- B. $V_{out} = D \cdot V_{in}$
- C. $V_{out} = V_{in} / (1-D)$
- D. $V_{out} = V_{in} \cdot (1-D)$

<details>
<summary>答案</summary>
B. $V_{out} = D \cdot V_{in}$。$D$ 为占空比。
</details>

### 2. Boost 拓扑
Boost（升压）转换器的占空比 $D$ 越大，输出电压越？
- A. 低
- B. 高
- C. 不变
- D. 不确定

<details>
<summary>答案</summary>
B. 高。$V_{out} = V_{in} / (1-D)$，$D$ 越大，$1-D$ 越小，输出越高。
</details>

### 3. 电感电流
Buck 转换器工作在 CCM（连续导通模式）时，电感电流？
- A. 始终为零
- B. 始终大于零
- C. 在开关周期内可能降到零
- D. 为负值

<details>
<summary>答案</summary>
B. 始终大于零。CCM 定义就是电感电流连续，始终大于零。
</details>

### 4. 开关损耗
开关损耗主要与哪些因素有关？
- A. 仅与导通电阻有关
- B. 与开关频率和开关时间有关
- C. 仅与输入电压有关
- D. 与电感值有关

<details>
<summary>答案</summary>
B. 与开关频率和开关时间有关。$P_{sw} \approx \frac{1}{2} V_{DS} I_D (t_r + t_f) f_{sw}$。
</details>

### 5. 输出纹波
增大 Buck 输出电容会？
- A. 增大输出电压纹波
- B. 减小输出电压纹波
- C. 不影响纹波
- D. 提高效率

<details>
<summary>答案</summary>
B. 减小输出电压纹波。$\Delta V_{out} \approx \Delta I_L / (8 f_{sw} C_{out})$。
</details>

---

## 二、填空题

### 6. Buck 占空比
输入 12V，输出 5V 的 Buck 转换器，理想占空比 $D$ = **_____**。

<details>
<summary>答案</summary>
0.417 或 41.7%。$D = V_{out}/V_{in} = 5/12 \approx 0.417$。
</details>

### 7. 效率
输入功率 10W，输出功率 8.5W，转换效率为 **_____** %。

<details>
<summary>答案</summary>
85%。$\eta = P_{out}/P_{in} \times 100\% = 8.5/10 \times 100\% = 85\%$。
</details>

### 8. CCM/DCM 边界
Buck 转换器负载电流减小时，会从 CCM 进入 **_____**。

<details>
<summary>答案</summary>
DCM（断续导通模式）。
</details>

---

## 三、简答题

### 9. 同步整流 vs 非同步整流
简述同步整流和非同步整流的区别及优缺点。

<details>
<summary>答案与解析</summary>

**非同步整流**：
- 使用二极管作为续流器件
- 简单、成本低
- 二极管正向压降导致损耗，效率较低

**同步整流**：
- 使用 MOSFET 替代二极管
- $R_{DS(on)}$ 小，导通损耗低
- 效率高，但需要驱动电路，成本和复杂度增加
- 需要死区时间控制防止上下管直通

**选择**：大电流、高效率应用选同步整流；小电流、低成本应用选非同步。
</details>

### 10. DC-DC 布局要点
列举 Buck 转换器 PCB 布局的 3 个关键要点。

<details>
<summary>答案与解析</summary>

1. **减小开关回路面积**：输入电容、高侧开关、低侧开关/二极管形成的回路要尽量小，降低 EMI。
2. **开关节点远离敏感信号**：SW 节点 dv/dt 大，要远离反馈线和模拟信号。
3. **反馈走线短而直**：反馈电阻靠近 IC，走线远离 SW 和电感，用地线屏蔽。
4. **大电流路径宽铜箔**：减小寄生电阻和发热。
5. **散热过孔**：功率器件下方放置散热过孔。
</details>

---

## 四、计算题

### 11. Buck 参数设计
设计一个 Buck 转换器：$V_{in} = 12V$，$V_{out} = 3.3V$，$I_{out} = 2A$，$f_{sw} = 500kHz$。要求电感电流纹波 $\Delta I_L = 0.6A$（30%）。求电感值。

<details>
<summary>答案与解析</summary>

$$ D = \frac{V_{out}}{V_{in}} = \frac{3.3}{12} = 0.275 $$

电感电流纹波公式：
$$ \Delta I_L = \frac{(V_{in} - V_{out}) \cdot D}{f_{sw} \cdot L} $$

解得：
$$ L = \frac{(V_{in} - V_{out}) \cdot D}{f_{sw} \cdot \Delta I_L} = \frac{(12 - 3.3) \times 0.275}{500\times10^3 \times 0.6} $$
$$ L = \frac{8.7 \times 0.275}{300\times10^3} = \frac{2.3925}{300\times10^3} \approx 7.98\ \mu H $$

取标准值 **8.2 μH** 或 **10 μH**。
</details>

### 12. Boost 设计
设计一个 Boost 转换器：$V_{in} = 3.3V$，$V_{out} = 5V$，输出电流 1A。估算输入电流（理想情况）。

<details>
<summary>答案与解析</summary>

理想效率下，输入功率 = 输出功率：
$$ P_{out} = 5V \times 1A = 5W $$
$$ P_{in} = 5W $$
$$ I_{in} = P_{in}/V_{in} = 5/3.3 \approx 1.52A $$

占空比：
$$ D = 1 - V_{in}/V_{out} = 1 - 3.3/5 = 0.34 $$

所以平均输入电流约为 1.52A，实际考虑效率会更高。
</details>

---

## 自评标准

| 正确率 | 水平 |
|--------|------|
| 90-100% | 已掌握，可独立设计简单 DC-DC |
| 70-89% | 基本掌握，重点复习电感计算和布局 |
| <70% | 需要重新学习 [[02-DC-DC转换器]] |

---

## 相关主题
- [[01-电源管理基础]] — 线性稳压与开关电源概念
- [[02-DC-DC转换器]] — 测验覆盖的理论基础
- [[01-PCB设计基础]] — DC-DC 布局要点
- [[13-Appendix/03-元器件选型指南/001-选型流程|元器件选型指南]] — MOSFET、二极管和电感选型
