

## v1.2.0（2026-11-15）

零基础友好改造（AI 产品经理视角：装了 = 用得起来，才算交付）。

| 改动 | 为什么 | 影响文件 |
|---|---|---|
| 新增 `onboard` 环境自检命令 | 0→1 小白最大断点是环境：git/gh/授权缺哪步，就给哪步的可复制命令与「看到什么算成功」 | `scripts/gh_repo_guard.py` |
| 新增 BEGINNER-GUIDE.md 零基础手册 | 文科生向：注册账号（建议 Gmail，GitHub 不支持 Google 一键登录）→ 装 git → 装 gh → 设备码 → 第一个仓库，全程照抄 | `BEGINNER-GUIDE.md`、`README.md` |
| 授权分两档 | 默认最小权限（够 95% 场景）；删库属进阶档，单独升、删前必须备份+确认，不给小白默认开 `delete_repo` | `scripts/gh_repo_guard.py`、`BEGINNER-GUIDE.md`、`SKILL.md` |

## v1.3.0（2026-11-15）

授权默认档翻转：日常档 → 管理档（账号主人拍板）。

| 改动 | 为什么 | 影响文件 |
|---|---|---|
| 默认授权改为管理档（含 delete_repo，一次到位） | 定位是完整仓库治理 / 冷库管理：建、改、删都要有，不给「先半授权、要删再升级」的两段体验 | `scripts/gh_repo_guard.py`、`README.md`、`QUICKSTART.md`、`BEGINNER-GUIDE.md`、`SKILL.md` |
| 删除护栏不随档位放开 | 能力给足 ≠ 风险放开：删前列清单 + tarball 备份 + 亲口确认，永远保留 | `SKILL.md`、`BEGINNER-GUIDE.md` |
| 原「进阶」章节改为「降级」章节 | 方向反转：管理档是默认，不要删库才降日常档 | `BEGINNER-GUIDE.md` |
