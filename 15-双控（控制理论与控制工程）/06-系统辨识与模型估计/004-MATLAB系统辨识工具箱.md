---
tags: [control-theory, control-engineering, system-identification, matlab]
date-created: 2026-07-03
---

# MATLAB 系统辨识工具箱

## 1. 工具箱概览

MATLAB 的 System Identification Toolbox 是工业界和学术界最常用的系统辨识平台之一。它将复杂的辨识算法封装成高级函数，让用户可以专注于"做什么"而不是"怎么做"。

```
┌─────────────────────────────────────────────────────────────┐
│            MATLAB System Identification Toolbox              │
├─────────────────────────────────────────────────────────────┤
│  Data Layer: iddata, detrend, idfilt, getexp, merge         │
├─────────────────────────────────────────────────────────────┤
│  Model Estimation:                                          │
│    arx, armax, oe, bj, n4sid, ssest,                        │
│    tfest, procest, greyest                                  │
├─────────────────────────────────────────────────────────────┤
│  Model Analysis:                                            │
│    compare, resid, sim, predict, bode, pzmap                │
├─────────────────────────────────────────────────────────────┤
│  Model Conversion:                                          │
│    idss, idtf, idpoly, idfrd, ss, tf, zpk                  │
└─────────────────────────────────────────────────────────────┘
```

## 2. 数据对象：iddata

一切辨识的起点是 `iddata` 对象，它将输入输出数据封装成统一格式。

```matlab
% Create iddata object from raw vectors
% y: output (Nx1 or Nxp)
% u: input  (Nx1 or Nxm)
% Ts: sampling time
data = iddata(y, u, Ts);

% Multi-experiment data (for merging multiple runs)
data1 = iddata(y1, u1, Ts);
data2 = iddata(y2, u2, Ts);
data_merged = merge(data1, data2);

% Split into estimation and validation sets
data_est = data(1:500);     % first 500 samples
data_val = data(501:end);   % remaining samples
```

### 2.1 数据预处理

```matlab
% Remove linear trend (drift removal)
data_detrend = detrend(data);

% High-pass filter to remove low-frequency disturbances
data_filtered = idfilt(data, 3, [0.05 0.5]);  % 3rd-order Butterworth, passband

% Select specific I/O channels
data_sub = data(:, [1 2], [1]);  % outputs 1,2 and input 1
```

## 3. 模型估计函数速查

| 函数 | 模型结构 | 适用场景 | 求解方法 |
|------|---------|---------|---------|
| `arx` | ARX: $A(q)y = B(q)u + e$ | 线性系统，快速 | 最小二乘（解析解） |
| `armax` | ARMAX: $Ay = Bu + Ce$ | 有色噪声环境 | 预测误差法（迭代） |
| `oe` | OE: $y = G(q)u + e$ | 输出端噪声 | 预测误差法（迭代） |
| `bj` | Box-Jenkins | 一般线性系统 | 预测误差法（迭代） |
| `n4sid` | 状态空间 | MIMO 系统 | 子空间方法 |
| `ssest` | 状态空间 | 连续/离散 | 预测误差法 |
| `tfest` | 传递函数 | SISO 频域/时域 | 最小二乘/PEM |
| `procest` | 过程模型 (FOPDT/SOPDT) | 工业过程 | 专门优化 |
| `greyest` | 灰箱状态空间 | 已知结构 | 预测误差法 |

## 4. 完整辨识流程示例

### 4.1 问题：辨识一个加热系统的模型

假设我们有一个加热炉，输入是加热功率 $P$ [kW]，输出是炉内温度 $T$ [$^\circ$C]。采集了 2000 秒的数据，采样周期 $T_s = 1$ s。

### 4.2 MATLAB 完整代码

