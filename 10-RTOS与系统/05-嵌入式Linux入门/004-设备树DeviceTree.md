---
tags: [embedded-linux, yocto, buildroot, device-tree, embedded]
date-created: 2026-06-15
---

# 设备树（Device Tree）

- 用 `.dts` 文件描述硬件，编译为 `.dtb`（二进制设备树 blob）
- 内核启动时读取 dtb，知道有哪些硬件、内存、中断
- 与内核分离：同一内核 + 不同 dtb 可支持不同板子
- 关键节点：memory、cpus、soc、chosen、aliases
- 覆盖（Overlay）：动态修改设备树，如启用树莓派 HAT

## RK3588 设备树要点
- **DDR 配置**：不同容量（4GB/8GB/16GB）对应不同 dts
- **PCIe 控制器**：可用于 NVMe SSD 或扩展卡
- **NPU 节点**：`rknpu` 节点配置 NPU 时钟和内存
- **显示接口**：HDMI、MIPI DSI、 eDP 可选配置
- **摄像头接口**：MIPI CSI 配置用于连接相机模组
- 常用文件：`rk3588s.dtsi`（核心定义）、`rk3588-orangepi-5.dts`（板级配置）

---

