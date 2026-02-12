# 🏢 Day 5: Sprint Week — Real Team Workflows

> *Friday morning. Lina has a standup at 9 AM. Fatima filed 5 bug reports overnight. Ahmed is debugging the API. Sara is reviewing PRs. Omar accidentally stashed his entire project. And you? You're about to learn how professionals survive this chaos — every single day.*

**⏱️ Time: ~50 minutes**
**Difficulty: 🔴 Hard**
**⭐ XP Available: 600**

**📍 Prerequisites:** Complete Days 1-4. Be inside `realcompanysteup` on `main`.

---

## 📖 THE STORY SO FAR

> **9:00 AM — Daily Standup**
>
> **Lina:** "Good morning team. Quick updates?"
>
> **Sara:** "I'm finishing the notification system. Should be done by lunch."
>
> **Ahmed:** "Fixing that API timeout bug Fatima found."
>
> **Youssef:** "Setting up staging environment."
>
> **Mehdi:** "Starting the user profile feature."
>
> **Omar:** "I, uh... I was working on something but my code disappeared."
>
> **Sara:** "Did you stash it?"
>
> **Omar:** "I don't know what that word means."
>
> **Sara:** *sighs* "OK. Today we're teaching stash."

---

## 🔬 LAB 1: Git Stash — Pause and Resume Your Work (80 XP)

> *You're halfway through building a feature. Suddenly, Sara calls you: "Drop everything! There's a critical bug in production!"*
>
> *Your code isn't ready to commit. You can't just leave it. What do you do?*

### The Problem:

```
You're on feature/notifications branch
You have UNFINISHED code
You need to switch to main to fix a bug
Git won't let you switch branches with uncommitted changes
```

### The Solution: STASH

> Think of `git stash` as a secret drawer. You throw your messy work in there, handle the emergency, then pull it back out when you're done.

### Step 1: Start working on a feature

```bash
git checkout -b feature/notifications
```

Edit `app.js` — add at the bottom:

```javascript
// Notification System (WORK IN PROGRESS)
function showNotification(message, type) {
    const notif = document.createElement('div');
    notif.className = `notification ${type}`;
    notif.textContent = message;
    document.body.appendChild(notif);
    // TODO: add auto-dismiss
    // TODO: add animation
    // TODO: add sound
}
```

**Check status:**

```bash
git status
```
→ `app.js` is modified but NOT committed.

### Step 2: EMERGENCY! Stash your work

> **Fatima:** "🚨 CRITICAL: The task list doesn't load! Production is broken!"
> **Sara:** "Everyone on main NOW. Mehdi, stash your stuff."

```bash
git stash push -m "WIP: notification system - half done"
```

**Check status:**

```bash
git status
```
→ Clean! Your changes are gone (but safely stored). **+10 XP**

**See what's stashed:**

```bash
git stash list
```
→ `stash@{0}: On feature/notifications: WIP: notification system - half done`

**+10 XP**

### Step 3: Fix the production bug

```bash
git checkout main
git checkout -b hotfix/fix-task-loading
```

Edit `app.js` — add at the bottom:

```javascript
// Hotfix: ensure tasks load on page start
window.addEventListener('DOMContentLoaded', () => {
    renderTasks();
    console.log('Tasks loaded successfully');
});
```

```bash
git add app.js
git commit -m "fix: ensure tasks load on DOMContentLoaded"
git checkout main
git merge hotfix/fix-task-loading
git branch -d hotfix/fix-task-loading
```

> **Fatima:** "Fix is live. Good work, team."

**+20 XP**

### Step 4: Go back to your feature and POP the stash

```bash
git checkout feature/notifications
```

```bash
git stash pop
```

→ Your unfinished notification code is BACK! Like nothing happened.

**+20 XP!**

🏅 **ACHIEVEMENT UNLOCKED: Firefighter — Stashed, fixed a bug, and resumed work!**

### Stash Commands Cheat Sheet:

