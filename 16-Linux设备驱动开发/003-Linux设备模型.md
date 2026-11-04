---
tags: [linux-driver, device-model, platform-bus, sysfs, embedded-linux, rk3588]
date-created: 2026-10-08
aliases: [Linux设备模型, kobject, platform总线, uevent, bus-device-driver]
---

# Linux 设备模型

[[002-字符设备驱动开发|字符设备]]回答了"用户态怎么访问驱动"，本篇回答"内核如何组织成千上万的设备与驱动"：kobject/sysfs 是地基，bus-device-driver 是骨架，platform 总线 + 设备树匹配是嵌入式驱动的主干道。

## 模型的三层地基

- **kobject**：内核对象基类，提供引用计数、`release()` 析构、uevent 通知。几乎所有设备/驱动/总线结构都内嵌 kobject。
- **kset**：kobject 的集合，对应 sysfs 的一级目录，如 `/sys/devices/platform/`。
- **sysfs**：内核对象树的文件系统视图。用户态在 `/sys` 里看到的目录层级就是设备模型的直接投影：

```
/sys/bus/platform/          总线视图：drivers/ 与 devices/ 互为镜像
/sys/devices/platform/      物理层级：设备挂在哪条总线上
/sys/class/                 功能视图：按能力分类（leds、input、tty…）
```

写驱动时可以直接在板上对照这三个目录游走，建立直观感受。uevent 是模型对外的广播：设备出现/消失时内核发 uevent，`udev`/`mdev` 收到后创建设备节点、执行规则——[[002-字符设备驱动开发|字符设备]]的 `/dev/mychar` 节点、模块自动加载都靠它。

## 总线、设备、驱动

三者关系是模型的核心：

- **bus_type**（如 `platform_bus_type`）：定义 `.match()` 匹配规则和 `.probe()` 调用时机；
- **device**：描述"有什么硬件"，由谁注册无所谓（传统手工 `platform_device_register`，嵌入式里多由设备树自动实例化）；
- **driver**：描述"怎么驱动"，注册时遍历总线上已有设备逐个尝试匹配。

匹配成功后总线调用驱动的 `probe()`，设备移除时调用 `remove()`。**驱动代码不感知板级细节**——这是设备模型配合设备树要达到的效果。嵌入式里这条总线几乎总是 platform 总线（片上外设与逻辑设备的集合）。

## 匹配链路（嵌入式主路径）

```
.dts 节点 (compatible = "myvendor,mycore")
    → 启动时 unflatten dtb，为节点创建 platform_device
        → platform 总线 .match()：比对驱动 of_match_table 与 compatible
            → 命中 → 调用 probe(pdev)，资源交接
```

一个驱动可服务多个板级实例（表内多个 compatible 或命中多个节点）；一个节点只交给一个驱动。驱动侧的对应物是这张表：

```c
static const struct of_device_id mycore_of_match[] = {
    { .compatible = "myvendor,mycore" },
    { }                              /* 空哨兵必须保留 */
};
MODULE_DEVICE_TABLE(of, mycore_of_match);   /* 让 .ko 携带别名，modprobe 可按 compatible 自动加载 */
```

## probe 生命周期与资源获取

probe 是驱动的"收货环节"，从设备树取五类资源：

| 资源 | 取法 | DT 属性（写法见 [[004-设备树开发]]） |
|------|------|---------|
| 普通属性 | `device_property_read_u32/string/u32_array` | `timeout-ms = <200>` 等自定义键 |
| 寄存器 | `platform_get_resource(pdev, IORESOURCE_MEM, 0)` + `devm_ioremap_resource` | `reg = <0x… 0x…>` |
| 中断 | `platform_get_irq(pdev, 0)` / `platform_get_irq_byname` | `interrupts = <…>` + `interrupt-names` |
| GPIO | `devm_gpiod_get(dev, "<name>", …)` | `<name>-gpios = <&gpioX …>` |
| 时钟/电源 | `devm_clk_get` / `devm_regulator_get` | `clocks` + `clock-names`、`<name>-supply` |

`devm_*` 前缀的函数把资源挂到设备生命周期上：probe 失败或 remove 时由内核自动回收，驱动不必写释放代码，这是现代驱动的默认写法。与之互补的约定是**资源唯一所有权**：同一外设的配置只能由一个层拥有（与 [[04-Microcontrollers/02-STM32系列/010-HAL、LL、寄存器与驱动分层|MCU 的驱动分层]]思想一致）。

`-EPROBE_DEFER`：probe 拿不到资源时**不要硬失败**。若依赖的时钟/电源/regulator 来自尚未加载的驱动，返回 `-EPROBE_DEFER`，内核把设备挂到延后队列待依赖就绪后重试；`dev_err_probe()` 会对该值自动降级为 debug 日志（它不是真错误）。症状对照：节点存在、驱动加载，却没有任何 probe 日志、设备文件未生成——八成在这里。

## 完整代码：platform 驱动