```matlab
%% System Identification Toolbox: Complete Workflow
% Heating furnace: power [kW] -> temperature [deg C]

clear; clc; close all;

%% 1. Generate synthetic data (replace with real data in practice)
Ts = 1;                         % sampling time [s]
N = 2000;
t = (0:N-1)' * Ts;

% True system: second-order with delay (FOPDT approximated as 2nd order)
zeta = 0.7;
wn = 0.1;                       % natural frequency [rad/s]
K = 5.0;                        % static gain [degC/kW]

% Continuous-time transfer function
s = tf('s');
G_true = K * wn^2 / (s^2 + 2*zeta*wn*s + wn^2);

% Generate input: PRBS-like signal for persistent excitation
rng(42);
u = 2 * rand(N, 1) - 1;
% Smooth slightly to avoid unrealistic high-frequency content
u = filter(0.3, [1 -0.7], u);
u = u / max(abs(u)) * 0.8;     % normalize to 80% max power

% Simulate with noise
y_noiseless = lsim(G_true, u, t);
y = y_noiseless + 0.5 * randn(N, 1);   % add noise

%% 2. Create and inspect iddata object
data = iddata(y, u, Ts);
data.Name = 'Heating Furnace';
data.InputName = {'Power'};
data.InputUnit = {'kW'};
data.OutputName = {'Temperature'};
data.OutputUnit = {'degC'};

figure;
plot(data);
title('Raw Input-Output Data');

%% 3. Preprocessing
data = detrend(data);           % remove mean/drift

% Split estimation / validation
data_est = data(1:1200);
data_val = data(1201:end);

%% 4. Try different model structures

% 4.1 ARX model (fast, analytic solution)
n_a = 2;  n_b = 2;  n_k = 1;   % delays and orders
m_arx = arx(data_est, [n_a n_b n_k]);

% 4.2 OE model (output error, better for output noise)
m_oe = oe(data_est, [n_b n_a n_k]);

% 4.3 State-space model (subspace method)
m_ss = n4sid(data_est, 2);      % 2nd-order state-space

% 4.4 Process model (FOPDT)
m_proc = procest(data_est, 'P2D');  % 2nd-order plus delay

%% 5. Model comparison on validation data
figure;
compare(data_val, m_arx, m_oe, m_ss, m_proc);
title('Model Comparison on Validation Data');
legend('ARX', 'OE', 'State-Space', 'Process', 'Measured');

%% 6. Residual analysis (whiteness check)
figure;
resid(data_val, m_oe);

%% 7. Frequency response comparison
figure;
w = logspace(-3, 0, 200);
bodeplot(m_arx, m_oe, m_ss, w);
legend('ARX', 'OE', 'State-Space');
title('Bode Plot Comparison');

%% 8. Display model parameters
fprintf('\n--- ARX Model ---\n');
disp(m_arx);
fprintf('\n--- OE Model ---\n');
disp(m_oe);
fprintf('\n--- State-Space Model ---\n');
disp(m_ss);

%% 9. Convert to standard control design formats
G_arx_tf = tf(m_arx);
G_oe_tf = tf(m_oe);
G_ss_ss = ss(m_ss);

fprintf('\n--- ARX as Transfer Function ---\n');
disp(G_arx_tf);

%% 10. Prediction horizon analysis
figure;
yp1 = predict(m_oe, data_val, 1);    % 1-step prediction
yp5 = predict(m_oe, data_val, 5);    % 5-step prediction
yp_inf = sim(m_oe, data_val);        % infinite-step (pure simulation)

plot(data_val.SamplingInstants, data_val.OutputData, 'k-', 'LineWidth', 1.5);
hold on;
plot(data_val.SamplingInstants, yp1.OutputData, 'r--');
plot(data_val.SamplingInstants, yp5.OutputData, 'g:');
plot(data_val.SamplingInstants, yp_inf.OutputData, 'b-.');
legend('Measured', '1-step pred', '5-step pred', 'Simulation');
title('Prediction vs Simulation Horizon');
```

### 4.3 结果解读

运行后你会看到：

1. **数据图**：输入输出时间序列，可以直观检查数据质量和信号范围。
2. **模型比较图**：各模型在验证数据上的预测表现，通常用拟合百分比 (Fit%) 评估：

$$
\text{Fit} = 100 \times \left( 1 - \frac{\| y - \hat{y} \|}{\| y - \bar{y} \|} \right)
$$

3. **残差分析图**：残差的自相关函数 (ACF) 和互相关函数 (CCF)。理想情况下，残差应为白噪声——ACF 在滞后 0 处有一个尖峰，其余都在置信区间内。
4. **Bode 图**：比较不同模型在频域上的差异。

## 5. 阶次选择自动化

### 5.1 arxstruc / selstruc

```matlab
% Automatic ARX order selection
V = arxstruc(data_est, data_val, struc(1:5, 1:5, 1:3));
% struc generates all combinations of na, nb, nk in given ranges

nn = selstruc(V, 0);   % 0 = minimize prediction error
% nn(1) = best na, nn(2) = best nb, nn(3) = best nk
m_best_arx = arx(data_est, nn);
```

### 5.2 信息准则：AIC / BIC

```matlab
% Compute AIC and BIC for a model
aic_value = aic(m_oe);

% Compare multiple models
models = {m_arx, m_oe, m_ss};
for i = 1:length(models)
    fprintf('Model %d: AIC = %.2f, BIC = %.2f\n', i, ...
        aic(models{i}), aic(models{i}) + 2*models{i}.na);
end
```

AIC（Akaike Information Criterion）：

