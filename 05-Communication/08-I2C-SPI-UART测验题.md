---
tags: [quiz, communication, uart, spi, i2c]
date-created: 2026-11-19
---

# I2C、SPI 与 UART 测验

先独立画图，再展开核对。遇到卡点时，用 [[00-Index/03-AI自学任务索引#通信协议：读出一帧 UART|串行通信自学任务]]中的提示方式，让 AI 先追问一个判断步骤。

## 1. UART 位序与时长

9600 baud、8N1、逻辑电平空闲为高，发送 0xA6。按时间顺序写出起始位、数据位和停止位，估算单帧时长。把波特率翻倍后，哪些结果变化？

<details><summary>核对</summary>

起始位为 0，数据低位先发，依次是 0、1、1、0、0、1、0、1，停止位为 1。单帧 10 位，约 1.042 ms。波特率翻倍后位序不变，时间减半。[[05-Communication/02-I2C-SPI-UART/002-UART异步串行通信|UART]]

</details>

## 2. SPI 时钟边沿

SPI 使用模式 0。标出片选有效后 SCK 的空闲电平、第一个采样边沿和数据更新边沿。示波图显示接收端配置成模式 1，最先应核对什么？

<details><summary>核对</summary>

模式 0 的 SCK 空闲为低，首个上升沿采样，下降沿更新后续位。检查收发两端对 CPOL、CPHA 的定义和实际数据稳定区间。[[05-Communication/02-I2C-SPI-UART/003-SPI同步串行接口|SPI]]

</details>

## 3. I2C 应答与排查

I2C 主机发送地址字节后，第九个时钟高电平期间 SDA 仍为高。按协议如何解释？列两个可以区分的原因和对应检查。

<details><summary>核对</summary>

这是 NACK。可检查发送的 7 位地址是否和器件配置相符，再查器件供电、复位或当前是否有应答条件。用波形核对 SDA 是否被释放、地址字节和第九个时钟的位置。[[05-Communication/02-I2C-SPI-UART/004-I2C总线与多设备仲裁|I2C]]

</details>
