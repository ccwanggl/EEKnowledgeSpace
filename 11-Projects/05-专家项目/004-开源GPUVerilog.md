---
tags: [projects, expert, advanced, diy, portfolio]
date-created: 2026-06-15
---

# 4. 开源 GPU（Verilog）

## 目标
用 FPGA 实现一个简化但功能完整的图形处理单元（GPU）。

### 硬件
- FPGA：Artix-7 / ECP5 / Zynq
- 显示接口：VGA / HDMI（通过 TMDS）
- 存储：SRAM / DDR

### 技能点
- 图形管线（顶点处理、光栅化、片段着色）
- 流水线设计
- 内存管理
- 驱动开发
- 计算机架构

### 扩展方向
- 支持 3D 变换
- 添加纹理映射
- 与 RISC-V 软核集成

### 项目来源与详细资源

**核心来源**
- Tiny-GPU：<https://github.com/cp024s/Tiny-GPU> — 极简 GPU Verilog 学习项目（学习 GPU 工作原理），含 rtl/（cache、control、core、dispatch、scheduler、top）、测试台和汇编器，docs/ 下有架构与验证文档
- FuryGPU（furygpu.com）— 一人四年从零做的 FPGA GPU：Xilinx Zynq UltraScale+，400 MHz 核心，4 个平铺光栅化器、FP32 前端、纹理单元（线性/双线性 + MIP）、PCIe 2.0 x4、DP/HDMI 输出，Quake 60 FPS；最难的部分是 Windows 驱动和自定义图形 API（FuryGL）
- Project F 的 FPGA 图形/显存系列教程（projectf.io，名称提及）— 2D 光栅化、帧缓冲、TMDS HDMI 编码
- LiteX SoC 构建框架（见 005/006 篇来源）适合把 GPU 挂到软核总线上做演示系统

**关键实现要点**
- 最小 GPU 设计顺序：显存/帧缓冲控制器 → 像素扫描输出（VGA/HDMI TMDS）→ 2D 加速（填充、blit）→ 光栅化 → 纹理 → （远期）shader
- 显示接口先用 VGA（DAC 电阻网络即可），HDMI 需 TMDS 编码 + 高速 IO 约束
- 参考 FuryGPU 的教训：硬件只占一半，驱动和软件栈工作量同样巨大

---

