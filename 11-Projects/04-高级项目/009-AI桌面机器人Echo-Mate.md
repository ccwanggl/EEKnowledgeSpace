---
tags: [projects, advanced, rv1106, linux, lvgl, ai, rknn, embedded-linux, rockchip]
date-created: 2026-11-19
---

# 9. AI 桌面机器人 Echo-Mate（RV1106 综合项目）

**目标**：嵌入式 Linux 系统 + LVGL GUI + AI 语音交互 + NPU 视觉推理的一体化综合项目。
**定位**：可复刻的开源桌面机器人，同时是一块全功能 RV1106 Linux 开发板，适合作为嵌入式方向的「综合练手项目 / 课设毕设参考」。

## 项目信息

| 项 | 内容 |
|----|------|
| 作者 | 油炸鸡开源硬件（no_chicken，B 站 UP 主） |
| 硬件开源 | [oshwhub.com/no_chicken/ai-desktop-robot-echo](https://oshwhub.com/no_chicken/ai-desktop-robot-echo) |
| 软件仓库 | [github.com/No-Chicken/Echo-Mate](https://github.com/No-Chicken/Echo-Mate) |
| 例程仓库 | [github.com/No-Chicken/Demo4Echo](https://github.com/No-Chicken/Demo4Echo) |
| 项目手册 | [no-chicken.com](https://no-chicken.com/content/Echo-Mate/intro.html) |
| 演示视频 | [B 站 BV161ZaYyEmF](https://www.bilibili.com/video/BV161ZaYyEmF/) |
| 复刻教程 | [B 站 BV1685qztEec](https://www.bilibili.com/video/BV1685qztEec) |
| 衍生参考 | rv1106_lico、an_ye/rv1106_demo 的引脚分配均参考本项目 |

## 功能概览

- LVGL 菜单式桌面助手：AI 聊天、翻译、看天气、备忘、PC 状态监控
- AI 语音助手：热词唤醒 → ASR → 意图识别 → LLM 对话 → TTS 播报
- AI 相机：YOLOv5s 目标检测（NPU 推理）
- 小电视（ffmpeg 推流演示）、小游戏（延续 OV-Watch 手表项目）
- 桌面机器人形态：3D 打印外壳 + 履带轮（电机驱动板 TC118S 驱动减速电机）

## 硬件架构

| 模块 | 选型 | 说明 |
|------|------|------|
| 主控 | 瑞芯微 RV1106（QFN128） | 单核 Cortex-A7 @1.2GHz + RISC-V MCU，1TOPS NPU（int4/int8/int16） |
| 内存 | 256MB DDR3L | 片载 |
| 存储 | SD 卡 或 板载 NAND Flash | 二选一 |
| Wi-Fi/BT | RTL8723BS（SDIO 接口） | **必须是 BS 版本**，别买错 |
| 屏幕 | 2.4 寸 SPI ST7789V + IIC FT6336U 触摸 | 型号 P024C128-CTP（淘宝浦洋） |
| 摄像头 | MIPI CSI 接口 | 直接用 Luckfox Pico 摄像头模组（SC3336） |
| 音频 | MX1.25mm 喇叭/MIC 接口 | |
| 供电 | Type-C（5V） | 后续可改电池供电 |
| 扩展 | 8 个空闲 GPIO 排针 | |
| 结构 | 层叠 PCB + 3D 打印外壳 | 嘉立创 7628 板材，20% 阻抗控制 |

### 复刻物料要点
- Wi-Fi 天线：立创 AIWF022（Wi-Fi7 内置 FPC 双频天线）
- 3D 外壳：嘉立创打印，主动轮/从动轮各两份，装配见 B 站教程
- 工具：焊接工具、USB 转 TTL 串口模块、瑞芯微驱动助手 + 烧录工具、MobaXterm

## 软件架构

### 系统层
- SDK：基于 Luckfox Pico 的 rv1106-sdk（Buildroot，Linux 5.10）
- 仓库结构：`Demo/`（DeskBot_demo 及各独立子 demo）+ `SDK/`（rv1106-sdk + 使用说明）
- 默认账号 `root / root`；支持串口登录与 SSH（USB 虚拟网卡）

### 应用层框架（UI 与业务分离）
```
DeskBot_demo/
├── bin/            # 可执行文件
├── common/         # 通用层（sys_manager 等硬件管理）
├── conf/           # 系统设置
├── gui_app/        # UI 层：pages / images / font / ui.c
├── lvgl/           # LVGL 核心
├── utils/
└── main.c
```
- **UI 层**：LVGL 图形库；PageManager 用栈结构管理多页面，支持字符注册/查询页面（比作者此前 OV-Watch 项目更方便扩展）
- **业务层**：AI Chat、AI 相机、YOLO 推理等具体功能；每个 APP 进入页面后开独立线程运行，主线程只做 UI 渲染
- **C/C++ 接口封装**：AIChat 用 C++ 实现、转 C 接口供 LVGL UI 层调用

### AI Chat 语音链路（Client–Server 架构）
```
唤醒(snowboy) → FSMN-VAD(端点检测) → SenseVoice(ASR+情感)
  → FastText(意图分类) → 通义千问(LLM, 阿里云API) → CosyVoice(TTS, 阿里云API)
```
- RV1106 单核 A7 算力不足，推理放 Server 端（自己电脑）；Client 在开发板上
- 通信：WebSocket + JSON，语音数据 opus 编码
- Server：Python 3.10（Ubuntu 22.04），或直接用打包好的 Windows exe（约 2GB）
- 后续版本意图识别改为基于 MCP 的 function call（LLM 直接输出意图 JSON）
- 自定义指令：改 FastText 数据集重新训练即可

### AI 相机（YOLO Camera）
- 图像捕获用 nihui 的 opencv-mobile（作者已编译好适配 Echo 的版本）
- YOLOv5s 预训练模型 → RKNN 部署到 NPU 推理
- 注意：opencv-mobile 方式方便但失去 VI/VPSS 硬件加速，帧率有损失；追求性能应改用 rkmpi 的 VI/VPSS 捕获
- 参考 Luckfox-pico rkmpi 例程（VI、RTSP 推流等）

## 复刻流程（免编译路线）

1. 手册下载最新固件（buildroot-SD 卡版 或 NAND 版），瑞芯微烧录工具烧录
2. 解压附件 `bin.rar`，传入开发板
3. 修改 `system_para.conf`：
   - `AI_Chat_Server` 地址改为同网段电脑的 IP
   - 填入高德 API key（天气）和阿里云百炼 API key（LLM），个人用户均免费
4. 电脑端运行 Server：`python ./main.py --access_token="123456"`（或运行 exe）
5. 板端执行：`cd ./bin && chmod +x ./main && ./main`
6. 天气/自动对时需先连 Wi-Fi（城市 adcode 见附件 Excel）

## 技能点图谱（为什么适合做综合项目）

| 方向 | 具体技能 |
|------|----------|
| 嵌入式 Linux | Buildroot 系统构建、固件烧录、驱动助手、U-Boot/内核基础 |
| GUI 开发 | LVGL、页面栈管理、UI/业务分层、C 接口封装 |
| 网络通信 | WebSocket 协议、JSON、opus 音频传输、TCP/IP 调试 |
| 多媒体 | rkmpi（VI/VPSS/VENC/RTSP）、ffmpeg、V4L2 |
| AI 部署 | RKNN 工具链、YOLOv5 量化部署、NPU 推理 |
| 语音链路 | VAD/ASR/TTS 模型串联、FastText 意图分类、模型训练 |
| C/C++ 工程 | 状态机、设计模式、多线程管理、堆栈链表数据结构 |
| 硬件 | RV1106 最小系统设计、SDIO Wi-Fi、SPI 屏、MIPI CSI、层叠 PCB |

## 注意事项

1. Wi-Fi 模块必须是 **RTL8723BS**（不是 DS 等其他后缀）
2. 最新固件以项目手册站为准，立创页面附件可能不是最新
3. 学习开发用 Ubuntu 22.04 虚拟机拉仓库；复刻只需烧固件 + 会基本 Linux 命令
4. 摄像头套件淘宝没有现成配套，直接搜「luckfox-pico 摄像头」购买
5. 软件以 GitHub 仓库和手册为准，硬件以立创开源平台 PCB 为准

## 参考

- Luckfox rkmpi 学习指南、新一代 kaldi（sherpa-onnx）、FunASR、SenseVoice、CosyVoice、FastText、OpenCV-Mobile、小智 ESP32（见项目页参考链接）
