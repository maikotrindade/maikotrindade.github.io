---
layout: post
title: "Jev: A Decision Model for the Boring, Important Parts of Your Pipeline"
date: 2026-10-15
published: true
categories: [ai-agents, llm]
tags: [Jev, TypeSafe, LLM, Classification, AIAgents, StructuredOutput]
description: "What Jev, TypeSafe AI's type-safe decision model, is good for, what changed in Jev 1.14, and how to use it for cheap classification next to an LLM."
keywords: "Jev, TypeSafe AI, Jev 1.14, decision model, System One model, LLM classification, structured output"
---

Most of the LLM calls I've put in production aren't really asking the model to write anything. They're asking it to decide: is this ticket urgent, which bucket does this PR belong in, does this comment need a reply. **Jev**, the first model from TypeSafe AI, is built for exactly that kind of call. It doesn't generate text at all. It returns typed values, and after reading through the Jev 1.14 release notes and Claire Vo's beginner episode on it, I think it's worth a closer look for anyone building agents or data pipelines.

### What Jev actually is

TypeSafe calls Jev a *System One Model*. The name borrows from the fast, intuitive half of Kahneman's thinking model, and the idea is that a lot of software needs quick judgment calls, not essays. TypeSafe spent about two years in stealth building it and describes the company as building "machine-native intelligence infrastructure for automation."

The API shape is simple. You send a `state` (your data, as text or JSON) and a set of named `questions`. Each question has a type, and Jev answers all of them in parallel against the same state. According to the <a href="https://docs.typesafe.ai/introduction" target="_blank" rel="noopener noreferrer" title="TypeSafe AI Jev documentation introduction">Jev docs</a>, there are three main question types:

- **choice**: pick one label from a list you define. Returns the `choice`, per-label `probabilities`, and a `confidence`.
- **score**: rate the state on an ordered rubric, lowest to highest. Returns a `score`, `probabilities`, and `confidence`.
- **noul**: is this statement true? Returns a single number between 0 and 1.

Because each question is evaluated independently, adding more questions to one request barely changes latency. That's a nice property. You can ask "which department?", "how frustrated is the customer?" and "is this urgent?" in a single round trip.

Here's roughly what a request looks like, based on the schema in the <a href="https://docs.typesafe.ai/introduction/quickstart" target="_blank" rel="noopener noreferrer" title="Jev API quick start guide">quick start guide</a>:

```bash
curl https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-latest",
    "state": "The app crashes every time I open settings. Third time reporting this!",
    "questions": {
      "department": {
        "type": "choice",
        "instructions": "Which team should handle this ticket?",
        "criteria": {
          "billing": "Payments, invoices, refunds",
          "technical": "Bugs, crashes, performance"
        }
      },
      "frustration": {
        "type": "score",
        "instructions": "How frustrated is the customer?",
        "criteria": ["Calm", "Annoyed", "Very frustrated"]
      },
      "is_urgent": {
        "type": "noul",
        "instructions": "This ticket needs a response today."
      }
    }
  }'
```

The response comes back keyed by your question IDs, each with its typed answer and probabilities, plus token usage. There's no parsing of free text, no "please respond in JSON" prompt, and no retry loop for malformed output. There are official SDKs too (`pip install typesafe-sdk` and `npm install @typesafe-ai/sdk`) if you'd rather not hand-roll HTTP.

### Why it's interesting: the price

The number that got my attention came from Claire Vo's <a href="https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and" target="_blank" rel="noopener noreferrer" title="How I AI: Jev for beginners, how to use it and what to build">How I AI episode on Jev for beginners</a>. Jev costs 4 cents per million input tokens, and there's no output charge. Since the output is just a handful of numbers and labels, that's most of the bill.

At that price, classification stops being something you budget for. Vo ran Jev over 1,700 pull requests for 9 cents and used pairwise clustering to see where her engineering time was actually going. That's a task I'd normally skip because it isn't worth a few dollars of GPT calls plus the time spent cleaning up the outputs. At 9 cents, you just do it.

### What people are building with it

The examples from the episode are a good map of where a decision model fits:

