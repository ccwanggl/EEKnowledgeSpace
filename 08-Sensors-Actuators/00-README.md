---
tags: [index, readme, 08-sensors-actuators]
date-created: 2026-06-17
---

# 传感器与执行器（08-Sensors-Actuators）

> 常见传感器接口、电机驱动、继电器、显示与音频等执行器。

---

## 模块导航

- [[08-Sensors-Actuators/01-传感器接口/01-传感器接口|传感器接口]]
- [[08-Sensors-Actuators/02-执行器控制/02-执行器控制|执行器控制]]
- [[08-Sensors-Actuators/03-电机驱动/03-电机驱动|电机驱动]]
- [[08-Sensors-Actuators/04-电机控制与PID/04-电机控制与PID|电机控制与PID]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "08-Sensors-Actuators"
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

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[02-MOC-主题索引|主题索引]]
- [[01-学习路线图|学习路线图]]

---

## 推荐资源

> 以下资源按相关性和学习阶段推荐，与 [[12-Resources/00-README|12-resources]] 中的完整资源列表互为补充。

### 推荐书籍

| 书籍 | 作者 | 级别 | 适用内容 | 获取方式 |
|------|------|------|----------|----------|
| 《Practical Electronics for Inventors》 | Paul Scherz & Simon Monk | 入门~进阶 | 传感器基础电路、模拟/数字接口、电机驱动、执行器控制 | 购买 |
| 《Op Amps for Everyone》 | Ron Mancini | 进阶 | 模拟传感器信号调理、数据采集系统 | TI 免费 PDF |
| 《Analog Engineer's Pocket Reference》 | TI | 速查 | 模拟传感器接口、ADC 设计、信号调理 | TI 免费 PDF |
| 《Programming Embedded Systems in C and C++》 | Michael Barr & Anthony Massa | 进阶 | 传感器/执行器固件编程、I2C/SPI/UART 驱动 | 购买 |
| 《Mastering STM32》 | Carmine Noviello | 进阶 | STM32 传感器接口、ADC/DAC、PWM、电机控制 | 免费在线 |
| 《Making Embedded Systems》 | Elecia White | 进阶 | 传感器/执行器系统设计、需求/架构/实现 | 购买 |
| 《Feedback Systems》 | Karl J. Åström & Richard M. Murray | 进阶 | PID 闭环控制、控制系统分析 | Caltech 免费 |
| 《The Art of Control Engineering》 | Dutton, Thompson, Barraclough | 进阶 | 控制理论入门、PID 调参、电机控制 | 购买 |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| GreatScott! | YouTube | 可视化解释，项目导向 | 传感器使用、电机驱动、PWM、H桥 |
| Paul McWhorter | YouTube | Arduino 最系统教程 | 传感器读取、伺服电机、步进电机、PID |
| Andreas Spiess | YouTube | 物联网、ESP32 深入 | 数字传感器接口、LoRa、WiFi 传感器 |
| Phil's Lab | YouTube | 模拟/数字电路、控制 | 运放信号调理、ADC、电机控制、PID |
| 唐老师讲电赛 | Bilibili | 电子设计竞赛（中文） | 运放应用、电源、传感器电路、电机控制 |
| 江协科技 | Bilibili | STM32 最系统中文教程（中文） | 传感器接口（I2C/SPI/ADC）、PWM、电机 |
| 速比特电子 | Bilibili | FOC 电机控制（中文） | BLDC/PMSM 驱动、FOC、Clark/Park 变换 |
| 爱上半导体 | Bilibili/YouTube | 硬件原理可视化极好（中文） | I2C、CAN、MOS管驱动、传感器原理 |
| TI Precision Labs | TI 官网 | 运放/ADC/传感器/电源（免费） | 模拟传感器信号链、ADC 选型、数据采集 |
| FastBit Embedded Brain Academy | YouTube | STM32 系统课程 | 传感器接口、定时器、PWM、电机控制 |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| AllAboutCircuits | 英文 | 最全面的免费电路教程 | 传感器电路基础、模拟/数字接口、数据采集 |
| DeepBlue Embedded | 英文 | 嵌入式教程质量极高 | STM32/ESP32 传感器驱动、ADC、PWM |
| Adafruit Learning System | 英文 | 传感器项目、库教程 | 各类传感器模块使用、执行器控制 |
| SparkFun Tutorials | 英文 | 教育友好 | 传感器基础、I2C/SPI/UART 接口入门 |
| Hackaday | 英文 | 每日硬件项目 | 传感器/执行器项目案例、电机控制 |
| EEWorld（电子工程世界） | 中文 | 国内最大 EE 社区 | 传感器应用、电机驱动、控制算法讨论 |

### 按子模块快速索引

| 子模块 | 首选资源 |
|--------|----------|
| **传感器接口** | 《Op Amps for Everyone》、TI Precision Labs、江协科技、AllAboutCircuits |
| **执行器控制** | 《Practical Electronics for Inventors》、GreatScott!、Adafruit Learning System |
| **电机驱动** | GreatScott!、Paul McWhorter、Phil's Lab、DeepBlue Embedded |
| **电机控制与PID** | 《Feedback Systems》、《The Art of Control Engineering》、速比特电子、Phil's Lab |
