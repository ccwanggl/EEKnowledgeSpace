---
tags: [quiz, freertos, rtos, embedded, foundation]
date-created: 2026-06-17
---

# FreeRTOS 测验题

> 测试对 FreeRTOS 核心概念的掌握程度。建议完成 [[02-FreeRTOS]] 和 [[01-RTOS基础]] 学习后自测。

---

## 一、选择题

### 第 1 题
FreeRTOS 中，任务从 Running 状态进入 Blocked 状态通常是因为？

A. 被更高优先级任务抢占  
B. 调用 vTaskDelay() 或等待事件  
C. 调用 vTaskSuspend()  
D. 任务结束

<details>
<summary>答案与解析</summary>

**答案：B**

解析：Blocked 状态表示任务在等待某个事件或延时到期；被抢占会回到 Ready；Suspend 会进入 Suspended。
</details>

### 第 2 题
以下哪种同步机制最适合保护共享资源，防止优先级翻转？

A. 二值信号量  
B. 互斥量（Mutex）  
C. 计数信号量  
D. 事件组

<details>
<summary>答案与解析</summary>

**答案：B**

解析：Mutex 支持优先级继承，可减少优先级翻转问题，适合保护共享资源。
</details>

### 第 3 题
在 FreeRTOS 中，configMAX_PRIORITIES 定义了？

A. 系统最大任务数  
B. 可用的优先级数量  
C. 堆内存大小  
D. 时间片长度

<details>
<summary>答案与解析</summary>

**答案：B**

解析：configMAX_PRIORITIES 定义任务优先级的最大数量，数值越大调度开销可能越大。
</details>

---

## 二、填空题

### 第 4 题
FreeRTOS 中用于任务间传递数据的主要机制是 ______，用于任务同步的主要机制是 ______。

<details>
<summary>答案与解析</summary>

**答案：队列（Queue）；信号量/事件组/任务通知**

解析：Queue 可传递数据；Semaphore/Event Group/Task Notification 用于同步。
</details>

### 第 5 题
在 FreeRTOS 中，______ 是一种轻量级的同步方式，可用于替代信号量。

<details>
<summary>答案与解析</summary>

**答案：任务通知（Task Notification）**

解析：任务通知比信号量更高效，资源占用更少，每个任务有 32 位通知值。
</details>

---

## 三、简答题

### 第 6 题
简述 FreeRTOS 中二值信号量和互斥量的主要区别。

<details>
<summary>答案与解析</summary>

**答案要点：**
- 二值信号量：用于任务/中断同步，没有所有权概念，不支持优先级继承；
- 互斥量：用于资源保护，有所有权，支持优先级继承，同任务获取和释放必须配对。
</details>

### 第 7 题
一个高优先级任务 H、中优先级任务 M、低优先级任务 L。L 持有一个 Mutex，H 也想获取该 Mutex。请解释什么是优先级翻转，以及 FreeRTOS 如何缓解。

<details>
<summary>答案与解析</summary>

**答案要点：**
- 优先级翻转：H 被 L 阻塞，M 反而先于 H 运行，导致高优先级任务响应延迟。
- 缓解：FreeRTOS Mutex 支持优先级继承。当 H 等待 L 持有的 Mutex 时，L 的优先级临时提升到 H 的级别，直到释放 Mutex，从而减少 M 造成的阻塞。
</details>

---

## 四、自评

| 得分 | 水平 |
|------|------|
| 90-100 | 优秀，FreeRTOS 概念清晰 |
| 70-89 | 良好，建议动手写多任务程序 |
| 50-69 | 合格，需重读 [[02-FreeRTOS]] 和 [[01-RTOS基础]] |
| <50 | 需要系统学习 RTOS |

---

## 相关主题
- [[02-FreeRTOS]]
- [[01-RTOS基础]]
- [[04-Microcontrollers/02-STM32系列/000-STM32系列|STM32 系列]]
- [[01-Foundations/08-嵌入式C编程/000-嵌入式C编程|08-嵌入式C编程]]
