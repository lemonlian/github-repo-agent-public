# 零基础使用指南：从没用过 GitHub，到让这个数字人管好你的仓库

> 写给完全没碰过 GitHub 的人。**你不需要懂任何术语**，照抄命令、看「看到什么算成功」就行。
> 全程大约 20 分钟。中途卡住，回到 `python3 scripts/gh_repo_guard.py onboard`，它会告诉你卡在哪一步。

## 先弄明白一件事：这个数字人怎么帮你

它是你的**仓库管家**：你只管说人话（「帮我盘一下仓库」「我要推代码了，先帮我查一下」「发个版本」），它替你跑命令、跑之前做安全检查、出问题告诉你怎么补救。两条底线它永远遵守：

1. **你的密码 / 令牌永远不交给它**——授权是你在 GitHub 官网自己点的，它碰不到你的密码；
2. **删东西之前必须先问你**——不可逆的动作，决定权永远在你。

## 第 0 步：注册一个 GitHub 账号（约 5 分钟）

还没有账号的话：

1. 打开 https://github.com/signup
2. 邮箱**建议填 Gmail**：一个邮箱通吃 GitHub / ChatGPT / Gemini，不用记好几套账号。
   ⚠️ 注意：GitHub **不支持 Google 一键登录**（跟 ChatGPT 不一样），密码要自己设、自己记好（建议存进浏览器或密码管理器）。
3. 用户名想一个：以后你的仓库网址长这样 `github.com/你的用户名/仓库名`，好记最重要。
4. 免费套餐（Free）就够，一路按提示走完。

**看到什么算成功**：能在右上角看到自己的头像，点进去有你的用户名。

## 第 1 步：装 git（约 5 分钟）

git 是把代码放进仓库的底层工具，装一次管终身。

**Mac**：打开「终端」（聚焦搜索搜"终端"），粘贴回车：

```bash
xcode-select --install
```

弹窗点「安装」，等进度条走完（约 5 分钟）。

**Windows**：去 https://git-scm.com/download/win 下载安装包，一路点「下一步」到装完。

**看到什么算成功**：终端里输入 `git --version`，回车，显示 `git version 2.x.x` 字样。

## 第 2 步：装 gh（约 1 分钟）

gh 是 GitHub 官方命令行，数字人靠它帮你干活。

**Mac**：`brew install gh`（没装过 brew 就先跑第 1 步的 xcode 命令，或看 https://brew.sh）
**Windows**：`winget install --id GitHub.cli`

装完**关掉终端重新打开**（不然找不到新命令）。

**看到什么算成功**：`gh --version` 显示 `gh version 2.x.x`。

## 第 3 步：授权连接（约 2 分钟，一串码，不碰密码）

在终端粘贴回车：

```bash
gh auth login --web --git-protocol https --skip-ssh-key --scopes "repo,read:org,gist,workflow,delete_repo"
```

按提示选 `Login with a web browser`，终端会显示一串形如 `XXXX-XXXX` 的码：

1. 复制这串码
2. 浏览器自动打开 https://github.com/login/device（没自动开就手动输网址）
3. 登录你的 GitHub 账号，粘贴这串码，点 Authorize（授权）

⚠️ 码只有 **15 分钟**有效，过期了别慌，重跑一遍上面的命令拿新码就行。

> **权限说明（重要）**：上面这条授权命令是**管理档**，一次到位——建仓、推代码、改描述、发版本、管理 topics 都行，**也包含删库能力**。给的是能力，不是风险：删除前数字人必须先列清单、先备份、先问你，这条护栏永远在。
> 如果你确定自己永远不需要删库，可以把命令里的 `--scopes "..."` 参数整段去掉，退回日常档。

最后跑一句：`gh auth setup-git`

**看到什么算成功**：`gh auth status` 显示 `✓ Logged in to github.com account 你的用户名`。

## 第 4 步：把数字人拿到手并自检（约 2 分钟）

```bash
git clone https://github.com/lemonlian/github-repo-agent-public.git
cd github-repo-agent-public
python3 scripts/gh_repo_guard.py onboard
```

**看到什么算成功**：4 步全是 `[PASS]`，最后打印「环境就绪」。
有任何 `[FAIL]`：它下面那几行就是给你的补救命令，抄着跑，跑完再来一遍。

## 第 5 步（可选）：建你的第一个仓库

```bash
gh repo create 我的第一个仓库 --public --description "这是什么｜给谁用｜什么状态" --clone
cd 我的第一个仓库
echo "# 我的第一个仓库" > README.md
git add README.md
git commit -m "第一次提交"
git push origin main
```

**看到什么算成功**：浏览器打开 `github.com/你的用户名/我的第一个仓库`，能看到 README。

## 第 6 步开始，说人话就行

| 你说 | 它做 |
|---|---|
| 「盘一下我的仓库」 | 列出你全部仓库，哪些描述不规范一目了然 |
| 「我要推代码了，先帮我查一下」 | 推送前四查，有问题先拦住 |
| 「看看哪些仓缺 Release」 | 版本历史体检 |
| 「帮我发个版本 v1.0」 | 打 tag + 建 Release（会再向你确认一次） |
| 「我是新手，从零帮我弄好环境」 | 就是你刚跑的 onboard |

## 卡住了？对号入座

| 现象 | 怎么办 |
|---|---|
| `command not found: gh/git` | 装完没重开终端；关掉重开再试 |
| 设备码说过期 | 15 分钟限制，重跑 `gh auth login ...` 拿新码 |
| 忘了 GitHub 密码 | github.com 登录页点「Forgot password」，用注册邮箱找回 |
| `push` 报错 `Connection timed out` | 网络问题，先重试两次；还不行找懂网络的朋友看代理 |
| `push` 被拦说「先修好 FAIL」 | 这是它在保护你：按 FAIL 提示处理完再推，**永远不要**网上搜来的 `--force` 硬推 |

## 三条安全底线（背下来也行）

1. **任何让你把 token / 密码粘贴给别人的做法都是错的**，直接拒绝；
2. **删仓库前必须备份 + 确认**，这是数字人的铁律，也是你自己该有的习惯；
3. 授权码（`XXXX-XXXX`）只在 GitHub 官方页面填，**别的任何网站要都别给**。

---

## 降级：确定不要删库能力时才需要（可先跳过）

第 3 步给的是管理档（含删库）。如果你确定自己永远不需要删库，可以退回日常档：

```bash
gh auth login --web --git-protocol https --skip-ssh-key
```

日常档不能删库，其余管理能力（建仓、推送、改描述、发版本）都在。哪天又想要删库能力了，重跑第 3 步的管理档命令即可。

无论哪一档，删除动作的铁律不变：先列清单 → `gh api repos/<owner>/<repo>/tarball` 备份 → 你亲口确认 → 才执行。
