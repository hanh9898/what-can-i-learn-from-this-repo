# Lesson format

A lesson is a pattern in the sense of Alexander's *A Pattern Language*: a solution that works because of the forces in its context. Write every lesson with these fields:

- **Name**: a short noun phrase for the practice (`Disclosed reference files`), reused unchanged in the brief, the report and any later run.
- **Context**: where the source uses it, in one or two sentences.
- **Forces**: the pressures that make it pay off in the source, such as scale, team size, a failure it prevents, or a tool it relies on. This field decides transfer, so name each force concretely.
- **Solution**: what the source does, described as a practice. Quote at most a few lines of source code, and only when prose cannot carry the idea.
- **Evidence**: the source location as `path:line`.
- **Label**: *match* (the target shares every force), *partial* (it shares some, or would after a small change), or *no* (a force is missing, so adopting it would be cargo cult), with a one-line reason naming the force.
- **Payoff** and **Cost**, for *match* and *partial* only: payoff as what the target gains in one sentence, cost as `S`, `M` or `L`.

## Ranking

Rank the brief by payoff over cost, highest first. Between equals, a *match* goes before a *partial*.
