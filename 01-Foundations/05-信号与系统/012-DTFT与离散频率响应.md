---
tags: [foundation, signals-and-systems]
date-created: 2026-11-04
date-updated: 2026-11-04
---

# 012-DTFT与离散频率响应

> [!abstract] 本章定位
> **前置知识**：006 的连续傅里叶变换、011 的序列和离散卷积。
> **本章回答**：离散序列有哪些频率？数字滤波器怎样改变每个频率？
> **本章边界**：建立 DTFT；有限数据的 DFT、窗函数和 FFT 在 014 展开。

## MIT 课程讲解

**MIT RES.6-007 第 11 讲：离散时间傅里叶变换**

用同一个一阶离散系统检查频率响应的周期性。

<iframe src="https://www.youtube.com/embed/HKMY-8BqWWw" title="MIT RES.6-007 第 11 讲：离散时间傅里叶变换" width="100%" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>

[打开原页](https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/resources/lecture-11-discrete-time-fourier-transform/)

## 1. 从复指数到分析与合成

离散 LTI 系统对 $e^{j\Omega n}$ 的零状态响应为

$$y[n]=\sum_kh[k]e^{j\Omega(n-k)}
=e^{j\Omega n}\underbrace{\sum_kh[k]e^{-j\Omega k}}_{H(e^{j\Omega})}.$$

求和存在时，复指数是本征序列。定义 DTFT 及逆变换：

$$X(e^{j\Omega})=\sum_{n=-\infty}^{\infty}x[n]e^{-j\Omega n},$$
$$x[n]=\frac1{2\pi}\int_{-\pi}^{\pi}X(e^{j\Omega})e^{j\Omega n}\,d\Omega.$$

绝对可和是 DTFT 作为普通连续函数存在的充分条件；平方可和可用均方意义处理，周期序列可用广义函数处理。有限序列也是定义中的特例。

## 2. 离散时间与连续频率

由于 $n$ 是整数，$X(e^{j(\Omega+2\pi)})=X(e^{j\Omega})$。积分只需一个完整周期，也可选 $[0,2\pi)$。DTFT 的频率变量连续，“离散时间”不表示“只剩几个频点”。

| 物理频率（$f_s=8\,\mathrm{kHz}$） | 数字角频率 | 含义 |
|---|---|---|
| 1 kHz | $\pi/4$ | 每个采样间隔相位前进 $\pi/4$ |
| 4 kHz | $\pi$ | 奈奎斯特频率 |
| 7 kHz | $7\pi/4\equiv-\pi/4$ | 与 -1 kHz 复指数采样序列相同 |

实余弦的 7 kHz 与 1 kHz 采样可能表现为同一频率；带相位时须同时检查相位符号。

## 3. 核心性质

| 时域 | DTFT |
|---|---|
| $a x[n]+b y[n]$ | $aX+bY$ |
| $x[n-n_0]$ | $e^{-j\Omega n_0}X$ |
| $e^{j\Omega_0n}x[n]$ | $X(e^{j(\Omega-\Omega_0)})$ |
| $x*h$ | $XH$ |
| $x[n]w[n]$ | $\frac1{2\pi}\int_{-\pi}^{\pi}X(e^{j\theta})W(e^{j(\Omega-\theta)})d\theta$ |

最后一行是频域周期卷积，是有限记录加窗产生谱展宽的基础。实序列满足 $X(e^{-j\Omega})=X^*(e^{j\Omega})$。

对能量序列，Parseval 关系为

$$\sum_n|x[n]|^2=\frac1{2\pi}\int_{-\pi}^{\pi}|X(e^{j\Omega})|^2d\Omega.$$

## 4. 贯穿案例：一阶递归滤波器

由上一章 $h[n]=(1-a)a^nu[n]$，$0<a<1$：

$$H(e^{j\Omega})=(1-a)\sum_{n=0}^{\infty}(ae^{-j\Omega})^n
=\frac{1-a}{1-ae^{-j\Omega}},$$
$$|H(e^{j\Omega})|=\frac{1-a}{\sqrt{1+a^2-2a\cos\Omega}}.$$

直流增益为 1，奈奎斯特处增益为 $(1-a)/(1+a)$。取 $a=1/2$，在 $\Omega=\pi$ 处增益为 $1/3$；因此它比直流更强地衰减快速交替输入。

对稳定系统，输入 $A\cos(\Omega_0n+\varphi)$ 的稳态输出为 $A|H(e^{j\Omega_0})|\cos(\Omega_0n+\varphi+\angle H)$。开机暂态另行叠加。

两点平均器的响应为

$$H(e^{j\Omega})=\frac12(1+e^{-j\Omega})=e^{-j\Omega/2}\cos(\Omega/2).$$

在 $\Omega=\pi$ 有零点，解释上一章交替序列输出为零。相位在幅度为零处没有定义。

## 5. 周期序列的傅里叶级数（DTFS）

周期为 $N$ 的序列只需要 $N$ 个不同的复指数基：

$$x[n]=\sum_{k=0}^{N-1}c_ke^{j2\pi kn/N},\qquad
c_k=\frac1N\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}.$$

系数按 $N$ 周期重复。其 DTFT 是每隔 $2\pi$ 重复的冲激线谱，在一个频率周期内，谱线权重为 $2\pi c_k$。不要把周期序列的冲激谱与有限序列的连续 DTFT 曲线混为一谈。

## 6. 与 Z 变换的连接和自测

Z 变换把单位模的频率因子推广为 $z=re^{j\Omega}$。当其收敛域包含单位圆时，代入 $z=e^{j\Omega}$ 得到 DTFT。下一章解释模长权重、ROC 与稳定性的关系。

1. $x[n]=\delta[n]-\delta[n-1]$ 的 DTFT 是什么？核对：$1-e^{-j\Omega}$，直流为零。
2. 为什么把 DTFT 积分范围改成 $[0,\pi]$ 通常不能直接重建原序列？核对：缺少半个频率周期；实信号也必须正确利用对称性及相应重建系数。
3. 求 $[1,1]$（其余为零）的能量并用 Parseval 核对。核对：时域为 2；$|X|^2=2+2\cos\Omega$，积分后同为 2。

> **上一章**：[[011-离散时间信号与系统]]
> **下一章**：[[013-Z变换与离散时间系统]]
