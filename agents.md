# AI Security Compendium - Agent Instructions

## About This Repo

This is a curated personal compendium of knowledge primarily focused on AI security, but also covering broader AI topics that are valuable to the maintainer. The primary audience is the repo owner. There is **no gatekeeping** on what gets added -- if the owner wants to add something, it gets added. Period.

## Repo Structure

```
ai-security/
  README.md                      # Top-level index with aggregators, system prompts, prompt design
  frameworks-and-governance/     # Risk frameworks, standards, policy, compliance
  architecture/                  # Secure AI design patterns, threat modeling
  prompt-security/               # Prompt injection, jailbreaking, prompt design
  agent-security/                # Agent frameworks, identity, trust, tools
    mcp/                         # MCP gateways, scanners, research, tooling
  coding-security/               # Secure vibe coding, SAST, secrets, platforms
  red-teaming/                   # Offensive AI security, tools, methodologies
  prevention-and-detection/      # Guardrails, firewalls, runtime protection, honeypots
  supply-chain/                  # AI supply chain risks and mitigations
  benchmarks/                    # Benchmarks, datasets, evaluation frameworks
  research/                      # Academic papers and surveys
  general-reading/               # Blog posts, talks, opinion, commentary
  resources/                     # Local PDFs and other files
```

Each directory has a `README.md` with categorized links.

## Adding a New Link

When the user wants to add a link, the agent should:

1. **Fetch the URL** to get the proper page title (use WebFetch or similar). If the URL is unreachable, use whatever title the user provides or extract the best title from the URL itself.

2. **Format as a markdown hyperlink**: `- [Page Title](https://url.example.com)`
   - Strip trailing garbage from titles (e.g. extra whitespace, pipe-separated site names can be kept or trimmed based on readability)
   - For arXiv papers, use the paper title from the page, not the arXiv ID
   - For GitHub repos, use the repo description if the repo name alone isn't descriptive
   - For tweets/X posts, summarize the key content briefly as the link text

3. **Classify the link** into the appropriate category/section:
   - If it's clearly an academic paper (arXiv, conference proceedings) -> `research/README.md`
   - If it's about MCP specifically -> `agent-security/mcp/README.md`
   - If it's about agent identity, NHI, OAuth for agents -> `agent-security/README.md` under "Agentic Identity / NHI"
   - If it's about agent tools, frameworks, or general agent security -> `agent-security/README.md` under "Agent Security Frameworks and Tools"
   - If it's about prompt injection, jailbreaking -> `prompt-security/README.md`
   - If it's about red teaming methodology or offensive tools -> `red-teaming/README.md`
   - If it's about guardrails, firewalls, detection -> `prevention-and-detection/README.md`
   - If it's about supply chain risks -> `supply-chain/README.md`
   - If it's about benchmarks or evaluation -> `benchmarks/README.md`
   - If it's about secure coding, SAST, or coding assistants -> `coding-security/README.md`
   - If it's about frameworks, governance, policy -> `frameworks-and-governance/README.md`
   - If it's about architecture or design patterns -> `architecture/README.md`
   - If it's a blog post, opinion piece, or general commentary -> `general-reading/README.md`
   - **When in doubt, ask the user** which section fits best. Present the top 2-3 candidate sections.

4. **Append the link** to the appropriate section in the target file. Place it at the end of the relevant subsection.

5. **Handle ambiguous or cross-cutting topics**: Some links span multiple categories (e.g., a paper about prompt injection could go in `research/` or `prompt-security/`). Default to the more specific category, but if the user has a preference, follow it.

## Link Format Examples

Good:
```markdown
- [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)
- [Agentic AI Red Teaming Playbook](https://www.pillar.security/agentic-ai-red-teaming-playbook)
- [Dark Visitors - A list of known AI agents on the internet](https://darkvisitors.com/)
```

Bad (bare URLs, no title):
```markdown
- https://arxiv.org/abs/2503.18813
- https://www.pillar.security/agentic-ai-red-teaming-playbook
```

If you encounter existing bare URLs in the repo, offer to convert them to proper hyperlinks when convenient.

## Bulk Additions

When the user provides multiple links at once:
- Process them in parallel where possible
- Group the results by target file/section
- Present the proposed additions for review before committing

## General Guidelines

- Don't argue about whether something belongs in this repo. If the user wants it added, add it.
- Don't restructure or reorganize existing content unless explicitly asked.
- Don't remove or modify existing links unless asked.
- When fetching titles, if a site blocks automated access, fall back gracefully -- use the URL path or ask the user for the title.
- PDFs stored locally go in the `resources/` directory and are linked with relative paths.

## Slash Command

The `/add-resource` command (defined in `.claude/commands/add-resource.md`) automates the full workflow:

```
/add-resource https://example.com/some-article
```

This will:
1. Fetch the page and extract a proper title
2. Classify the link into the correct repo section
3. **If classification is ambiguous** -- stop and ask the user rather than guessing
4. Append the formatted hyperlink to the right file and section
5. Confirm what was added and where