- **PR categorization**: the 1,700 PRs above, grouped into themes to show where effort went.
- **Personal meta-analysis**: running Jev over your own local Claude Code and Codex sessions to see patterns in how you work with agents.
- **Gmail triage**: Jev scores incoming email, and a regular LLM drafts the follow-ups only for the ones that matter.
- **Product insights graph**: in ChatPRD, 1,100 signals turned into around 200,000 classifications.
- **Audience dashboard**: a searchable dashboard built from 4,500 YouTube comments for close to nothing.
- **Voice-to-color emotion app**: a real-time demo pairing Jev with the OpenAI Realtime Voice API.

The pattern across all of them is the same. Jev handles the high-volume scoring, routing and labeling. A general-purpose LLM handles anything that needs words. Vo mentions she doesn't really use Jev alone anymore, and that matches how I'd use it. It's a cheap, fast filter in front of an expensive model, not a replacement for one.

If you've read my post on <a href="https://maikotrindade.com/ai-agents/engineering/2026/07/02/loop-engineering-autonomous-agents.html" target="_blank" rel="noopener" title="Loop Engineering: designing the control loop behind autonomous agents">designing the control loop behind autonomous agents</a>, this is the "should I keep going?" and "which tool next?" kind of decision. Having those come back as a typed value with a probability attached makes termination conditions and routing a lot easier to reason about than parsing a sentence.

### What's new in Jev 1.14

TypeSafe published the <a href="https://typesafe.ai/blog/jev-1-14" target="_blank" rel="noopener noreferrer" title="Jev 1.14 release notes from TypeSafe AI">Jev 1.14 release notes</a> on October 14, 2026, framed around two audiences: builders who need production reliability, and dreamers who want to experiment. Their answer is a set of "danger zone" flags. Experimental features sit behind API headers, so you have to opt in explicitly, and TypeSafe is clear that they aren't ready for production.

#### Composable images (danger zone)

It turns out Jev 1.13 was already multimodal, it just wasn't advertised. Now you can add images through a find-and-replace in `assets`, and reference them in `state`, `instructions` or `criteria`. Turn it on with:

```bash
TypeSafe-Danger-Zone-Images: true
```

TypeSafe's own advice is worth repeating: every model, Jev included, does worse on multimodal input than on pure text. Break your questions into the simplest pieces you can.

#### The new `box` type

This one is only enabled for `jev-1.14.0`. It returns a single bounding box, and it's the first output type that isn't just a smarter `if` statement. I read it as a hint about where System One models are heading: still typed and constrained, but answering more than "which one?" or "how much?".

#### Longer context (danger zone)

Jev can handle more context than the production limit allows. TypeSafe capped it on purpose because reliability drops on long inputs. You can lift the cap with:

```bash
TypeSafe-Danger-Zone-Long-Context: true
```

They still recommend keeping context short, and honestly that's good advice for any classifier. If the decision depends on 50 pages of input, it's probably more than one decision.

#### Model aliases and deprecation

- `jev-1.14.0` is available now under the `jev-preview` alias. Improvements are small and broad, with multilingual support expected to gain the most.
- `jev-latest` moves to 1.14.0 one week after the announcement.
- `jev-1.13.0` stays around for a while. The notice gives 60 days for 1.13.0 and 30 days for 1.14.0, with a formal deprecation policy promised before that kicks in.

If you're in production, pin a version. Pointing a pipeline at `jev-latest` and letting a model swap happen under you is a classic way to get a silent shift in your label distribution.

#### Opt-in data sharing and an internal benchmark

You can now opt in to let your queries help TypeSafe find model weaknesses. They say they still won't train on your queries. They also shared an internal estimate of developer-relevant intelligence, with a lot of caveats: it compares only open-weight models, the methodology will change, and it's probably biased toward Jev. Their own advice is to trust your evals over theirs, which I appreciate.

### Should you try it?

If you have a pipeline where an LLM is being used as a glorified `when` expression, yes, probably. Ticket routing, content moderation, lead scoring, log triage, agent routing. Those are the places where typed outputs and near-zero cost add up fast.

I'd start small. Pick one classification step you already run with a general LLM, write the same questions as Jev `choice` or `score` types, and compare the outputs on a few hundred real examples. Look at the `confidence` values too. Low-confidence answers are a natural place to hand off to a bigger model or a human.

And I'd leave the danger zone headers alone in anything that matters, at least for now. TypeSafe is telling you they're rough, and it's nice when a vendor says that out loud.
