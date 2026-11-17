---
tags: [esp8266, esp12e, webserver, iot, experiment]
date-created: 2026-11-17
---

# 实验笔记：ESP8266 Web 控制台（ESP-12E 通用开发板 TYPE-C 版）

## 实验目标

让 ESP8266（ESP-12F 模组）连接路由器后充当 Web 服务器，实现：

- 浏览器网页实时开关板载 LED（交互式，双向）
- 每 2 秒轮询 ADC 电压 / WiFi 信号强度
- mDNS 免记 IP（`http://esp8266-demo.local`）

**成品文件**：[[ESP8266_WebServer.ino]]（固件）、`preview.html`（浏览器模拟版，无硬件可预览交互）。

## 实验环境

| 项 | 值 |
|---|---|
| 硬件 | ESP-12F 模组通用开发板（Taobao TYPE-C 版，CH340 转串口） |
| Arduino 板型 | NodeMCU 1.0 (ESP-12E Module)（失败则退 Generic ESP8266 Module，Flash Mode DIO，4MB） |
| USB 驱动 | CH340/CH341（Win10+ 一般免驱） |
| 内核库 | esp8266 by ESP8266 Community（≥3.0） |

## 实验步骤与现象

1. 修改 `.ino` 开头的 `WIFI_SSID / WIFI_PASS` → 上传。
2. **上电自检**：板载蓝灯闪 3 下（GPIO2，低电平点亮）。不闪说明灯在 GPIO16（部分板变种），改 `LED_PIN` 重新烧录。
3. 串口监视器 115200 观察：`IP = 192.168.x.x`、`mDNS: http://esp8266-demo.local`。
4. 浏览器打开 IP → 点"切换 LED"，板灯立即响应；ADC/信号强度每 2s 刷新。

## 踩坑记录

| 现象 | 原因与对策 |
|---|---|
| 卡 `connecting....` | 手动进下载模式：按住 FLASH 键复位，或按住 FLASH 点上传，出现 connecting 后松开 |
| 上传成功但灯不闪 | 灯在 GPIO16：`LED_PIN` 改 16 |
| 网页偶尔打不开/重启 | heap 耗尽（Exception 29）：网页存 PROGMEM、JSON 用短缓冲，别在回调里做字符串拼接 |
| 连不上 WiFi | 检查路由器是否开了 WPA3（ESP8266 仅支持 WPA/WPA2）；确认 2.4GHz（不支持 5GHz） |

## ESP-12E 引脚速查（D 标号 ↔ GPIO ↔ 功能）

| 板载丝印 | GPIO | 常用功能 | 注意 |
|---|---|---|---|
| D0 | 16 | 普通 IO / 深睡眠唤醒 | **不支持中断、不支持 PWM** |
| D1 | 5 | I2C SCL / PWM | — |
| D2 | 4 | I2C SDA / PWM | — |
| D3 | 0 | PWM / 按键 | **启动模式选择脚**，上拉电阻，作输出慎用 |
| D4 | 2 | **板载 LED（低电平亮）** / TX1 | 启动时决定 UART 下载，上拉，勿外部强拉低 |
| D5 | 14 | SPI SCK / PWM | — |
| D6 | 12 | SPI MISO / PWM | 上拉 |
| D7 | 13 | SPI MOSI / PWM | — |
| D8 | 15 | SPI CS / PWM | **启动须为低电平**（接了 Flash CS），作输出慎用 |
| D9 | 3 | RX0 | 串口下载/监视用，慎占 |
| D10 | 1 | TX0 | 同上，打印会冲突 |
| A0 | ADC0 | 模数转换 | **模组裸片量程 0~1V；开发板带分压，0~3.3V**；唯一 ADC |
| — | 6~11 | — | **不可用**（接片内 Flash） |

三条布线红线（直接决定能不能开机）：
1. GPIO15 必须保持低电平启动；
2. GPIO0 低电平=下载模式、高电平/悬空=运行；
3. GPIO2 启动时应为高电平或悬空（上拉）。

