---
layout: post
title: "The Verification Phase: Why Testing Matters More When Agents Write the Code"
seo_title: "Why Verification Matters for Coding Agents"
date: 2026-11-20 09:00:00 -0700
published: true
categories: [ai-agents, engineering]
tags: [AI, agents, coding agents, verification, software testing, React Native, Maestro, agent-device, end-to-end testing, pstack]
description: "Why verification, not generation, is the bottleneck for coding agents, with a React Native guide to every test layer, AI-driven E2E, and review evidence."
keywords: "coding agents verification, testing AI generated code, React Native end-to-end testing, Maestro, agent-device, AI E2E testing, pstack verification skill, Lauren Tan All Code Is Slop"
image: /public/img/verification-phase-coding-agents.png
---

Coding agents made writing code cheap. They didn't make *knowing the code works* cheap. In her AI Engineer Code Summit talk, Lauren Tan (poteto online) explained how her team at SpaceXSI ships thousands of agent-written pull requests a month with a revert rate around half a percent. The secret isn't the model. It's the phase most of us still treat as an afterthought: **verification**.

Verification for coding agents means running the changed software, observing the behavior the change was supposed to produce, and keeping evidence a reviewer can check. It's not the same as "the tests pass", and it's what lets you trust code you didn't read line by line. This post explains that phase and what it looks like in a React Native app.

## Why verification became the bottleneck

The talk, <a href="https://www.youtube.com/watch?v=O_zcc6Xl12g" target="_blank" rel="noopener noreferrer" title="All Code Is Slop (Except Mine) by Lauren Tan on YouTube">All Code Is Slop (Except Mine)</a>, has a few numbers worth remembering. Lauren shipped around 3,000 PRs in the month before the talk. Her team shipped around 11,000, with a revert rate of about 0.5%. And in 2024 she reviewed PRs from about three colleagues, while today it's closer to 300.

Nobody can read the diffs of 300 people. Generation takes minutes now, so the cost has moved from writing code to checking it. Agents also make checking harder in specific ways:

- **They copy what they see.** An anti-pattern in the codebase gets copied by the next agent, then copied again.
- **They justify their mistakes.** Her team saw agents patch a bug with timers, then write comments explaining why the timers were needed. The next agent trusted the comments and added more timers.
- **Their own tests prove little.** Tests written by the agent that wrote the code encode the same misunderstanding. As the <a href="https://aiidelist.com/blog/lauren-tan-grok-bot-pstack-workflow" target="_blank" rel="noopener noreferrer" title="Lauren Tan's Grok Bot workflow with pstack and Cursor Cloud Agents">AI IDE List write-up of her workflow</a> notes, the builder saying the tests passed adds no independent evidence.

## Constrain first, then verify

Lauren's rule is that every correction to an agent becomes a deterministic check: a lint rule, a type, or an API that makes the mistake impossible. A prompt saying "don't do X" works sometimes. A lint rule works every time, especially when its message tells the agent what to do instead:

```javascript
// eslint.config.js: stop agents from hardcoding colors in screens
export default [{
  files: ["src/screens/**/*.{ts,tsx}"],
  rules: {
    "no-restricted-syntax": ["error", {
      selector: "Property[key.name=/^(color|backgroundColor|borderColor)$/] > Literal",
      message: "Don't hardcode colors. Use a token from src/design-system/tokens.ts."
    }]
  }
}];
```

Every bug that's impossible is one you don't have to verify. Constraints shrink the problem, and verification covers what's left.

## What counts as verification

The key idea, which Lauren's open-source <a href="https://flaviocopes.com/pstack.md" target="_blank" rel="noopener noreferrer" title="Flavio Copes: A deep dive into pstack">pstack plugin</a> is built around, is that **a green build isn't evidence**. You have to observe the behavior that motivated the change, in the running app, and keep proof of it. The proof depends on the change:

| Change type | What counts as evidence |
| --- | --- |
| Bug fix | Reproduce the bug, fix it, rerun the same reproduction |
| Refactor | Characterization tests that stay green through each step |
| Performance | A trace compared against a baseline. "It feels faster" doesn't count |
| Visual change | Screenshots diffed against approved baselines |
| Data change | Read back the stored values and check them directly |

