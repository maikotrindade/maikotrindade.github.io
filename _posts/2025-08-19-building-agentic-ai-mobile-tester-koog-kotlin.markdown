---
layout: post
title: "Building an Agentic AI Mobile Tester with Koog and Kotlin"
date: 2025-08-19
published: true
categories: [AI, Kotlin, Android, Development, Agents]
tags: [Koog, Kotlin, AI, Android, Agentic, Testing, Compose]
description: "How to build an autonomous Android mobile testing agent using Koog and Kotlin, replacing repetitive manual test scripts with LLM-driven end-to-end test execution."
---

Testing Android apps is often repetitive, time-consuming, and hard to scale. Recently, I started experimenting with **agentic AI** to automate mobile testing—combining Kotlin, Koog, and LLMs to build a smart tester that can execute real end-to-end scenarios.  

The result is my new project: **[Koog - Agentic Mobile Tester](https://github.com/maikotrindade/mobile-tester-agent)**.  

---

## Why I Built This
As an Android developer, I’ve used Espresso, UIAutomator, and other frameworks. They’re powerful, but still rigid: you need to write detailed test scripts and keep them updated. I wanted to explore whether an **AI agent** could take high-level goals like _“Log in and navigate to the profile screen”_ and figure out the steps automatically.

---

## How It Works
The project is powered by **Koog.ai** and **Kotlin**, using an **LLM as the reasoning engine** (options include Gemini, Llama, GPT, or Gwen). Here’s the flow:


### [Ktor API & Koog Agent (Backend)](https://github.com/maikotrindade/mobile-tester-agent)

The backend is built with **Ktor** in Kotlin and powered by a custom **Koog agent** (`MobileTestAgent`) plus a toolkit of device actions (`MobileTestTools`).

**Ktor API**
The Ktor server exposes endpoints that receive test scenarios and configuration (LLM model, temperature, iterations). Each request is routed to the `MobileTestAgent`, which runs the scenario with the chosen parameters.

**MobileTestAgent (Koog Agent)**
`MobileTestAgent` encapsulates the Koog agent setup. It translates high-level test goals into an iterative reasoning process, where the LLM plans actions like *"tap login button"* or *"enter text"*. The agent respects limits such as max iterations and temperature to balance creativity and determinism.

**MobileTestTools (Device Interaction)**
`MobileTestTools` provides the executable layer via **ADB commands**. It includes functions for:
- Interactions: `tap()`, `typeText()`, `scroll()`, `swipe()`
- Checks: `assertTextVisible()`, `getUiHierarchy()`
- Utilities: `launchApp()`, `installApk()`, `takeScreenshot()`

These functions are registered as tools within Koog, so when the agent plans an action, Koog calls the corresponding method directly.

**Execution Flow**
- Ktor receives a scenario and sends it to the agent.  
- Koog plans the next step using the LLM.  
- The selected `MobileTestTools` method executes the action on the device.  
- Feedback (UI state, success/failure) is fed back into the agent.  
- This loop continues until the scenario ends or max iterations are hit.  

At the end, a structured report is generated with actions, results, and optional artifacts (like screenshots), and returned to the frontend dashboard.

### [User Input (Frontend Dashboard)](https://github.com/maikotrindade/mobile-tester-agent-frontend)  
   - Users create test scenarios (goals & steps) via a ReactJS dashboard.  
   - The site was designed with [Stitch](https://stitch.withgoogle.com/) and stores data in **Cloud Firestore**.  
   - Users can also tweak AI agent parameters like:  
     - Model (Gemini, GPT, etc.)  
     - Temperature  
     - Max iterations  

### [Sample Android App](https://github.com/maikotrindade/mobile-tester-agent-sample-app)  
   - To showcase the system, I created a simple demo Android app.  
   - The agent can interact with it and validate flows end-to-end.  

---

## Example Flow
- User defines a scenario:  
  _“Tap Add Post button → Input "some text" in the Description → Tap Create Post button”_  

- The AI agent receives it, plans the steps, and uses **ADB actions** (tap, type, scroll, assert text).  
- A report is generated with success/failure details.  

No need to maintain test scripts—just provide the goal.  

<img src="https://maikotrindade.com/public/img/ai-agentic-mobile-tester-koog.gif" width="390" height="240" alt="AI Agentic Mobile Tester"/>

---

### Why Kotlin + Koog?
Kotlin gave me the flexibility to build a clean API with Ktor and manage complex agent logic easily. Koog.ai, with its **Model Context Protocol (MCP)** integration and agentic design, allowed me to connect the LLM with Android tooling like ADB seamlessly.  

This mix of **Kotlin, LLMs, and Android dev tools** opens a new way of thinking about mobile testing: instead of scripting, you describe intentions.

---

### What’s Next
- Improving reporting (screenshots, videos, structured logs).  
- Expanding to iOS and Web end-to-end testing.  
- Exploring CI/CD integration for real-world teams.  

---

### Links
- 🔗 [Koog - Agentic Mobile Tester (Agent)](https://github.com/maikotrindade/mobile-tester-agent)  
- 🔗 [Frontend Dashboard](https://github.com/maikotrindade/mobile-tester-agent-frontend)  
- 🔗 [Sample Android App](https://github.com/maikotrindade/mobile-tester-agent-sample-app)  
- 🔗 [LinkedIn post](https://www.linkedin.com/posts/maikotrindade_ai-aiagents-android-activity-7362894658969985025-02Jw?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAUawAwBJqLuU627P_RUiatzkteEsE66KbY) 

---

This was a fun experiment mixing **Kotlin + AI agents + Android testing**. If you’re curious about agentic AI, Koog, or just want to rethink mobile testing, I’d love feedback, feel free to DM on LinkedIn! 🚀
