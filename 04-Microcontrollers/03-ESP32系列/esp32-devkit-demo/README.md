---
tags: [esp32, devkitc, wroom-32, webserver, iot, experiment]
date-created: 2026-11-17
---

# 实验笔记：ESP32 Web 控制台（通用 ESP32 DevKit，CP2102/CH340/CH9102 版）

## 实验目标

让 ESP32（ESP32-WROOM-32 模组）连接路由器后充当 Web 服务器，实现：

- 浏览器网页实时开关板载 LED（交互式，双向）
- 每 2 秒轮询 ADC 电压 / WiFi 信号 / 片上温度
- mDNS 免记 IP（`http://esp32-devkit.local`）

**成品文件**：[[ESP32_WebServer.ino]]（固件）。

## 实验环境

| 项 | 值 |
|---|---|
| 硬件 | 通用 ESP32 DevKit（Taobao，ESP32-WROOM-32 模组，双核 240MHz，WiFi + BLE 4.2，4MB Flash） |
| 板型变体 | USB 桥 CP2102 / CH340 / CH9102 × MICRO / TYPE-C × 30Pin / 38Pin —— 程序通用，只是驱动和引脚排针数量不同 |
| Arduino 板型 | **ESP32 Dev Module**（espressif 官方内核，≥2.x） |
| USB 驱动 | 按板上桥接芯片装：CP2102 → Silicon Labs CP210x VCP；CH340 → Win10+ 免驱；CH9102 → 沁恒 CH343/CH9102 驱动 |

## 实验步骤与现象

1. 修改 `.ino` 开头的 `WIFI_SSID / WIFI_PASS` → 上传。
2. **上电自检**：板载蓝灯闪 3 下（GPIO2，低电平点亮）。
3. 串口监视器 115200：`IP = 192.168.x.x`、`mDNS: http://esp32-devkit.local`。
4. 浏览器打开 IP → 点"切换 LED"，板灯立即响应；ADC/温度每 2s 刷新。

## 踩坑记录

| 现象 | 原因与对策 |
|---|---|
| 卡 `Connecting....` | 按住 **BOOT** 键点上传，出现 Connecting 后松开（或按住 BOOT 再点 EN 复位进入下载模式） |
| 设备管理器出现"未知设备" | 桥接芯片是 CH9102，需手动装沁恒驱动；CP2102 装 Silicon Labs 驱动 |
| 串口能开但上传失败 | USB 线只供电不通数据，换一根全功能线 |
| ADC 读数接近 4095 / 抖动大 | 引脚悬空；GPIO34 是输入专用脚，没有内部上拉，需要接传感器或下拉 |
| WiFi 连不上 | 确认 2.4GHz（不支持 5GHz 单频路由）；WPA3 需内核 ≥ 2.0.3 |
| ADC2 引脚（0/2/12-15/25-27）读数异常 | **ADC2 与 WiFi 共存冲突**——WiFi 工作时用 ADC1（32-39） |

## ESP32 DevKit 引脚速查（30Pin/38Pin 通用）

| GPIO | 常用功能 | 注意 |
|---|---|---|
| 0 | 下载模式选择 / 普通 IO | **低电平=下载模式**，板载 BOOT 键，作输出慎用 |
| 1 (TX0) / 3 (RX0) | 串口 | 下载/监视占用，慎作他用 |
| 2 | **板载 LED（低电平亮）** / ADC2 / 启动绑定 | 启动时须为高电平或悬空 |
| 4, 16, 17, 18, 19, 21, 22, 23 | 通用 IO，I2C/SPI 常用 | 安全区，随便用（I2C 默认 SDA=21，SCL=22） |
| 5 | SPI CS / VSPI | **启动须为高电平**（接了上拉），输出有毛刺 |
| 12 | ADC / 触摸 | **启动须为低电平**，接外部上拉会进不了下载模式 |
| 13, 14, 15 | ADC2 / PWM / VSPI | 15 号启动绑定（上拉），一般无碍 |
| 25, 26 | **DAC1 / DAC2** + ADC2 | 全芯片仅 2 路真 DAC，做波形输出用 |
| 27, 14, 12, 13, 9*, 10*, 4, 2, 15 | 触摸传感器 T0–T9 | 无电容按键芯片时的免费触摸方案 |
| 32–39 | **ADC1（WiFi 下唯一可用）** | **34–39 仅输入、无内部上拉下拉**；32/33 可作 DAC 唤醒 |
| 6–11 | — | **不可用**（接片内 SPI Flash） |
| EN | 复位 | 板载 EN 键 |