The question to ask isn't "did the agent test it?" It's "what would I have to see to believe this works?" Then make the agent show you exactly that.

## The test layers in a React Native app

Verification is a stack. Each layer catches different mistakes at a different cost, and the agent should run the cheap ones on every change.

| Layer | What it catches | Typical tools |
| --- | --- | --- |
| Unit | Logic bugs in prices, reducers, validation | Jest, fast-check for property-based tests |
| Component | A screen that renders or reacts wrong | React Native Testing Library |
| Integration | Bugs between screen, store, and network | Jest with the network mocked (MSW) |
| Contract | App and API disagreeing on a payload | Pact, or a schema check in CI |
| Design system | Off-token colors, broken shared components | Storybook stories, lint rules |
| Screenshot | Unintended visual changes | Image diffs on a fixed simulator |
| End-to-end | The user can't actually finish the flow | agent-device, Maestro |

Two tips make the lower layers much stronger with agents. Prefer **property-based tests** for core logic, because they describe intent ("the total always equals the sum of the items") instead of mirroring the implementation. And query components by role and label in React Native Testing Library, so a missing accessibility label fails the test.

## AI-driven end-to-end testing

End-to-end is where AI changes verification the most. Lauren's team lets agents run the app and hand back screenshots and videos instead of claims. On React Native, two tools cover this.

**<a href="https://github.com/callstack/agent-device" target="_blank" rel="noopener noreferrer" title="agent-device by Callstack on GitHub">agent-device</a>** is Callstack's CLI that lets a coding agent drive iOS and Android apps. The agent reads an accessibility snapshot, acts on elements by ref, and sees what changed:

```bash
agent-device open ShopApp --platform ios
agent-device snapshot -i
# @e4 [button] "Remove Coffee"
agent-device press @e4 --settle
# + @e9 [text] "Your cart is empty"
agent-device screenshot ./evidence/cart-empty.png
agent-device close
```

The agent gets a description of the screen, not just pass or fail, so it can notice on its own that the empty state never appeared. Because the snapshot comes from the accessibility tree, an unlabeled button shows up right away.

**<a href="https://maestro.dev/" target="_blank" rel="noopener noreferrer" title="Maestro mobile UI testing framework">Maestro</a>** keeps what the agent learned. Once the fix is verified, the agent saves the path it took as a flow and commits it with the PR, so CI replays it on every future change, with no LLM involved:

```yaml
# .maestro/cart-remove-last-item.yaml
appId: com.example.shop
---
- launchApp:
    clearState: true
- startRecording: cart-remove-last-item
- tapOn: "Add to cart"
- tapOn:
    id: "cart-tab"
- tapOn: "Remove Coffee"
- assertVisible: "Your cart is empty"
- takeScreenshot: cart-empty
- stopRecording
```

The AI does the expensive, exploratory part once. The deterministic tool keeps the result forever. Agents also help write flows from a plain-language description, fix flows when a label changes, and read failed runs to tell a real bug from a flaky wait. Lauren's team goes further: on every release, an agent uses the app, hunts for bugs, and opens fix PRs.

## The human in the loop

Automated checks answer "does it work?" They're weak at "is it good?" That's why verification has to produce **artifacts** that both an AI and a human can review:

- videos of the end-to-end flows
- screenshots in light mode, dark mode, and large text, plus diffs against baselines
- accessibility snapshots showing what a screen reader will announce
- logs from Metro, the device, and the app
- performance traces for startup, scrolling, and key flows
- observability data, like crash and error reports from staging builds
- reports from every test layer

A **verifier agent** with fresh context reviews the evidence first. It checks that the video shows the fixed behavior, the logs have no new errors, and the screenshot diffs only touch the screens the task mentioned. Then a **human** reviews what needs judgment: visual quality, accessibility with VoiceOver or TalkBack, performance against the baseline, and whether the change solves the user's problem.

Lauren describes the shift directly:

> "our code review process has now really shrunk into looking at verification artifacts instead"
> <cite>Lauren Tan, All Code Is Slop (Except Mine)</cite>

The diff is still there, but it's no longer where trust comes from. Two rules keep this honest: the agent that wrote the code is never the only one who verifies it, and any new commit means verifying again.

## The verification phase, organized

