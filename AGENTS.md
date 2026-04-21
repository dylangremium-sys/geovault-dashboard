# AGENTS.md

## Execution mode
Strict execution only.

## Core rule
If it is not written to disk and committed to git, it does not exist.

## Non-negotiable rules
1. No drift
- Do not add features beyond the approved task
- Do not invent files, routes, or components

2. No assumptions
- Do not assume backend endpoints
- Do not assume env vars
- Do not assume response shapes
- Verify from code only

3. Files or nothing
- Chat output is not implementation
- Plans are not implementation
- Only tracked files count

4. Repo truth first
- Trust the repository state over prior chat claims
- Trust current branches over historical summaries
- Mark anything missing from code as NOT IMPLEMENTED

5. One task at a time
- Complete only the current approved task
- Do not redesign architecture unless explicitly requested
