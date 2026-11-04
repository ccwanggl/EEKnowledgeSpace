---
tags: [embedded-linux, yocto, buildroot, device-tree, embedded]
date-created: 2026-06-15
---

# RKNN 与 NPU 开发

RK3588 集成的 6 TOPS NPU 是其核心优势之一，可用于边缘 AI 推理。

## RKNN 工具链

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| **RKNN-Toolkit2** | 模型转换（ONNX/TensorFlow → RKNN）、精度分析、性能评估 | 开发 PC 上 |
| **RKNPU2 Runtime** | 设备端 C/C++ 推理库 | 部署到 RK3588 |
| **RKNN-Toolkit-Lite2** | 设备端 Python API | 快速原型验证 |
| **librga** | 2D 图形加速（图像缩放、格式转换）| 预处理/后处理 |
| **RKLLM** | 大语言模型转换与部署 | 边缘 LLM |

### RKNN 开发四种模式（速查）

> 根据实际部署场景，RKNN 开发有四种典型工作模式：

| 模式 | 开发环境 | 运行环境 | 适用场景 | 特点 |
|------|----------|----------|----------|------|
| **① PC 模拟** | PC（Ubuntu 22.04 x86） | PC 模拟 NPU | 模型验证、精度分析 | 无需开发板，快速迭代 |
| **② PC 控板** | PC + RKNN-Toolkit2 | 连接 RK3588 板端 NPU | 联调测试 | 模型在 PC 转换，推理在板端 |
| **③ 板端 C++** | PC 交叉编译 | RK3588 板端运行 | 产品化部署 | 性能最高，需交叉编译环境 |
| **④ 板端 Python** | RK3588 板端（RKNN-Lite2） | RK3588 板端运行 | 快速原型、算法验证 | 开发最便捷，适合调试 |

**典型开发流程**：
```
PC端：Ubuntu 22.04 + RKNN-Toolkit2
  ↓
模型训练（PyTorch）→ 导出 ONNX
  ↓
RKNN-Toolkit2 转换 → .rknn 文件
  ↓
板端：RKNN-Lite2（Python）快速验证 或 C++ 交叉编译部署
```

### 模型部署流程
```
训练好的模型 (PyTorch/TensorFlow)
    ↓
导出为 ONNX / TensorFlow Lite
    ↓
RKNN-Toolkit2 转换 → .rknn 模型
    ↓
RKNPU2 Runtime 在 RK3588 上推理
```

### 支持的模型类型
- **目标检测**：YOLOv5/v8/v11、RT-DETR
- **图像分割**：SAM（Segment Anything）
- **语音识别**：Whisper
- **多模态**：CLIP
- **大语言模型**：TinyLlama 1.1B（10-15 token/s）、Qwen2 0.5B

### NPU 性能监控
```bash
cat /sys/kernel/debug/rknpu/load    # 查看 NPU 负载
```

### 性能优化技巧
1. **多线程推理**：rknn-multi-threaded 可提升 40% 性能
2. **零拷贝**：使用 RGA 进行图像预处理，避免 CPU 复制
3. **INT8 量化**：相比 FP16 推理速度提升 2-3 倍
4. **批量推理**：一次处理多帧，提高 NPU 利用率

---

