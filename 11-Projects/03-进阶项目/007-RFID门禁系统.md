---
tags: [projects, intermediate, diy, control, communication]
date-created: 2026-06-15
---

# 7. RFID 门禁系统

**目标**：理解 SPI 通信、卡片认证、存储、执行器。

## 硬件
- STM32 / Arduino
- RFID 读卡器（RC522，SPI 接口）
- RFID 卡/钥匙扣（MIFARE Classic 1K）
- 继电器（控制电磁锁）
- 可选：EEPROM（存储已授权卡号）
- 可选：OLED/蜂鸣器/LED 指示状态

### 技能点
- RC522 SPI 通信和寄存器操作
- MIFARE 卡片认证（密钥 A/B）
- 读写卡片数据块
- 权限管理（添加/删除卡号）
- 继电器驱动和锁控制

### 扩展
- 加 RTC，记录刷卡时间日志
- 加 WiFi，远程开锁/查看记录
- 加指纹模块（R307），双重认证
- 加键盘密码，多种开锁方式

### 项目来源与详细资源

- **MFRC522 官方 Arduino 库（miguelbalboa/rfid）**：https://github.com/miguelbalboa/rfid — DumpInfo（读 UID）、ReadWrite（读写数据块）、MifareClassicValueBlock 等完整例程；库文档见 docs.arduino.cc/libraries/mfrc522/
- **Random Nerd Tutorials《Security Access using MFRC522》**（门禁项目的经典实现，含继电器控制电磁锁接线）：https://randomnerdtutorials.com/security-access-using-mfrc522-rfid-reader-with-arduino/
- **NXP MFRC522 数据手册**（npx.com，寄存器级 SPI 操作说明）+ **MIFARE Classic 1K 存储结构**：16 扇区 × 4 块 × 16 字节，默认密钥 FF FF FF FF FF FF
- **RC522 接线注意**：必须 3.3V 供电（5V 会烧毁）；Arduino Uno 接线 SDA→D10、SCK→D13、MOSI→D11、MISO→D12、RST→D9
- **⚠️ 安全提示**：MIFARE Classic 的 Crypto1 加密已被公开破解，UID 可克隆——本项目的门禁仅限学习，真实安防请用 DESFire 或 CPU 卡（库不支持，需换 PN532/PN7150 或国产 FM1208）
- **指纹扩展**：R307 AS608 光学指纹模块（UART，串口协议简单）
- **开源参考**：立创开源平台搜索 "门禁" 有大量完整工程（含 PCB、继电器驱动、OLED 界面）

---