<a href="https://maikotrindade.com/public/img/verification-phase-coding-agents.png" target="_blank" rel="noopener" title="Full-size verification phase diagram"><img src="https://maikotrindade.com/public/img/verification-phase-coding-agents.png" width="720" height="501" style="max-width: 100%; height: auto;" alt="Verification phase workflow for coding agents: an agent change passes lint and types, unit and component tests, integration and contract tests, then AI-driven end-to-end tests with agent-device and Maestro. Screenshot tests and observability feed an evidence bundle that a verifier agent and a human review before merge, with findings looping back to the agent."/></a>

1. **Constrain.** Lint rules, types, and architecture make whole classes of bugs impossible.
2. **Run the fast tests.** Unit, component, integration, contract, and design system tests on every change.
3. **Verify on a real app.** The agent drives the app with agent-device, then saves the path as a Maestro flow.
4. **Collect evidence.** Videos, screenshots, accessibility snapshots, logs, traces, and observability data go on the PR.
5. **Review by AI, then by a human.** A verifier agent checks the evidence. A human judges visuals, accessibility, and performance.
6. **Merge, or loop back.** Findings go back to the agent, and a new commit means verifying again.

Lauren warned that automating this loop before the codebase is in good shape just produces more slop, faster. Her team spent months on constraints and verification before letting agents merge most of their own PRs. That's the order that works: earn the trust first, then hand over the autonomy.

For the mobile side of this, I also wrote about <a href="https://maikotrindade.com/ai-agents/engineering/2026/11/02/why-coding-agents-struggle-mobile-harness.html" target="_blank" rel="noopener" title="Why coding agents struggle with mobile development">why coding agents struggle with mobile, and the harness that fixes it</a>, and about <a href="https://maikotrindade.com/ai-agents/engineering/2026/07/24/loop-engineering-verifying-ai-written-code-no-middleman.html" target="_blank" rel="noopener" title="Loop engineering in practice: verifying AI-written code">verifying AI-written code in practice</a>.

## References

- Lauren Tan, <a href="https://www.youtube.com/watch?v=O_zcc6Xl12g" target="_blank" rel="noopener noreferrer" title="All Code Is Slop (Except Mine) by Lauren Tan, AI Engineer on YouTube">All Code Is Slop (Except Mine)</a>, AI Engineer Code Summit, November 2026 (video), and the <a href="https://ai.engineer/code/2026/talks/lauren-tan" target="_blank" rel="noopener noreferrer" title="AI Engineer Code 2026 talk page for Lauren Tan">talk page</a>
- Lauren Tan (@poteto), <a href="https://x.com/poteto/status/2111133080526495985" target="_blank" rel="noopener noreferrer" title="Lauren Tan (poteto) post on X">post on X</a>
- AI IDE List, <a href="https://aiidelist.com/blog/lauren-tan-grok-bot-pstack-workflow" target="_blank" rel="noopener noreferrer" title="Lauren Tan's Grok Bot Workflow: Chief of Staff, Cloud Agents, and pstack">Lauren Tan's Grok Bot Workflow: Chief of Staff, Cloud Agents, and pstack</a>, September 2026
- Flavio Copes, <a href="https://flaviocopes.com/pstack.md" target="_blank" rel="noopener noreferrer" title="A deep dive into pstack by Flavio Copes">A deep dive into pstack</a>, August 2026
- Callstack, <a href="https://github.com/callstack/agent-device" target="_blank" rel="noopener noreferrer" title="agent-device on GitHub">agent-device</a>
- <a href="https://maestro.dev/" target="_blank" rel="noopener noreferrer" title="Maestro mobile UI testing">Maestro</a>, <a href="https://callstack.github.io/react-native-testing-library/" target="_blank" rel="noopener noreferrer" title="React Native Testing Library documentation">React Native Testing Library</a>, <a href="https://fast-check.dev/" target="_blank" rel="noopener noreferrer" title="fast-check property-based testing">fast-check</a>, and <a href="https://docs.pact.io/" target="_blank" rel="noopener noreferrer" title="Pact contract testing documentation">Pact</a>
- Diagram made with <a href="https://github.com/tt-a1i/archify" target="_blank" rel="noopener noreferrer" title="Archify diagram tool on GitHub">Archify</a>
