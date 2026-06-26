# Ralph Loop Context

## Your Mission

You are implementing features for **[PROJECT_NAME]**.

Your goal is to implement features one by one until ALL features pass their validation.

## Important Files

1. **PRD-ralph.md** - The list of features with validation steps and passes status
2. **activity.md** - Log of what has been completed in previous loops
3. **This file (prompt.md)** - Context and rules for each loop

## Rules

1. **ONE feature per loop** - Focus on implementing a single feature completely
2. **Validate with agent-browser** - Use browser automation to verify your work
3. **Update activity.md** - Log what you did at the end of each loop
4. **Update PRD-ralph.md** - Set `passes: true` only when validation succeeds
5. **Exit condition** - Only output "promise complete" when ALL passes=true

## Agent-Browser Commands (Windows + WSL)

```bash
# CRITICAL: Always use bash -c pattern to avoid EAGAIN errors

wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://[WINDOWS_IP]:[PORT]'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
wsl -d Ubuntu -- bash -c "npx agent-browser click e1"
wsl -d Ubuntu -- bash -c "npx agent-browser type e1 'your text here'"
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

**Note:** Element refs use syntax `e1`, `e2` (NOT `@e1`)

## Workflow per Feature

```
1. Read PRD-ralph.md → Find first feature with passes=false
2. Read activity.md → Understand what was done before
3. Implement the feature
4. Start the app if needed (backend + frontend)
5. Open browser with agent-browser
6. Execute validation steps
7. If validation passes:
   - Update PRD-ralph.md: set passes=true
   - Update activity.md: log completion
8. If validation fails:
   - Fix the issue
   - Retry validation
9. Close browser
10. Check if ALL passes=true → output "promise complete" and EXIT
11. Otherwise → loop continues with next feature
```

## Next Action

1. Read activity.md
2. Read PRD-ralph.md
3. Find the first feature with `passes: false`
4. Implement it
5. Validate with agent-browser
6. Update files
7. Continue or exit

---

**REMEMBER:** Only output "promise complete" when every single feature has `passes: true`.
