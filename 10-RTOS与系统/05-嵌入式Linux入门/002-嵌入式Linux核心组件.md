---
tags: [embedded-linux, yocto, buildroot, device-tree, embedded]
date-created: 2026-06-15
---

# 嵌入式 Linux 核心组件

## 启动流程（Boot Flow）
```
ROM Bootloader（固化）→ SPL/FSBL（极小二级引导）→ U-Boot（主引导）→ Linux Kernel → Rootfs → Init System（systemd/busybox）→ Applications
```

### 内核（Kernel）
- **Linux 内核**：裁剪版，去掉不需要的驱动和子系统
- **Rockchip 内核**：RK3588 使用瑞芯微维护的 Linux 内核分支，包含 Mali GPU、NPU、VPU 驱动
- **配置**：`make menuconfig`，启用特定硬件支持
- **设备树（Device Tree）**：描述硬件，替代硬编码。RK3588 使用 `.dts` 描述 DDR、PCIe、HDMI、MIPI 等
- **驱动**：字符设备、块设备、网络设备、平台设备、NPU 驱动（rknpu）
- **模块（Module）**：可动态加载的驱动，减少内核体积

### 文件系统（Rootfs）
- **BusyBox**：极简 Unix 工具集，单二进制替代 300+ 工具
- **Yocto / Buildroot**：构建完整根文件系统的工具。RK3588 有官方 Buildroot 支持
- **systemd**：现代 init 系统，服务管理、日志、网络、定时器
- **OpenRC / runit**：轻量 init 替代方案
- **Ubuntu Rockchip**：官方 Ubuntu 22.04/24.04 LTS 移植，推荐用于 RK3588

### 构建系统

| 工具 | 特点 | 适用 | RK3588 支持 |
|------|------|------|-------------|
| **Buildroot** | 简单、快速、易理解 | 快速原型、小系统 | ✅ 官方 Buildroot 支持 |
| **Yocto** | 极其灵活、复杂、工业标准 | 产品化、定制发行版 | ✅ 社区支持 |
| **OpenWrt** | 路由器专用，网络功能完善 | 路由器、网关、AP | ✅ 可移植 |
| **Ubuntu Rockchip** | 现成发行版，快速部署 | 通用设备、开发板 | ✅ 官方 22.04/24.04 |
| **Armbian** | ARM 板优化发行版 | 树莓派替代板、开发板 | ✅ 官方 RK3588 支持 |
| **NixOS** | 声明式配置、可复现 | 服务器、开发 | ✅ 社区支持（香橙派/ROCK 5A）|

---

