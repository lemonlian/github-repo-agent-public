# 5 分钟跑通

## 1. 装好 gh 并授权（一串码，不碰密钥）

```bash
brew install gh                      # macOS；其他系统见 https://cli.github.com
gh auth login --web --git-protocol https --skip-ssh-key --scopes "repo,workflow,delete_repo,read:org,write:org,admin:org,gist,notifications,read:user,user,read:packages,write:packages,delete:packages,read:discussion,write:discussion,read:public_key,write:public_key,admin:public_key,read:gpg_key,write:gpg_key,admin:gpg_key"
# 终端给一串形如 XXXX-XXXX 的码，浏览器打开 https://github.com/login/device 填进去
gh auth setup-git                    # 让 git push 走 https
```

**不要配 SSH 私钥**。SSH 只能 push，建库 / 改设置 / 删库这些管理动作做不了；而且把私钥交给 Agent 等于把账号交出去。

## 2. 检查环境

```bash
python3 scripts/gh_repo_guard.py check
python3 scripts/gh_repo_guard.py status
```

`status` 用 `/user/repos` 而不是 `/users/<name>/repos`——后者只返回 public 仓，会让你误判自己只有一半仓库。

## 3. 推代码前跑一次

```bash
python3 scripts/gh_repo_guard.py preflight /path/to/your/repo
```

四查：https 通道、工作区干净、diff 里没密钥、远端 HEAD 可快进。任一 FAIL 就先修，别硬推。

## 4. 看版本缺口 / 发里程碑

```bash
python3 scripts/gh_repo_guard.py audit
python3 scripts/gh_repo_guard.py release /path/to/your/repo --tag v1.1.0 --notes "改了什么" --confirm
```

`release` 不加 `--confirm` 会拒绝执行——**打 tag 是人的决定，不是 Agent 的**。

## 5. 装进 WorkBuddy

把本仓 `SKILL.md` 所在目录软链或复制到 `~/.workbuddy/skills/<name>/`：

```bash
ln -s "$(pwd)" ~/.workbuddy/skills/<name>
```

之后说「盘一下我的仓库」「推之前帮我查一下」「看看哪些仓缺 Release」就会触发。
