---
tags: [mcu, startup, linker, bootloader, embedded-c]
date-created: 2026-06-15
---

# Bootloader 与 OTA

## Bootloader 作用
- 初始化最小硬件环境
- 检查是否需要升级固件
- 跳转到应用固件执行
- 常见功能：USB/串口/IAP 升级、双 Bank 切换、安全启动

### OTA（Over-The-Air）升级
- 通过无线方式更新固件
- 流程：下载新固件 → 校验完整性 → 写入备用 Bank → 标记升级标志 → 复位 → Bootloader 切换到新固件
- 必须考虑断电安全、回滚机制、完整性校验

### 启动地址配置
- Cortex-M 可通过 `VTOR` 寄存器重定向向量表
- 某些 MCU 通过 Option Byte / Fuse 选择启动 Bank

---

