---
tags: [index, moc, overview]
date-created: 2026-06-15
date-modified: 2026-07-27
---

# EE 工程知识库

这套知识库以电子工程和嵌入式开发为基础，重点支撑控制理论与 FOC 电机控制的学习、仿真和工程实现。

## 从这里开始

- **现在学一个小任务** · [[00-Index/03-AI自学任务索引|全库 AI 自学任务]] · [[01-Foundations/09-学习方法与工具/011-用AI安排碎片时间自学|碎片时间自学方法]]。按目标和空档选一道题或一次验证。

- **按目标学习** · [[00-Index/01-学习路线图|学习路线图]]给出 FOC 主线、通用电子工程路线与阶段完成标志。
- **查一个主题** · [[00-Index/02-MOC-主题索引|主题索引]]直达各知识领域。
- **验收与复习** · [[00-Index/08-测验题索引|测验题索引]] · [[00-Index/07-闪卡复习库|闪卡复习库]]。

## 知识领域

| 领域 | 内容 |
|------|------|
| [[01-Foundations/00-README]] | 数学、物理、电路、器件、信号、ADC/DAC、嵌入式 C |
| [[02-Analog-Electronics/00-README]] | 放大器、运放、模拟滤波器 |
| [[03-Digital-Electronics/00-README]] | 数字逻辑、状态机、FPGA、Verilog |
| [[04-Microcontrollers/00-README]] | STM32、ESP32、RISC-V、中断、DMA、启动流程 |
| [[05-Communication/00-README]] | I2C、SPI、UART、CAN、USB、以太网、无线通信 |
| [[06-PCB-Design/00-README]] | 原理图、层叠、阻抗、信号完整性、EMC、制造 |
| [[07-Power-Management/00-README]] | DC-DC、电源架构、电池管理、低功耗 |
| [[08-Sensors-Actuators/00-README]] | 传感器接口、电机驱动、基础控制 |
| [[09-Debugging-Tools/00-README]] | 示波器、逻辑分析仪、日志、JTAG、SWD |
| [[10-RTOS与系统/00-README]] | FreeRTOS、Zephyr、RT-Thread、嵌入式 Linux |
| [[11-Machine-Vision/000-README]] | 图像处理、标定、嵌入式视觉（建设中） |
| [[11-Projects/00-README]] | 从入门项目到系统级项目 |
| [[12-Resources/00-README]] | 课程、书籍、网站、标准与认证 |
| [[13-Appendix/00-README]] | 术语、工具、元器件选型和知识库维护 |
| [[14-FOC-电机控制/00-README]] | 电机模型、坐标变换、SVPWM、观测器、辨识与实现 |
| [[15-双控（控制理论与控制工程）/00-README]] | 经典控制、现代控制、数字控制、辨识、MPC 与实现 |
| [[16-Linux设备驱动开发/00-README]] | Linux 设备模型、设备树、中断、GPIO/pinctrl、外设驱动、调试与工程实战 |

## 测验题索引

### 基础理论

- [[01-Foundations/10-电路分析测验题|电路分析]]
- [[01-Foundations/11-电子元器件测验题|电子元器件]]
- [[01-Foundations/12-信号与系统测验题|信号与系统]]
- [[01-Foundations/13-嵌入式C编程测验题|嵌入式 C]]

### 模拟与数字

- [[02-Analog-Electronics/04-模拟电路基础测验题|模拟电路基础]]
- [[02-Analog-Electronics/05-运算放大器测验题|运算放大器]]
- [[03-Digital-Electronics/06-数字逻辑测验题|数字逻辑]]
- [[03-Digital-Electronics/07-组合逻辑电路测验题|组合逻辑电路]]

### MCU、通信和 RTOS

- [[04-Microcontrollers/08-STM32测验题|STM32]]
- [[05-Communication/08-I2C-SPI-UART测验题|I2C、SPI 与 UART]]
- [[05-Communication/09-CAN总线测验题|CAN 总线]]
- [[10-RTOS与系统/06-RTOS基础测验题|RTOS 基础]]
- [[10-RTOS与系统/07-FreeRTOS测验题|FreeRTOS]]

### PCB、电源、传感器和调试

- [[06-PCB-Design/07-PCB设计基础测验题|PCB 设计基础]]
- [[06-PCB-Design/08-PCB层叠与阻抗设计测验题|PCB 层叠与阻抗]]
- [[07-Power-Management/06-电源管理基础测验题|电源管理基础]]
- [[07-Power-Management/07-DC-DC测验题|DC-DC]]
- [[08-Sensors-Actuators/05-传感器接口测验题|传感器接口]]
- [[09-Debugging-Tools/06-调试工具综合测验题|调试工具]]

> 控制理论和 FOC 的自测题分布在各主题笔记末尾，尚未形成独立题库。

## 闪卡复习

闪卡用于记忆定义、公式条件、单位、故障现象与排查顺序，不适合代替推导和项目实践。建议范围：

