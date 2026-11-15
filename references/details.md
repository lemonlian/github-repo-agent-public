# 深入细节：命令输出怎么读、FAIL 怎么处理、兜底怎么走

> 本文件是 `SKILL.md` 的细节层（渐进披露）。上面定判断，这里定操作。按需读对应小节，不必通读。

## 一、`preflight` FAIL 处理矩阵

| FAIL | 原因 | 处理 | 绝对不要 |
|---|---|---|---|
| 工作区干净 | 有未提交改动 | 先 commit（改了什么写清楚），或明确放弃后 `git checkout -- <file>` | 带着脏区硬推 |
| 推前无密钥混入 | diff 命中 `gho_` / `ghp_` / `github_pat_` / `PRIVATE KEY` / `password=...` | **停止推送**。从文件删掉凭据；已 commit 的用 `git reset --soft HEAD^` 重做；已推过的按泄露处理：撤销 token + 评估清历史 | 「下次再删」先推了再说 |
| 远端 HEAD 可快进 | 别的会话 / 别人已推过 | `git fetch origin` → `git pull --ff-only` → 重新 preflight | `--force`、`--no-verify`、reset --hard 后重推 |
| 通道是 https | remote 还是 `git@github.com:` | `gh auth setup-git` → `git remote set-url origin https://github.com/<owner>/<repo>.git` | 往 Agent 文件里写私钥换 SSH |

## 二、`git push` 失败的网络兜底（按顺序试）

1. `git -c http.version=HTTP/1.1 push origin main` —— 代理下最常见的修复。
2. 再重试 1–2 次；`Empty reply from server` 通常重试即通。
3. 仍失败 → **Git Data API 兜底**（不 force、不丢历史、SHA 与本地一致）：
   ```bash
   # ① 逐文件建 blob（base64）
   gh api -X POST repos/<owner>/<repo>/git/blobs --input - <<< '{"content":"<base64>","encoding":"base64"}'
   # ② 建 tree（base_tree 用远端 HEAD 的 tree，只放变更文件）
   gh api -X POST repos/<owner>/<repo>/git/trees --input - <<< '{"base_tree":"<远端tree_sha>","tree":[{"path":"README.md","mode":"100644","type":"blob","sha":"<blob_sha>"}]}'
   # ③ 建 commit（parents 用远端 HEAD，message 用本地 git log 原文）
   gh api -X POST repos/<owner>/<repo>/git/commits --input - <<< '{"tree":"<新tree>","parents":["<远端HEAD>"],"message":"..."}'
   # ④ 移动分支指针
   gh api -X PATCH repos/<owner>/<repo>/git/refs/heads/main --input - <<< '{"sha":"<新commit>"}'
   ```
   注意：`gh api` 传 JSON body 必须显式 `--input -`，否则 422。

## 三、回退方案怎么选

| 场景 | 用什么 | 命令 |
|---|---|---|
| 只想撤某个文件 | 单文件 checkout | `git checkout <tag> -- <path>` 后 commit |
| 想看旧版整体长什么样 | 整仓临时回看 | `git checkout <tag>` → 看完 `git checkout main` |
| 想撤销某次提交（不动历史） | revert | `git revert <commit>` |
| 想下某个版本的整包 | Release 下载 | `gh release download <tag> --repo <owner>/<repo>` |

> 回退前先备份 `config/` 下自己改过的实例文件。改公共历史的操作（rebase / filter-branch / force）一律不做。

## 四、盘点口径的坑

- 全量盘点只用 `user/repos?per_page=100&affiliation=owner`；`users/<name>/repos` **只返回 public**，会漏掉一半仓。
- 返回正好 100 个时可能有下一页，`page=2` 继续翻。
- fork / archived 仓默认跳过版本审计（`audit --all` 才查），它们的规范是「保留原名 + 三段式描述写明上游」，不是打 tag。

## 五、发版纪律（`release --confirm`）

- 版本号由人决定，Agent 只执行。不加 `--confirm` 会拒绝，这是故意的。
- 打完 tag 必须三件事一起做：GitHub Release（`gh release create`，光有 tag 不算）、`CHANGELOG.md` 记一行（改了什么 / 为什么 / 影响哪些文件）、README 版本索引表补一行含真实 commit 号。
- CHANGELOG 遵循 [Keep a Changelog 1.1.0](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [SemVer](https://semver.org/)：改了行为加 minor，破坏兼容才加 major。
