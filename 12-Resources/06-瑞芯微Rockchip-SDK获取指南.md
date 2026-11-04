---
tags: [rockchip, sdk, rk3588, rv1106, 嵌入式linux, bsp]
date-created: 2026-10-28
---

# 瑞芯微（Rockchip）SDK 获取指南

> 目标芯片：RK3588 / RV1106。瑞芯微 SDK 分**管控分发的完整 BSP** 和**公开资源**两类，不同芯片的开放程度差别很大，本文按芯片分别说明。

---

## 总览：两条获取路线

| 路线 | 适用场景 | 门槛 |
|------|----------|------|
| **官方商务渠道** | 量产项目、需要完整 BSP 源码 + FAE 支持 | NDA + SSH 公钥授权 + Redmine 账号 |
| **板卡厂商 / 开源渠道** | 评估、学习、原型验证 | 无门槛，git clone / 网盘直接下载 |

官方商务渠道统一流程：

1. 联系瑞芯微业务代表、代理商，或官方客服 `400-7700-590` / `service@rock-chips.com` 申请对应芯片 SDK（通常需签 NDA、提供公司信息）。
2. 向技术窗口提交 **SSH 公钥**，获得瑞芯微代码服务器（`ssh://git@www.rockchip.com.cn`）访问授权。
3. 注册 [redmine.rockchip.com.cn](https://redmine.rockchip.com.cn) 账号，用 repo 同步代码；在 Redmine「补丁发布」项目中订阅邮件通知，跟踪 SDK 补丁。
4. SDK 内参考文档：《Rockchip_User_Guide_SDK_Application_And_Synchronization_CN.pdf》（docs/cn/Others/ 目录）。

---

## RK3588（应用处理器，AIoT 旗舰）

### 官方 SDK（管控分发）

SDK 基于 kernel 5.10、U-Boot v2017.09，支持 Debian 11 和 Buildroot 2021.11，适用于 RK3588 / RK3588S / RK3588M。

获得授权后同步命令：

```bash
git clone ssh://git@www.rockchip.com.cn/repo/rk/tools/repo
mkdir rk3588 && cd rk3588
repo init --repo-url ssh://git@www.rockchip.com.cn/repo/rk/tools/repo \
  -u ssh://git@www.rockchip.com.cn/linux/rockchip/platform/manifests \
  -b linux -m rk3588_linux_release.xml
.repo/repo/repo sync -c --no-tags
```

也可向技术窗口索取 SDK 初始压缩包（如 `RK3588_LINUX_SDK_RELEASE_V1.x.x_xxx.tgz`），解压后 `repo sync -l && repo sync -c` 检出源码，与在线同步等效。

### 免申请替代：板卡厂商 SDK（推荐评估阶段使用）

**Firefly（萤火虫）**——RK3588 生态最成熟，SDK 公开：

```bash
sudo apt install -y repo git python git-lfs
mkdir rk3588 && cd rk3588

# 完整 SDK
repo init --no-clone-bundle \
  --repo-url https://github.com/Firefly-rk-linux-utils/git-repo.git --no-repo-verify \
  -u https://github.com/Firefly-rk-linux/manifests.git \
  -b master -m rk3588_linux_release.xml

# 或仅 BSP（device/docs/kernel/u-boot/rkbin/tools/交叉编译链，只够编 Ubuntu/Debian 固件）
repo init -u https://github.com/Firefly-rk-linux/manifests.git \
  -b master -m rk3588_linux_bsp_release.xml --no-clone-bundle \
  --repo-url https://github.com/Firefly-rk-linux-utils/git-repo.git --no-repo-verify

.repo/repo/repo sync -c --no-tags
.repo/repo/repo start firefly --all
```

国内网络差时可先下载 Firefly 提供的「SDK 基础包」（split 分卷压缩包），再增量同步 gitlab 代码。Yocto 版本走 `gitlab.com/firefly-linux/manifests.git -m rk3588_yocto_kirkstone_release.xml`。

**野火 LubanCat**——另一套公开 RK3588 SDK：

```bash
repo init -u https://github.com/LubanCat/manifests.git -b linux -m rk3588_linux_release.xml
.repo/repo/repo sync -c -j4
```

LubanCat RK3588 SDK 要求 **Ubuntu 20.04+**；Firefly 官方推荐 **Ubuntu 18.04**。常用仓库分支：`kernel` / `debian` / `ubuntu` 均为 `stable-5.10-rk3588`。

### 环境要求

- x86_64 主机，Ubuntu LTS（真机或 Docker），**不要用虚拟机共享文件夹和非英文路径**
- 全程普通用户编译，不要 root
- 硬盘 ≥ 40 GB

```bash
sudo apt-get install repo git ssh make gcc libssl-dev liblz4-tool \
  expect g++ patchelf chrpath gawk texinfo diffstat binfmt-support \
  qemu-user-static live-build bison flex fakeroot cmake \
  gcc-multilib g++-multilib unzip device-tree-compiler ncurses-dev
```

---

## RV1106（视觉 SoC，IPC/AI 相机）

> 单核 Cortex-A7 + 0.5 TOPS NPU，面向 IPC 视觉。注意型号是 **RV1106** 不是 RK1106。

### 最便捷：Luckfox（幸狐）开源 SDK —— 完全公开

Luckfox Pico 系列（RV1103/RV1106）的 SDK 在 GitHub/Gitee **完全开源**，是当前 RV1106 开发的事实标准入口：

```bash
# 国内推荐 Gitee
git clone --recursive https://gitee.com/LuckfoxTECH/luckfox-pico.git
# 或 GitHub
git clone --recursive https://github.com/LuckfoxTECH/luckfox-pico.git
```

环境要求 **Ubuntu 22.04 x86_64**（仅支持此版本；WSL2 可用）：

```bash
# 1. 安装依赖
sudo apt-get install -y git ssh make gcc gcc-multilib g++-multilib module-assistant \
  expect gawk texinfo libssl-dev bison flex fakeroot cmake unzip gperf autoconf \
  device-tree-compiler libncurses5-dev pkg-config bc python-is-python3 passwd \
  openssl openssh-server openssh-client vim file cpio rsync curl

# 2. 安装交叉编译工具链（arm-rockchip830-linux-uclibcgnueabihf）
cd luckfox-pico/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf/
source env_install_toolchain.sh

# 3. 选择板型并编译
cd {SDK_PATH}
./build.sh lunch   # 选择 RV1106_Luckfox_Pico_Pro_Max / Ultra / Pi 等
./build.sh         # 全量编译（约 1~3 小时）
./build.sh firmware  # 打包固件，输出在 output/image
```

SDK 目录结构：

```text
├── build.sh -> project/build.sh   # 编译脚本
├── media/      # 多媒体编解码、ISP（rkaiq）算法，可独立编译
├── sysdrv/     # U-Boot、kernel、rootfs，可独立编译
├── project/    # 参考应用、编译配置
├── output/     # 编译产物镜像
└── tools/      # 打包与烧录工具
```

烧录：Windows 下用 SocToolKit（[files.luckfox.com](https://files.luckfox.com/wiki/Luckfox-Pico/Software/SocToolKit.zip)），按住 BOOT 键上电进入 MaskRom 烧写 `output/image`。

文档：[wiki.luckfox.com](https://wiki.luckfox.com/zh/Luckfox-Pico-RV1106/SDK/SDK-Image-Compilation)

### 官方渠道

RV1106 官方完整 SDK 同样走商务申请（见上文总览）；预编译固件可在官方固件下载中心 [redmine.rock-chips.com/urllist](https://redmine.rock-chips.com/urllist) 的「RV 系列 SDK」栏获取（含 RV1126B、RV1106B/RV1103B 等）。

### NPU / AI 开发配套（完全公开）

| 仓库 | 用途 |
|------|------|
| `github.com/airockchip/rknn-toolkit2` | 模型转换（ONNX/TF → RKNN）、量化、PC 端仿真 |
| `github.com/rockchip-linux/rknpu2` | 板端 RKNN Runtime（C API） |
| `github.com/airockchip/librga` | 图像格式转换/缩放加速库 |
| `github.com/airockchip/rknn_model_zoo` | YOLO 等模型部署示例（RV1106 选 `-DTARGET_SOC=rv110x`） |

视觉应用常用 **opencv-mobile**（nihui 的精简 OpenCV，有 luckfox-pico 预编译包），体积仅为官方 OpenCV 的 1/10。

---

## 官方公开资源汇总

| 资源 | 地址 | 内容 |
|------|------|------|
| 固件下载中心 | redmine.rock-chips.com/urllist | 预编译固件、烧录工具、Toolchain、Debian/ROS2 镜像 |
| AI SDK | github.com/airockchip | RKNN 全系列工具链与模型 Zoo |
| 开源 Wiki | opensource.rock-chips.com | 老芯片（RK3288/RK3399/RK3328）Linux SDK 文档 |
| GitHub 开源仓 | github.com/rockchip-linux | kernel/u-boot/buildroot 等（注意：2025 年底 mpp 仓因 FFmpeg DMCA 投诉被禁用，媒体处理代码有变动） |
| Toybrick 社区 | t.rock-chips.com | 官方论坛 + Wiki |
| Gitee 文档仓 | gitee.com/rk3576/linux_bsp_docs 等 | BSP 开发文档镜像 |

---

## 选型建议

- **评估/学习**：RV1106 直接用 Luckfox 开源 SDK；RK3588 用 Firefly 或 LubanCat 公开 SDK，均无需申请。
- **量产项目**：走官方商务渠道拿完整 BSP + FAE 支持，并订阅 Redmine 补丁发布。
- **机器视觉方向**：RV1106 + RKNN + opencv-mobile 是成本最低的端侧方案；算力需求高（多路视频/大模型）再上 RK3588（6 TOPS NPU）。

## 相关笔记

- [[12-Resources/00-README|学习资源]]
- [[04-Microcontrollers/00-README|微控制器]]
- [[11-Machine-Vision/000-README|机器视觉]]
