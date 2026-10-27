# MobiSys 论文

唯一主文档是 `main.tex`。在 Overleaf 中选择它作为 Main document，使用 pdfLaTeX 编译。

| 位置 | 内容 |
|---|---|
| `main.tex` | 标题、摘要和章节入口 |
| `mobisys-01` 至 `mobisys-09` | 当前正文九章 |
| `mobisys-appendix.tex` | 当前附录 |
| `mobisys-references.tex` | 当前参考文献 |
| `images/` | 正文实际引用的三张图 |
| `scripts/` | 结果图生成脚本 |
| `archive/` | 旧稿、候选图、旧说明及原始 ACM 示例（如存在） |
| `exports/` | 按日期保存的历史 PDF 和源码包，仅本地保留 |
| `build/` | 本地编译产物和图片预览，不提交 GitHub |

当前内容以源码及编辑器自动生成的预览为准。`exports/2026-10-21/` 中的初稿早于后续修改，属于历史快照。

本地使用 `latexmk main.tex` 时，`.latexmkrc` 会将产物放入 `build/`。编辑器预览由内置编译器管理。结果图脚本位于 `scripts/make_draft_figures.py`，运行环境需安装 matplotlib；它从已有汇总数值绘图，PDF 写入 `images/`，PNG 预览写入 `build/figure-previews/`。

GitHub 和 Overleaf 需要显式同步。更新前先拉取另一端的修改；本地文件不会通过聊天自动同步。GitHub 上保留 `acmart.cls` 供 Overleaf 使用；其余原始模板文件归档在 `archive/acm-template/`。

实验原始交接材料位于本地项目上一级的 `paper_notes/`，参考论文位于 `reference/`。它们不属于论文编译依赖。
