---
tags: [projects, expert, advanced, diy, portfolio]
date-created: 2026-06-15
---

# 5. Matter/Thread 边界路由器

## 目标
构建一个支持 Matter 和 Thread 协议的智能家居边界路由器。

### 硬件
- 主控：Raspberry Pi / ESP32-C6 / nRF52840 + Linux 主机
- Thread RCP：nRF52840 / EFR32
- 网络：Ethernet / WiFi

### 技能点
- Thread 协议栈（OpenThread）
- Matter 协议
- 边界路由器架构
- 网络安全与证书
- Linux 网络配置

### 扩展方向
- 多生态兼容（HomeKit、Google Home、Alexa）
- 自定义 Matter 设备
- OTA 升级

### 项目来源与详细资源

**核心来源**
- OpenThread Border Router（OTBR）官方仓库：<https://github.com/openthread/ot-br-posix> — Google 发布的 Thread 边界路由器开源实现（POSIX 平台），功能：Thread ↔ Wi-Fi/以太网双向 IP 路由、mDNS/SRP 服务发现、DHCPv6 前缀委派、NAT64、外部 Commissioning；官方 CodeLab 在 openthread.io（中国可访问 openthread.google.cn）
- Raspberry Pi 搭建教程（project-chip/connectedhomeip 官方文档）：<https://github.com/project-chip/connectedhomeip/blob/master/docs/platforms/openthread/openthread_border_router_pi.md> — 用 nRF52840 DK/Dongle 作 RCP 的标准流程
- OpenThread 协议栈仓库：<https://github.com/openthread/openthread> — Thread 1.3 开源实现，含 CLI（ot-ctl）
- Matter（Project CHIP）官方仓库：<https://github.com/project-chip/connectedhomeip> — 应用层协议开源实现；Home Assistant 的 OTBR 集成文档在 home-assistant.io/integrations/otbr/（REST API 默认 8081 端口）

**关键实现要点**
- 架构：RCP（802.15.4 射频协处理器，跑 Spinel 协议）← USB/串口 → Linux 主机（ot-br-posix）→ mDNS 服务发现
- RCP 固件：nRF52840 / EFR32 / CC2652 烧 OpenThread RCP 固件（注意 RCP 与 NCP 模式区别，现代 OTBR 用 RCP）
- 调试工具：ot-ctl（Thread 网络状态）、chip-tool（Matter 设备调试/控制）、OTBR Web GUI（默认 80/8080 端口）

---