| Command | What It Does | Analogy |
|---------|-------------|---------|
| `git stash` | Save changes, clean workspace | Shove stuff in a drawer |
| `git stash push -m "desc"` | Save with a label | Label the drawer |
| `git stash list` | See all stashes | Look at all drawers |
| `git stash pop` | Restore + delete stash | Take stuff out, close drawer |
| `git stash apply` | Restore but KEEP stash | Take stuff out, leave drawer open |
| `git stash drop` | Delete a stash | Empty the drawer |

**+20 XP for mastering all stash commands!**

**Clean up:**

```bash
git restore app.js
git checkout main
git branch -D feature/notifications
```

---

## 🔬 LAB 2: Git Blame — CSI: Code Scene Investigation (60 XP)

> *Fatima found a bug. She needs to know WHO wrote the broken code, WHEN, and in WHICH commit. Enter `git blame` — the detective tool.*

> **Fatima:** "Line 15 of `server.py` has a bug. Who wrote it?"
> **Ahmed:** "Don't look at me."
> **Sara:** "It's literally your file, Ahmed."
> **Ahmed:** "...let's check `git blame`."

### Step 1: Blame a file

```bash
git blame server.py
```

**Output looks like:**

```
abc1234 (Mehdi  2026-02-09 10:00:00) # TaskFlow Backend API
abc1234 (Mehdi  2026-02-09 10:00:00) from http.server import HTTPServer
abc1234 (Mehdi  2026-02-09 10:00:00) import json
...
def5678 (Mehdi  2026-02-09 14:30:00)     def do_POST(self):
```

Each line shows: **commit hash** | **author** | **date** | **the code**

**+20 XP**

### Step 2: Blame specific lines

```bash
git blame -L 5,15 server.py
```

→ Only shows blame for lines 5-15. Useful for big files!

**+10 XP**

### Step 3: Find WHY a line was written

When you see a suspicious commit hash, inspect it:

```bash
git show <commit-hash>
```

→ Shows the full commit message and diff. Now you know WHO wrote it, WHEN, and WHY.

**+10 XP**

### When to use blame at TechCorp:

| Situation | `git blame` helps by... |
|-----------|------------------------|
| "Who wrote this weird function?" | Finding the author |
| "When was this line added?" | Finding the date |
| "Why was this written this way?" | Finding the commit message |
| "This used to work, what changed?" | Finding the change |
| "Who do I ask about this code?" | Finding the expert |

**+20 XP**

> **Omar:** "So everyone can see every line I've ever written?"
> **Ahmed:** "Yes."
> **Omar:** "...including the `asdfgh.py` file?"
> **Ahmed:** "ESPECIALLY the `asdfgh.py` file."

---

## 🔬 LAB 3: Git Cherry-Pick — Steal One Commit (80 XP)

> *Ahmed is working on an experimental branch with 5 commits. Only ONE of them has a critical fix you need RIGHT NOW. You don't want all 5 — just that one.*

> **Sara:** "Ahmed, we need your database timeout fix on main. But NOT the experimental caching stuff."
> **Ahmed:** "Just cherry-pick the fix commit."
> **Omar:** "Pick cherries? From a tree? What?"
> **Sara:** "...from a branch, Omar. A GIT branch."

### Step 1: Create Ahmed's experimental branch with multiple commits

```bash
git checkout -b experiment/ahmed-testing
```

```bash
echo "Experiment 1: caching layer" > experiment1.txt
git add experiment1.txt
git commit -m "experiment: try caching layer"

echo "Experiment 2: websockets" > experiment2.txt
git add experiment2.txt
git commit -m "experiment: try websocket support"

echo "CRITICAL FIX: database timeout" > critical-fix.txt
git add critical-fix.txt
git commit -m "fix: resolve database connection timeout issue"

echo "Experiment 3: GraphQL" > experiment3.txt
git add experiment3.txt
git commit -m "experiment: try GraphQL schema"

echo "Experiment 4: microservices" > experiment4.txt
git add experiment4.txt
git commit -m "experiment: microservice architecture POC"
```

5 commits. You ONLY need the `fix: resolve database connection timeout issue`.

### Step 2: Find the commit hash

```bash
git log --oneline -5
```

Copy the hash next to `fix: resolve database connection timeout issue`.

**+15 XP**

### Step 3: Cherry-pick it to main

```bash
git checkout main
git cherry-pick <paste-the-hash-here>
```

