---
tags: [mcu, startup, linker, bootloader, embedded-c]
date-created: 2026-06-15
---

# 链接脚本（Linker Script）

## 作用
- 告诉链接器如何安排代码和数据在存储器中的位置
- 定义 Flash、RAM 的起始地址和大小
- 定义 `.text`、`.rodata`、`.data`、`.bss` 等段的加载地址和运行地址

### 典型段
| 段 | 内容 | 存储位置 |
|------|------|----------|
| `.text` | 代码、常量 | Flash（运行也在 Flash） |
| `.rodata` | 只读数据（字符串、const） | Flash |
| `.data` | 已初始化的全局/静态变量 | RAM（初始化值从 Flash 复制） |
| `.bss` | 未初始化的全局/静态变量 | RAM（启动时清零） |
| `.stack` | 栈 | RAM 顶部向下增长 |
| `.heap` | 堆 | RAM 中，向上增长 |

### 链接脚本示例（GNU ld）
```ld
MEMORY
{
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
  RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 128K
}

SECTIONS
{
  .text :
  {
    KEEP(*(.vectors))
    *(.text*)
    *(.rodata*)
  } > FLASH

  __data_load = LOADADDR(.data);
  .data :
  {
    __data_start = .;
    *(.data*)
    __data_end = .;
  } > RAM AT > FLASH

  .bss :
  {
    __bss_start = .;
    *(.bss*)
    *(COMMON)
    __bss_end = .;
  } > RAM
}
```

---