```c
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/property.h>
#include <linux/gpio/consumer.h>
#include <linux/clk.h>
#include <linux/regulator/consumer.h>
#include <linux/device.h>

struct mycore {
    struct gpio_desc *reset;
    struct clk *clk;
    struct regulator *power;
    u32 timeout_ms;
};

/* ---- sysfs 属性：把驱动内部状态暴露给用户态 ---- */

static ssize_t timeout_show(struct device *dev, struct device_attribute *attr,
                            char *buf)
{
    struct mycore *priv = dev_get_drvdata(dev);
    return sysfs_emit(buf, "%u\n", priv->timeout_ms);
}

static ssize_t timeout_store(struct device *dev, struct device_attribute *attr,
                             const char *buf, size_t count)
{
    struct mycore *priv = dev_get_drvdata(dev);
    u32 val;

    if (kstrtou32(buf, 10, &val))
        return -EINVAL;
    priv->timeout_ms = val;
    return count;
}
static DEVICE_ATTR_RW(timeout);

/* ---- probe / remove ---- */

static int mycore_probe(struct platform_device *pdev)
{
    struct device *dev = &pdev->dev;
    struct mycore *priv;

    priv = devm_kzalloc(dev, sizeof(*priv), GFP_KERNEL);
    if (!priv)
        return -ENOMEM;

    if (device_property_read_u32(dev, "timeout-ms", &priv->timeout_ms))
        priv->timeout_ms = 100;                    /* dts 没写就给默认值 */

    priv->reset = devm_gpiod_get(dev, "reset", GPIOD_OUT_HIGH);
    if (IS_ERR(priv->reset))
        return dev_err_probe(dev, PTR_ERR(priv->reset), "no reset gpio\n");

    priv->clk = devm_clk_get(dev, "core");
    if (IS_ERR(priv->clk))
        return dev_err_probe(dev, PTR_ERR(priv->clk), "no core clock\n");
    clk_prepare_enable(priv->clk);

    priv->power = devm_regulator_get(dev, "power");
    if (IS_ERR(priv->power))
        return dev_err_probe(dev, PTR_ERR(priv->power), "no power regulator\n");
    regulator_enable(priv->power);

    dev_info(dev, "probed: timeout=%u ms clk=%lu Hz\n",
             priv->timeout_ms, clk_get_rate(priv->clk));

    platform_set_drvdata(pdev, priv);
    return device_create_file(dev, &dev_attr_timeout);
}

static int mycore_remove(struct platform_device *pdev)
{
    device_remove_file(&pdev->dev, &dev_attr_timeout);
    return 0;
}

static const struct of_device_id mycore_of_match[] = {
    { .compatible = "myvendor,mycore" },
    { }
};
MODULE_DEVICE_TABLE(of, mycore_of_match);

static struct platform_driver mycore_driver = {
    .probe  = mycore_probe,
    .remove = mycore_remove,
    .driver = {
        .name           = "mycore",
        .of_match_table = mycore_of_match,
    },
};
module_platform_driver(mycore_driver);   /* 一个宏完成注册与注销 */

MODULE_LICENSE("GPL");
```

要点：

- 申请/注册顺序 = 释放的逆序，任一步失败回滚已获资源（devm 管释放，你管不再使用）。
- sysfs 属性的约定：`show` 返回写入 buf 的长度（用 `sysfs_emit`，自动保证缓冲安全）；`store` 校验输入成功后返回 `count`。
- `remove` 返回值随版本变化：6.11 之前为 `int remove()`，6.11 起为 `void remove()`，按目标内核选择。
- 把业务代码塞进 probe 是反模式：probe 只做资源获取与最小初始化，耗时校准、固件加载放 deferred work。

## 常见陷阱

- **compatible 不一致**：dts 与驱动表差一个字符，表现为"模块加载了但 probe 从未被调用"。
- **`status = "disabled"`**：上游 dtsi 默认关闭的外设，板级 dts 必须显式 `"okay"`。
- **资源泄漏与重复申请**：非 devm 资源（`request_irq` 的老式用法、`ioremap`）必须在错误路径与 remove 里配对释放。
- **sysfs 写入不校验**：用户态会写入任何字节，`store` 必须验证。

## 检查清单

- `of_match_table` 空哨兵结尾，`MODULE_DEVICE_TABLE` 不省略。
- 所有资源获取失败路径正确回滚；依赖未就绪返回 `-EPROBE_DEFER`。
- sysfs 属性 show/store 成对、有边界校验。

## 实验

1. 按 [[004-设备树开发]] 的绑定写出 `myvendor,mycore` 节点（dts 或 overlay），编译部署后 `dmesg | grep mycore` 确认 probe 日志。
2. `echo 500 > /sys/bus/platform/devices/mycore/.../timeout` 再 `cat` 回读。
3. 把 `compatible` 故意改错，观察"加载正常但 probe 不执行"，用 `dmesg` 与 `/sys/bus/platform/devices/` 定位。

## 继续学习

- [[004-设备树开发]] — 匹配链路的硬件描述侧：绑定、overlay、调试
- [[005-中断体系开发]] — probe 资源清单里中断的展开
