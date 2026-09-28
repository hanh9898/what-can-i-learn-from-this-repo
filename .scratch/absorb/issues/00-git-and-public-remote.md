# 00: Git repo and public remote

**What to build:** This folder becomes a git repo with an integration branch, and that branch is pushed to a public repo named `what-can-i-learn-from-this-repo` on the author's personal GitHub account. Paseo waves can then branch worktrees off a pinned base commit, and the plugin marketplace has a URL to install from.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] `git rev-parse --is-inside-work-tree` succeeds, and the current branch is `main`
- [x] The first commit holds every existing file, and `.gitignore` excludes the `skill-creator` eval workspace
- [x] Commits carry the author identity the user chose for this public repo
- [x] The public GitHub repo exists under the chosen account, and `main` tracks `origin/main`
- [x] `/matt-with-paseo` locates stage C on this checkout

## Comments

- Done on 2026-09-29. `main` tracks `origin/main` at https://github.com/hanh9898/what-can-i-learn-from-this-repo (public). Repo-local author: `hanh9898 <56497031+hanh9898@users.noreply.github.com>`. `.gitignore` excludes `absorb-workspace/`. Stage C holds: tickets exist under `.scratch/absorb/issues/`, and there is no `wave*-common-rules.md`.
