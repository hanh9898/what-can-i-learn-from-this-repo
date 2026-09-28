# 02: Source given as a GitHub URL

**What to build:** Running `/absorb <github-url>` does the following:

- Shallow-clones the source into the OS temp directory, outside the target.
- Records the commit SHA in the report.
- Links every lesson in the brief and the report by a permalink at that SHA.
- Deletes the clone when the run ends.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] A run given a GitHub URL completes without the user cloning anything.
- [ ] The report states the source URL and the exact SHA that was read.
- [ ] Every lesson link is a permalink at that SHA and resolves.
- [ ] No clone remains in the temp directory, and nothing except the report was written inside the target.
