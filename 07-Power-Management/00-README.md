---
tags: [index, readme, 07-power-management]
date-created: 2026-06-17
---

# 电源管理（07-Power-Management）

> LDO、DC-DC、电池管理、低功耗设计与热管理。

---

## 从一个任务开始

[[00-Index/03-AI自学任务索引#电源管理：解释 Buck 的开关行为|电源管理：解释 Buck 的开关行为]]。先试做，根据卡点回正文或找 AI 提示，再用变式独立验收。

## 模块导航

- [[07-Power-Management/01-电源管理基础/01-电源管理基础|电源管理基础]]
- [[07-Power-Management/02-DC-DC转换器/02-DC-DC转换器|DC-DC转换器]]
- [[07-Power-Management/03-电源架构设计/03-电源架构设计|电源架构设计]]
- [[07-Power-Management/04-电池管理系统/04-电池管理系统|电池管理系统]]
- [[07-Power-Management/05-低功耗设计/05-低功耗设计|低功耗设计]]

---

## 本目录文件

```dataview
TABLE file.name AS 文件名, date-created AS 创建日期
FROM "07-Power-Management"
WHERE file.name != "00-README"
SORT file.name ASC
```

---

## 推荐学习路径

1. 先浏览本目录下的核心概念文件。
2. 完成相关 [[00-Index/04-练习与复习#按主题找练习和测验|测验题]] 检验理解。
3. 结合 [[01-项目总览]] 中的项目动手实践。
4. 遇到问题时查阅 [[01-调试工具概述|调试工具]] 和 [[02-工具清单|工具清单]]。

---

## 返回上级

- [[00-Index/00-README|知识库首页]]
- [[02-MOC-主题索引|主题索引]]
- [[01-学习路线图|学习路线图]]

---

## 推荐资源

> 以下资源按相关性和学习阶段推荐，与 [[12-Resources/00-README|12-resources]] 中的完整资源列表互为补充。

### 推荐书籍

| 书籍 | 作者 | 级别 | 适用内容 | 获取方式 |
|------|------|------|----------|----------|
| 《Switching Power Supplies A-Z》 | Sanjaya Maniktala | 进阶 | 02-DC-DC转换器（Buck/Boost/拓扑）、03-电源架构设计 | 购买 |
| 《Control Loop Cookbook》 | TI | 进阶 | 02-DC-DC转换器（环路补偿、波特图分析、稳定性） | 免费 PDF |
| 《The Art of Electronics》 | Paul Horowitz & Winfield Hill | 全级别 | 01-电源管理基础（LDO、线性稳压器、开关电源原理） | 购买 |
| 《Signal Integrity and Power Integrity - Simplified》 | Eric Bogatin | 中级 | 03-电源架构设计（电源完整性PI、PDN设计、去耦） | 购买 |
| 《Practical Electronics for Inventors》 | Paul Scherz & Simon Monk | 入门 | 01-电源管理基础（电源章节、基础电路） | 购买 |
| 《Analog Engineer's Pocket Reference》 | TI | 参考 | 01-电源管理基础（公式速查、LDO压差、热计算） | 免费 PDF |

### 推荐视频与课程

| 资源 | 平台 | 特点 | 适用内容 |
|------|------|------|----------|
| Phil's Lab | YouTube | 电源设计实操、控制环路、PCB、测量 | 02-DC-DC转换器、03-电源架构设计 |
| EEVblog | YouTube | 电源评测、电子工程深入讲解、仪器使用 | 01-电源管理基础、综合 |
| TI Precision Labs | TI 官网 | 免费视频，电源、ADC、运放、传感器 | 01-电源管理基础、02-DC-DC转换器 |
| 唐老师讲电赛 | Bilibili | 中文，电源、运放、电子设计竞赛 | 01-电源管理基础、02-DC-DC转换器 |
| 爱上半导体 | Bilibili/YouTube | 中文，硬件原理可视化，MOS管、LDO、开关电源 | 01-电源管理基础（半导体原理、MOS管驱动） |
| MIT OCW: 6.002 Circuits and Electronics | MIT | 经典 MIT 电路与电子学课程 | 01-电源管理基础 |
| Microchip University | Microchip | 官方免费课程，含电池充电管理、电源 | 04-电池管理系统 |

### 推荐博客与网站

| 网站 | 语言 | 特点 | 适用内容 |
|------|------|------|----------|
| AllAboutCircuits | 英文 | 最全面的免费电路教程，含电源设计专栏 | 01-电源管理基础、02-DC-DC转换器 |
| EEWorld（电子工程世界） | 中文 | 国内最大 EE 社区，电源板块活跃 | 综合 |
| Hackaday | 英文 | 每日硬件项目，含电源管理/低功耗项目 | 03-电源架构设计、05-低功耗设计（实践） |
| DeepBlue Embedded | 英文 | 嵌入式教程质量极高，含低功耗设计 | 04-电池管理系统、05-低功耗设计 |
