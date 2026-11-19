---
tags: [index, readme, 06-pcb-design]
date-created: 2026-06-17
---

# PCB 设计（06-PCB-Design）

> 原理图设计、PCB 布局布线、阻抗控制、信号完整性与 EMC。

---

## 从一个任务开始

[[00-Index/03-AI自学任务索引#PCB 设计：完成第一块小板的检查|PCB 设计：完成第一块小板的检查]]。先试做，根据卡点回正文或找 AI 提示，再用变式独立验收。

## 模块导航

- [[06-PCB-Design/01-PCB设计基础/01-PCB设计基础|PCB设计基础]]
- [[06-PCB-Design/02-信号完整性基础/02-信号完整性基础|信号完整性基础]]
- [[06-PCB-Design/03-PCB层叠与阻抗设计/03-PCB层叠与阻抗设计|PCB层叠与阻抗设计]]
- [[06-PCB-Design/04-信号完整性与EMC/04-信号完整性与EMC|信号完整性与EMC]]
- [[06-PCB-Design/05-KiCad教程/05-KiCad教程|KiCad教程]]
- [[06-PCB-Design/06-PCB制造与打样/06-PCB制造与打样|PCB制造与打样]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "06-PCB-Design"
WHERE file.name != "00-README"
SORT file.name ASC
```

---

## 推荐学习路径

1. 先浏览本目录下的核心概念文件。
2. 完成相关 [[00-Index/04-练习与复习#按主题找练习和测验|测验题]] 检验理解。
3. 结合 [[01-项目总览]] 中的项目动手实践。
4. 遇到问题时查阅 [[01-调试工具概述|调试工具]] 和 [[02-工具清单|工具清单]]。

---

## 推荐资源

> 以下资源按相关性和学习阶段推荐，与 [[12-Resources/00-README|12-resources]] 中的完整资源列表互为补充。

### 推荐书籍

| 书籍 | 作者 | 级别 | 适用内容 | 获取方式 |
|------|------|------|----------|----------|
| 《Signal Integrity and Power Integrity - Simplified》 | Eric Bogatin | 入门~进阶 | 信号完整性基础、电源完整性、传输线理论、阻抗控制（对应 `02-信号完整性基础`、`03-PCB层叠与阻抗设计`） | 购买 |
| 《PCB Design for Real-World EMI Control》 | Bruce Archambeault | 进阶 | EMC 设计实践、电磁兼容、PCB 布局中的 EMI 抑制（对应 `04-信号完整性与EMC`） | 购买 |
| 《The Art of Electronics》 | Paul Horowitz & Winfield Hill | 入门~进阶 | 电路设计基础、原理图设计参考、模拟/数字电路基础（对应 `01-PCB设计基础`） | 购买 |
| 《Op Amps for Everyone》 | Ron Mancini (TI) | 入门~进阶 | 运放电路设计、原理图设计参考、模拟信号调理（对应 `01-PCB设计基础`） | **免费** (TI PDF) |
| 《Analog Engineer's Pocket Reference》 | TI | 速查 | 模拟电路设计速查、常用公式与参数（全模块参考） | **免费** (TI PDF) |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| Robert Feranec | YouTube | PCB 设计高级技巧、Altium Designer 实战、EMC 设计原则 | PCB 布局布线、EMC 设计（对应 `01-PCB设计基础`、`04-信号完整性与EMC`） |
| Phil's Lab | YouTube | 模拟/数字电路、PCB 设计、FPGA、控制、电源设计 | PCB 设计全流程、信号完整性（对应 `01-03` 全模块） |
| DigiKey: Intro to KiCad | DigiKey 官网 | **免费** 官方 KiCad 课程，从安装到完成 PCB | KiCad 工具使用（对应 `05-KiCad教程`） |
| Phil's Lab PCB 课程 | YouTube | **免费** PCB 设计全流程，从原理图到制造 | PCB 设计完整流程（对应 `01-PCB设计基础`、`06-PCB制造与打样`） |
| TI Precision Labs | TI 官网 | **免费** 运放、ADC、电源、传感器视频课程 | 模拟电路基础、信号链设计（对应 `01-PCB设计基础`） |
| 凡亿教育 | Bilibili/官网 | **中文** PCB 设计课程（Altium/KiCad） | PCB 设计工具、高速 PCB 设计（对应 `05-KiCad教程`、`03-PCB层叠与阻抗设计`） |
| EEVblog | YouTube | 世界最大电子工程博客，Dave Jones 深入讲解电路与仪器 | 电路原理、测量技巧、设计经验（全模块参考） |
| GreatScott! | YouTube | 可视化解释，项目导向，从基础到进阶 | 电子基础概念、项目实践（对应 `01-PCB设计基础`） |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| AllAboutCircuits | 英文 | 最全面的免费电路教程，从欧姆定律到射频 | 电路理论基础、设计参考（全模块参考） |
| Hackaday | 英文 | 每日硬件项目、新闻、教程，社区活跃 | PCB 设计案例、制造技巧、开源项目（对应 `06-PCB制造与打样`） |
| Adafruit Learning System | 英文 | 传感器、项目、库教程，教育友好 | 元件选型、项目实践（对应 `01-PCB设计基础`） |
| SparkFun Tutorials | 英文 | 教育友好，从基础到传感器、PCB 设计 | 基础电子知识、PCB 入门（对应 `01-PCB设计基础`） |
| EEWorld（电子工程世界） | **中文** | 国内最大 EE 社区，论坛、文章、资料丰富 | 国内设计经验、PCB 制造资源、技术讨论（全模块参考） |

---

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[02-MOC-主题索引|主题索引]]
- [[01-学习路线图|学习路线图]]
