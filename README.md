# github-repo-agent-public

> **30 秒讲清**：这是一个「管 GitHub 仓库的 Agent」，通用版。它帮你把仓库名字、描述、版本历史、推送纪律统一起来，并在每次推代码前跑一遍安全检查。装好 `gh` 就能用，不需要给它任何密码。

| 项目 | 内容 |
|---|---|
| 这是什么 | 自研的 GitHub 仓库治理编排层（Agent 技能 + 可跑脚本） |
| 给谁用 | 任何要管多个 GitHub 仓库的人或团队；纯占位符，可直接公开 |
| 什么状态 | v1.0.0 可用；GitHub 可见性 **Public**；不含任何凭据 |
| 依赖 | GitHub CLI `gh`、Python 3.9+、git |
| 协议 | MIT，见 LICENSE |

## 一、先说清楚：这不是二创

二创是「基于已有作品改编」，要继承上游协议。本仓**没有复制任何第三方 skill 的代码**，只是调用官方 `gh` CLI 与 GitHub REST API，并在外面套一层自己的判断：

- 调用官方工具是**集成**，不继承 `cli/cli` 的 MIT；使用 GitHub 服务遵守其官方服务条款即可。
- 真正属于作者的是「什么时候推、推之前查什么、怎么退回去」这套规矩，所以按**自研资产**立 LICENSE。
- 这个区分不是文字游戏：误标成二创 = 主动继承 AGPL / NC 一类协议，商业化会被直接堵死。

## 二、凭据安全（最重要的一节）

**本仓不含、也永远不该含任何 token、密码、SSH 私钥。** 两个版本的差别不是「有没有密码」，而是「有没有私有上下文」：

| | 通用版 | 专属版 |
|---|---|---|
| 凭据 | 都没有 | 都没有 |
| 上下文 | 纯占位符、通用方法论 | 真实仓名清单与主人长期规矩 |
| GitHub 可见性 | Public | Private |

授权状态一律通过 `gh auth status` 查询，凭据由本机钥匙串 / gh 自己托管。没授权时 Agent 只负责引导你去 `https://github.com/login/device` 填一串设备码，**不会让你把 token 贴进对话**。

> 为什么这么较真：一旦把 token 写进文件并推上去，它就永久留在 git 历史里，删掉当前文件没用，只能改密码 + 清历史。

## 三、安装（从零到能跑）

**完全没用过 GitHub？** 先读 [BEGINNER-GUIDE.md](BEGINNER-GUIDE.md)：从注册账号（建议 Gmail 当注册邮箱，注意 GitHub 不支持 Google 一键登录）→ 装 git → 装 gh → 设备码授权 → 建第一个仓库，每步都写清「看到什么算成功」，照抄 20 分钟走完。卡住就跑 `python3 scripts/gh_repo_guard.py onboard`，缺哪步它给哪步的命令。

**有基础的老手**走速通版：


```bash
# 1. 装 gh（macOS）
brew install gh
# 其他系统：https://cli.github.com

# 2. 设备码授权，一串码，不碰密钥
gh auth login --web --git-protocol https --skip-ssh-key --scopes "repo,workflow,delete_repo,read:org,write:org,admin:org,gist,notifications,read:user,user,read:packages,write:packages,delete:packages,read:discussion,write:discussion,read:public_key,write:public_key,admin:public_key,read:gpg_key,write:gpg_key,admin:gpg_key"
gh auth setup-git

# 3. 拿本仓
git clone https://github.com/lemonlian/github-repo-agent-public.git
cd github-repo-agent-public

# 4. 自检
python3 scripts/gh_repo_guard.py check
python3 scripts/gh_repo_guard.py status
```

**没 gh 授权能不能用？** 不能连线上，但 `SKILL.md`、`QUICKSTART.md`、版本索引这些文档照常可读；装好授权后所有命令立刻可用。

把 `SKILL.md` 所在目录链到 WorkBuddy 技能目录即可触发：

```bash
ln -s "$(pwd)" ~/.workbuddy/skills/github-repo-agent-public
```

## 四、六个命令能干什么

| 命令 | 作用 | 会不会改线上 |
|---|---|---|
| `onboard` | 零基础环境自检：git / gh / 授权，缺哪步给哪步命令 | 只读 |
| `check` | 查 gh 授权、https 通道 | 只读 |
| `status` | 盘点全部仓（含 Private）、检查三段式描述与 topics | 只读 |
| `preflight <路径>` | 推前四查：通道 / 工作区 / 密钥 / 远端 HEAD 是否可快进 | 只读 |
| `audit` | 列出 tag 与 Release 缺口 | 只读 |
| `release <路径> --tag ... --confirm` | 打 tag + 建 GitHub Release | **写**，需显式确认 |