三条布线红线（决定能不能开机/下载）：
1. GPIO0 低电平 = 下载模式，高电平 = 运行（板载 BOOT 键拉到它）；
2. GPIO12 启动须为低电平（决定 VDD_SDIO 电压），外部上拉会下载失败；
3. GPIO2 启动时应为高电平或悬空。

## 应用案例（完整可烧录）

### 案例 1：Web 控制台（本实验）

见 [[ESP32_WebServer.ino]]。要点：HTML 存 PROGMEM；控制 `POST`、查询 `GET` 分离；ESP32 比 ESP8266 多了片上温度 `temperatureRead()`。

### 案例 2：BLE 通知（ESP8266 做不到，ESP32 独占）

手机装 **nRF Connect** App，ESP32 当 BLE 服务器，按键变化实时推送通知——无路由器也能和手机交互。

```cpp
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define BTN_PIN 4                              // 按键接 GPIO4 → GND
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHAR_UUID           "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLECharacteristic* pChar;
unsigned long pressCount = 0;

void setup() {
  pinMode(BTN_PIN, INPUT_PULLUP);
  BLEDevice::init("ESP32-BLE-Demo");
  BLEServer* pServer = BLEDevice::createServer();
  BLEService* pService = pServer->createService(SERVICE_UUID);
  pChar = pService->createCharacteristic(
      CHAR_UUID, BLECharacteristic::PROPERTY_NOTIFY);
  pChar->addDescriptor(new BLE2902());         // 允许客户端订阅
  pService->start();
  BLEAdvertising* pAdv = BLEDevice::getAdvertising();
  pAdv->addServiceUUID(SERVICE_UUID);
  pAdv->start();
  Serial.println("BLE 广播中：ESP32-BLE-Demo");
}

void loop() {
  static bool last = HIGH;
  bool now = digitalRead(BTN_PIN);
  if (last == HIGH && now == LOW) {           // 按下沿
    pressCount++;
    uint32_t v = pressCount;
    pChar->setValue((uint8_t*)&v, 4);         // 推送按键计数
    pChar->notify();
  }
  last = now;
  delay(20);
}
```

验证：nRF Connect 连接 `ESP32-BLE-Demo`，订阅该特征，每按一次键收到 +1 的数值。

### 案例 3：DAC 输出正弦波（示波器/扬声器直连 GPIO25）

```cpp
// GPIO25 = DAC1，DMA 外设自动搬运，CPU 零负担，DAC 外设支持直接连 I2S DMA
#include <driver/dac_cosine.h>

void setup() {
  dac_cosine_config_t cfg = {};
  cfg.chan_mask = DAC_CHAN_MASK_CH0;          // DAC1 = GPIO25
  cfg.freq_hz   = 1000;                       // 1kHz 正弦
  cfg.clk_src   = DAC_COSINE_CLK_SRC_DEFAULT;
  cfg.atten     = DAC_COSINE_ATTEN_DB_0;      // 满幅 ~3.3V
  dac_cosine_new_channel(&cfg, NULL);
  dac_cosine_start(DAC_CHAN_MASK_CH0);
}

void loop() {}
```

验证：示波器接 GPIO25 看到 1kHz 正弦；接功放+喇叭可发声。ESP8266 没有 DAC，这是 ESP32 的硬件级差异。

### 案例 4：ArduinoOTA 空中升级

```cpp
#include <WiFi.h>
#include <ArduinoOTA.h>

const char* SSID = "YourWiFi";
const char* PASS = "YourWiFi_Password";

void setup() {
  Serial.begin(115200);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  ArduinoOTA.setHostname("esp32-ota");
  ArduinoOTA.begin();
  Serial.println("OTA 就绪：Arduino IDE → 网络端口 → esp32-ota");
}

void loop() { ArduinoOTA.handle(); }
```

验证：IDE `工具 → 端口` 出现网络端口 `esp32-ota at 192.168.x.x`。

