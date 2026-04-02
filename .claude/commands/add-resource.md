---
description: Add a new resource link to the AI security compendium with proper title and classification
argument-hint: <url> [url2] [url3] ...
allowed-tools: [WebFetch, Read, Edit, Write, Glob, Grep, AskUserQuestion, Bash]
---

# Add Resource

You are adding a new resource link to the AI security compendium.

The user provided: $ARGUMENTS

Split the arguments by spaces to extract one or more URLs. Process all URLs through the steps below.

## Step 0: Pull Latest Changes

Run `git pull` to ensure the local branch is up to date before making changes.

## Step 1: Fetch Page Titles

For each URL, use WebFetch to extract a suitable title for the markdown hyperlink. **Fetch all URLs in parallel** to save time.

**Title selection priority:**
- Blog post: use the article/post title
- arXiv paper: use the paper title (not the arXiv ID)
- GitHub repo: use the repo description if it's descriptive; otherwise use the repo name with a brief summary
- Tweet/X post: write a brief summary of the post content as the link text
- Product/landing page: use the main heading or product name with a brief descriptor
- PDF: extract the document title if possible

If a page is unreachable or blocks automated access, ask the user for a suitable title using AskUserQuestion.

**Title cleanup:**
- Remove trailing site names after pipes or dashes if they add noise (e.g., " | ArXiv" can be dropped, but " - Google Security Blog" may be kept if it adds context)
- Strip leading/trailing whitespace
- Truncate excessively long titles to something readable

## Step 2: Classify All Links

Read the repo structure to determine the correct placement for each URL. The categories are:

| Category | File | What belongs here |
|---|---|---|
| Frameworks & Standards | `foundations/frameworks-and-standards/README.md` | Risk frameworks, standards (NIST, OWASP, MITRE ATLAS) |
| Governance & Policy | `foundations/governance-and-policy/README.md` | Compliance, AI policy, legal, trust |
| Threat Modeling | `foundations/threat-modeling/README.md` | Threat modeling frameworks, tools, methodologies |
| Architecture | `foundations/architecture/README.md` | Secure AI design patterns, principles |
| Prompt Injection | `attacks/prompt-injection/README.md` | Prompt injection taxonomy, techniques, datasets, defenses |
| Jailbreaking | `attacks/jailbreaking/README.md` | Jailbreaking techniques, research |
| Model Attacks | `attacks/model-attacks/README.md` | Poisoning, backdoors, extraction, adversarial ML |
| Supply Chain | `attacks/supply-chain/README.md` | Dependency attacks, model integrity, signing |
| Incidents | `attacks/incidents/README.md` | Real-world breaches, exploits, case studies |
| Guardrails & Firewalls | `defense/guardrails-and-firewalls/README.md` | Guardrails, firewalls, runtime protection |
| Sandboxing & Isolation | `defense/sandboxing-and-isolation/README.md` | Runtime containment, sandboxing, code execution |
| Detection & Monitoring | `defense/detection-and-monitoring/README.md` | Vulnerability scanners, security platforms, threat detection |
| Secrets Management | `defense/secrets-management/README.md` | Protecting secrets from AI agents |
| Honeypots & Deception | `defense/honeypots-and-deception/README.md` | Honeypots and adversary engagement |
| Agent Security | `agents/agent-security/README.md` | Agent-specific security concerns, threats |
| Agent Identity | `agents/agent-identity/README.md` | OAuth, NHI, authentication, authorization |
| MCP | `agents/mcp/README.md` | MCP protocol, gateways, scanners, tooling |
| Agent Frameworks | `agents/agent-frameworks/README.md` | General agent frameworks, platforms, tools |
| Secure Coding | `coding/secure-coding/README.md` | Rules files, vibe coding security, secure prompt engineering |
| Code Analysis | `coding/code-analysis/README.md` | SAST, code review, vulnerability scanning |
| Coding Tools | `coding/coding-tools/README.md` | IDE integrations, copilots, assistants |
| Research Papers | `research/papers/README.md` | Academic papers and surveys |
| Benchmarks | `research/benchmarks/README.md` | Evaluation frameworks and datasets |
| Safety & Alignment | `research/safety-and-alignment/README.md` | AI safety, alignment, privacy |
| Red Teaming | `practice/red-teaming/README.md` | Offensive AI security, attack tools, methodologies |
| Engineering Patterns | `practice/engineering-patterns/README.md` | Harness engineering, building patterns |
| Privacy | `practice/privacy/README.md` | Data leakage, PII protection, exfiltration |
| General Reading | `general/README.md` | Blog posts, talks, opinion pieces, commentary |

### CRITICAL: Confidence Requirement

You must be **certain** about each classification. Evaluate honestly:

- **If a link clearly fits one category**: mark it as resolved.
- **If a link could fit 2+ categories roughly equally**: mark it as ambiguous.
- **If a link doesn't fit any existing category well**: mark it as uncategorized.

After classifying all links, present a summary table showing each URL, its title, and its proposed category. If **any** links are ambiguous or uncategorized, gather them into a **single** AskUserQuestion call:
- For ambiguous links: list the candidate categories, your recommendation, and whether a new subsection might be appropriate.
- For uncategorized links: propose a new category name and location.

Do NOT proceed to editing until all classifications are resolved.

**Examples of ambiguity that MUST be escalated:**
- A blog post about a new prompt injection attack (general? attacks/prompt-injection? research?)
- A tool that does both red teaming and detection (practice/red-teaming? defense/detection-and-monitoring?)
- An academic paper about MCP security (research/papers? agents/mcp?)

When in doubt, ask. Never guess.

## Step 3: Read Target Files

Read each unique target README.md file to understand its current structure and subsections. If multiple links go to the same file, only read it once.

## Step 4: Add All Links

For each link, append it to the end of the appropriate subsection in its target file:

```markdown
- [Page Title](https://the-url.com)
```

Use the Edit tool to make each change. Do not rewrite entire files.

## Step 5: Sync Obsidian Vault

Run `python3 scripts/sync-vault.py` to regenerate the Obsidian vault from the updated READMEs.

## Step 6: Commit and Push

Use Bash to git add all modified files (including vault changes) and create a single commit. Use the message format:
- For a single link: `Add resource: <title>`
- For multiple links: `Add <N> resources`

Then push to the current branch.

## Step 7: Confirm

Present a summary table to the user with columns:
- Title
- Category/file
- Markdown line inserted

Include the commit hash at the end.
