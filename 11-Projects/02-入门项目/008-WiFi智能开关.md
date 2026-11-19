---
tags: [projects, beginner, diy, hands-on]
date-created: 2026-06-15
---

# 8. WiFi 智能开关

**目标**：综合物联网入门。

## 硬件
- ESP32 或 ESP8266（如 NodeMCU）
- 继电器模块（5V，带光耦隔离）
- 轻触开关（手动控制）
- 5V/3.3V 电源

### 技能点
- ESP32 GPIO 控制继电器
- WiFi 连接（Station 模式）
- Web 服务器（HTTP 或 WebSocket）
- 手机/电脑通过浏览器控制
- 安全考虑：继电器隔离、过零检测、OTA 更新

### 扩展
- 加 MQTT，接入 Home Assistant
- 加 Matter 支持，跨平台控制
- 加功率监测（HLW8032、PZEM-004T）
- 设计 PCB，做成产品级

### 资源
- **Andreas Spiess** — 智能开关项目
- **Random Nerd Tutorials** — ESP32 Web 服务器教程（[[02-博客与网站推荐]]）

### 项目来源与详细资源

- **Random Nerd Tutorials — ESP32 继电器 Web 服务器**（最完整的入门实现：继电器原理、光耦隔离、多路控制网页 + 完整代码）：https://randomnerdtutorials.com/esp32-relay-module-ac-web-server/
- **Random Nerd Tutorials 主页**（ESP32/ESP8266/Arduino/Raspberry Pi 全系列教程，含 MicroPython 版）：https://randomnerdtutorials.com/
- **免开发固件路线**：
  - **Tasmota**（开源 ESP8266/ESP32 固件，Web UI + MQTT + Home Assistant 集成，刷机即用）：https://tasmota.github.io/docs/
  - **ESPHome**（YAML 配置生成固件，Home Assistant 官方生态）：https://esphome.io
- **功率监测扩展**：PZEM-004T（Modbus）或 HLW8032，配合 Tasmota 功率校准文档（tasmota.github.io/docs/Power-Monitoring-Calibration）
- **安全要点**：市电侧务必光耦隔离 + 继电器罩外壳；固件上传瞬间继电器误动作可用 `early_pin_init: false`（ESPHome）规避

---