**Expected:**
```
[main xyz1234] fix: resolve database connection timeout issue
 1 file changed, 1 insertion(+)
 create mode 100644 critical-fix.txt
```

**+25 XP!**

### Step 4: Verify

```bash
git log --oneline -3
```

→ The fix is on `main`. None of the experiments are.

```bash
ls *.txt
```

→ Only `critical-fix.txt` was brought over. Not the experiment files.

**+20 XP!**

**Clean up:**

```bash
git branch -D experiment/ahmed-testing
```

**+20 XP**

> **Fatima:** "Cherry-pick is great for hotfixes. Take exactly what you need, nothing more."
> **Omar:** "Can I cherry-pick my lunch from someone else's branch?"
> **Everyone:** 😑

---

## 🔬 LAB 4: Git Log Power Moves (40 XP)

> **Sara:** "If you only know `git log --oneline`, you're missing out. Here's what I use every day."

### The Visual Graph (see branches merge):

```bash
git log --oneline --graph --all --decorate
```

→ Beautiful ASCII art of your branch history! **+10 XP**

### Search commits by message:

```bash
git log --oneline --grep="fix"
```

→ Only shows commits with "fix" in the message. **+10 XP**

> **Fatima:** "This is how I find which commits fixed which bugs."

### See commits by author:

```bash
git log --oneline --author="Mehdi"
```

→ Only YOUR commits. Perfect for standup reports!

**+10 XP**

### See files changed in each commit:

```bash
git log --oneline --stat -5
```

→ Shows which files were changed and how many lines. **+10 XP**

---

## 💥 BOSS FIGHT: The Sprint Simulation (200 XP)

> **Lina:** "OK team, here's the sprint scenario. Mehdi — I want to see you handle this entire workflow solo. Consider it your graduation test."
>
> **⏱️ Try to finish in under 15 minutes!**

### The scenario:

```
📋 SPRINT BOARD:

🎫 TICKET-101: Add task priority feature        (Assigned: Mehdi)
🎫 TICKET-102: Fix CSS alignment bug            (Assigned: Mehdi)
🐛 CRITICAL: API error on empty input           (Mid-sprint emergency!)
```

### Phase 1: Start your feature (TICKET-101) — 40 XP

```bash
git checkout main
git pull  # Always pull before starting!
git checkout -b feature/task-priority
```

Edit `app.js` — add:

```javascript
// Task Priority System
function setPriority(taskId, priority) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.priority = priority; // 'low', 'medium', 'high'
        renderTasks();
    }
}

function getPriorityColor(priority) {
    const colors = { low: '#27ae60', medium: '#f39c12', high: '#e74c3c' };
    return colors[priority] || '#95a5a6';
}
```

```bash
git add app.js
git commit -m "feat: add task priority system with color coding"
```

**+40 XP**

### Phase 2: Emergency interrupt! Stash and fix — 50 XP

> **Fatima:** "🚨 CRITICAL: The API crashes when someone submits an empty task title!"

You're mid-feature! Stash it:

```bash
git stash push -m "WIP: task priority feature"
```

Fix the bug:

```bash
git checkout main
git checkout -b hotfix/empty-input-crash
```

Edit `server.py` — add this comment near the top (simulating a fix):

```python
# Input validation: reject empty task titles - Hotfix by Mehdi
```

```bash
git add server.py
git commit -m "fix: reject empty task titles in API input validation"
git checkout main
git merge hotfix/empty-input-crash
git branch -d hotfix/empty-input-crash
```

> **Fatima:** "Fix confirmed. Nice work, Mehdi."

**+50 XP**

### Phase 3: Resume your feature — 30 XP

```bash
git checkout feature/task-priority
git stash pop
```

→ Your priority code is back! Continue working:

```bash
git add .
git commit -m "feat: complete task priority with UI integration"
```

**+30 XP**

### Phase 4: Fix the CSS bug too (TICKET-102) — 40 XP

```bash
git checkout main
git checkout -b bugfix/css-alignment
```

Edit `style.css` — add:

```css
/* Fix: task items alignment on mobile */
@media (max-width: 600px) {
    .task-item {
        flex-direction: column;
        align-items: flex-start;
    }
    
    #search-input {
        font-size: 14px;
    }
}
```

