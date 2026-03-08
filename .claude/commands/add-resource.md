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

You must be **certain** about each classification. Evaluate honestly:

- **If a link clearly fits one category**: mark it as resolved.
- **If a link could fit 2+ categories roughly equally**: mark it as ambiguous.
- **If a link doesn't fit any existing category well**: mark it as uncategorized.

After classifying all links, present a summary table showing each URL, its title, and its proposed category. If **any** links are ambiguous or uncategorized, gather them into a **single** AskUserQuestion call:
- For ambiguous links: list the candidate categories, your recommendation, and whether a new subsection might be appropriate.
- For uncategorized links: propose a new category name and location.

Do NOT proceed to editing until all classifications are resolved.

**Examples of ambiguity that MUST be escalated:**
- A blog post about a new prompt injection attack (general-reading? prompt-security? research?)
- A tool that does both red teaming and detection (red-teaming? prevention-and-detection?)
- An academic paper about MCP security (research? agent-security/mcp?)

When in doubt, ask. Never guess.

## Step 3: Read Target Files

Read each unique target README.md file to understand its current structure and subsections. If multiple links go to the same file, only read it once.

## Step 4: Add All Links

For each link, append it to the end of the appropriate subsection in its target file:

```markdown
- [Page Title](https://the-url.com)
```

Use the Edit tool to make each change. Do not rewrite entire files.

## Step 5: Commit and Push

Use Bash to git add all modified files and create a single commit. Use the message format:
- For a single link: `Add resource: <title>`
- For multiple links: `Add <N> resources`

Then push to the current branch.

## Step 6: Confirm

Present a summary table to the user with columns:
- Title
- Category/file
- Markdown line inserted

Include the commit hash at the end.