## 应用案例（完整可烧录）

### 案例 1：Web 控制台（本实验）

见 [[ESP8266_WebServer.ino]]。要点：HTML 存 PROGMEM 不占 RAM；状态查询 `GET`（幂等轮询）与控制 `POST`（写操作）分离。

### 案例 2：DHT22 温湿度 → MQTT 上云

依赖库：`DHT sensor library`（Adafruit）、`PubSubClient`（knolleary）。

```cpp
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const char* SSID = "YourWiFi";
const char* PASS = "YourWiFi_Password";
const char* MQTT_SERVER = "broker.emqx.io";   // 公共测试 broker
const char* TOPIC = "home/lab/temperature";

WiFiClient espClient;
PubSubClient mqtt(espClient);
DHT dht(D2, DHT22);                            // 数据脚接 D2(GPIO4)

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  mqtt.setServer(MQTT_SERVER, 1883);
}

void loop() {
  if (!mqtt.connected()) {
    if (mqtt.connect("esp8266-lab")) mqtt.subscribe(TOPIC);
    delay(2000); return;
  }
  mqtt.loop();

  static unsigned long last = 0;
  if (millis() - last < 10000) return;         // 每 10s 上报
  last = millis();

  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t)) return;
  char payload[64];
  snprintf(payload, sizeof(payload), "{\"temp\":%.1f,\"hum\":%.1f}", t, h);
  mqtt.publish(TOPIC, payload);
  Serial.println(payload);
}
```

验证：MQTT X 客户端订阅 `home/lab/temperature`，每 10 秒收到一条 JSON。

### 案例 3：继电器远程开关（带 10 分钟自动关断保护）

继电器模块接 D6（GPIO12，高电平触发类模块；低电平触发则反相）。**给不可自动恢复负载（电热、电机）必须加超时关断**。

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* SSID = "YourWiFi";
const char* PASS = "YourWiFi_Password";
const int RELAY_PIN = 12;                      // D6
const unsigned long AUTO_OFF_MS = 10UL * 60 * 1000;

ESP8266WebServer server(80);
bool relayOn = false;
unsigned long relayOnAt = 0;

void sendPage() {
  server.send(200, "text/html",
    "<meta charset=utf-8><body style='font-family:system-ui;text-align:center'>"
    "<h1>继电器</h1><h2 style='color:" + String(relayOn ? "green'>已接通" : "gray'>已断开") + "</h2>"
    "<a href='/toggle'><button style='font-size:24px;padding:16px 40px'>切换</button></a>"
    "<p>10 分钟无操作自动断开</p></body>");
}

void setup() {
  pinMode(RELAY_PIN, OUTPUT); digitalWrite(RELAY_PIN, LOW);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  server.on("/", []() { sendPage(); });
  server.on("/toggle", []() {
    relayOn = !relayOn;
    digitalWrite(RELAY_PIN, relayOn ? HIGH : LOW);
    relayOnAt = millis();
    sendPage();
  });
  server.begin();
}

void loop() {
  server.handleClient();
  if (relayOn && millis() - relayOnAt > AUTO_OFF_MS) {
    relayOn = false;                           // 超时保护关断
    digitalWrite(RELAY_PIN, LOW);
  }
}
```

### 案例 4：SmartConfig 一键配网（免硬编码 WiFi 密码）

手机装"ESPTOUCH"App（乐鑫官方），长按设备键进入配网模式，手机输 WiFi 密码一键下发；配网结果自动持久化到 Flash。

```cpp
#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin();                                // 优先用上次保存的凭据
  if (WiFi.waitForConnectResult(10000) != WL_CONNECTED) {
    Serial.println("进入 SmartConfig 模式（App 一键配网）...");
    WiFi.beginSmartConfig();
    while (!WiFi.smartConfigDone()) { delay(500); Serial.print('.'); }
    Serial.println("\n配网成功，等待连接...");
  }
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.printf("已连接: %s\n", WiFi.localIP().toString().c_str());
}

