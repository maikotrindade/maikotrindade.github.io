---
layout: post
title: "Loop Engineering in Practice: What No Middleman Taught Me About Verifying AI-Written Code"
seo_title: "Loop Engineering: Verifying AI-Written Code"
date: 2026-07-24 09:00:00 -0700
published: true
categories: [ai-agents, engineering]
tags: [AI, agents, loop engineering, verification, Detox, React Native, XState, autonomous agents]
description: "How the No Middleman loop verifies AI-written React Native code with Detox, an adversarial checker, and invariants, instead of trusting the diff."
keywords: "loop engineering, AI code verification, Detox, React Native, adversarial checker, autonomous agents, XState"
image: /public/img/android-dev.png
---

GitLab's <a href="https://ir.gitlab.com/news/news-details/2026/GitLab-Research-Reveals-Organizations-Are-Generating-AI-Code-Faster-Than-They-Can-Control-It/default.aspx" target="_blank" rel="noopener noreferrer" title="GitLab 2026 AI Accountability Report">2026 AI Accountability Report</a> found that 78% of developers say they're writing and committing code faster with AI tools. It also found that overall software delivery hasn't sped up to match. The gap is explained by one number: 85% of respondents say AI has shifted the bottleneck from writing code to reviewing and validating it. Everyone got a faster typist. Almost nobody got a faster team.

That's the exact problem I've been building against with <a href="https://github.com/maikotrindade/no-middleman-react-native" target="_blank" rel="noopener noreferrer" title="No Middleman on GitHub">No Middleman</a>, a Claude Code plugin for React Native that lets an agent loop on a feature or bug fix unattended, but only ever hands you a pull request that's already been proven against a real emulator, not just asserted as done. I wrote about the general shape of agent control loops in <a href="https://maikotrindade.com/ai-agents/engineering/2026/07/02/loop-engineering-autonomous-agents.html" target="_blank" rel="noopener" title="Loop Engineering: Designing the Control Loop Behind Autonomous Agents">a previous post</a>. This one is about the part of that loop that actually matters once you let the agent run without you watching: verification.

### Trusting the diff doesn't scale

The default way most of us review AI-generated code right now is to read the diff and decide if it looks right. That works when the change is small and you already understand the surrounding code. It stops working the moment the agent is iterating on its own, because "looks right" is a judgment about static text, and the failure modes that matter, a race condition, a mock that silently changed behavior, a test that got loosened instead of the code getting fixed, don't show up in a diff. They show up when the thing runs.

GitLab's finding lines up with what you'd expect from that: reviewing and validating AI output is slower and harder than writing the prompt that generated it, so the bottleneck moved downstream instead of disappearing. Reading harder isn't the fix. Verifying differently is.

### Assess, act, verify

No Middleman's loop is a typed `LoopSpec` run on XState v5: a trigger, an intake (a goal plus the file globs it's allowed to touch), a composite verification chain ordered cheap to expensive, and a stopping rule with a hard budget. Nothing about "done" is left to the model's judgment.

```bash
nm verify --e2e
```

That single command is the thing the loop iterates against. It runs typecheck, lint, unit tests, and a build, in that order, fail-fast, before it ever touches an emulator. Only once those pass does it get to the expensive check. Cheap gates first means a broken import gets caught in seconds, not after a five-minute Detox run.

### Detox as the oracle, not a formality

The headline gate is a Detox end-to-end flow, and the workflow deliberately puts a human at the point where the test is defined, not where it's checked. You write the goal, a `spec-author` agent drafts the acceptance flow, and you approve it before anything starts. That red test is the contract. The agent never gets to negotiate what "done" means after the fact, because the definition was fixed before it wrote a line of code.

The dev client compiles once, cached by a hash of the native inputs, and every iteration after that just reloads JS. That's what makes a real Detox run cheap enough to sit inside a loop instead of being a once-a-day CI job: the expensive part only happens when something native actually changed.

### The checker can't be the maker

The part I'd guess most people skip is the one that matters most: green isn't the finish line. Once the suite passes, a separate Opus agent, one that never touched the implementation, reviews the diff specifically hunting for the ways a model games its own tests: weakened assertions, mocks that quietly make the test meaningless, timing masked instead of fixed, scope that crept outside what the goal asked for. It's an adversarial checker by design, not an optimistic second opinion.

That split exists because letting an agent grade its own homework is exactly how you get a green checkmark on code that doesn't actually work. If the same model that wrote the fix also decides whether the fix is good, its incentive is to reach green by whatever path is shortest, and loosening a test is a shorter path than fixing the underlying bug. Separating maker from checker removes that incentive.

### Invariants, not intentions

The loop won't even start if a spec violates one of eight hard rules: `require-verifiable-stop`, `bounded-retries`, `maker-neq-checker`, `tests-only-strengthen`, `external-state-only`, `read-only-by-default`, `human-approves-acceptance`, `pr-not-merge`. `tests-only-strengthen` is the one doing the most quiet work: a test can get stricter as the loop iterates, never looser. That closes off the single easiest way an unsupervised agent could cheat its way to a passing run.

`pr-not-merge` closes the other one. The loop's output is always a draft pull request, whether the checker accepted the change or the iteration budget ran out first. Nothing merges itself. A hard cap on iterations, tokens, and wall-clock time, plus a reserve the loop never spends on iteration, means it always has enough left to write a clean handoff instead of dying mid-edit. And if something looks wrong while it's running, `touch .nm/KILL` halts it between iterations and leaves a clean worktree behind.

### The two ends you still own

The name is literal: the loop removes you from its interior, the part where you'd otherwise sit watching each edit-reload-verify cycle and nudging it back on track. It doesn't remove you from the two ends. You write the acceptance test that defines what "done" means, and you review the PR that comes out. Autonomous interior, human bookends. That's a different claim than "the agent tested itself," and it's the reason I trust the output more than I trust a diff someone asks me to skim.

### What this means for reviewing AI code generally

The GitLab numbers describe a team where AI made the input to review faster without making review itself faster, which is a bottleneck relocation, not a productivity gain. The fix isn't reading diffs more carefully. It's building a verifier that runs the code and grades it against a test you wrote and a checker that has no stake in the outcome, so that by the time a human opens the PR, the question isn't "does this look right," it's "do I approve of the test that already proved it."