$$
\text{AIC} = 2k - 2 \ln(\hat{L})
$$

其中 $k$ 为参数个数，$\hat{L}$ 为最大似然值。AIC 越小越好，它在拟合优度和模型复杂度之间做了惩罚平衡。

## 6. 灰箱辨识：greyest

灰箱辨识是工具箱的强大功能之一。假设我们知道系统的结构（如直流电机方程），但某些参数未知。

```matlab
% Grey-box example: first-order system with unknown parameters
% dx/dt = -a*x + b*u
% y = x + e

% Define continuous-time state-space structure
% Parameters: p = [a; b]
function [A, B, C, D, K, x0] = my_ode(p)
    A = -p(1);
    B =  p(2);
    C = 1;
    D = 0;
    K = 0;
    x0 = 0;
end

% Create idgrey object
odefun = 'my_ode';
parameters = {'a', 0.5; 'b', 1.0};  % initial guesses
m_grey = idgrey(odefun, parameters, 'c');  % 'c' = continuous time

% Estimate
m_est = greyest(data_est, m_grey);
disp(m_est);
```

## 7. 常见错误与纠正

### 错误 1：忘记设置采样时间 Ts

**场景**：`data = iddata(y, u)` 没有指定第三个参数 `Ts`。

**问题**：工具箱默认 `Ts = 1`，如果实际采样时间是 0.01 s，则所有连续时间模型（如 `tfest`、`ssest`）的估计结果将完全错误——时间尺度偏差了 100 倍。

**纠正**：始终显式指定 `Ts`：

```matlab
data = iddata(y, u, Ts);   % Ts is mandatory for correct interpretation
```

### 错误 2：在 `compare` 中使用估计数据而不是验证数据

**场景**：用 `compare(data_est, m)` 评估模型，发现拟合度高达 99%。

**问题**：模型在训练数据上表现好不代表泛化能力强。高拟合度可能只是过拟合——模型记住了噪声模式而不是系统动态。

**纠正**：始终将数据分为 **estimation set** 和 **validation set**，用验证集评估模型：

```matlab
compare(data_val, m);   % use VALIDATION data for fair assessment
```

一个经验法则：拟合度在验证集上比估计集下降不超过 10% 是可以接受的。如果下降超过 20%，说明模型过拟合，应该降低阶次或增加正则化。

## 8. 自测习题

**习题 1**：在 MATLAB 中，`arx(data, [na nb nk])` 的第三个参数 `nk` 表示什么？如果 `nk = 0` 和 `nk = 2`，对模型有什么影响？

<details>
<summary>答案</summary>

`nk` 表示输入到输出的**纯延迟**，以采样周期为单位：

- `nk = 0`：当前输入 $u(t)$ 立即影响当前输出 $y(t)$（严格适当系统，物理上通常不可能）。
- `nk = 1`：输入有一个采样周期的延迟，$u(t-1)$ 影响 $y(t)$。这是最常见的设置。
- `nk = 2`：输入有两个采样周期的延迟，$u(t-2)$ 影响 $y(t)$。

延迟设置不正确会导致：
- 延迟过小（$nk$ 太小）：模型出现非因果行为或需要高阶 $B(q)$ 来补偿缺失的延迟。
- 延迟过大（$nk$ 太大**：$B(q)$ 的领先系数被强制为零，降低模型灵活性。

</details>

**习题 2**：`resid(data, model)` 输出的残差自相关图 (ACF) 中，如果除滞后 0 外还有多个点超出置信区间，说明什么？

<details>
<summary>答案</summary>

说明模型**没有充分捕捉系统的动态特性**，残差中仍然含有可预测的成分。这通常意味着：

1. 模型阶次太低，需要增加 $n_a$ 或 $n_b$；
2. 模型结构选择不当（如用 ARX 拟合 OE 系统）；
3. 输入-输出延迟估计错误；
4. 存在未建模的非线性特性。

</details>

**习题 3**：为什么 `n4sid`（子空间辨识）比 `oe` 更适合 MIMO 系统？

<details>
<summary>答案</summary>

`n4sid` 直接在状态空间框架下工作，估计 $(A, B, C, D)$ 矩阵。状态空间表示天然支持 MIMO 系统：

- $B$ 矩阵的每一列对应一个输入通道；
- $C$ 矩阵的每一行对应一个输出通道；

一次估计即可得到所有输入输出之间的动态关系。

相比之下，`oe` 模型在 MIMO 情况下需要为每个输入-输出对估计一个传递函数，计算量大且难以保证系统的物理一致性（如共同极点）。子空间方法通过 QR 分解和 SVD 一次性提取所有信息，对 MIMO 系统更加高效和稳健。

</details>
