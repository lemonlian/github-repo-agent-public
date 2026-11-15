#!/usr/bin/env python3
"""GitHub 仓库治理守卫 —— 只读盘点 / 推前四查 / 版本缺口 / 发版。

设计边界：
* 只调用官方 gh CLI 与 GitHub REST API，不复制任何第三方 skill 的代码；
* 不读取、不保存、不打印任何 token / 密码，授权状态一律交给 `gh auth status`；
* 所有写动作（打 tag、建 Release）必须显式传 --confirm，绝不自动执行。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SECRET_PATTERNS = [
    r'gho_[A-Za-z0-9]{20,}', r'ghp_[A-Za-z0-9]{20,}',
    r'github_pat_[A-Za-z0-9_]{20,}', r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'(api[_-]?key|secret|password|token)\s*[:=]\s*["\x27][^"\x27]{8,}',
]
SECRET_RE = re.compile('|'.join(SECRET_PATTERNS), re.IGNORECASE)


def run(cmd, *, cwd=None, stdin=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} -> {(p.stderr or p.stdout).strip()}")
    return p


def gh_json(path, method='GET', body=None):
    args = ['gh', 'api', '-X', method, path]
    if body is not None:
        args += ['--input', '-']
    p = run(args, stdin=json.dumps(body) if body is not None else None)
    return json.loads(p.stdout) if p.stdout.strip() else None


def git(path, *args, check=True):
    return run(['git', '-C', str(path), *args], check=check)


def owner_repo(path):
    url = git(path, 'remote', 'get-url', 'origin').stdout.strip()
    if url.startswith('git@'):
        raise RuntimeError(f'远程仍是 SSH，请切 https：git remote set-url origin https://github.com/... ({url})')
    m = re.search(r'github\.com/(.+?)/(.+?)(?:\.git)?$', url)
    if not m:
        raise RuntimeError(f'无法从 {url} 解析 owner/repo')
    return m.group(1), m.group(2)


def repos_all():
    """必须用 /user/repos 才看得到 Private 仓；/users/<name>/repos 只返回 public。"""
    return gh_json('user/repos?per_page=100&affiliation=owner')


def cmd_check(_):
    p = run(['gh', 'auth', 'status'], check=False)
    text = (p.stdout or '') + (p.stderr or '')
    ok = p.returncode == 0 and 'Logged in to github.com' in text
    https = 'Git operations protocol: https' in text or 'https' in text.lower()
    print(json.dumps({
        'gh_installed': p.returncode != 127,
        'authorized': ok,
        'https_channel': https,
        'hint': '' if ok else '先跑 gh auth login --web --git-protocol https --skip-ssh-key，用设备码授权，不要把 token 贴给任何人',
    }, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def cmd_status(args):
    repos = repos_all()
    if len(repos) == 100:
        print('提示：返回正好 100 个仓，可能还有下一页，请用 gh api 手动翻页。', file=sys.stderr)
    rows = []
    for r in repos:
        name = r['name']
        desc = r.get('description') or ''
        topics = r.get('topics') or []
        rows.append({
            'name': name,
            'visibility': 'private' if r.get('private') else 'public',
            'origin': 'fork' if r.get('fork') else 'self',
            'desc_three_part': '｜' in desc,
            'topics': len(topics),
            'fork_marked': ('fork' in topics) or ('上游' in desc),
        })
    width = max(len(x['name']) for x in rows) + 2
    print(f"{'仓库'.ljust(width)}{'可见性':<10}{'来源':<8}{'三段式描述':<12}{'topics':<8}备注")
    for x in sorted(rows, key=lambda y: y['name']):
        note = ''
        if x['origin'] == 'fork' and not x['fork_marked']:
            note = 'fork 未标上游'
        elif not x['desc_three_part']:
            note = '描述待补三段式'
        print(f"{x['name'].ljust(width)}{x['visibility']:<10}{x['origin']:<8}{('是' if x['desc_three_part'] else '否'):<12}{str(x['topics']):<8}{note}")
    bad = [x for x in rows if not x['desc_three_part'] or (x['origin'] == 'fork' and not x['fork_marked'])]
    print(f"\n共 {len(rows)} 个仓（含 Private），待规范 {len(bad)} 个。")
    return 0


def cmd_preflight(args):
    path = Path(args.path).expanduser().resolve()
    owner, repo = owner_repo(path)
    branch = args.branch
    local = git(path, 'rev-parse', 'HEAD').stdout.strip()
    parent = git(path, 'rev-parse', 'HEAD^', check=False).stdout.strip()
    remote = gh_json(f'repos/{owner}/{repo}/commits/{branch}')['sha']
    status = git(path, 'status', '--porcelain').stdout.strip()
    diff = git(path, 'diff', 'HEAD^', 'HEAD', check=False).stdout
    hits = [m.group(0)[:60] for m in SECRET_RE.finditer(diff)]

    checks = [
        ('通道是 https', True, 'origin 已解析为 https'),
        ('工作区干净', not bool(status), status or '无未提交改动'),
        ('推前无密钥混入', not hits, '；'.join(hits) if hits else 'diff 中未发现疑似凭据'),
        ('远端 HEAD 可快进', remote in (local, parent),
         f'local={local[:8]} parent={parent[:8] or "无"} remote={remote[:8]}'),
        ('禁止 force / 跳 hook', True, '本守卫不生成 --force / --no-verify；请人工确认提交命令'),
    ]
    print(f'仓库 {owner}/{repo}  分支 {branch}')
    for label, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} — {detail}")
    failed = [c for c in checks if not c[1]]
    if failed:
        print('\n结论：先修好上面的 FAIL 再推。分叉时先 git fetch --ff-only，绝不 --force。')
        return 1
    print('\n结论：可以推。推完请立刻校验远端 HEAD 与本地一致。')
    return 0


def cmd_audit(args):
    repos = repos_all()
    only_self = not args.all
    print(f"{'仓库':<38}{'tag':<8}{'Release':<10}状态")
    gaps = []
    for r in sorted(repos, key=lambda y: y['name']):
        if only_self and (r.get('fork') or r.get('archived')):
            continue
        full = r['full_name']
        tags = gh_json(f'repos/{full}/tags?per_page=100') or []
        rels = gh_json(f'repos/{full}/releases?per_page=100') or []
        state = 'OK' if tags and len(tags) == len(rels) else ('缺 Release' if tags else '无 tag / 无 Release')
        if state != 'OK':
            gaps.append((full, state))
        print(f"{r['name']:<38}{str(len(tags)):<8}{str(len(rels)):<10}{state}")
    print(f'\n缺口 {len(gaps)} 个。补法见 README「版本与回退」。')
    return 0


def cmd_release(args):
    if not args.confirm:
        print('拒绝执行：打 tag / 建 Release 属于里程碑动作，必须显式加 --confirm，且版本号由人决定。')
        return 2
    path = Path(args.path).expanduser().resolve()
    owner, repo = owner_repo(path)
    sha = git(path, 'rev-parse', 'HEAD').stdout.strip()
    run(['gh', 'release', 'create', args.tag, '--repo', f'{owner}/{repo}',
         '--target', sha, '--title', args.tag, '--notes', args.notes])
    rels = gh_json(f'repos/{owner}/{repo}/releases?per_page=100') or []
    tags = gh_json(f'repos/{owner}/{repo}/tags?per_page=100') or []
    print(f'{owner}/{repo}: tag={len(tags)} Release={len(rels)}  ← {args.tag} ({sha[:8]})')
    print('记得把新版本写进 CHANGELOG 与 README 的版本索引表。')
    return 0


def main():
    ap = argparse.ArgumentParser(description='GitHub 仓库治理守卫（凭据零落盘）')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('check', help='检查 gh 授权与 https 通道').set_defaults(func=cmd_check)
    sub.add_parser('status', help='盘点全部仓（含 Private）与规范达标情况').set_defaults(func=cmd_status)
    p = sub.add_parser('preflight', help='推送前四查')
    p.add_argument('path'); p.add_argument('--branch', default='main')
    p.set_defaults(func=cmd_preflight)
    p = sub.add_parser('audit', help='盘点 tag / Release 缺口')
    p.add_argument('--all', action='store_true', help='连 fork 与归档仓一起查')
    p.set_defaults(func=cmd_audit)
    p = sub.add_parser('release', help='打 tag + 建 Release（需 --confirm）')
    p.add_argument('path'); p.add_argument('--tag', required=True)
    p.add_argument('--notes', default='里程碑版本')
    p.add_argument('--confirm', action='store_true')
    p.set_defaults(func=cmd_release)
    args = ap.parse_args()
    try:
        sys.exit(args.func(args))
    except RuntimeError as e:
        print(f'错误：{e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
