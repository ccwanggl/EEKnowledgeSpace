---
tags: [rtos, real-time, multitasking, embedded]
date-created: 2026-06-15
---

# 为什么需要 RTOS

## 超级循环的局限
```c
while (1) {
    read_sensor();    // 10ms
    process_data();   // 50ms
    update_display(); // 5ms
    check_uart();     // 1ms
    delay(100ms);
}
```
- 问题 1：如果 process_data() 耗时变长，传感器读取延迟增加
- 问题 2：UART 数据可能在 delay 期间到达，丢失
- 问题 3：紧急事件（如电机过流）无法立即响应
- 问题 4：代码耦合，添加新功能困难

### RTOS 的解决方案
- **多任务**：每个功能独立任务，并行执行（伪并行）
- **优先级调度**：高优先级任务抢占低优先级，紧急事件立即响应
- **同步机制**：任务间通信不破坏封装
- **确定性**：调度延迟可预测（通常 < 1ms）

---

