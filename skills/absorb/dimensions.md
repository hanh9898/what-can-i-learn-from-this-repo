# Dimensions

Each dimension below gets its own sweep; sweeps run one after another go in this order. The lens sets the depth: go deep on a dimension where the target hurts or is changing, and skim the rest for anything the lens did not foresee. Skimming a dimension still produces its lessons, or "nothing worth transferring".

1. **Architecture and module boundaries**: how the code is split, what each module hides, where the seams sit, how dependencies point.
2. **Testing**: what is tested at which seam, how tests stay fast and deterministic, what fixtures and evals look like.
3. **Tooling, DX and CI**: scripts, linters, hooks, CI jobs, release flow, and the checks that turn a mistake into a failing build.
4. **Docs and agent config**: README, `CLAUDE.md` / `AGENTS.md`, glossaries, ADRs, skills, and how each is reached.
5. **Conventions**: naming, error handling, file layout, commit and ticket shape, anything the repo does the same way everywhere.
6. **Dependency choices**: what the source pulls in versus builds itself, and why.
