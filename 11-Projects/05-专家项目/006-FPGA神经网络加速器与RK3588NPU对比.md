---
tags: [projects, expert, advanced, diy, portfolio]
date-created: 2026-06-15
---

# 6. FPGA 神经网络加速器（与 RK3588 NPU 对比学习）

## 目标
在 FPGA 上实现一个 CNN 推理加速器，并对比理解 FPGA 与专用 NPU（如 RK3588）在 AI 推理上的差异和适用场景。

### 硬件方案 A：FPGA 实现
- **FPGA**：Zynq / Artix-7 / ECP5
- **摄像头**：OV5640 / OV2640
- **显示**：LCD / HDMI
- **存储**：SRAM / DDR

### 硬件方案 B：RK3588 NPU 实现（对比参考）
- **主控**：RK3588（香橙派 5 / ROCK 5B）
- **摄像头**：MIPI CSI 摄像头模组
- **NPU**：6 TOPS INT8，支持 YOLOv8、ResNet 等
- **工具链**：RKNN-Toolkit2 + RKNPU2

### 技能点
- CNN 模型结构与量化原理（INT8/FP16）
- FPGA 端：卷积加速器设计（并行乘加阵列、Winograd 变换）
- RK3588 端：RKNN 模型转换、RGA 预处理、多线程推理优化
- AXI 总线 / AXI Stream 数据流设计（FPGA）
- 软硬件协同设计（FPGA 软核 + 加速器 或 RK3588 CPU + NPU）
- 性能对比：FPS、功耗、延迟、开发周期

### 对比分析维度
| 维度 | FPGA 加速器 | RK3588 NPU |
|------|-------------|------------|
| **灵活性** | 极高，可定制任意算子 | 固定算子支持，需适配 |
| **性能** | 取决于 FPGA 资源，通常较低 | 6 TOPS，优化后可达高 FPS |
| **功耗** | 较高（5-15W） | 较低（整机 5-10W） |
| **开发周期** | 长（数月） | 短（数天，模型转换即可） |
| **成本** | 开发板 $100-500 | 开发板 ¥500-900 |
| **适用** | 研究、定制算子、低延迟 | 产品化、快速部署、边缘 AI |

### 扩展方向
- 在 RK3588 上实现相同网络，对比端到端性能
- 视频流实时处理（GStreamer + RGA + NPU）
- 与 RISC-V 软核集成（FPGA 端）或 RKLLM 边缘 LLM（RK3588 端）
- 多模型流水线：检测 + 跟踪 + 识别

### 项目来源与详细资源

**核心来源**
- hls4ml 官方仓库：<https://github.com/fastmachinelearning/hls4ml> — Keras/PyTorch/ONNX → HLS C++ → Vivado/Vitis HLS 综合为 RTL，专注超低延迟推理（CERN L1 触发背景，微秒级），文档 <https://fastmachinelearning.org/hls4ml/>，教程 notebooks 在 hls4ml-tutorial 仓库，`pip install hls4ml`
- FINN（AMD/Xilinx 开源）：<https://github.com/Xilinx/FINN> — 量化神经网络（Brevitas/QONNX 训练）→ dataflow 架构编译器，Docker 运行，配套 finn-examples 预置示例
- 两工具对比论文（MLSys 2022）：<https://cds.cern.ch/record/2826586/files/2206.11791.pdf> — 同平台对比 hls4ml 与 FINN 的资源/延迟/能耗取舍
- RK3588 端对照部署：RKNN-Toolkit2 + rknn_model_zoo（见 003 篇来源），YOLOv8 官方 demo 含模型转换和 C 推理全链路

**关键实现要点**
- FPGA 流：训练（QKeras/Brevitas 量化感知训练）→ 编译（hls4ml/FINN）→ HLS 综合 → IP 集成 → 上板
- 资源-延迟权衡核心参数：量化位宽（1–12 bit）、ReuseFactor（并行度）、FIFO 深度（dataflow 平衡）
- 公平对比实验：同一网络分别部署 FPGA 加速器和 RK3588 NPU，测量端到端延迟/功耗/FPS

---

