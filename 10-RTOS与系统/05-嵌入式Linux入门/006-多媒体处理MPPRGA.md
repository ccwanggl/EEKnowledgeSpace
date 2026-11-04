---
tags: [embedded-linux, yocto, buildroot, device-tree, embedded]
date-created: 2026-06-15
---

# 多媒体处理（MPP / RGA）

RK3588 内置强大的 VPU（视频处理单元）和 RGA（2D 图形加速）。

## MPP（Media Process Platform）
- 硬件加速视频编解码：8K@60fps H.265/H.264 解码，8K@30fps 编码
- GStreamer 插件：通过 `gst-rkmpi` 使用硬件加速
- FFmpeg 支持：通过 `ffmpeg-rk` 使用 RKMPP 硬件加速

### RGA（2D Raster Graphic Acceleration）
- 硬件加速：图像缩放、旋转、格式转换（NV12/RGB）、裁剪
- 用途：AI 推理前的图像预处理、摄像头数据转换
- 库：`librga`

### 典型视频管线
```
摄像头 (MIPI CSI) → RGA (格式转换) → NPU (AI推理) → RGA (OSD叠加) → HDMI/编码输出
```

---