void loop() {}
```

### 案例 5：ArduinoOTA 空中升级（产品化必备）

```cpp
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>

const char* SSID = "YourWiFi";
const char* PASS = "YourWiFi_Password";

void setup() {
  Serial.begin(115200);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  ArduinoOTA.setHostname("esp8266-ota");
  ArduinoOTA.begin();                          // 注意：配网后再 begin
  Serial.println("OTA 就绪，Arduino IDE → 网络端口 → esp8266-ota");
}

void loop() { ArduinoOTA.handle(); }
```

验证：Arduino IDE 菜单 `工具 → 端口` 里出现网络端口 `esp8266-ota at 192.168.x.x`，直接网络上传新固件。

## 官方手册（本地归档）

ESP-12E 是**安信可（AI-Thinker）**基于**乐鑫 ESP8266EX** 芯片的模组，完整资料分两层：模组级（封装/引脚/天线/RF 参数）看安信可规格书，芯片级（寄存器/外设/电气特性/低功耗细节）看乐鑫手册。以下 PDF 已归档至 [Assets/datasheets/esp8266/](../../../Assets/datasheets/esp8266/)，随知识库离线可查：

| 文件 | 层级 | 内容 | 何时查 |
|---|---|---|---|
| [ESP-12E_Specification_EN_AI-Thinker_20220807.pdf](../../../Assets/datasheets/esp8266/ESP-12E_Specification_EN_AI-Thinker_20220807.pdf) | 模组 | 引脚定义、封装尺寸、推荐外围电路、RF 指标 | 画板/接线/查引脚功能 |
| [ESP-12F_Specification_CN_AI-Thinker_20201207.pdf](../../../Assets/datasheets/esp8266/ESP-12F_Specification_CN_AI-Thinker_20201207.pdf) | 模组 | 同上（中文版；12F 与 12E 引脚兼容，Flash 容量不同） | 快速查阅 |
| [ESP8266EX_Datasheet_v7.1_EN.pdf](../../../Assets/datasheets/esp8266/ESP8266EX_Datasheet_v7.1_EN.pdf) / [CN](../../../Assets/datasheets/esp8266/ESP8266EX_Datasheet_CN.pdf) | 芯片 | 概述、电气特性、功耗数据、启动模式、管脚描述 | 查时序/电流/极限参数 |
| [ESP8266_Technical_Reference_v1.7_EN.pdf](../../../Assets/datasheets/esp8266/ESP8266_Technical_Reference_v1.7_EN.pdf) / [CN](../../../Assets/datasheets/esp8266/ESP8266_Technical_Reference_CN.pdf) | 芯片 | **TRM**：GPIO/中断矩阵、定时器、I2S、UART、SDIO、寄存器级细节 | 写底层驱动/查寄存器 |

官方在线入口（获取更新版）：
- 乐鑫文档中心：https://www.espressif.com/zh-hans/support/documents/technical-documents （ESP8266 分类下还有《硬件设计指南》《Wi-Fi 射频指标》《ESP-TOUCH 配网指南》）
- 安信可文档中心：https://docs.ai-thinker.com/esp8266 （模组规格书 + SDK/固件/云平台对接教程）

## 与本章其他笔记的关系

- [[003-核心特性]] — 功耗/安全特性表（案例 2/4 的 WiFi 部分）
- [[05-低功耗设计]] — Deep Sleep + ULP 配合 RTC 唤醒的电池方案
- [[000-无线通信]] — MQTT/CoAP/TCP 协议细节
- [[02-FreeRTOS]] — ESP8266 RTOS SDK 下的多任务写法

## 验收自测

1. 网页开关 LED 延迟 < 1s，与串口打印的 IP 一致；
2. 断路由器电源重启板子，继电器案例的自动关断是否生效（用 LED 模拟验证，勿直接带电热负载）；
3. 用 `MQTT X` 订阅案例 2 主题，连续 1 分钟无丢包；
4. 说出 GPIO0/GPIO2/GPIO15 三条启动红线（面试常考）。
