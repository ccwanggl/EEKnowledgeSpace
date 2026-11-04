---
tags: [foc, motor-control, clarke-transform]
date-created: 2026-06-30
---

> **Clarke 变换做什么**：把定子上三条相隔 $120°$ 的 $abc$ 量，改写成固定正交平面内的 $\alpha\beta$ 量。对三相三线、零序为零的 FOC 系统，这一步没有丢失基波信息，只是把三个相关变量换成两个独立变量。

[[001-三相坐标系与自然坐标系]] 已经说明了 $i_a+i_b+i_c=0$ 的物理前提，以及相电压、线电压和极点电压的区别。本篇从这个前提出发，说明投影系数从何而来、等幅值与等功率为何不能混用，以及代码中该怎样验证。

```mermaid
graph LR
    abc["abc：绕组、采样与逆变器直接使用的量"] -->|"Clarke"| ab["αβ：二维静止平面"]
    ab -->|"Park"| dq["dq：随转子转动的平面"]
```

![[14-FOC-电机控制/assets/foc_current_transform.png|1500]]
*图：Clarke 变换把三相基波量投影到静止的 $\alpha\beta$ 平面；本篇只处理这一步。*

## 1. 三相量为什么可以投影到二维

令 $\alpha$ 轴与 $a$ 相绕组轴重合，$\beta$ 轴比 $\alpha$ 轴逆时针转 $90°$。三个绕组在空间上的单位向量投影为：

| 相轴 | 在 $\alpha$ 轴上的投影 | 在 $\beta$ 轴上的投影 |
|---|---:|---:|
| $a$ | $1$ | $0$ |
| $b$ | $-1/2$ | $+\sqrt3/2$ |
| $c$ | $-1/2$ | $-\sqrt3/2$ |

![[14-FOC-电机控制/assets/clarke_projection_geometry.png|1500]]
*图：三相空间轴投影到 $\alpha\beta$ 正交轴。*

因此，未标定的几何投影是：

$$
\begin{aligned}
x_\alpha'&=x_a-\frac12x_b-\frac12x_c\\
x_\beta'&=\frac{\sqrt3}{2}(x_b-x_c)
\end{aligned}
$$

这里 $x$ 可以是电流、电压、磁链或基波磁动势。对三相三线系统，$x_a+x_b+x_c=0$ 时只有两个独立自由度；$x_\alpha'$、$x_\beta'$ 恰好提供这两个自由度。若存在中线、对地回路、传感器偏置或故障引起的零序量，仍可计算二维投影，但不能把第三相简单重构为负和。

代入正序平衡量：

$$
x_a=X_m\cos\theta,\quad x_b=X_m\cos(\theta-120°),\quad x_c=X_m\cos(\theta+120°)
$$

得到 $x_\alpha'=\frac32X_m\cos\theta$、$x_\beta'=\frac32X_m\sin\theta$。几何投影的空间矢量幅值是单相峰值的 $3/2$；两套常用 Clarke 变换只是对这个投影采用不同标定。

## 2. 等幅值：控制代码最常见的约定

等幅值变换将几何投影乘以 $2/3$：

$$
\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}=
\frac23
\begin{bmatrix}
1&-\frac12&-\frac12\\
0&\frac{\sqrt3}{2}&-\frac{\sqrt3}{2}
\end{bmatrix}
\begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix}
$$

于是平衡正序量满足：

$$x_\alpha=X_m\cos\theta,\qquad x_\beta=X_m\sin\theta$$

也就是说，$\alpha\beta$ 空间矢量幅值与单相峰值相同。对零序为零的逆变换为：

$$
\begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix}=
\begin{bmatrix}
1&0\\
-\frac12&\frac{\sqrt3}{2}\\
-\frac12&-\frac{\sqrt3}{2}
\end{bmatrix}
\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}
$$

本知识库后续 FOC 主线采用这一约定。它便于按相电流峰值设置限幅：当 $(i_a,i_b,i_c)=(I,-I/2,-I/2)$ 时，恰有 $i_\alpha=I$、$i_\beta=0$。

### 零序与功率系数

若希望保留等幅值约定下的零序，可定义 $x_0=(x_a+x_b+x_c)/3$，并在逆变换中给每相加上 $x_0$。这套变量并非单位正交标定，因此瞬时功率应写成：

$$p_{abc}=\frac32(u_\alpha i_\alpha+u_\beta i_\beta)+3u_0i_0$$

三相三线 FOC 中通常 $u_0=i_0=0$，故常见简式为 $p_{abc}=\frac32(u_\alpha i_\alpha+u_\beta i_\beta)$。不要把这条 $3/2$ 系数遗漏到功率、损耗或能量计算里。

## 3. 等功率：用于保持内积的约定

等功率变换把三相空间的三个正交基归一化为单位长度：

$$
\begin{bmatrix}x_\alpha\\x_\beta\\x_0\end{bmatrix}=
\sqrt{\frac23}
\begin{bmatrix}
1&-\frac12&-\frac12\\
0&\frac{\sqrt3}{2}&-\frac{\sqrt3}{2}\\
\frac{1}{\sqrt2}&\frac{1}{\sqrt2}&\frac{1}{\sqrt2}
\end{bmatrix}
\begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix}
$$

