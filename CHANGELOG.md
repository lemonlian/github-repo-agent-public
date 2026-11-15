

## v1.2.0（2026-11-15）

零基础友好改造（AI 产品经理视角：装了 = 用得起来，才算交付）。

| 改动 | 为什么 | 影响文件 |
|---|---|---|
| 新增 `onboard` 环境自检命令 | 0→1 小白最大断点是环境：git/gh/授权缺哪步，就给哪步的可复制命令与「看到什么算成功」 | `scripts/gh_repo_guard.py` |
| 新增 BEGINNER-GUIDE.md 零基础手册 | 文科生向：注册账号（建议 Gmail，GitHub 不支持 Google 一键登录）→ 装 git → 装 gh → 设备码 → 第一个仓库，全程照抄 | `BEGINNER-GUIDE.md`、`README.md` |
| 授权分两档 | 默认最小权限（够 95% 场景）；删库属进阶档，单独升、删前必须备份+确认，不给小白默认开 `delete_repo` | `scripts/gh_repo_guard.py`、`BEGINNER-GUIDE.md`、`SKILL.md` |
