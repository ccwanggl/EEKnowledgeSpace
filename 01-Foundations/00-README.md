---
tags: [index, readme, 01-foundations]
date-created: 2026-06-17
---

# 基础理论（01-Foundations）

> 电子工程的数学、物理与电路分析基础，是后续所有主题的基石。

---

## 模块导航

- [[01-Foundations/01-数学与物理基础/000-README|数学与物理基础]]
- [[01-Foundations/02-电路基础理论/000-README|电路基础理论]]
- [[01-Foundations/03-电路分析方法/000-电路分析方法|电路分析方法]]
- [[01-Foundations/04-电子元器件/000-README|电子元器件]]
- [[01-Foundations/05-信号与系统/000-信号与系统|信号与系统]]
- [[01-Foundations/06-ADC与DAC基础/000-ADC与DAC基础|ADC与DAC基础]]
- [[01-Foundations/07-测量与仪器基础/000-测量与仪器基础|测量与仪器基础]]
- [[01-Foundations/08-嵌入式C编程/000-嵌入式C编程|嵌入式C编程]]
- [[01-Foundations/09-学习方法与工具/000-学习方法与工具|学习方法与工具]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "01-Foundations"
WHERE file.name != "00-README"
SORT file.name ASC
```

---

## 推荐学习路径

1. 先浏览本目录下的核心概念文件。
2. 完成相关 [[08-测验题索引|测验题]] 检验理解。
3. 结合 [[01-项目总览]] 中的项目动手实践。
4. 遇到问题时查阅 [[01-调试工具概述|调试工具]] 和 [[02-工具清单|工具清单]]。

---


## 推荐资源

> 以下资源按相关性和学习阶段推荐，与 [[12-Resources/00-README|12-resources]] 中的完整资源列表互为补充。

### 推荐书籍

| 书籍 | 作者 | 级别 | 适用内容 | 获取方式 |
|------|------|------|----------|----------|
| 《The Art of Electronics》 | Paul Horowitz & Winfield Hill | 入门-进阶 | 电路基础、模拟/数字电路、元器件、信号处理 | 购买 |
| 《Practical Electronics for Inventors》 | Paul Scherz & Simon Monk | 入门 | 电路基础、元器件、模拟电路，数学较少 | 购买 |
| 《Engineering Mathematics》 | K.A. Stroud | 入门 | 数学与物理基础（微积分、线性代数、复数） | 购买 |
| 《Op Amps for Everyone》 | Ron Mancini | 入门-进阶 | 运放原理、电路分析、信号处理（对应 `02-电路基础理论`、`03-电路分析方法`） | **TI 免费 PDF** |
| 《Analog Engineer's Pocket Reference》 | TI | 入门 | 模拟电路速查、ADC/DAC 参数、常用公式 | **TI 免费 PDF** |
| 《Digital Design and Computer Architecture》 | David Harris & Sarah Harris | 入门-进阶 | 数字逻辑、信号与系统、计算机架构（对应 `05-信号与系统`、`06-ADC与DAC基础`） | 购买 |
| 《Feedback Systems》 | Karl J. Åström & Richard M. Murray | 进阶 | 控制理论、信号系统分析（对应 `05-信号与系统`） | **Caltech 免费在线** |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| **GreatScott!** | YouTube | 可视化解释，项目导向，从基础到进阶 | 电路基础、元器件、动手实验（对应 `02-电路基础理论`、`04-电子元器件`） |
| **Afrotechmods** | YouTube | 动画清晰，概念解释极好，适合零基础 | 电路基础、信号与系统、模拟电路（对应 `02-电路基础理论`、`05-信号与系统`） |
| **EEVblog** | YouTube | 世界最大电子工程博客，Dave Jones 讲解深入 | 测量与仪器基础、电路分析、元器件评测（对应 `07-测量与仪器基础`、`04-电子元器件`） |
| **3Blue1Brown** | YouTube | 数学可视化，傅里叶变换、线性代数、微积分 | 数学与物理基础（对应 `01-数学与物理基础`、`05-信号与系统`） |
| **Ben Eater** | YouTube | 计算机架构、数字逻辑、网络协议的顶级教程 | 数字逻辑、信号系统、ADC/DAC 原理（对应 `05-信号与系统`、`06-ADC与DAC基础`） |
| **Phil's Lab** | YouTube | 模拟/数字电路、PCB、控制、电源设计 | 电路分析方法、信号处理、控制系统（对应 `03-电路分析方法`、`05-信号与系统`） |
| **W2AEW** | YouTube | 测试设备、测量技巧、电路实验、射频基础 | 测量与仪器基础、电路分析实验（对应 `07-测量与仪器基础`） |
| **爱上半导体** | Bilibili/YouTube | 硬件原理可视化极好，**中文** | 电路基础、元器件原理、通信协议（对应 `02-电路基础理论`、`04-电子元器件`） |
| **MIT OCW: 6.002 Circuits and Electronics** | MIT OpenCourseWare | 经典 MIT 电路课程，**免费** | 电路基础理论、电路分析方法（对应 `02-电路基础理论`、`03-电路分析方法`） |
| **Khan Academy: Electrical Engineering** | Khan Academy | 电路、半导体、信号处理，**免费** | 电路基础、数学与物理基础（对应 `01-数学与物理基础`、`02-电路基础理论`） |
| **TI Precision Labs** | Texas Instruments | 运放、ADC、电源、传感器，**免费视频** | ADC/DAC 基础、模拟电路、信号链（对应 `06-ADC与DAC基础`、`02-电路基础理论`） |
| **nandland Verilog Tutorial** | nandland | 免费 Verilog 课程 | 数字逻辑基础（对应 `05-信号与系统`） |
| **HDLBits** | HDLBits | 在线 Verilog 编程练习 | 数字逻辑与电路设计（对应 `05-信号与系统`） |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| **AllAboutCircuits** | 英文 | 最全面的免费电路教程，从欧姆定律到射频 | 电路基础理论、电路分析方法、元器件（对应 `02-电路基础理论`、`03-电路分析方法`、`04-电子元器件`） |
| **SparkFun Tutorials** | 英文 | 教育友好，从基础到传感器 | 电路基础、元器件入门、学习方法（对应 `02-电路基础理论`、`04-电子元器件`、`09-学习方法与工具`） |
| **EEWorld（电子工程世界）** | **中文** | 国内最大 EE 社区 | 电路分析、元器件、信号系统、测量仪器讨论（对应全模块） |
| **DeepBlue Embedded** | 英文 | 嵌入式教程质量极高，STM32/ESP32 | 嵌入式 C 编程基础（对应 `08-嵌入式C编程`） |
| **Adafruit Learning System** | 英文 | 传感器、项目、库教程 | 元器件应用、动手实验（对应 `04-电子元器件`） |
| **Hackaday** | 英文 | 每日硬件项目、新闻、教程 | 电路分析案例、元器件应用、学习方法（对应 `02-电路基础理论`、`09-学习方法与工具`） |

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[02-MOC-主题索引|主题索引]]
- [[01-学习路线图|学习路线图]]