该矩阵为正交矩阵，逆变换就是其转置。若电压和电流都用同一套等功率变换，则：

$$p_{abc}=u_\alpha i_\alpha+u_\beta i_\beta+u_0i_0$$

等功率变量的 $\alpha\beta$ 幅值会比等幅值变量大 $\sqrt{3/2}$ 倍：

$$
\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}_{power}=
\sqrt{\frac32}
\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}_{amplitude}
$$

它适合理论推导和需要直接计算内积的场合；它并不比等幅值更准确，只是量纲标定不同。两套变换都能实现 FOC，前提是正变换、反变换、PI 限幅、调制电压、功率和转矩公式采用同一套定义。

## 4. 一组数据同时检查两种标定

取 $i_a=10\ \mathrm A$、$i_b=-3\ \mathrm A$、$i_c=-7\ \mathrm A$，电流和为零。

| 项目 | 等幅值 | 等功率 |
|---|---:|---:|
| $i_\alpha$ | $10.000\ \mathrm A$ | $12.247\ \mathrm A$ |
| $i_\beta$ | $2.309\ \mathrm A$ | $2.828\ \mathrm A$ |
| 矢量幅值 | $10.263\ \mathrm A$ | $12.570\ \mathrm A$ |

两列幅值之比为 $\sqrt{3/2}$。用这类已知零序为零的向量做往返测试，比只检查某一行矩阵更容易发现比例、相序或 $\beta$ 轴符号错误。

## 5. 软件实现：先固定约定，再追求简化

以下 C 代码采用本知识库的**等幅值、$a-b-c$ 相序、零序为零**约定。`ClarkeAmplitudeFast` 只接收两相采样，隐含条件是第三相可由三线制约束重构。

```c
#include <math.h>

#define SQRT3_BY_2  0.86602540378f
#define TWO_BY_3    0.66666666667f
#define SQRT2_BY_3  0.81649658093f

void ClarkeAmplitude(float ia, float ib, float ic, float *ialpha, float *ibeta)
{
    *ialpha = TWO_BY_3 * (ia - 0.5f * ib - 0.5f * ic);
    *ibeta = TWO_BY_3 * SQRT3_BY_2 * (ib - ic);
}

void ClarkeAmplitudeFast(float ia, float ib, float *ialpha, float *ibeta)
{
    *ialpha = ia;
    *ibeta = (ia + 2.0f * ib) / 1.73205080757f;
}

void InverseClarkeAmplitude(float ialpha, float ibeta, float *ia, float *ib, float *ic)
{
    *ia = ialpha;
    *ib = -0.5f * ialpha + SQRT3_BY_2 * ibeta;
    *ic = -0.5f * ialpha - SQRT3_BY_2 * ibeta;
}

void ClarkePower(float ia, float ib, float ic, float *ialpha, float *ibeta)
{
    *ialpha = SQRT2_BY_3 * (ia - 0.5f * ib - 0.5f * ic);
    *ibeta = SQRT2_BY_3 * SQRT3_BY_2 * (ib - ic);
}
```

若硬件采三相电流，可在变换前记录 $i_a+i_b+i_c$；若该值持续大于噪声阈值，应排查采样偏置、零序路径和传感器极性，不应静默套用快速公式。电压通道也应遵守相同的相序与标定约定，否则电流环会表现为增益偏差或旋转方向错误。

## 6. 常见错误与定位顺序

| 现象 | 常见原因 | 先检查什么 |
|---|---|---|
| 电流幅值整体差 $\sqrt{3/2}$ | 等幅值与等功率混用 | 正、逆 Clarke 的系数及 PI 输入输出定义 |
| 转矩方向反了或 $i_q$ 符号异常 | $b,c$ 相接反，或 $\beta$ 轴符号相反 | 相序、传感器极性、Park 角度正方向 |
| 两电阻重构在特定扇区失真 | 采样窗口不足或错误假设第三相 | PWM 采样时刻与重构条件 |
| 功率计算相差 $3/2$ | 使用等幅值变量却按等功率公式相乘 | 电压、电流是否使用同一标定 |
| 三相往返变换后不一致 | 零序不为零却使用零序为零逆变换 | $i_a+i_b+i_c$ 与零序通道 |

## 7. 自测

1. 对 $(i_a,i_b,i_c)=(6,-3,-3)\ \mathrm A$，等幅值变换的 $i_\alpha$、$i_\beta$ 各是多少？
2. 若等幅值变量为 $(i_\alpha,i_\beta)=(4,0)\ \mathrm A$，逆 Clarke 后三相电流是多少？
3. 在等幅值约定中，为什么功率公式前有 $3/2$，而等功率约定中没有？

<details>
<summary>参考答案</summary>

1. $(6,0)\ \mathrm A$。
2. $(4,-2,-2)\ \mathrm A$。
3. 等幅值变换不是单位正交标定；等功率变换保持三相内积，因此两套变量的功率关系不同。
</details>

## 延伸阅读

- [[001-三相坐标系与自然坐标系]]：三相自然坐标系、零序与电压层级。
- [[003-Park变换与旋转坐标系]]：把静止的 $\alpha\beta$ 量旋转到 $dq$ 平面。
- [MathWorks：Clarke Transform](https://www.mathworks.com/help/mcb/ref/clarketransform.html)：三相三线、两电阻采样与零序处理。