### 案例 5：双核分工（FreeRTOS 任务绑核）

ESP32 是双核，把通信和实时控制拆到两个核，互不抢 CPU：

```cpp
#include <WiFi.h>

void taskComm(void* p) {                      // 绑核 0：通信
  while (true) {
    Serial.printf("核%d 空闲堆栈: %u\n",
        xPortGetCoreID(), uxTaskGetStackHighWaterMark(NULL));
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskControl(void* p) {                   // 绑核 1：实时控制
  pinMode(2, OUTPUT);
  while (true) {                              // 1ms 周期的"实时"任务
    digitalWrite(2, !digitalRead(2));
    vTaskDelay(pdMS_TO_TICKS(1));
  }
}

void setup() {
  Serial.begin(115200);
  // 第四个参数是核号：0=协议栈所在核(PRO_CPU)，1=应用核(APP_CPU)
  xTaskCreatePinnedToCore(taskComm,    "comm",    4096, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(taskControl, "control", 2048, NULL, 2, NULL, 1);
}

void loop() {}
```

验证：LED 以 1ms 翻转不受串口打印影响；串口同时打印两核的堆栈水位。

## 官方手册（本地归档）

本板基于**乐鑫 ESP32** 芯片 + **ESP32-WROOM-32 模组**。以下 PDF 已归档至 [Assets/datasheets/esp32/](../../../Assets/datasheets/esp32/)，随知识库离线可查：

| 文件 | 层级 | 内容 | 何时查 |
|---|---|---|---|
| [esp32_datasheet_cn.pdf](../../../Assets/datasheets/esp32/esp32_datasheet_cn.pdf) | 芯片 | 概述、电气特性、功耗、外设列表、启动模式、管脚描述 | 查极限参数/管脚功能 |
| [esp32-wroom-32_datasheet_cn.pdf](../../../Assets/datasheets/esp32/esp32-wroom-32_datasheet_cn.pdf) | 模组 | 引脚定义、封装尺寸、推荐外围电路、RF 指标 | 画板/接线 |
| [esp32-wroom-32d_esp32-wroom-32u_datasheet_cn.pdf](../../../Assets/datasheets/esp32/esp32-wroom-32d_esp32-wroom-32u_datasheet_cn.pdf) | 模组 | IPEX 天线版（32U）与外置天线版差异 | 选型对比 |
| [esp32-wrover-b_datasheet_cn.pdf](../../../Assets/datasheets/esp32/esp32-wrover-b_datasheet_cn.pdf) | 模组 | 带 PSRAM 版（8MB PSRAM + 4MB Flash） | 需要大内存（摄像头/音频缓冲）时 |
| [esp32_devkitc_v4_sch.pdf](../../../Assets/datasheets/esp32/esp32_devkitc_v4_sch.pdf) | 开发板 | **DevKitC V4 官方原理图**（电源/自动下载电路/按键/LED） | 理解板上每个元件的作用 |

官方在线入口（获取更新版）：
- 乐鑫文档中心：https://www.espressif.com/zh-hans/support/documents/technical-documents
- ESP-IDF 开发板指南：https://docs.espressif.com/projects/esp-dev-kits/zh_CN/latest/esp32/esp32-devkitc/user_guide.html

## 与本章其他笔记的关系

- [[003-核心特性]] — 双核架构、外设矩阵（案例 5 的任务绑核）
- [[002-开发框架]] — Arduino 内核 vs ESP-IDF 的选择
- [[../esp8266-webserver-demo/README]] — 姊妹实验：同一套 Web 控制台在 ESP8266 上的实现与差异对照
- [[005-推荐资源]] — ESP32 进阶学习路径

## 验收自测

1. 网页开关 LED 延迟 < 1s，与串口打印的 IP 一致；
2. 说出 CP2102 / CH340 / CH9102 三种桥接芯片对应的驱动来源；
3. 说出 GPIO34–39 为什么是 ADC 首选引脚（仅输入 + 无内部上下拉 + ADC1）；
4. 解释为什么 WiFi 工作时 ADC2 读数不可靠，改用哪组引脚；
5. 案例 5 中，通信任务和控制任务分别绑在哪个核，为什么这样分工。
