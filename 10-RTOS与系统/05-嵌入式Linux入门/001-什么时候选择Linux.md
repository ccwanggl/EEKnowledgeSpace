---
tags: [embedded-linux, yocto, buildroot, device-tree, embedded]
date-created: 2026-06-15
---

# 什么时候选择 Linux

## 选择 Linux 的信号
- 需要完整 TCP/IP 协议栈、WiFi/蓝牙管理、USB 设备/host 支持
- 需要图形界面（Qt、GTK、Web）
- 需要运行复杂应用（Python、Node.js、数据库、Web 服务器）
- 需要多用户、安全、文件系统层次
- 需要容器（Docker）、虚拟化
- 需要 AI 推理（NPU、GPU 加速）
- 处理器性能：ARM Cortex-A 系列、x86、RISC-V 64 位
- 典型场景：RK3588 边缘 AI 盒子、NVR、工业平板、机器人主控、ARM 服务器

### 不选择 Linux 的场景
- 资源极度受限（<1MB Flash、<256KB RAM）
- 硬实时需求（确定性 < 1ms 响应）
- 超低功耗、电池供电常开设备
- 简单控制任务（用 RTOS 或裸机更合适）

---

