---
layout: post
title: "An Introduction to Edge Computing and Edge AI"
date: 2026-09-14
published: true
categories: [ai, edge-computing]
tags: [EdgeAI, EdgeComputing, OnDeviceAI, SmallLanguageModels, TinyML, HuggingFace, AgTech]
description: "Intro to edge computing and Edge AI: why inference is moving on-device, the newest small models on Hugging Face, AgTech uses, and what research says next."
image: /public/img/edge-ai-intro.png
keywords: "edge computing, edge AI, on-device AI, small language models, Gemma 4, SmolLM3, TinyML, agtech, precision agriculture"
---

Edge computing means running computation close to where data is produced, on a phone, a camera, a gateway in a barn, instead of shipping everything to a data center first. Edge AI is the same idea applied to machine learning: the model runs on (or next to) the device, so predictions happen in milliseconds, keep working offline, and don't send raw data anywhere. This post covers the basics, the small models that make it practical in 2026, a quick look at agriculture, and where the research says things are going.

<img src="https://maikotrindade.com/public/img/edge-ai-intro.png" width="380" height="240" alt="Edge AI diagram: phone, camera, drone and sensor each running a local neural network, loosely connected to a distant cloud"/>

### What edge computing actually is

The cloud model is simple: devices collect data, send it to a big data center, and wait for an answer. That works until it doesn't. Bandwidth costs money, round trips add latency, and some places (a field, a ship, a mine) just don't have a reliable connection.

Edge computing pushes part of that work back toward the source. Weisong Shi and colleagues framed it this way in <a href="https://ieeexplore.ieee.org/document/7488250" target="_blank" rel="noopener noreferrer" title="Edge Computing: Vision and Challenges, IEEE Internet of Things Journal, 2016">Edge Computing: Vision and Challenges</a> (IEEE IoT Journal, 2016), where the "edge" is any computing resource along the path between the data source and the cloud. Mahadev Satyanarayanan's <a href="https://ieeexplore.ieee.org/document/7807196" target="_blank" rel="noopener noreferrer" title="The Emergence of Edge Computing, IEEE Computer, 2017">The Emergence of Edge Computing</a> (IEEE Computer, 2017) adds the idea of *cloudlets*: small data centers one network hop away from users.

In practice there are a few layers:

- **Device edge:** phones, microcontrollers, cameras, drones, cars.
- **Near edge:** gateways, routers, an NVIDIA Jetson sitting in a shed.
- **Far edge / regional:** telecom edge servers and small regional data centers.
- **Cloud:** training, aggregation, anything heavy that isn't time-sensitive.

You don't pick one. Most real systems split the work across tiers.

### From edge computing to Edge AI

Edge AI is what you get when the workload you're moving closer to the data is model inference. Zhou et al. called it "the last mile of AI" in <a href="https://arxiv.org/abs/1905.10083" target="_blank" rel="noopener noreferrer" title="Edge Intelligence: Paving the Last Mile of Artificial Intelligence with Edge Computing">Edge Intelligence: Paving the Last Mile of Artificial Intelligence with Edge Computing</a> (Proceedings of the IEEE, 2019), and the reasons they gave still hold:

- **Latency.** A crop-spraying drone can't wait 400 ms for a server to say "that's a weed".
- **Privacy.** Audio, health data and photos never leave the device.
- **Cost.** No per-token API bill and much less upstream bandwidth.
- **Availability.** It keeps working with no signal.

