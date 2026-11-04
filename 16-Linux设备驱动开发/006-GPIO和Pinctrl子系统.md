---
tags: [linux-driver, gpio, pinctrl, interrupt, embedded-linux, rk3588]
date-created: 2026-10-08
aliases: [GPIO驱动, pinctrl, gpiod, 按键中断]
---

# GPIO 和 Pinctrl 子系统

GPIO 是驱动入门的第一块真实硬件。在 Linux 上它不是"读写某个寄存器"那么简单，而是分两层：**pinctrl** 负责管脚配置（复用功能、上下拉、驱动强度），**GPIO 子系统**负责输入输出与中断。先用用户态工具验证硬件，再写内核驱动，是这块外设的标准节奏。

## 两层各管什么

| 层 | 职责 | RK3588 上的实现 |
|----|------|----------------|
| pinctrl | 每个管脚"是谁"：复用到 GPIO/SPI/UART…、上拉/下拉/悬空、驱动强度 | `pinctrl-rockchip` 驱动，由 dts 的 `rockchip,pins` 描述 |
| GPIO | 管脚"在干嘛"：输入读电平、输出写电平、边沿/电平中断 | GPIO 框架，`gpio4` 等 gpiochip 暴露给用户态和内核 |

思路差异值得注意：MCU 上 GPIO 配置是往寄存器写值（见 [[04-Microcontrollers/02-STM32系列/006-GPIO、EXTI与引脚复用|GPIO、EXTI 与引脚复用]]），Linux 上配置写在设备树里由 pinctrl 驱动统一执行，驱动代码拿到的是**已配置好的描述符**，只管语义操作。

## 设备树写法

管脚配置（pinctrl 节点，定义在 dtsi 的 `&pinctrl` 下扩充）：

```dts
&pinctrl {
    my_btnled_pins: my-btnled-pins {
        rockchip,pins =
            /*  <bank  引脚     复用功能        上下拉>   bank 0~4 对应 GPIO0~4 */
            <4 RK_PB1 RK_FUNC_GPIO &pcfg_pull_none>,   /* LED 输出，不上拉 */
            <4 RK_PB2 RK_FUNC_GPIO &pcfg_pull_up>;     /* 按键输入，上拉 */
    };
};
```

消费节点（声明用途 + 关联管脚配置）：

```dts
/ {
    btnled {
        compatible = "myvendor,btnled";
        pinctrl-names = "default";               /* 名字固定为 default（可有 idle/sleep 等多状态） */
        pinctrl-0 = <&my_btnled_pins>;
        led-gpios    = <&gpio4 RK_PB1 GPIO_ACTIVE_HIGH>;
        button-gpios = <&gpio4 RK_PB2 GPIO_ACTIVE_LOW>;
    };
};
```

三个要点：

- `RK_FUNC_GPIO` 把管脚复用到 GPIO；若是 `RK_FUNC_1`/`RK_FUNC_2` 则是复用到某外设信号，此时该管脚由对应外设驱动接管，不能再当 GPIO 用——**复用冲突是最常见的管脚问题**（引脚被别的功能占住，GPIO 操作无效）。
- `GPIO_ACTIVE_LOW` 声明"低电平为真"。有了这个语义，`gpiod_set_value(led, 1)` 会自动输出低电平——电平反相逻辑从驱动代码里消失，只在 dts 声明一次。
- `&gpio4` 的 bank 编号与 `rockchip,pins` 的第一个数一致；RK3588 共 GPIO0~GPIO4 五组。

## 内核态代码：按键中断 + LED 输出

```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/gpio/consumer.h>
#include <linux/interrupt.h>

struct btnled {
    struct gpio_desc *led;
    struct gpio_desc *btn;
    int irq;
    unsigned int press_count;
};

static irqreturn_t btn_thread_fn(int irq, void *data)
{
    struct btnled *priv = data;
    bool pressed = !gpiod_get_value(priv->btn);   /* ACTIVE_LOW：读到 0 才是"按下" */

    if (pressed) {
        priv->press_count++;
        gpiod_set_value(priv->led, (priv->press_count & 1));   /* 每按一次翻转 LED */
        pr_info("btnled: pressed %u times\n", priv->press_count);
    }
    return IRQ_HANDLED;
}

static int btnled_probe(struct platform_device *pdev)
{
    struct device *dev = &pdev->dev;
    struct btnled *priv;
    int irq, ret;

    priv = devm_kzalloc(dev, sizeof(*priv), GFP_KERNEL);
    if (!priv)
        return -ENOMEM;

    priv->led = devm_gpiod_get(dev, "led", GPIOD_OUT_LOW);
    if (IS_ERR(priv->led))
        return PTR_ERR(priv->led);

    priv->btn = devm_gpiod_get(dev, "button", GPIOD_IN);
    if (IS_ERR(priv->btn))
        return PTR_ERR(priv->btn);

    irq = gpiod_to_irq(priv->btn);                /* GPIO → 中断号 */
    if (irq < 0)
        return irq;

    ret = devm_request_threaded_irq(dev, irq,
                                    NULL,           /* 主处理函数：NULL → 全部在线程里执行 */
                                    btn_thread_fn,
                                    IRQF_TRIGGER_FALLING | IRQF_ONESHOT,
                                    "mybtn", priv);
    if (ret)
        return ret;

    priv->irq = irq;
    platform_set_drvdata(pdev, priv);
    dev_info(dev, "btnled ready, irq=%d\n", irq);
    return 0;
}

static int btnled_remove(struct platform_device *pdev)
{
    return 0;   /* devm 资源自动回收 */
}

static const struct of_device_id btnled_of_match[] = {
    { .compatible = "myvendor,btnled" },
    { }
};
MODULE_DEVICE_TABLE(of, btnled_of_match);

static struct platform_driver btnled_driver = {
    .probe  = btnled_probe,
    .remove = btnled_remove,
    .driver = {
        .name = "btnled",
        .of_match_table = btnled_of_match,
    },
};
module_platform_driver(btnled_driver);
MODULE_LICENSE("GPL");
```

