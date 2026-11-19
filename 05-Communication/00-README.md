---
tags: [index, readme, 05-communication]
date-created: 2026-06-17
date-updated: 2026-09-29
---

# 通信协议（05-Communication）

> 从芯片间总线到工业总线、有线高速接口与无线链路，建立"先判断层次、再选协议、最后动手调试"的完整能力。

嵌入式通信的问题很少出在"协议选错了"，多数出在层次判断错了：把一个物理层问题（终端电阻、地电位差）当成协议问题去改代码，或者反过来把协议参数问题（采样点、地址偏移）当成硬件问题去换器件。这个目录按协议族组织，每篇都按"电气与时序参数 → 配置计算 → 常见故障"展开，目的就是让问题能一次落到正确的层次上。

## 从一个任务开始

[[00-Index/03-AI自学任务索引#通信协议：读出一帧 UART|通信协议：读出一帧 UART]]。先试做，根据卡点回正文或找 AI 提示，再用变式独立验收。

## 模块导航

| 模块 | 覆盖内容 | 入口 |
|---|---|---|
| 01 | 分层模型、协议分类、选型方法 | [[05-Communication/01-通信协议概述/000-通信协议概述\|通信协议概述]] |
| 02 | UART、SPI、I2C 的帧、时序与总线设计 | [[05-Communication/02-I2C-SPI-UART/000-I2C-SPI-UART\|I2C-SPI-UART]] |
| 03 | CAN 与 CAN FD 的仲裁、帧格式、位时序、高层协议 | [[05-Communication/03-CAN总线/000-CAN总线\|CAN 总线]] |
| 04 | RS-485 物理层与 Modbus 应用层 | [[05-Communication/04-RS-485与Modbus/000-RS-485与Modbus\|RS-485 与 Modbus]] |
| 05 | USB 版本、枚举、设备类、供电与 PD | [[05-Communication/05-USB协议/000-USB协议\|USB 协议]] |
| 06 | 以太网物理层、TCP/IP 裁剪、lwIP、应用协议与 TLS | [[05-Communication/06-以太网与TCP-IP/000-以太网与TCP-IP\|以太网与 TCP/IP]] |
| 07 | BLE、WiFi、Thread/Zigbee/Matter、LoRa、蜂窝物联网 | [[05-Communication/07-无线通信-BLE-WiFi-Matter/000-无线通信\|无线通信]] |

## 各协议速率怎么算

速率问题分两层：**标称速率**（PHY/波特率档位）和**有效吞吐**（扣掉帧开销、仲裁、轮询间隙后的净数据率）。评估"这条链路带不带得动"，用的是后者。

### 芯片间：UART / SPI / I2C

- **UART**：字节率 = 波特率 ÷ 每帧位数。`8N1` 为 10 位/字节，`115200` 波特 → 约 `11.5 kB/s`。双方时钟误差合计要 ≤2%~3%（16 倍过采样、三取二表决），详见 [[05-Communication/02-I2C-SPI-UART/002-UART异步串行通信|002]]。
- **SPI**：字节率 = $f_{SCK} ÷ 8$，全双工。上限由时序约束定：$T_{SCK} > t_{su}+t_{hd}+t_{skew}$，再留 20%~50% 裕量，详见 [[05-Communication/02-I2C-SPI-UART/003-SPI同步串行接口|003]]。`8 MHz` 时钟 → 约 `1 MB/s`。
- **I2C**：字节率 = $f_{SCL} ÷ 9$（8 数据位 + 1 ACK），还要再扣起始、地址、重起始。`100 k` → 约 `11.1 kB/s`，`400 k` → 约 `44.4 kB/s`。$f_{SCL}$ 不是想提就提，上拉电阻必须落在

$$R_{p,\min}=\frac{V_{DD}-V_{OL}}{I_{OL}},\qquad R_{p,\max}=\frac{t_{r,\max}}{0.847\,C_b}$$

之间。算例：`3.3 V`、总线电容 `100 pF` 时，100 k 档允许约 1~11.8 kΩ（常用 4.7 kΩ），400 k 档收紧到约 1~3.5 kΩ（常用 2.2 kΩ），详见 [[05-Communication/02-I2C-SPI-UART/004-I2C总线与多设备仲裁|004]]。

### CAN / CAN FD

- **位时间**：波特率 = $f_{clk}$ ÷ (BRP × N_TQ)，N_TQ = 1 + BS1 + BS2，采样点 = (1+BS1)/N_TQ，常用 87.5%（N_TQ = 16 或 20）。算例：`8 MHz` 时钟做 `500 kbps`：TQ = 125 ns、BRP = 1、N_TQ = 16 → 1+6+7+2，详见 [[05-Communication/03-CAN总线/005-位时序与同步|005]]。
- **长度—速率**：1M/40 m、500k/100 m、250k/250 m、125k/500 m（降到 10k 可到 5 km），见 [[05-Communication/03-CAN总线/004-物理层与拓扑设计|004]]。
- **负载率**：负载率 = Σ(帧位数 × 发送频率) ÷ 波特率，建议控制在 30%~50%。算例：20 节点各发标准帧（约 111 位）100 Hz，`20×111×100/500k ≈ 44%`，已接近上限；有效吞吐只有标称的 40%~60%。
- **CAN FD**：仲裁段 ≤1M 不变，数据段提到 2/5/8M，配合最长 64 B 载荷（DLC 非线性），刷写和大报文场景吞吐数倍提升；代价是布线更短（500k+5M 仅十米级），见 [[05-Communication/03-CAN总线/003-CAN-FD扩展|003]]。

### RS-485 / Modbus

- **速率—距离**：10 Mbps≈12 m、1 Mbps≈120 m、`115.2 kbps`≈800 m、`≤100 kbps`≈1.2 km，字节率算法与 UART 相同。
- **Modbus RTU 轮询周期**：

$$T_{cycle}\approx\sum_i\left(\frac{(N_{req,i}+N_{rsp,i})\times10}{B}+T_{gap}+T_{proc,i}\right)$$

帧间隔 $T_{gap}$ ≥ 3.5 字符时间（`9600` 波特下约 `3.65 ms`，`115200` 下约 `0.3 ms`）。算例：8 个从站、请求 8 B + 响应 20 B、`115200` 波特、处理 2 ms → 整轮约 38 ms，刷新率约 26 Hz，详见 [[05-Communication/04-RS-485与Modbus/004-Modbus软件实现|004]]。

### USB

先定**传输类型**再算带宽（[[05-Communication/05-USB协议/003-传输类型、端点与设备类|003]]）：

- 全速帧 1 ms、高速微帧 125 µs；带宽按帧/微帧配额分配，不能拿 480 M 除 2 折算。
- 中断传输：全速每帧最多 64 B → 上限约 `64 kB/s`（HID 键鼠量级）；批量传输全速要到 `1 MB/s` 需每帧约 19 个满 64 B 包；等时传输每帧最多 1023 B。
- 经验有效吞吐：FS ≈ `1 MB/s`，HS ≈ `35~40 MB/s`，5 Gbps ≈ `400 MB/s`，10 Gbps ≈ `0.9~1 GB/s`。CDC-ACM 适合流式大数据，HID 免驱但 ≤64 kB/s。

### 以太网

- 线上开销固定 38 B（前导 7 + SFD 1 + MAC 头 14 + FCS 4 + 帧间间隙 12），最大帧效率 = 1500/1538 ≈ 97.5%；TCP 再扣 40 B 头，1460/1538 ≈ 94.9% 是上限，实测约为线速的 70%~90%。
- TCP 吞吐还受窗口限制：吞吐_max ≈ 窗口字节数 ÷ RTT。`100 ms` RTT 想跑满 10 Mbps 需要约 `125 kB` 窗口——已超出多数 MCU 的 RAM，评估联网能力时先算这笔账，见 [[05-Communication/06-以太网与TCP-IP/002-TCP-IP协议栈与嵌入式裁剪|002]]。

### 无线

- **BLE**：吞吐 ≈ 净荷 × 每连接事件包数 ÷ 连接间隔。默认 MTU 23 B 只剩 20 B 净荷，1M PHY 实际只有几百 kbps 以下；协商 MTU 517 + 数据长度扩展 + 2M PHY 可到约 `1.4 Mbps`。连接间隔 7.5 ms~4 s 是功耗与延迟的主旋钮：`1 s` 间隔 + 从机延迟 9 平均电流约 20 µA，压到 `100 ms` 则到毫安级，见 [[05-Communication/07-无线通信-BLE-WiFi-Matter/002-BLE低功耗蓝牙|002]]。
- **WiFi**：标称速率是特定配置的 PHY 速率（"150M" = n 单流 20 MHz 短 GI），实际吞吐约为标称一半且随包长急剧恶化；链路规划按应用带宽 ×2~3，以 iperf 实测为准，见 [[05-Communication/07-无线通信-BLE-WiFi-Matter/003-WiFi与低功耗联网|003]]。
- **Thread/Zigbee**：PHY 固定 250 kbps，MAC 帧上限 127 B，6LoWPAN 压缩后应用吞吐只有几十 kbps 级；适合灯控与传感器，不适合吞吐场景，见 [[05-Communication/07-无线通信-BLE-WiFi-Matter/004-Thread-Zigbee与Matter|004]]。
- **LoRa**：$R_b \approx SF \cdot BW / 2^{SF} \cdot CR$。SF12/BW125k 约 `293 bps`，SF7 约 `5.5 kbps`；SF 每升一档灵敏度 +2.5 dB、空中时间近翻倍。按 1% 占空比：SF12 发 20 B 空中时间 1~2 s，一天只能发约 576 次；SF7 几十 ms，可每 10 s 一次，见 [[05-Communication/07-无线通信-BLE-WiFi-Matter/005-LoRa与LoRaWAN|005]]。
- **蜂窝物联网**：NB-IoT 上行几十 kbps、静态场景电池可达数年；LTE-M 约 `1 Mbps` 且支持移动；RedCap 数~数十 Mbps。报文虽小但协议开销占比极高，均值估算要留 ×3~10 倍余量，见 [[05-Communication/07-无线通信-BLE-WiFi-Matter/006-其他无线技术与蜂窝物联网|006]]。

## 实际应用案例

各协议在真实产品中的典型位置（选型论证见各模块正文）：

- **UART**：调试日志与命令行；GNSS 模块 NMEA 输出（默认 9600）；蓝牙透传模块（HC-05/06 类）；Modbus RTU 与 RS-485 的物理承载。
- **SPI**：NOR Flash 固件与字库、TFT 屏、高精度 ADC/DAC、nRF24L01 类射频模块、SD 卡——板内、点对点、要速度的场景。
- **I2C**：IMU/气压/温度等传感器、EEPROM、RTC、PMIC、OLED——"板上小器件总线"，10 节点以内；地址冲突与 400 pF 总线电容是扩容的两道墙。
- **CAN**：汽车动力与车身网络；伺服与机器人（CANopen，1~127 节点）；工程机械与农机（J1939，29 位 ID）；电机驱动器（接 [[14-FOC-电机控制/00-README|FOC 电机控制]]）；电池 BMS。
- **RS-485/Modbus**：PLC 轮询变频器、电表、温控仪；楼宇自控；远程抄表；变频器干扰强的车间用隔离收发器 + 屏蔽双绞线 + 单点接地。
- **USB**：固件升级（DFU）、调试与数据二合一的虚拟串口（CDC-ACM）、免驱键鼠（HID）、U 盘与摄像头（bulk/isochronous）；同时是供电入口，PD 3.1 EPR 可到 240 W。
- **以太网**：设备网页配置、传感器上云（MQTT）、固件回传（TFTP/HTTP POST）；工业相机数 MB/s 需千兆；PoE 摄像头一线供电。
- **BLE**：键鼠与手柄（7.5~15 ms 连接间隔）、手环与 Beacon 广播、门锁与医疗设备（高于 Just Works 的配对等级）、电池供电传感器（µA 级待机）。
- **WiFi**：摄像头视频、智能家居配网（SmartConfig/AP/BLE/二维码四法）、ESP32 透传模组；视频类常选 5 GHz 避开 2.4 GHz 拥塞。
- **Thread/Zigbee/Matter**：Hue/IKEA/小米等存量灯控生态；Matter over Thread 必须部署边界路由器；量产前完成设备证书注入。
- **LoRa/LoRaWAN**：农业墒情、远程表计、井盖与烟感——城市 2~5 km、每天数百次小报文；不适合连续数据流。
- **蜂窝（NB-IoT/LTE-M）**：固定安装的抄表、井盖、烟感（NB-IoT + PSM/eDRX）；可穿戴与车载追踪（LTE-M 支持切换）；务必先核算流量套餐与漫游限制。

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-updated AS 更新日期
FROM "05-Communication"
WHERE file.name != "00-README"
SORT file.name ASC
```

## 自测与复习

| 测验 | 覆盖范围 |
|---|---|
| [[05-Communication/08-I2C-SPI-UART测验题\|I2C / SPI / UART 测验题]] | 协议特点、时序模式、上拉与仲裁计算、协议选择 |
| [[05-Communication/09-CAN总线测验题\|CAN 总线测验题]] | 电平与仲裁、帧格式、位时序计算、物理层设计 |

复习入口见 [[00-Index/06-交互式学习中心|交互式学习中心]] 与 [[00-Index/07-闪卡复习库|闪卡复习库]]。

## 推荐的进入顺序

1. 先读 [[05-Communication/01-通信协议概述/000-通信协议概述|通信协议概述]]，把分层、分类和选型方法建立起来。
2. 按项目需要选一条主线动手：芯片间通信走 02，工业现场走 03 或 04，需要供电与枚举的走 05，联网走 06，无线产品走 07。
3. 每一条主线上都先跑通最小闭环（能收发、能观测），再动参数（提速、加长、加节点）。
4. 用对应的测验题检验理解，把调不通的现象记录成可检索的故障条目。

遇到通信故障时，先按 [[05-Communication/01-通信协议概述/001-通信协议基础与分层模型|通信协议基础与分层模型]] 的分层表判断问题落在哪一层，再去查对应模块的故障表。工具侧的使用方法见 [[09-Debugging-Tools/00-README|调试工具]]。

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[01-Foundations/00-README|基础知识]]

## 推荐资料

> 各模块内部的专门资料（数据手册、规范原文、应用笔记）列在对应模块的枢纽页；这里是跨协议的通用读物。

| 资源 | 适用内容 |
|---|---|
| Jan Axelson《Serial Port Complete》 | UART、RS-232/485、I2C、SPI 的工程细节 |
| Jan Axelson《USB Complete》 | USB 从协议到设备类 |
| W. Richard Stevens《TCP/IP Illustrated, Vol. 1》 | 协议行为的权威参考 |
| Ben Eater（YouTube） | 用面包板与示波器演示串行通信与网络的逐位实现 |
| 各协议官方规范 | NXP UM10204（I²C）、Motorola SPI Block Guide、ISO 11898（CAN）、modbus.org（Modbus）、USB-IF 规范 |
| 各半导体厂商应用笔记 | 物理层计算、隔离与保护、协议栈移植 |
