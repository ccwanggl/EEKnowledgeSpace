---
tags: [index, readme, 03-digital-electronics]
date-created: 2026-06-17
---

# 数字电子电路（03-Digital-Electronics）

> 逻辑门、组合/时序电路、FPGA、Verilog 等数字系统设计。

---

## 从一个任务开始

[[00-Index/03-AI自学任务索引#数字电子：从真值表到验证|数字电子：从真值表到验证]]。先试做，根据卡点回正文或找 AI 提示，再用变式独立验收。

## 模块导航

- [[03-Digital-Electronics/01-数字逻辑基础/001-核心概念|数字逻辑基础]]
- [[03-Digital-Electronics/02-组合逻辑电路/001-核心特点|组合逻辑电路]]
- [[03-Digital-Electronics/03-时序逻辑与状态机/001-锁存器与触发器|时序逻辑与状态机]]
- [[03-Digital-Electronics/04-FPGA入门/001-FPGA核心概念|FPGA入门]]
- [[03-Digital-Electronics/05-Verilog与HDL/001-核心思想硬件vs软件|Verilog与HDL]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "03-Digital-Electronics"
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
| 《Digital Design and Computer Architecture》 | David Harris & Sarah Harris | 中-高级 | 01-数字逻辑基础、02-组合逻辑电路、03-时序逻辑与状态机、05-Verilog与HDL | 购买 |
| 《FPGA Prototyping by Verilog Examples》 | Pong P. Chu | 中-高级 | 04-FPGA入门、05-Verilog与HDL | 购买 |
| 《Computer Organization and Design RISC-V Edition》 | Patterson & Hennessy | 高级 | 03-时序逻辑与状态机、04-FPGA入门 | 购买 / 免费PDF（riscv.org） |
| 《Practical Electronics for Inventors》 | Paul Scherz & Simon Monk | 入门级 | 01-数字逻辑基础（数字电路章节） | 购买 |
| 《The Art of Electronics》 | Paul Horowitz & Winfield Hill | 中-高级 | 01-数字逻辑基础、02-组合逻辑电路 | 购买 |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| **Ben Eater** | YouTube | 8-bit CPU 面包板系列，数字逻辑顶级可视化教程 | 01-数字逻辑基础、02-组合逻辑电路、03-时序逻辑与状态机 |
| **nandland** | YouTube | FPGA 和 Verilog 教程，从基础到项目 | 04-FPGA入门、05-Verilog与HDL |
| **MIT OCW: 6.004 Computation Structures** | MIT OpenCourseWare | 从门电路到处理器，经典计算机架构课程 | 01-数字逻辑基础、02-组合逻辑电路、03-时序逻辑与状态机 |
| **HDLBits** | 网站 | 在线 Verilog 编程练习，即时反馈 | 05-Verilog与HDL |
| **nandland Verilog Tutorial** | 网站/YouTube | 免费 Verilog 课程，适合零基础入门 | 05-Verilog与HDL |
| **GreatScott!** | YouTube | 可视化解释，数字电路项目导向 | 01-数字逻辑基础 |
| **Afrotechmods** | YouTube | 动画清晰，数字电路概念解释极好 | 01-数字逻辑基础 |
| **Phil's Lab** | YouTube | 模拟/数字电路、FPGA、控制设计 | 02-组合逻辑电路、04-FPGA入门 |
| **艾熊博士** | Bilibili | FPGA、Verilog、数字设计（中文） | 04-FPGA入门、05-Verilog与HDL |
| **爱上半导体** | Bilibili/YouTube | 硬件原理可视化极好，MOS管、I2C、LCD等（中文） | 01-数字逻辑基础 |
| **Coursera "FPGA Design for Embedded Systems"** | Coursera (UC Boulder) | FPGA 设计系统课程 | 04-FPGA入门 |
| **Khan Academy: Electrical Engineering** | Khan Academy | 免费数字电路基础课程 | 01-数字逻辑基础 |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| **AllAboutCircuits** | 英文 | 最全面的免费电路教程，数字电路章节详尽 | 01-数字逻辑基础、02-组合逻辑电路 |
| **Hackaday** | 英文 | 每日硬件项目、新闻、数字电路教程 | 全模块 |
| **EEWorld（电子工程世界）** | 中文 | 国内最大 EE 社区，数字电路讨论丰富 | 全模块 |
