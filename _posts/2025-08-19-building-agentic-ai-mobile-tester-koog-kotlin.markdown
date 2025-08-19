---
layout: post
title: "Building an Agentic AI Mobile Tester with Koog and Kotlin"
date: 2025-08-19
published: true
categories: [AI, Kotlin, Android, Development, Agents]
tags: [Koog, Kotlin, AI, Android, Agentic, Testing, Compose]
---

Testing Android apps is often repetitive, time-consuming, and hard to scale. Recently, I started experimenting with **agentic AI** to automate mobile testing—combining Kotlin, Koog, and LLMs to build a smart tester that can execute real end-to-end scenarios.  

The result is my new project: **[Koog - Agentic Mobile Tester](https://github.com/maikotrindade/mobile-tester-agent)**.  

---

## Why I Built This
As an Android developer, I’ve used Espresso, UIAutomator, and other frameworks. They’re powerful, but still rigid: you need to write detailed test scripts and keep them updated. I wanted to explore whether an **AI agent** could take high-level goals like _“Log in and navigate to the profile screen”_ and figure out the steps automatically.

---

## How It Works
The project is powered by **Koog.ai** and **Kotlin**, using an **LLM as the reasoning engine** (options include Gemini, Llama, GPT, or Gwen). Here’s the flow:

1. **User Input (Frontend Dashboard)**  
   - Users create test scenarios (goals & steps) via a ReactJS dashboard.  
   - The site was designed with [Stitch](https://stitch.withgoogle.com/) and stores data in **Cloud Firestore**.  
   - Users can also tweak AI agent parameters like:  
     - Model (Gemini, GPT, etc.)  
     - Temperature  
     - Max iterations  

   👉 [Frontend Repo](https://github.com/maikotrindade/mobile-tester-agent-frontend)

2. **Ktor API & Koog Agent (Backend)**  
   - The AI tester runs inside a **Ktor-based API** in Kotlin.  
   - Scenarios are passed to the Koog agent, which uses **agentic reasoning** to decide the sequence of actions.  
   - The agent is connected to an Android emulator or physical device through **ADB tools**.  
   - Results are collected and turned into **test execution reports**.  

   👉 [Agent Repo](https://github.com/maikotrindade/mobile-tester-agent)

3. **Sample Android App**  
   - To showcase the system, I created a simple demo Android app.  
   - The agent can interact with it and validate flows end-to-end.  

   👉 [Sample App Repo](https://github.com/maikotrindade/mobile-tester-agent-sample-app)

---

## Example Flow
- User defines a scenario:  
  _“Tap Add Post button → Input "some text" in the Description → Tap Create Post button”_  

- The AI agent receives it, plans the steps, and uses **ADB actions** (tap, type, scroll, assert text).  
- A report is generated with success/failure details.  

No need to maintain test scripts—just provide the goal.  

<img src="https://maikotrindade.com/public/img/ai-agentic-mobile-tester-koog.gif" width="450" height="280" alt="AI Agentic Mobile Tester"/>

---

## Why Kotlin + Koog?
Kotlin gave me the flexibility to build a clean API with Ktor and manage complex agent logic easily. Koog.ai, with its **Model Context Protocol (MCP)** integration and agentic design, allowed me to connect the LLM with Android tooling like ADB seamlessly.  

This mix of **Kotlin, LLMs, and Android dev tools** opens a new way of thinking about mobile testing: instead of scripting, you describe intentions.

---

## What’s Next
- Improving reporting (screenshots, structured logs).  
- Expanding to multi-app flows.  
- Exploring CI/CD integration for real-world teams.  

---

## Links
- 🔗 [Koog - Agentic Mobile Tester (Agent)](https://github.com/maikotrindade/mobile-tester-agent)  
- 🔗 [Frontend Dashboard](https://github.com/maikotrindade/mobile-tester-agent-frontend)  
- 🔗 [Sample Android App](https://github.com/maikotrindade/mobile-tester-agent-sample-app)  

---

This was a fun experiment mixing **Kotlin + AI agents + Android testing**. If you’re curious about agentic AI, Koog, or just want to rethink mobile testing, I’d love feedback! 🚀
