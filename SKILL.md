---
name: github-repo-agent-public
description: |
  通用版 GitHub 仓库治理 Agent。把「什么时候推、推之前查什么、怎么退回去」固化成可跑的守卫，覆盖仓情盘点、命名与描述规范、推送前四查、tag/Release 历史版本与回退。只调官方 gh CLI 与 REST API，凭据零落盘。
  Examples:
    - "盘一下我的仓库，看看哪些描述还没写成三段式"
    - "我改完代码了，推之前帮我查一下"
    - "看看哪些仓缺 Release，帮我补上"
    - "帮我发个版本 v1.1.0"
    - "GitHub 仓库整理：名字、描述、topics 都过一遍"
    - "我是新手，从零开始帮我弄好 GitHub 环境"
agent_created: true
---

# github-repo-agent-public · GitHub 仓库治理守卫（通用版）

一句话定位：**命令谁都会敲，值钱的是知道什么时候不该敲。**

## 这不是二创，先说清楚

本技能没有复制任何第三方 skill 或开源项目的代码，只**调用**官方 `gh` CLI 与 GitHub REST API，外面套一层自己的判断逻辑。
「基于已有作品改编」才叫二创，才要继承上游协议（AGPL / CC BY-NC-SA 一类，会直接堵死商业化）；
调用官方工具是**集成**，不继承它的 MIT。真正属于作者资产的是下面这套治理规矩，不是命令。
所以本仓按自研资产立 LICENSE，也不要把它塞进「第三方二创件」目录。

## 铁律（不可绕过）

1. **凭据零落盘**。不读、不存、不打印任何 token / 密码 / 私钥。授权状态只问 `gh auth status`；没授权就引导设备码流程 `gh auth login --web --git-protocol https --skip-ssh-key`，让账号主人自己在浏览器点确认。`.gitignore` 必须拦 `.env` / `*.pem` / `*.token`。
2. **通道只用 https + gh 设备码**。不配 SSH 私钥——SSH 只能 push，建库 / 改设置 / 删库都做不了，而且把私钥交给 Agent 等于把账号交出去。
3. **不擅自打 tag、不擅自升版本号**。里程碑由人决定；打 tag 必须同时建 GitHub Release、补 README 版本索引与回退命令。
4. **推前四查**：https 通道 / 工作区干净 / diff 里无密钥 / 远端 HEAD 可快进。有分叉先 `git fetch` + `git pull --ff-only`，**绝不 `--force`、绝不 `--no-verify`**。
5. **推后校验远端 HEAD 与本地一致**，不留「本地已改、线上还旧」的悬空状态。
6. **删除类动作永远列清单 + 二次确认**。删库不可逆，先 `gh api repos/<owner>/<repo>/tarball` 归档并 `gzip -t` 校验。
7. **fork 不套自建命名模板**。给上游项目贴自己的受众后缀，等于把别人的项目标成自己的版本；fork 走「保留原名 + 三段式描述写明上游 + topics 标注」。
8. **盘点必须看全量**：用 `/user/repos?affiliation=owner`，不要用 `/users/<name>/repos`（只返回 public，会漏掉一半仓库）。

## 治理动作（都能直接跑）

| 想做什么 | 命令 |
|---|---|
| 零基础环境自检（缺哪步给哪步命令） | `python3 scripts/gh_repo_guard.py onboard` |
| 检查授权与通道 | `python3 scripts/gh_repo_guard.py check` |
| 盘点全部仓 + 规范达标 | `python3 scripts/gh_repo_guard.py status` |
| 推前四查 | `python3 scripts/gh_repo_guard.py preflight <本地仓路径>` |
| 查 tag / Release 缺口 | `python3 scripts/gh_repo_guard.py audit` |
| 发里程碑版本 | `python3 scripts/gh_repo_guard.py release <路径> --tag vX.Y.Z --notes "..." --confirm` |

`release` 不加 `--confirm` 会拒绝执行，这是故意的。面向完全没用过 GitHub 的用户，引导走 `BEGINNER-GUIDE.md` 与 `onboard`：先注册（建议 Gmail 当注册邮箱）、再装 git / gh、再设备码授权。**授权默认管理档**（含 `delete_repo`，建改删一次到位，定位是完整仓库治理）；确定不要删库能力的用户可退日常档。删除护栏不随档位放开：列清单、备份、亲口确认。

## 深入细节（渐进披露）

本文件只保留判断与铁律。详细的命令输出解读、FAIL 处理矩阵、Git Data API 兜底步骤、回退方案选择，都在 `references/details.md` —— 当上表命令的输出你不知道怎么处理时，去读那个文件。

## 三层结构（为什么这不只是套壳）

1. **集成层**：`gh` CLI / REST API，负责跟 GitHub 说话。谁都能调。
2. **编排层**：把顺序固化——盘点 → 命名 → 描述 → 推前四查 → 推送 → 校验 → 打 tag / 建 Release → 写版本索引。顺序错了就是事故。
3. **判断层**：什么时候该推、什么时候该停、fork 该不该改名、分叉了该先 fetch 还是该报警。**这一层才是产品**，也是通用版与专属版的真正差别。