**命名与描述规范**（`status` 会查）：

- 自建 Agent 仓：`<用途>-<形态>-<受众>`，例如 `github-repo-agent-public`。
- description 三段式：`这是什么｜给谁用｜什么状态`。
- fork 仓：保留原名 + 描述写明上游全名 + topics 标 `fork` / `third-party` / `reference`。
- 历史归档（自建、非 Agent）：`<用途>-<技术栈>-<年份>`。

## 五、版本记录怎么写（每次提交都要带）

1. `CHANGELOG.md` 加一行：版本号 / 日期 / 改了什么 / 为什么改 / 影响哪些文件。
2. 里程碑打 tag 并**同时建 GitHub Release**（光有 tag 不算，要页面上看得到、点得开、下得了整包）。
3. README 第六节版本索引补一行。
4. 回退入口写清楚：上一个 tag 或 commit 是什么、怎么退。

## 六、版本与回退（历史版本，随时能退回来）

| tag | 日期 | commit | 一句话改动 |
|---|---|---|---|
| v1.4.0 | 2026-11-15 | 9b36212 | 授权升级为全权限档（21 项 scope 一次拉满，清单经设备码接口实测合法），删除护栏不变 |
| v1.3.0 | 2026-11-15 | c6ca085 | 授权默认档翻转为管理档（含 delete_repo，一次到位），删除护栏不变 |
| v1.2.0 | 2026-11-15 | c47f62e | 零基础友好：新增 onboard 环境自检命令 + BEGINNER-GUIDE.md 手册 + 授权分两档（默认最小权限，删库进阶档） |
| v1.1.0 | 2026-11-15 | 7f205e1 | 对标学习增强：Examples 触发例句、渐进披露层 references、Keep a Changelog 声明 |
| v1.0.0 | 2026-11-15 | `7b3ad88` | 建立自研编排层、凭据零落盘、五个治理命令、README 与回退章节 |

```bash
# 看有哪些版本
git tag --sort=-creatordate | head -20

# 只退单个文件（推荐，不丢别的东西）
git checkout v1.0.0 -- scripts/gh_repo_guard.py
git checkout v1.0.0 -- README.md

# 整仓临时回看
git checkout v1.0.0
git checkout main          # 看完切回来

# 撤销某一次提交（不动历史）
git revert <commit>

# 直接下载某个 Release 整包
gh release download v1.0.0 --repo lemonlian/github-repo-agent-public
```

> 回退前先备份你的配置实例（`config/` 下你自己改过的文件），别把本地配置覆盖没了。

## 七、不用问作者：常见问题自查

| 现象 | 先查这里 |
|---|---|
| `gh: command not found` | `brew install gh`；其他系统看 cli.github.com |
| 提示未授权 | 跑上面安装节的授权命令（全权限档，含 `--scopes`），浏览器填设备码 |
| 设备码过期 | 码只有 15 分钟有效，重跑登录命令拿新码 |
| `status` 里仓库数比想象少 | 一定要用 `/user/repos`，`/users/<name>/repos` 只返回 public |
| `preflight` 报「远端 HEAD 可快进」FAIL | 别的会话推过了：`git fetch` → `git pull --ff-only`，**不要 --force** |
| `git push` 报 `CONNECT tunnel failed 502` | 先 `git config --global http.version HTTP/1.1` 重试；仍失败走 GitHub Git Data API 兜底（blobs→trees→commits→PATCH refs），见 SKILL.md |
| 删库没权限 | token 缺 `delete_repo` scope：用安装节的全权限授权命令（21 项 scope）重新授权 |
| 想换电脑 | 不用搬任何凭据：新机器装 gh → 设备码授权 → clone 本仓 → `check` 通过即可 |
| 能不能给 Agent 我的密码 | **不能**。任何要你贴 token / 私钥的做法都是错的，请直接拒绝 |
| 支持找谁 | 提 issue；协议见 `LICENSE` |

## 八、目录说明

```
SKILL.md                    Agent 技能定义（铁律 + 治理动作 + 三层结构）
README.md                   本文件
QUICKSTART.md               5 分钟跑通
CHANGELOG.md                每次改动的变更说明
LICENSE                     协议
scripts/gh_repo_guard.py    五个命令的可跑实现
config/policy.example.json          策略配置（示例，复制成 policy.json 后自己填）
examples/usage.md           典型用法与 FAIL 处理表
references/details.md       深入细节（FAIL 矩阵 / API 兜底 / 回退选择 / 发版纪律）
BEGINNER-GUIDE.md           零基础手册（没用过 GitHub 也能 20 分钟跑通）
```

