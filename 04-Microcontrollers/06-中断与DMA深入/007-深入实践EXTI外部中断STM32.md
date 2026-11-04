---
tags: [mcu, interrupt, dma, stm32, embedded]
date-created: 2026-06-15
---

# 深入实践：EXTI 外部中断（STM32）

> 以下内容为从江协科技 STM32 教程整理的标准库和 HAL 库 EXTI 完整配置流程，可直接用于工程实践。

## 中断与 NVIC 结构回顾

STM32F10x 芯片有 **84 个中断通道**，包括 16 个内核中断和 68 个可屏蔽中断。中断由 **NVIC（嵌套向量中断控制器）** 统一管理，本质是一个开关与选择器，控制芯片的中断相关功能。

每个中断通道拥有 **16 个可编程的优先等级**，可对优先级进行分组，进一步设置**抢占优先级**和**响应优先级**。

| 优先级类型 | 作用 | 规则 |
|----------|------|------|
| **抢占优先级** | 中断嵌套 | 高优先级可打断低优先级中断 |
| **响应优先级** | 排队顺序 | 仅在相同抢占优先级内比较 |

> **注意**：内核外设（NVIC、SysTick）由 ARM 公司设计，片上外设（GPIO、TIM 等）由 ST 公司设计，因此有内核中断和可屏蔽中断的区别。

### EXTI 外部中断结构

EXTI（External Interrupt/Event Controller）可以检测指定 GPIO 口的电平信号，当产生电平变化时，向 NVIC 发出中断申请。

**STM32F10x 支持的外部中断源**：
- EXTI0 ~ EXTI4：独立中断通道
- EXTI9_5：共用一个中断通道
- EXTI15_10：共用一个中断通道
- 额外：PVD 输出、RTC 闹钟、USB 唤醒、以太网唤醒

**触发方式**：上升沿、下降沿、双边沿、软件触发

**响应类型**：中断响应（打断 CPU）或事件响应（给其他外设发脉冲，不触发中断）

### AFIO 复用功能引脚

AFIO（Alternate Function I/O）的作用是**数据选择器**：
- 复用引脚功能重映射
- 中断引脚选择（将 GPIO 映射到 EXTI 线）

### 标准库 EXTI 配置完整代码

```c
// exti.h
#ifndef EXTI_H_
#define EXTI_H_

#include "stm32f10x.h"

#define KEY_UP_GPIO_Port  GPIOA
#define KEY_UP_Pin        GPIO_Pin_0
#define KEY_UP_RCC        RCC_APB2Periph_GPIOA

#define KEY_GPIO_Port     GPIOE
#define KEY1_Pin          GPIO_Pin_3
#define KEY0_Pin          GPIO_Pin_4
#define KEY_RCC           RCC_APB2Periph_GPIOE

void KEY_Init(void);
void My_EXTI_Init(void);

#endif
```

