# 变更记录

格式遵循 [Keep a Changelog 1.1.0](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/)。

## v1.0.0（2026-11-15）

首个可用版本。

| 改动 | 为什么 | 影响文件 |
|---|---|---|
| 建立自研编排层，只调官方 `gh` / REST API | 明确不是二创，避免继承第三方协议，保留商业化空间 | `SKILL.md`、`README.md`、`LICENSE` |
| 凭据零落盘，授权状态交给 `gh auth status` | 防止 token 进入 git 历史（git 历史里的密钥删不干净） | `scripts/gh_repo_guard.py`、`.gitignore` |
| 落地五条治理动作 check / status / preflight / audit / release | 把「什么时候推、推前查什么、怎么退」固化成可跑命令 | `scripts/gh_repo_guard.py` |
| README 写全安装、回退、常见问题自查 | 别人看完不用再问作者 | `README.md`、`QUICKSTART.md` |
| tag + GitHub Release + 版本索引 | 每个里程碑页面上看得到、点得开、下得了整包 | 本文件、README 第六节 |


## v1.1.0（2026-11-15）

对标 GitHub 生态同类能力后的增强（调研结论：无同层级完整竞品，学到三个单点优点）。

| 改动 | 为什么 | 影响文件 |
|---|---|---|
| frontmatter 加 Examples 触发例句 | 学 issue-crafter：例句让 Agent 端准确识别意图，减少误触发 | `SKILL.md` |
| 新增渐进披露层 references/details.md | 学 wshobson/agents：SKILL.md 只留判断，细节按需读，上下文成本降一半 | `references/details.md`、`SKILL.md` |
| CHANGELOG 声明 Keep a Changelog + SemVer | 学 changelog-automation：格式对齐业界标准，别人看得懂 | `CHANGELOG.md` |