```bash
git add style.css
git commit -m "fix: task item alignment on mobile screens"
git checkout main
git merge bugfix/css-alignment
git branch -d bugfix/css-alignment
```

**+40 XP**

### Phase 5: Merge your feature — 20 XP

```bash
git merge feature/task-priority
git branch -d feature/task-priority
```

**+20 XP**

### Phase 6: Final check — 20 XP

```bash
git log --oneline -8
git branch
git status
```

- Should see all your commits in order
- Only `main` branch should exist
- Working tree should be clean

**+20 XP!**

🏅 **ACHIEVEMENT UNLOCKED: Sprint Survivor — Handled a full sprint workflow!**

> **Lina:** "That's exactly how a professional developer handles a sprint. Feature work, emergency fixes, stashing, branching, merging — all in a day's work."
>
> **Sara:** "I'm impressed, Mehdi."
>
> **Omar:** "I got confused at Phase 2 and committed to main directly."
>
> **Youssef:** "OMAR—"

---

## ❓ FINAL QUIZ — Day 5

1. You're coding on `feature/x`. Sara says "fix this bug NOW." You have uncommitted changes. What do you do? (Exact commands)
2. `git blame server.py` shows Ahmed as the author of line 42. What does that tell you?
3. What's the difference between `git stash pop` and `git stash apply`?
4. Ahmed's branch has 10 commits. You need only commit #7. What command?
5. **HARD:** You stashed 3 things. How do you restore the SECOND one?
6. **HARDER:** Why is it dangerous to cherry-pick the same commit to multiple branches?
7. **HARDEST:** In the sprint simulation, why did we stash instead of just committing the WIP code?

---

## 🧠 Day 5 Summary

| Command | What It Does | Real-Life Use |
|---------|-------------|---------------|
| `git stash push -m "msg"` | Save work temporarily | Interrupted by urgent bug |
| `git stash pop` | Restore stashed work | Resume after fix |
| `git blame <file>` | Who wrote each line | Finding the right person to ask |
| `git cherry-pick <hash>` | Grab one commit | Taking a fix without all experiments |
| `git log --grep="text"` | Search commit messages | Finding related changes |
| `git log --author="name"` | Filter by author | Standup reports |
| `git log --graph --all` | Visual branch map | Understanding project history |

---

## 🏆 Day 5 Scorecard

```
LAB 1: Git stash .................. 80 XP
LAB 2: Git blame .................. 60 XP
LAB 3: Git cherry-pick ............ 80 XP
LAB 4: Log power moves ............ 40 XP
BOSS: Sprint simulation ........... 200 XP
BONUS: Extra challenges ........... +40 XP
────────────────────────────────────────
TOTAL                              600 XP

YOUR SCORE: ____ / 600
RUNNING TOTAL: ____ / 2400
```

---

## 📝 Quiz Answers

1. `git stash push -m "WIP"` → `git checkout main` → `git checkout -b hotfix/name` → fix → commit → merge → `git checkout feature/x` → `git stash pop`
2. Ahmed wrote line 42, and it was added in that specific commit. You can `git show <hash>` to see WHY.
3. `pop` restores AND deletes the stash. `apply` restores but KEEPS it in the stash list (useful if you might need it again).
4. `git cherry-pick <hash-of-commit-7>`
5. `git stash apply stash@{1}` (stashes are 0-indexed, so the second is `{1}`)
6. It creates duplicate commits in history. When branches merge, you might get conflicts with yourself.
7. Because WIP code is messy — it might not compile, tests might fail. You don't want half-finished code in your commit history. Stash is for temporary "hide this mess while I handle something else."

---

## ⏭️ Next Episode

**[Day 6: The Power Tools ⚡ →](day-06-advanced-tricks.md)**

> The FINAL day. You'll learn the weapons that senior developers wield: **rebase** (rewrite history), **interactive rebase** (squash messy commits), **bisect** (find bugs in seconds), **tags** (version releases), **reflog** (recover ANYTHING), and more. Omar accidentally deletes a branch. You'll save him. With `git reflog`. 🦸
