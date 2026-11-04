---
tags: [freertos, rtos, embedded, multitasking]
date-created: 2026-06-15
---

# 配置与裁剪（FreeRTOSConfig.h）

```c
#define configUSE_PREEMPTION            1   // 抢占式调度
#define configUSE_IDLE_HOOK             0   // 空闲钩子
#define configUSE_TICK_HOOK             0   // Tick 钩子
#define configCPU_CLOCK_HZ              80000000  // CPU 频率
#define configTICK_RATE_HZ              1000      // 1kHz Tick
#define configMAX_PRIORITIES            5         // 优先级数
#define configMINIMAL_STACK_SIZE        128       // 最小栈（words）
#define configTOTAL_HEAP_SIZE           10240     // 堆大小（bytes）
#define configUSE_MUTEXES               1
#define configUSE_COUNTING_SEMAPHORES   1
#define configUSE_QUEUE_SETS            0
#define configUSE_TASK_NOTIFICATIONS    1
#define configUSE_TRACE_FACILITY        1   // 用于 Trace
```

---