The catch is obvious: devices have little memory, little power and slow memory bandwidth. So most of Edge AI is about making models smaller without making them dumb. The classic toolbox includes quantization, pruning and distillation (see Han et al.'s <a href="https://arxiv.org/abs/1510.00149" target="_blank" rel="noopener noreferrer" title="Deep Compression paper on arXiv">Deep Compression</a>), plus newer LLM-specific tricks like activation-aware quantization (<a href="https://arxiv.org/abs/2306.00978" target="_blank" rel="noopener noreferrer" title="AWQ: Activation-aware Weight Quantization paper on arXiv">AWQ</a>). Training can also stay distributed: <a href="https://arxiv.org/abs/1602.05629" target="_blank" rel="noopener noreferrer" title="Communication-Efficient Learning of Deep Networks from Decentralized Data (federated learning)">federated learning</a> lets devices improve a shared model without uploading their raw data.

### The newest small models worth knowing

A couple of years ago "on-device LLM" mostly meant a demo. Now the open model hubs have a solid lineup sized for phones and single-board computers. A few I'd look at first on <a href="https://huggingface.co/models" target="_blank" rel="noopener noreferrer" title="Hugging Face model hub">Hugging Face</a>:

- **Gemma 4 E2B / E4B (Google).** The "E" stands for *effective* parameters (about 2.3B and 4.5B). They take text, image and audio input, have a 128K context, and ship as Apache 2.0. Google publishes ready-to-run builds for its on-device runtime in <a href="https://ai.google.dev/edge/litert-lm/models/gemma-4" target="_blank" rel="noopener noreferrer" title="Gemma 4 on LiteRT-LM, Google AI Edge docs">LiteRT-LM</a>, and reports up to 2.2x faster decoding on mobile GPUs with multi-token prediction.
- **SmolLM3 (Hugging Face).** A fully open 3B model trained on 11T tokens, with the data and training recipe published. The <a href="https://huggingface.co/blog/smollm3" target="_blank" rel="noopener noreferrer" title="SmolLM3 announcement on the Hugging Face blog">SmolLM3 write-up</a> is one of the best free explanations of how a small model gets trained.
- **Phi-4-mini (Microsoft).** <a href="https://huggingface.co/microsoft/Phi-4-mini-instruct" target="_blank" rel="noopener noreferrer" title="Phi-4-mini-instruct model card on Hugging Face">Phi-4-mini-instruct</a> is 3.8B, MIT licensed, strong at reasoning for its size. Phi-4-multimodal adds vision and speech.
- **Others worth a look:** Qwen3.5 (0.8B and 4B), Ministral 3, IBM Granite 4.0 Nano, Liquid AI's LFM2.5 and Llama 3.2 1B/3B.

Phones also ship their own: Gemini Nano on Android and Apple's Foundation Models framework on iOS. As an Android developer I find that part interesting, because it changes the question from "can I run a model here?" to "which one is already on the device?".

If you want to try one on your laptop in a minute, llama.cpp can pull a quantized GGUF straight from Hugging Face:

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF -p "Explain edge computing in one sentence."
```

One warning from recent research. The August 2026 study <a href="https://arxiv.org/abs/2608.15693" target="_blank" rel="noopener noreferrer" title="Large Models for Small Devices: Recent Advances and Empirical Analysis of Edge AI Deployment, arXiv 2608.15693">Large Models for Small Devices</a> (Das et al.) measured compression on real hardware and found that no technique wins everywhere. Q5_K_M quantization held up well for question answering, while pruning hurt it badly. For image segmentation the ranking flipped. Pruning also broke k-quant block alignment, made files 21 to 49% *bigger*, and slowed a Raspberry Pi by up to 3.4x. They even found a compressed model with 71% accuracy that was putting 97 of 100 answers in the same class. So benchmark your model on your device, with your data. Paper numbers don't transfer as well as we'd like.

### A quick look at Edge AI in AgTech

Agriculture is probably the best argument for Edge AI. Farms are big, connectivity is bad, margins are thin, and decisions are time-sensitive.

Some places where it's already useful:

- **Plant disease detection** from a phone photo, offline. This line of work goes back to datasets like <a href="https://arxiv.org/abs/1511.08060" target="_blank" rel="noopener noreferrer" title="An open access repository of images on plant health (PlantVillage) on arXiv">PlantVillage</a>, and today runs on MobileNet or EfficientNet-class models.
- **Targeted spraying**, where cameras on the boom tell crop from weed in real time and only spray weeds.
- **Livestock monitoring** with collar sensors and cameras that flag lameness or unusual behavior locally.
- **Soil and irrigation sensors** on microcontrollers that decide when to water without a server.

The March 2026 review <a href="https://arxiv.org/abs/2603.15085" target="_blank" rel="noopener noreferrer" title="Affordable Precision Agriculture: low-cost, low-power Edge AI and TinyML review, arXiv 2603.15085">Affordable Precision Agriculture</a> by Samanta and Saha surveyed 2023 to 2026 work and found a few patterns. Most precision-ag systems still depend on the cloud, which shuts out smallholders. Cheap microcontrollers (ESP32, STM32) dominate the hardware. Quantization shows up in about half the papers, while pruning and hardware-aware architecture search are rarely tried. And most papers don't report RAM, latency or energy, so it's hard to compare anything. Their summary of the direction is "localized inference with centralized training", which matches what I'd expect: train in the cloud, run in the field.

I wrote about the human side of this in <a href="https://maikotrindade.com/ai/sustainability/2026/08/14/ai-beyond-tech-farms-data-center-race.html" target="_blank" rel="noopener" title="AI Beyond Tech: Slower Data Centers, Smarter Human Uses">AI Beyond Tech: farms and the data center race</a>. Edge AI is the technical piece that makes a lot of those ideas affordable.

### The future of Edge AI

So where is this going? The academic work points in a few directions, and they mostly agree.

**Small models become the default, not the fallback.** NVIDIA researchers argue in <a href="https://arxiv.org/abs/2506.02153" target="_blank" rel="noopener noreferrer" title="Small Language Models are the Future of Agentic AI, arXiv 2506.02153">Small Language Models are the Future of Agentic AI</a> (Belcak et al., 2025) that most agent sub-tasks are narrow and repetitive, so a small model is good enough and much cheaper. Large models get called only when needed. That fits the edge perfectly.

**Agents move onto devices.** The survey <a href="https://arxiv.org/abs/2501.03265" target="_blank" rel="noopener noreferrer" title="Cognitive Edge Computing: A Comprehensive Survey on Optimizing Large Models and AI Agents for Pervasive Deployment">Cognitive Edge Computing</a> looks at how reasoning models and autonomous agents can run on constrained hardware, and the broader <a href="https://arxiv.org/abs/2503.06027" target="_blank" rel="noopener noreferrer" title="Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models">Empowering Edge Intelligence</a> survey (later in ACM Computing Surveys) covers the on-device model landscape and its open problems.

**The network becomes part of the model.** <a href="https://arxiv.org/abs/2604.22906" target="_blank" rel="noopener noreferrer" title="Network Edge Inference for Large Language Models: Principles, Techniques, and Opportunities">Network Edge Inference for Large Language Models</a> (2026) argues that the design problem is shifting from "fit everything on one device" to co-designing model, memory, compute and communication across device, edge server and cloud. Think split inference, speculative decoding with a small draft model on the phone, and KV caches that live on a nearby server.

**Measurement gets serious.** Das et al. call for tools that profile prefill and decode separately and recommend a configuration per device. Benchmarks like <a href="https://arxiv.org/abs/2106.07597" target="_blank" rel="noopener noreferrer" title="MLPerf Tiny Benchmark paper on arXiv">MLPerf Tiny</a> started this for microcontrollers. LLMs on phones need the same discipline, because memory bandwidth, not FLOPs, is usually what limits you.

My own take: the cloud isn't going away, it's just becoming the place where models are trained and where the hard 10% of requests go. The other 90% (classify this leaf, summarize this note, answer this simple question) will happen on hardware you already own. For mobile developers that's good news. On-device AI is turning into a normal part of the app, like camera or location, and the people who understand memory, battery and latency on real devices are going to be useful for a long time.

### References

- Shi et al., <a href="https://ieeexplore.ieee.org/document/7488250" target="_blank" rel="noopener noreferrer" title="Edge Computing: Vision and Challenges">Edge Computing: Vision and Challenges</a>, IEEE IoT Journal, 2016
- Satyanarayanan, <a href="https://ieeexplore.ieee.org/document/7807196" target="_blank" rel="noopener noreferrer" title="The Emergence of Edge Computing">The Emergence of Edge Computing</a>, IEEE Computer, 2017
- Zhou et al., <a href="https://arxiv.org/abs/1905.10083" target="_blank" rel="noopener noreferrer" title="Edge Intelligence on arXiv">Edge Intelligence: Paving the Last Mile of AI with Edge Computing</a>, 2019
- Das et al., <a href="https://arxiv.org/abs/2608.15693" target="_blank" rel="noopener noreferrer" title="Large Models for Small Devices on arXiv">Large Models for Small Devices</a>, arXiv, 2026
- Samanta and Saha, <a href="https://arxiv.org/abs/2603.15085" target="_blank" rel="noopener noreferrer" title="Affordable Precision Agriculture on arXiv">Affordable Precision Agriculture</a>, arXiv, 2026
- Belcak et al., <a href="https://arxiv.org/abs/2506.02153" target="_blank" rel="noopener noreferrer" title="Small Language Models are the Future of Agentic AI on arXiv">Small Language Models are the Future of Agentic AI</a>, arXiv, 2025
- <a href="https://arxiv.org/abs/2604.22906" target="_blank" rel="noopener noreferrer" title="Network Edge Inference for LLMs on arXiv">Network Edge Inference for Large Language Models</a>, arXiv, 2026
- Hugging Face, <a href="https://huggingface.co/blog/smollm3" target="_blank" rel="noopener noreferrer" title="SmolLM3 blog post">SmolLM3: smol, multilingual, long-context reasoner</a>
- Google AI Edge, <a href="https://ai.google.dev/edge/litert-lm/models/gemma-4" target="_blank" rel="noopener noreferrer" title="Gemma 4 on LiteRT-LM">Gemma 4 on LiteRT-LM</a>
