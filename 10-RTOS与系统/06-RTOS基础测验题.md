---
tags: [quiz, rtos, embedded, freertos, practice]
date-created: 2026-06-17
---

# RTOS 基础测验题

> 覆盖 RTOS 核心概念：任务、调度、同步、中断、内存管理。建议先完成 [[01-RTOS基础]] 后再做。

---

## 一、选择题

### 1. 调度算法
FreeRTOS 默认采用哪种任务调度算法？
- A. 时间片轮转
- B. 优先级抢占式调度
- C. 最早截止时间优先
- D. 协作式调度

<details>
<summary>答案</summary>
B. 优先级抢占式调度。高优先级任务就绪时立即抢占 CPU，同优先级任务按时间片轮转（可选）。
</details>

### 2. 上下文切换
任务上下文切换通常发生在？
- A. 任意指令执行期间
- B. 系统 tick 中断或任务主动让出时
- C. 仅在 main 函数返回时
- D. 仅在硬 fault 时

<details>
<summary>答案</summary>
B. 系统 tick 中断或任务主动让出时。调度器在 tick 中断中检查任务就绪状态，决定是否切换。
</details>

### 3. 信号量与互斥量
保护共享资源时，应优先使用？
- A. 二值信号量
- B. 互斥量（Mutex）
- C. 计数信号量
- D. 事件组

<details>
<summary>答案</summary>
B. 互斥量（Mutex）。Mutex 支持优先级继承，可防止优先级反转问题。
</details>

### 4. 栈溢出检测
RTOS 任务栈溢出最可靠的检测方式是？
- A. 增大栈空间
- B. 使用栈溢出钩子函数（Stack Overflow Hook）和 MPU/Guard 区
- C. 减少局部变量
- D. 关闭中断

<details>
<summary>答案</summary>
B. 使用栈溢出钩子函数和 MPU/Guard 区。FreeRTOS 提供 `vApplicationStackOverflowHook`，MPU 可设置栈边界保护。
</details>

### 5. 中断安全
在中断服务函数（ISR）中调用 FreeRTOS API 时，应使用？
- A. 普通 API
- B. 以 FromISR 结尾的 API
- C. 任何 API 都可以
- D. 不能调用任何 RTOS API

<details>
<summary>答案</summary>
B. 以 FromISR 结尾的 API。如 `xSemaphoreGiveFromISR`、`xQueueSendFromISR`，避免在中断中执行调度导致问题。
</details>

---

## 二、填空题

### 6. 任务状态
FreeRTOS 任务基本状态包括：运行（Running）、就绪（Ready）、阻塞（Blocked）、**_____**。

<details>
<summary>答案</summary>
挂起（Suspended）。挂起状态任务必须由 `vTaskResume` 显式恢复。
</details>

### 7. 临界区
进入临界区常用的方法是调用 **_____** 关闭中断，退出时恢复。

<details>
<summary>答案</summary>
taskENTER_CRITICAL() / taskEXIT_CRITICAL()。也可使用 `vTaskSuspendAll()` 挂起调度器。
</details>

### 8. 优先级反转
低优先级任务持有互斥量时，中等优先级任务抢占 CPU，导致高优先级任务阻塞的现象称为 **_____**。

<details>
<summary>答案</summary>
优先级反转（Priority Inversion）。互斥量的优先级继承机制可缓解该问题。
</details>

---

## 三、判断题

### 9. 任务数量
RTOS 中任务越多越好，可以提高 CPU 利用率。

<details>
<summary>答案</summary>
错误。任务过多会增加上下文切换开销、栈内存占用和调度复杂度。应按功能合理划分任务。
</details>

### 10. 中断优先级
在 Cortex-M 中，使用 FreeRTOS 时，configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY 以上的中断不能调用 FreeOS API。

<details>
<summary>答案</summary>
正确。高于 configMAX_SYSCALL_INTERRUPT_PRIORITY 的中断不会被 RTOS 临界区屏蔽，调用 FromISR API 会破坏内核一致性。
</details>

---

## 四、设计题

### 11. 任务划分设计
为一个智能家居传感器节点设计 RTOS 任务，功能包括：按键检测、传感器采样、LoRa 发送、LED 指示、低功耗管理。

<details>
<summary>答案与解析</summary>

| 任务 | 优先级 | 周期/触发 | 说明 |
|------|--------|-----------|------|
| 按键检测 | 中 | 10 ms | 去抖动后发送通知 |
| 传感器采样 | 高 | 100 ms | I2C/SPI 读取，放入队列 |
| LoRa 发送 | 中 | 事件触发 | 从队列取数据发送 |
| LED 指示 | 低 | 事件触发 | 状态更新，非关键 |
| 低功耗管理 | 低 | 1 s | 检查空闲条件进入 sleep |

同步机制：
- 按键 → LoRa：二值信号量或消息队列。
- 传感器数据 → LoRa：消息队列缓存。
- LED 状态：事件组或全局标志位加互斥量保护。

注意：
- 采样任务优先级较高，确保数据不丢失。
- LoRa 发送耗时较长，优先级不宜最高，避免阻塞其他任务。
- 进入低功耗前确保外设已关闭或进入空闲状态。
</details>

### 12. 优先级反转案例分析
三个任务 A（优先级低）、B（优先级中）、C（优先级高）共享一个 Mutex：
- A 获得 Mutex 后被 B 抢占
- C 请求 Mutex 阻塞
- 系统出现长时间阻塞

分析原因并给出解决方案。

<details>
<summary>答案与解析</summary>

**原因**：
- A 持有 Mutex，B 抢占 A 运行，C 因等待 Mutex 阻塞。
- 由于 B 持续运行，A 无法释放 Mutex，C 长时间等待。

**解决方案**：
1. **优先级继承**：使用 Mutex 而非二值信号量，FreeRTOS 会自动将 A 优先级临时提升到 C 的级别，直到释放 Mutex。
2. **降低临界区粒度**：减少持锁时间，降低被抢占概率。
3. **避免在临界区内阻塞**：持锁期间不要调用可能阻塞的 API。
4. **资源分层**：高优先级任务优先获取资源，低优先级任务延后访问。
</details>

---

## 自评标准

| 正确率 | 水平 |
|--------|------|
| 90-100% | 已掌握，可进入 [[02-FreeRTOS]] 项目实践 |
| 70-89% | 基本掌握，重点复习任务同步与中断安全 |
| <70% | 需要重新学习 [[01-RTOS基础]] |

---

## 相关主题
- [[01-RTOS基础]] — 测验覆盖的理论基础
- [[02-FreeRTOS]] — 常用 RTOS 实践
- [[06-中断与DMA深入]] — 中断与任务协同
- [[05-嵌入式Linux入门]] — 更复杂的操作系统