```c
// exti.c
#include "exti.h"

void KEY_Init()
{
    GPIO_InitTypeDef GPIO_InitStruct;
    RCC_APB2PeriphClockCmd(KEY_UP_RCC | KEY_RCC, ENABLE);

    // KEY_UP (PA0) 接电源，配置为下拉输入
    GPIO_InitStruct.GPIO_Pin = KEY_UP_Pin;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IPD;
    GPIO_Init(KEY_UP_GPIO_Port, &GPIO_InitStruct);

    // KEY1/KEY0 (PE3/PE4) 接地，配置为上拉输入
    GPIO_InitStruct.GPIO_Pin = KEY1_Pin | KEY0_Pin;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(KEY_GPIO_Port, &GPIO_InitStruct);
}

void My_EXTI_Init()
{
    NVIC_InitTypeDef NVIC_InitStruct;
    EXTI_InitTypeDef EXTI_InitStruct;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);

    // 将 GPIO 引脚映射到 EXTI 线
    GPIO_EXTILineConfig(GPIO_PortSourceGPIOA, GPIO_PinSource0);  // PA0 -> EXTI0
    GPIO_EXTILineConfig(GPIO_PortSourceGPIOE, GPIO_PinSource3);  // PE3 -> EXTI3
    GPIO_EXTILineConfig(GPIO_PortSourceGPIOE, GPIO_PinSource4);  // PE4 -> EXTI4

    // NVIC 配置：EXTI0
    NVIC_InitStruct.NVIC_IRQChannel = EXTI0_IRQn;
    NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority = 2;
    NVIC_InitStruct.NVIC_IRQChannelSubPriority = 3;
    NVIC_InitStruct.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStruct);

    // NVIC 配置：EXTI3
    NVIC_InitStruct.NVIC_IRQChannel = EXTI3_IRQn;
    NVIC_InitStruct.NVIC_IRQChannelSubPriority = 1;
    NVIC_Init(&NVIC_InitStruct);

    // NVIC 配置：EXTI4
    NVIC_InitStruct.NVIC_IRQChannel = EXTI4_IRQn;
    NVIC_InitStruct.NVIC_IRQChannelSubPriority = 0;
    NVIC_Init(&NVIC_InitStruct);

    // EXTI 配置：EXTI0 上升沿触发
    EXTI_InitStruct.EXTI_Line = EXTI_Line0;
    EXTI_InitStruct.EXTI_Mode = EXTI_Mode_Interrupt;
    EXTI_InitStruct.EXTI_Trigger = EXTI_Trigger_Rising;
    EXTI_InitStruct.EXTI_LineCmd = ENABLE;
    EXTI_Init(&EXTI_InitStruct);

    // EXTI 配置：EXTI3/EXTI4 下降沿触发
    EXTI_InitStruct.EXTI_Line = EXTI_Line3 | EXTI_Line4;
    EXTI_InitStruct.EXTI_Trigger = EXTI_Trigger_Falling;
    EXTI_Init(&EXTI_InitStruct);
}

// 中断服务函数
void EXTI0_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line0) == SET)
    {
        if (GPIO_ReadInputDataBit(KEY_UP_GPIO_Port, KEY_UP_Pin) == 1)
        {
            GPIO_ResetBits(LED0_GPIO_Port, LED0_Pin);
            GPIO_ResetBits(LED1_GPIO_Port, LED1_Pin);
        }
        EXTI_ClearITPendingBit(EXTI_Line0);
    }
}

void EXTI3_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line3) == SET)
    {
        if (GPIO_ReadInputDataBit(KEY_GPIO_Port, KEY1_Pin) == 0)
        {
            GPIO_SetBits(LED0_GPIO_Port, LED0_Pin);
        }
        EXTI_ClearITPendingBit(EXTI_Line3);
    }
}

void EXTI4_IRQHandler(void)
{
    if (EXTI_GetITStatus(EXTI_Line4) == SET)
    {
        if (GPIO_ReadInputDataBit(KEY_GPIO_Port, KEY0_Pin) == 0)
        {
            GPIO_SetBits(LED1_GPIO_Port, LED1_Pin);
        }
        EXTI_ClearITPendingBit(EXTI_Line4);
    }
}
```

```c
// main.c
#include "exti.h"

int main()
{
    SysTick_Init(72);
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    LED_Init();
    KEY_Init();
    My_EXTI_Init();
    while (1)
    {
        // 主循环空闲，所有工作由中断处理
    }
}
```

### HAL 库 EXTI 配置（CubeMX）

```c
// 在 CubeMX 中配置 GPIO 为 EXTI 模式，生成代码后

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_0)  // 按键按下
    {
        HAL_GPIO_TogglePin(LED0_GPIO_Port, LED0_Pin);
    }
    __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_0);  // 清除中断标志
}
```

### 外部中断应用场景

| 场景 | 检测方式 | 实现要点 |
|------|----------|----------|
| **旋转编码器** | 正交波形（A/B相） | 检测相位差判断正反转，计数脉冲 |
| **对射式红外传感器** | 方波信号 | 计数方波个数或测量频率 |
| **霍尔传感器** | 磁信号变化 | 检测磁场有无，用于无刷电机换相 |

### 标准库 EXTI 配置步骤总结

1. 使能 IO 口时钟（RCC），配置 IO 口模式为输入
2. 开启 AFIO 时钟，设置 IO 口与中断线的映射关系
3. 初始化 EXTI（选择中断输入源和触发方式）
4. 配置 NVIC 中断分组和优先级
5. 编写 EXTI 中断服务函数（必须清空中断标志位）

---

