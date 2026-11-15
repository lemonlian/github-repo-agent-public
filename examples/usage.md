# 用法示例

## 盘点仓情

```bash
python3 scripts/gh_repo_guard.py status
```

输出会告诉你：一共几个仓（含 Private）、哪些是 fork、哪些描述还没写成三段式、哪些 topics 为空。

## 推前四查（最常见的用法）

```bash
python3 scripts/gh_repo_guard.py preflight ~/code/my-repo --branch main
```

典型 FAIL 与处理：

| FAIL | 怎么处理 |
|---|---|
| 工作区干净 | 有未提交改动 → 先 commit，或明确放弃 |
| 推前无密钥混入 | diff 里出现 `gho_` / `ghp_` / `PRIVATE KEY` → **别推**，先从文件内容删掉，必要时撤销这次 commit |
| 远端 HEAD 可快进 | 别人（或另一个 AI 会话）已经推过 → `git fetch` 后 `git pull --ff-only`，绝不 `--force` |

## 发版

```bash
python3 scripts/gh_repo_guard.py audit
python3 scripts/gh_repo_guard.py release ~/code/my-repo --tag v1.1.0 --notes "补齐回退章节" --confirm
```

发完把 tag / 日期 / commit / 一句话改动补进 README 的版本索引表，再推上去。
