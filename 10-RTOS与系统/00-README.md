---
tags: [index, readme, 10-rtos与系统]
date-created: 2026-06-17
---

# RTOS 与系统（10-RTOS与系统）

> FreeRTOS、Zephyr、RT-Thread 及嵌入式 Linux 基础。

---

## 从一个任务开始

[[00-Index/03-AI自学任务索引#实时系统：比较任务的周期与响应|实时系统：比较任务的周期与响应]]。先试做，根据卡点回正文或找 AI 提示，再用变式独立验收。

## 模块导航

- [[10-RTOS与系统/01-RTOS基础/01-RTOS基础|RTOS基础]]
- [[10-RTOS与系统/02-FreeRTOS/02-FreeRTOS|FreeRTOS]]
- [[10-RTOS与系统/03-Zephyr/03-Zephyr|Zephyr]]
- [[10-RTOS与系统/04-RT-Thread/04-RT-Thread|RT-Thread]]
- [[10-RTOS与系统/05-嵌入式Linux入门/05-嵌入式Linux入门|嵌入式Linux入门]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "10-RTOS与系统"
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

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[02-MOC-主题索引|主题索引]]
- [[01-学习路线图|学习路线图]]

---

## 推荐资源

> 以下资源按相关性和学习阶段推荐，与 [[12-Resources/00-README|12-Resources]] 中的完整资源列表互为补充。本模块涵盖 FreeRTOS、Zephyr、RT-Thread 及嵌入式 Linux 基础，资源选取围绕这些核心主题展开。

### 推荐书籍

| 书籍 | 作者 | 级别 | 适用内容 | 获取方式 |
|------|------|------|----------|----------|
| **《Mastering the FreeRTOS Real Time Kernel》** | Richard Barry | 初级~中级 | FreeRTOS 内核原理、任务调度、同步机制、中断管理；对应 [[02-FreeRTOS]] 全部内容 | 免费 PDF — freertos.org |
| **《Making Embedded Systems》** | Elecia White | 初级~中级 | 嵌入式系统设计方法、需求分析、架构设计、实现与测试；对应 [[01-RTOS基础]] 中的 RTOS 选型与系统设计思路 | 亚马逊/多抓鱼 |
| **《Programming Embedded Systems in C and C++》** | Michael Barr & Anthony Massa | 初级~中级 | 固件编程核心技能、中断、驱动、调试；对应 [[01-RTOS基础]] 的"为什么需要 RTOS"及 [[02-FreeRTOS]] 的 API 实践 | 亚马逊/O'Reilly |
| **《The Definitive Guide to ARM Cortex-M3/M4》** | Joseph Yiu | 中级~高级 | ARM Cortex-M 架构深入、NVIC、SysTick、MPU；理解 RTOS 运行的硬件基础，对应 [[01-RTOS基础]] 核心概念中的上下文切换与中断 | 亚马逊/电子版 |
| **《Linux Device Drivers》第3版** | Jonathan Corbet 等 | 中级~高级 | 嵌入式 Linux 设备驱动、内核模块、字符设备；对应 [[16-Linux设备驱动开发/00-README|16-Linux设备驱动开发]] 全部内容 | 免费在线 — lwn.net |
| **《Mastering STM32》** | Carmine Noviello | 中级 | STM32  HAL/LL 库及 FreeRTOS 集成；对应 [[02-FreeRTOS]] 在 STM32 上的移植与实践 | 免费在线 — github.com/cnovak/mstm32 |
| **《Embedded C》** | Michael J. Pont | 初级 | 嵌入式 C 编程基础、位操作、寄存器访问；对应 [[01-RTOS基础]] 的入门铺垫 | 亚马逊/多抓鱼 |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| **FastBit Embedded Brain Academy** | YouTube | STM32 嵌入式最系统的课程，含 FreeRTOS 专题 | [[02-FreeRTOS]] 实践、任务管理、信号量、队列 |
| **正点原子** | Bilibili | STM32 中文系统教程，含 FreeRTOS 章节 | [[02-FreeRTOS]] 中文入门、STM32 移植（中文） |
| **野火电子** | Bilibili | STM32/FPGA 教程，含 RTOS 对比与实战 | [[01-RTOS基础]] 的"常见 RTOS"对比、[[04-RT-Thread]] 入门（中文） |
| **Nordic DevAcademy** | 官网 | BLE、Zephyr、nRF52 开发官方课程 | [[03-Zephyr]] 入门、Zephyr 内核与设备模型 |
| **Bootlin Training** | 官网/YouTube | 免费嵌入式 Linux 培训视频，内核驱动、Yocto、Buildroot | [[05-嵌入式Linux入门]] 全部内容 |
| **Coursera "Embedded Systems"** | Coursera | UC Boulder 开设，ARM Cortex-M 系列课程 | [[01-RTOS基础]] 的调度、中断、低功耗设计 |
| **Paul McWhorter** | YouTube | Arduino/Raspberry Pi 最系统的嵌入式入门教程 | [[01-RTOS基础]] 入门铺垫、理解嵌入式编程思维 |
| **江协科技** | Bilibili | STM32 标准库+HAL 最系统的中文教程，含 FreeRTOS 项目 | [[02-FreeRTOS]] 在 STM32 上的项目实践（中文） |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| **DeepBlue Embedded** | 英文 | 嵌入式教程质量极高，STM32/ESP32 固件开发，含 FreeRTOS 深度文章 | [[02-FreeRTOS]] 配置裁剪、调试技巧、内存管理 |
| **FreeRTOS 官方文档** | 英文 | 官方 API 参考、快速入门指南、移植说明 | [[02-FreeRTOS]] 全部内容，特别是 [[002-核心API]] 和 [[003-配置与裁剪FreeRTOSConfigh]] |
| **Zephyr Project 官方文档** | 英文 | Zephyr 内核、设备驱动、网络、安全完整文档 | [[10-RTOS与系统/03-Zephyr/03-Zephyr|Zephyr]] 全部内容，特别是 [[10-RTOS与系统/03-Zephyr/003-架构|Zephyr 架构]] |
| **RT-Thread 官方文档** | 中文/英文 | 中文 RTOS 文档最全，含内核、组件、BSP 指南 | [[10-RTOS与系统/04-RT-Thread/04-RT-Thread|RT-Thread]] 全部内容，特别是 [[10-RTOS与系统/04-RT-Thread/002-核心特点|RT-Thread 核心特点]] 和 [[10-RTOS与系统/04-RT-Thread/003-架构|RT-Thread 架构]] |
| **Hackaday** | 英文 | 每日硬件项目、RTOS 应用案例、新闻 | 跨模块项目灵感，结合 [[11-Projects/00-README|11-Projects]] 实践 |
| **EEWorld（电子工程世界）** | 中文 | 国内最大 EE 社区，RTOS 讨论区、技术文章 | [[01-RTOS基础]] 的选型讨论、[[04-RT-Thread]] 社区资源（中文） |
