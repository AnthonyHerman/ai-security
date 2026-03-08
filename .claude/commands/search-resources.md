---
description: Search the AI security compendium for resources matching a query
argument-hint: <search query>
allowed-tools: [Grep, Read, Glob]
---

# Search Resources

Search the AI security compendium for resources matching the user's query.

The user searched for: $ARGUMENTS

## Step 1: Search

Use Grep to search all `README.md` files in the repository for lines matching the query. Search case-insensitively. Try multiple search strategies in parallel:

1. Grep for the exact query string
2. Grep for individual keywords from the query (if the query has multiple words)

## Step 2: Present Results

For each matching line:
- Show the markdown link as-is (so the user can click it)
- Show which file and section it was found in (derive the section from the nearest `##` heading above the match)

Group results by category/file. If there are no results, say so and suggest alternative search terms the user might try.
