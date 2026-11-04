---
tags: [debugging, uart, logging, printf, rtt, embedded]
date-created: 2026-06-15
---

# UART printf 重定向

## 原理
- 重写 C 库的 `_write` 或 `fputc` 函数
- 将标准输出重定向到 UART 外设
- 通过 USB 转串口模块在 PC 端查看

### STM32 HAL 示例
```c
#include "stdio.h"
#include "usart.h"

int _write(int file, char *ptr, int len)
{
    HAL_UART_Transmit(&huart1, (uint8_t*)ptr, len, HAL_MAX_DELAY);
    return len;
}

// 使用
printf("ADC value: %d\r\n", adc_val);
```

### 裸机示例
```c
void uart_putc(char c) {
    while (!(USART1->SR & USART_SR_TXE));
    USART1->DR = c;
}

int _write(int file, char *ptr, int len) {
    for (int i = 0; i < len; i++) uart_putc(ptr[i]);
    return len;
}
```

### 注意事项
- `printf` 比较耗时，避免在中断中调用
- 大容量输出可能阻塞程序，可用 DMA 方式
- 浮点数打印会显著增加代码体积

---

