# AI Security Resources

A curated collection of resources covering AI security, LLM safety, prompt injection, agent security, secure coding practices, and related topics.

---

## Table of Contents

### Foundations
- [Frameworks and Standards](foundations/frameworks-and-standards/README.md) -- Risk frameworks, standards, and foundational security references
- [Governance and Policy](foundations/governance-and-policy/README.md) -- Compliance, AI policy, legal, and trust
- [Threat Modeling](foundations/threat-modeling/README.md) -- Threat modeling frameworks, tools, and methodologies
- [Architecture](foundations/architecture/README.md) -- Secure AI design patterns and principles

### Attacks
- [Prompt Injection](attacks/prompt-injection/README.md) -- Taxonomy, techniques, datasets, and defenses
- [Jailbreaking](attacks/jailbreaking/README.md) -- Jailbreaking techniques and research
- [Model Attacks](attacks/model-attacks/README.md) -- Poisoning, backdoors, extraction, and adversarial ML
- [Supply Chain](attacks/supply-chain/README.md) -- Dependency attacks, model integrity, and signing
- [Incidents](attacks/incidents/README.md) -- Real-world breaches, exploits, and case studies

### Defense
- [Guardrails and Firewalls](defense/guardrails-and-firewalls/README.md) -- Guardrails, firewalls, and runtime protection
- [Sandboxing and Isolation](defense/sandboxing-and-isolation/README.md) -- Runtime containment and code execution security
- [Detection and Monitoring](defense/detection-and-monitoring/README.md) -- Vulnerability scanners and threat detection
- [Secrets Management](defense/secrets-management/README.md) -- Protecting secrets from AI agents
- [Honeypots and Deception](defense/honeypots-and-deception/README.md) -- Honeypots and adversary engagement
- [Anti-Crawling](defense/anti-crawling/README.md) -- Tarpits, cloaking, data poisoning, and crawler access control

### Agents
- [Agent Security](agents/agent-security/README.md) -- Agent-specific security concerns and threats
- [Agent Identity](agents/agent-identity/README.md) -- OAuth, NHI, authentication, and authorization
- [MCP (Model Context Protocol)](agents/mcp/README.md) -- Gateways, scanners, research, and tooling
- [Agent Frameworks](agents/agent-frameworks/README.md) -- General agent frameworks, platforms, and tools

### Coding
- [Secure Coding](coding/secure-coding/README.md) -- Rules files, vibe coding security, and secure prompt engineering
- [Code Analysis](coding/code-analysis/README.md) -- SAST, code review, and vulnerability scanning
- [Coding Tools](coding/coding-tools/README.md) -- IDE integrations, copilots, and assistants

### Research
- [Papers](research/papers/README.md) -- Academic papers and surveys
- [Benchmarks](research/benchmarks/README.md) -- Evaluation frameworks and datasets
- [Safety and Alignment](research/safety-and-alignment/README.md) -- AI safety, alignment, and privacy

### Practice
- [Red Teaming](practice/red-teaming/README.md) -- Offensive AI security, tools, and methodologies
- [Engineering Patterns](practice/engineering-patterns/README.md) -- Harness engineering and building patterns
- [Privacy](practice/privacy/README.md) -- Data leakage, PII protection, and exfiltration

### General
- [General Reading](general/README.md) -- Blog posts, talks, opinion, and commentary

---

## Lists and Aggregators

- [Awesome LLM Security (corca-ai)](https://github.com/corca-ai/awesome-llm-security)
- [Awesome LLM Safety](https://github.com/ydyjya/Awesome-LLM-Safety)
- [Awesome LLM Security (christiancscott)](https://github.com/christiancscott/awesome-LLM-security)
- [Awesome LLM Supply Chain Security](https://github.com/ShenaoW/awesome-llm-supply-chain-security)
- [Awesome LLMSecOps](https://github.com/wearetyomsmnv/Awesome-LLMSecOps)
- [Awesome LLM Agent Security](https://github.com/wearetyomsmnv/Awesome-LLM-agent-Security)
- [Awesome LM-SSP](https://github.com/ThuCCSLab/Awesome-LM-SSP)
- [System Prompt Leaks](https://github.com/asgeirtj/system_prompts_leaks)
- [AI Security Forum Quick List](https://aisecurityforum.substack.com/p/quick-list-of-high-impact-ai-security)
- [Awesome AI Security (TalEliyahu)](https://github.com/TalEliyahu/Awesome-AI-Security)

## System Prompts

- [System Prompts and Models of AI Tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

## Prompt Design

- [Google Vertex AI - Introduction to Prompt Design](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design)
- [Learn Prompting](https://learnprompting.org/docs/introduction)
- [PromptZ2H](https://promptz2h.com/)

## Claude Code Skills

This repo includes custom [Claude Code](https://claude.com/claude-code) slash commands for managing the compendium:

- `/add-resource <url> [url2] ...` -- Fetch titles, classify links into the correct category, and commit them to the repo.
- `/search-resources <query>` -- Search across all compendium files for resources matching a keyword or topic.
