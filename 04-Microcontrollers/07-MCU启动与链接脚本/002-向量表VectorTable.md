---
tags: [mcu, startup, linker, bootloader, embedded-c]
date-created: 2026-06-15
---

# 向量表（Vector Table）

## 作用
- 定义异常和中断处理函数的入口地址
- Cortex-M 向量表位于 Flash 起始地址（0x0800_0000 典型）
- 第一个字是初始 MSP 主栈指针值，第二个字是 Reset_Handler 地址

### 常见向量
| 偏移 | 名称 | 说明 |
|------|------|------|
| 0x00 | MSP 初始值 | 主堆栈指针初始值 |
| 0x04 | Reset | 复位后首先执行 |
| 0x08 | NMI | 不可屏蔽中断 |
| 0x0C | HardFault | 严重错误 |
| 0x10 | MemManage | 内存管理错误 |
| ... | IRQ0~N | 外设中断 |

### 启动文件示例（ARM CMSIS 风格）
```asm
    AREA    RESET, DATA, READONLY
    EXPORT  __Vectors
    EXPORT  __Vectors_End
    EXPORT  __Vectors_Size

__Vectors
    DCD     __initial_sp          ; Top of Stack
    DCD     Reset_Handler           ; Reset Handler
    DCD     NMI_Handler             ; NMI Handler
    DCD     HardFault_Handler       ; HardFault Handler
    ...
__Vectors_End
```

---

