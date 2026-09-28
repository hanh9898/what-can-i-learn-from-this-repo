# 00: Git repo and public remote

**What to build:** This folder becomes a git repo with an integration branch, and that branch is pushed to a public repo named `what-can-i-learn-from-this-repo` on the author's personal GitHub account. Paseo waves can then branch worktrees off a pinned base commit, and the plugin marketplace has a URL to install from.

**Blocked by:** None (can start immediately)

**Status:** ready-for-human

- [ ] `git rev-parse --is-inside-work-tree` succeeds, and the current branch is `main`
- [ ] The first commit holds every existing file, and `.gitignore` excludes the `skill-creator` eval workspace
- [ ] Commits carry the author identity the user chose for this public repo
- [ ] The public GitHub repo exists under the chosen account, and `main` tracks `origin/main`
- [ ] `/matt-with-paseo` locates stage C on this checkout
