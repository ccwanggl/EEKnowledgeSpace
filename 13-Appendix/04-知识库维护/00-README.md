---
tags: [maintenance, index]
date-created: 2026-07-14
---

# 知识库维护

## 自动检查

在知识库根目录运行：

```powershell
python "13-Appendix/04-知识库维护/validate_vault.py"
python "13-Appendix/04-知识库维护/validate_code_examples.py"
```

检查范围包括：

- 正文 WikiLink 的缺失、歧义和目录伪链接。
- 本地图片引用。
- Markdown 代码围栏和显示公式标记。
- 一级标题数量和标题层级跳跃。
- 标记为 `python`、`py` 或 `python3` 的代码块语法。

脚本忽略 `.obsidian`、`.trash`、`copilot`、`Clippings` 和 `Excalidraw`，这些目录不是正式知识正文。

同目录下的 `normalize_*`、`repair_missing_links.py` 和 `build_readme_navigation.py` 是本次重构使用的迁移脚本，保留用于审计和复现，不作为日常编辑命令。日常检查运行 `validate_vault.py` 和 `validate_code_examples.py`；后者只解析 Python 语法，不执行笔记中的代码。

## 编辑约定

- 每篇正式笔记只保留一个一级标题。
- 跨目录链接使用库根目录相对路径，并提供自然的显示名称。
- 只有已有目标笔记的概念才使用 WikiLink；普通术语不创建空链接。
- 公式必须写明适用条件、符号定义和单位。
- 外部图片需要来源说明，关键图优先本地保存，避免依赖热链。
- 主题总览负责学习顺序和静态入口，Dataview 只作为辅助视图。

## 历史与备份

- 重构前完整备份：`E:/EEDevSpace/backups/EEKnowledgeSpace-before-restructure-20260714.zip`
- 原总首页：[[00-Index/99-历史总索引归档|历史总索引归档]]