两个设计点：

- **threaded IRQ**：硬件中断上下文不能睡眠，按键消抖需要睡眠——`devm_request_threaded_irq` 把实际处理放到内核线程（可被抢占、可睡眠）。`IRQF_ONESHOT` 在线程处理完之前屏蔽该中断线，防止抖动重入。电平触发型器件（如某些中断脚）可用主处理函数返回 `IRQ_WAKE_THREAD` 的拆分写法。中断体系的完整理论见 [[005-中断体系开发]]。
- **中断触发沿与有效电平的对应**：低有效按键平时为高，按下变低 → 触发沿选 `IRQF_TRIGGER_FALLING`。选错沿的典型症状是按一次记两次数（沿抖动）或完全没反应。

## 用户态对照：libgpiod

写内核驱动之前，先用 libgpiod 验证管脚接线与电平语义（也是 shell 脚本自动化的标准工具）：

```bash
sudo gpiodetect                      # 列出所有 gpiochip
sudo gpioinfo gpiochip4              # 查看 GPIO4 每个引脚的占用与方向
sudo gpioget gpiochip4 9             # 读 GPIO4_B1（RK 编号 RK_PB1 = 8+1 = 9）
sudo gpioset gpiochip4 9=1           # 输出高
sudo gpiomon --falling-edge gpiochip4 10   # 监视 GPIO4_B2 下降沿（按键）
```

RK 引脚宏换算：`RK_PB1` = bank 内编号 `8*1 + 1 = 9`。C 程序用 `gpiod_chip_open_by_name("gpiochip4")` + `gpiod_chip_get_line()` + `gpiod_line_request_input/output()` 一套描述符 API。

**选型判据**：管脚由设备驱动管理、需要中断/精确时序 → 内核驱动；一次性配置、脚本自动化、原型验证 → libgpiod；两者不要同时占用同一管脚（gpiod 请求机制会拒绝，见下）。

## 常见陷阱

- **请求 GPIO 失败 `-EBUSY`**：管脚已被其它驱动（含 gpio-sysfs 遗留占用）申请。`gpioinfo` 看占用者，`/sys/kernel/debug/pinctrl` 看复用状态。
- **`gpiod_set_value` 没效果**：多半是 pinctrl 没配（管脚还复用在外设功能上）或 bank 号写错，GPIO 框架报错通常在 dmesg。
- **按键中断风暴**：消抖没做或触发沿选错；软件消抖（线程里 `msleep(10)` 后复核电平）是底线，硬件消抖（RC/施密特）更稳。
- **`/sys/class/gpio` 老接口已废弃**：`echo N > export` 那套（integer GPIO 编号）在新内核逐步移除，新代码一律 gpiod。
- **`gpiod_to_irq` 失败**：不是所有 GPIO 都能产生中断，RK3588 全部 GPIO 支持，但复用不对时返回负值，记得检查。

## 检查清单

- pinctrl 的 bank/引脚/复用/上下拉四个字段逐一核对原理图。
- `pinctrl-names`/`pinctrl-0` 配对，消费节点管脚名（`led-gpios`）与 `devm_gpiod_get(dev, "led", ...)` 的 con_id 对应。
- 中断号、触发沿、有效电平三者的逻辑一致性（低有效 + 上拉 → 下降沿）。
- 用户态验证先行：gpiodetect/gpioinfo/gpioget 通过后再写内核代码。

## 实验

1. 按上图接 LED（GPIO4_B1 串 1kΩ 限流电阻）与按键（GPIO4_B2 对地，用上拉）。
2. `gpioinfo`/`gpioget` 验证电平语义，先跑通 `gpiomon` 看按键波形。
3. 加载上面的驱动，`cat /proc/interrupts | grep mybtn` 确认中断注册，按键观察计数与 LED 翻转；示波器/逻辑分析仪对照中断触发点。

## 继续学习

- [[005-中断体系开发]] — GPIO 中断的理论根基
- [[007-主流外设驱动]] — GPIO 之后最常见的外设驱动
- [[04-Microcontrollers/02-STM32系列/006-GPIO、EXTI与引脚复用|GPIO、EXTI 与引脚复用]] — 同一件事的 MCU 视角
- [[008-驱动调试排错]] — dynamic debug 与 ftrace 定位中断问题
