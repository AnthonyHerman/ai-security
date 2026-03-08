---
description: Add a new resource link to the AI security compendium with proper title and classification
argument-hint: <url>
allowed-tools: [WebFetch, Read, Edit, Write, Glob, Grep, AskUserQuestion]
---

# Add Resource

You are adding a new resource link to the AI security compendium.

The user provided: $ARGUMENTS

## Step 1: Fetch the Page Title

Use WebFetch to visit the URL and extract a suitable title for the markdown hyperlink.

**Title selection priority:**
- Blog post: use the article/post title
- arXiv paper: use the paper title (not the arXiv ID)
- GitHub repo: use the repo description if it's descriptive; otherwise use the repo name with a brief summary
- Tweet/X post: write a brief summary of the post content as the link text
- Product/landing page: use the main heading or product name with a brief descriptor
- PDF: extract the document title if possible

If the page is unreachable or blocks automated access, ask the user for a suitable title using AskUserQuestion.

**Title cleanup:**
- Remove trailing site names after pipes or dashes if they add noise (e.g., " | ArXiv" can be dropped, but " - Google Security Blog" may be kept if it adds context)
- Strip leading/trailing whitespace
- Truncate excessively long titles to something readable

## Step 2: Classify the Link

Read the repo structure to determine the correct placement. The categories are:

| Category | File | What belongs here |
|---|---|---|
| Frameworks & Governance | `frameworks-and-governance/README.md` | Risk frameworks, standards, policy, compliance, regulations |
| Architecture | `architecture/README.md` | Secure AI design patterns, threat modeling |
| Prompt Security | `prompt-security/README.md` | Prompt injection, jailbreaking, prompt hardening |
| Agent Security - Identity/NHI | `agent-security/README.md` (under "Agentic Identity / NHI") | Agent identity, OAuth for agents, NHI, authentication |
| Agent Security - Frameworks/Tools | `agent-security/README.md` (under "Agent Security Frameworks and Tools") | Agent frameworks, tools, general agent security |
| Agent Security - Research | `agent-security/README.md` (under "Research") | Academic papers specifically about agent security |
| MCP | `agent-security/mcp/README.md` | MCP protocol, gateways, scanners, MCP-specific tooling |
| Coding Security | `coding-security/README.md` | Secure coding, SAST, vibe coding security, coding assistants, secrets management |
| Red Teaming | `red-teaming/README.md` | Offensive AI security, attack tools, red team methodologies |
| Prevention & Detection | `prevention-and-detection/README.md` | Guardrails, firewalls, runtime protection, honeypots, defensive tools |
| Supply Chain | `supply-chain/README.md` | AI/ML supply chain risks, model poisoning, dependency risks |
| Benchmarks | `benchmarks/README.md` | Benchmarks, datasets, evaluation frameworks |
| Research | `research/README.md` | Academic papers and surveys (general AI security) |
| General Reading | `general-reading/README.md` | Blog posts, talks, opinion pieces, commentary |

### CRITICAL: Confidence Requirement

You must be **certain** about the classification. Evaluate honestly:

- **If the link clearly fits one category**: proceed to Step 3.
- **If the link could fit 2+ categories roughly equally**: STOP. Do NOT guess. Instead:
  1. Tell the user which categories are candidates and why.
  2. Suggest which one you'd lean toward and explain your reasoning.
  3. Also consider whether a new subsection or category might be appropriate -- if so, propose the section name and file path.
  4. Use AskUserQuestion to get the user's decision before proceeding.
- **If the link doesn't fit any existing category well**: STOP. Do NOT force it. Instead:
  1. Explain that no existing category is a clean fit.
  2. Propose a new category name and where it would live (directory + README.md).
  3. Ask the user whether to create it or place the link somewhere existing.

**Examples of ambiguity that MUST be escalated:**
- A blog post about a new prompt injection attack (general-reading? prompt-security? research?)
- A tool that does both red teaming and detection (red-teaming? prevention-and-detection?)
- An academic paper about MCP security (research? agent-security/mcp?)

When in doubt, ask. Never guess.

## Step 3: Read the Target File

Read the target README.md file to understand its current structure and subsections. Determine the correct subsection to append the link to.

## Step 4: Add the Link

Append the formatted link to the end of the appropriate subsection in the target file:

```markdown
- [Page Title](https://the-url.com)
```

Use the Edit tool to make the change. Do not rewrite the entire file.

## Step 5: Confirm

Report to the user:
- The title extracted
- The file and section where the link was added
- The formatted markdown line that was inserted