- 电路定律、常用等效模型和单位换算
- 傅里叶、拉普拉斯、Z 变换的适用条件
- 一阶、二阶系统指标及公式边界
- ADC、PWM、定时器和通信协议的关键约束
- FOC 坐标变换符号、采样时序、保护条件和调试顺序

含 `#flashcard` 标签的笔记通过 Dataview 自动汇总。闪卡答案应包含必要条件——比如记录调节时间公式时，需同时写明误差带、系统阶次、阻尼范围和近似条件。

## 知识图谱

### 知识体系总览

```mermaid
graph TD
    A[数学与物理基础] --> B[电路基础]
    B --> C[模拟电子]
    B --> D[数字电子]
    C --> E[电源管理]
    D --> F[FPGA]
    D --> G[微控制器]
    G --> H[通信协议]
    G --> I[传感器与执行器]
    H --> J[RTOS与系统]
    I --> J
    J --> N[Linux设备驱动]
    C --> K[PCB设计]
    D --> K
    E --> K
    H --> K
    G --> L[调试工具]
    H --> L
    K --> M[项目实践]
    J --> M
    N --> M
    L --> M
    I --> M
```

### 电子工程全景

```mermaid
graph TB
    subgraph Theory["理论基础"]
        T1["电路定律<br/>欧姆定律 KCL/KVL"]
        T2["半导体物理<br/>PN结 载流子"]
    end
    subgraph Components["元器件层"]
        Passive["无源器件<br/>R / C / L / 晶振"]
        Active["有源器件<br/>二极管 / BJT / MOSFET"]
    end
    subgraph Circuits["电路层"]
        PassiveC["无源电路<br/>分压 / RC滤波"]
        ActiveC["有源电路<br/>放大 / 振荡 / 驱动"]
    end
    subgraph IC["集成电路"]
        AIC["模拟IC<br/>运放 / ADC-DAC"]
        DIC["数字IC<br/>逻辑 / MCU / 接口"]
    end
    subgraph IO["输入/输出"]
        IN["输入<br/>传感器 / 麦克风"]
        OUT["输出<br/>电机 / 显示 / 天线"]
    end
    subgraph Power["电源系统"]
        BAT["电池 / 储能"]
        DC["DC稳压"]
        AC["AC变换"]
    end
    subgraph System["系统应用"]
        SYS["机器人 / 物联网 / 各类电子设备"]
    end
    Theory --> Components
    Passive --> PassiveC
    Active --> ActiveC
    PassiveC --> ActiveC
    ActiveC --> IC
    Power --> IC
    IC --> System
    IN --> System
    OUT --> System
    Power --> System
```

### 主题依赖关系

| 主题 | 前置依赖 | 支撑后续 |
|------|----------|----------|
| 数学物理 | 无 | 电路分析、信号与系统 |
| 电路分析 | 数学物理 | 模拟、数字、电源 |
| 信号与系统 | 数学物理、电路分析 | 滤波器、通信、控制 |
| 运算放大器 | 电路分析、信号与系统 | 滤波器、仪器放大 |
| 数字逻辑 | 电路分析 | MCU、FPGA |
| 微控制器 | 数字逻辑、C 语言 | 通信、传感器、RTOS |
| 通信协议 | 微控制器、信号与系统 | 物联网、网络系统 |
| 电源管理 | 电路分析、模拟电子 | PCB、系统供电 |
| 传感器与执行器 | 微控制器、模拟电子 | 机器人、自动化 |
| PCB 设计 | 模拟、数字、电源 | 项目落地 |
| 调试工具 | 各阶段并行 | 问题诊断、故障排查 |
| RTOS | 微控制器、通信 | 复杂系统、项目 |
| 项目实践 | 各主题综合 | 专家深化 |

### 学习闭环

```mermaid
graph LR
    A[理论学习] --> B[仿真验证]
    B --> C[实验测试]
    C --> D[项目应用]
    D --> E[问题反馈]
    E --> A
```

### 信号链：从物理到数字

```mermaid
graph LR
    Physical["物理量<br/>温度/压力/光/声音"]
    --> Sensor["传感器"]
    --> Conditioning["信号调理<br/>放大/滤波/电平移位"]
    --> ADC["ADC 采样量化"]
    --> DSP["数字处理<br/>MCU/DSP/FPGA"]
    --> DAC["DAC"]
    --> Actuator["执行器/输出"]
```

## 使用说明

- 第一次学习一个主题时，从领域 README 或模块总览进入，不依赖文件名猜测顺序。
- 公式和代码旁的条件、假设与单位属于正文的一部分，复用前需要一起检查。
- 外部资源可能变化，优先使用官方文档、教材和原始论文。
- 学习状态记录在具体主题或项目中，完成一节后做对应测验并记录仍无法解释的问题。
- 发现断链或渲染问题时，运行[[13-Appendix/04-知识库维护/00-README|知识库维护检查]]。
