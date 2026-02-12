# ⚡ Day 6: The Power Tools — Advanced Git Mastery

> *Saturday. Well, not really — but this is the BONUS level. You've learned the fundamentals. Now it's time for the weapons that make senior developers look like wizards. Rebase. Squash. Bisect. Reflog. These are the tools Sara uses every day and Ahmed won't shut up about.*

**⏱️ Time: ~60 minutes**
**Difficulty: 🔴🔴 Expert**
**⭐ XP Available: 600**

**📍 Prerequisites:** Complete Days 1-5. Be inside `realcompanysteup` on `main`.

---

## 📖 THE STORY SO FAR

> **#dev-team — Sara:**
> "OK, Mehdi has crushed it this week. Time for the senior-level tools. After today, you'll know everything I know."
>
> **Youssef:** "Everything? Even the reflog trick?"
>
> **Sara:** "Especially the reflog trick. Someone's going to need it soon."
>
> *Everyone looks at Omar.*
>
> **Omar:** "Why are you all looking at me?"
>
> **Ahmed:** "No reason. 😊"

---

## 🔬 LAB 1: Git Rebase — Clean History (100 XP)

### The Problem with `git merge`

Every merge creates a **merge commit**. After weeks of work, your history looks like spaghetti:

```
Messy merge history:
*   merge feature/x
|\
| * fix typo
| * add button
|/
*   merge feature/y
|\
| * oops
| * update title
|/
* Initial commit
```

### Rebase: The Clean Alternative

Rebase **replays** your commits on top of the latest `main`. No merge commits. Clean straight line.

```
Before rebase:                     After rebase:
main:    A ── B ── C               main:    A ── B ── C
                    \                                   \
feature:             D ── E        feature:              D' ── E'
                                   (same changes, just moved forward)
```

> **Ahmed:** "Think of rebase like this: you wrote your essay in Word. Your teacher updated the textbook. Rebase takes your essay and re-writes it based on the NEW edition of the textbook. Same essay, just updated references."

### Step 1: Set up the scenario

```bash
git checkout main
echo "// Performance monitoring v1" >> app.js
git add app.js
git commit -m "feat: add performance monitoring"
```

**Create your feature branch:**

```bash
git checkout -b feature/user-settings
```

```bash
echo "function getUserSettings() { return { theme: 'light', lang: 'en' }; }" > settings.js
git add settings.js
git commit -m "feat: add user settings module"
```

```bash
echo "function saveSettings(data) { localStorage.setItem('settings', JSON.stringify(data)); }" >> settings.js
git add settings.js
git commit -m "feat: add save settings to localStorage"
```

**Meanwhile, somebody pushes to main (simulate it):**

```bash
git checkout main
echo "# Security headers applied" >> server.py
git add server.py
git commit -m "fix: apply security headers to all responses"
```

**See the divergence:**

```bash
git log --oneline --graph --all
```

→ `main` and `feature/user-settings` have diverged!

**+20 XP**

### Step 2: Rebase your feature branch

```bash
git checkout feature/user-settings
git rebase main
```

**Expected:**
```
Successfully rebased and updated refs/heads/feature/user-settings.
```

**Check the history:**

```bash
git log --oneline --graph --all
```

→ **Straight line!** Your commits sit cleanly on top of the latest main.

**+30 XP!**

### Step 3: Merge with fast-forward (clean!)

```bash
git checkout main
git merge feature/user-settings
```

→ **Fast-forward!** No merge commit. Clean, linear history.

```bash
git branch -d feature/user-settings
```

**+30 XP!**

### ⚠️ THE GOLDEN RULE OF REBASE

> **Sara writes this on the whiteboard in RED marker:**
>
> **"NEVER rebase commits that have been pushed to a shared branch."**
>
> Rebase rewrites history. If teammates already have your old commits, their history won't match. Chaos ensues.
>
> **Only rebase YOUR LOCAL branches before pushing.**

**+20 XP for understanding the danger!**

> **Omar:** "What if I already rebased a pushed branch?"
> **Sara:** "Then you pray. And buy everyone coffee."

---

## 🔬 LAB 2: Interactive Rebase — Squash Messy Commits (100 XP)

> *The most powerful Git feature that 90% of developers never learn.*

> **Ahmed:** "Mehdi, your last PR had 6 commits. Three of them were 'fix typo.' That's not acceptable."
>
> **Sara:** "Interactive rebase lets you clean up your commit history BEFORE pushing. Squash those typo fixes into the real commits."

### Step 1: Create a messy history

```bash
git checkout -b feature/login-page
```

```bash
echo "<form id='login'>" > login.html
echo "  <input type='text' name='username'>" >> login.html
echo "</form>" >> login.html
git add login.html
git commit -m "add login page"
```

```bash
echo "<form id='login'>" > login.html
echo "  <input type='text' name='username' placeholder='Username'>" >> login.html
echo "</form>" >> login.html
git add login.html
git commit -m "fix typo in login"
```

```bash
echo "function validateLogin(user, pass) { return user.length > 0 && pass.length > 0; }" > login.js
git add login.js
git commit -m "add login validation"
```

```bash
echo "function validateLogin(user, pass) { return user.length > 3 && pass.length > 6; }" > login.js
git add login.js
git commit -m "fix: minimum length should be 3 for user, 6 for pass"
```

```bash
echo ".login-form { max-width: 400px; margin: 0 auto; }" > login.css
git add login.css
git commit -m "add login page CSS"
```

```bash
echo ".login-form { max-width: 400px; margin: 0 auto; padding: 20px; }" > login.css
git add login.css
git commit -m "oops forgot padding"
```

**See the mess:**

```bash
git log --oneline -6
```

```
f1a2b3c oops forgot padding
d4e5f6a add login page CSS
a7b8c9d fix: minimum length should be 3 for user, 6 for pass
1234567 add login validation
89abcde fix typo in login
fedcba9 add login page
```

**6 commits. Half of them are "fix typo" and "oops". Embarrassing.** 😬

**+20 XP**

### Step 2: Interactive rebase

```bash
git rebase -i HEAD~6
```

Your editor opens with:

```
pick fedcba9 add login page
pick 89abcde fix typo in login
pick 1234567 add login validation
pick a7b8c9d fix: minimum length should be 3 for user, 6 for pass
pick d4e5f6a add login page CSS
pick f1a2b3c oops forgot padding
```

**Change it to:**

```
pick fedcba9 add login page
fixup 89abcde fix typo in login
pick 1234567 add login validation
fixup a7b8c9d fix: minimum length should be 3 for user, 6 for pass
pick d4e5f6a add login page CSS
fixup f1a2b3c oops forgot padding
```

> 💡 **Interactive rebase keywords:**
>
> | Keyword | Short | What it does |
> |---------|-------|-------------|
> | `pick` | `p` | Keep this commit as-is |
> | `squash` | `s` | Combine with commit above (keep BOTH messages) |
> | `fixup` | `f` | Combine with commit above (throw away this message) |
> | `reword` | `r` | Keep commit, change the message |
> | `edit` | `e` | Pause here, let you modify things |
> | `drop` | `d` | DELETE this commit entirely |

**Save and close the editor.**

**+30 XP!**

### Step 3: Admire the clean history

```bash
git log --oneline -3
```

```
abc1234 add login page CSS
def5678 add login validation
ghi9012 add login page
```

**6 messy commits → 3 clean ones!** 

**+30 XP!**

🏅 **ACHIEVEMENT UNLOCKED: History Rewriter — Squashed commits with interactive rebase!**

**Clean up:**

```bash
git checkout main
git merge feature/login-page
git branch -d feature/login-page
```

**+20 XP**

> **Ahmed:** "THAT is what I want to see in PRs. Clean commits. No 'oops'. No 'fix typo'."
> **Omar:** "But what if my code IS all oops?"
> **Ahmed:** 😑

---

## 🔬 LAB 3: Git Revert — Safely Undo Pushed Commits (60 XP)

> *Remember Day 2's `git reset`? That rewrites history — dangerous for shared branches. `git revert` creates a NEW commit that undoes an old one. Safe for pushed code!*

> **Youssef:** "Someone deployed a broken feature to production. Who was it?"
> **Omar:** "...definitely not me."
> **Youssef:** "The commit has your name on it, Omar."
> **Omar:** 😅

### Step 1: Make a "bad" commit

```bash
echo "// THIS FEATURE BREAKS EVERYTHING" >> app.js
echo "function badFeature() { throw new Error('OOPS'); }" >> app.js
git add app.js
git commit -m "feat: add exciting new feature"
```

### Step 2: Revert it (creates a new commit that undoes the old one)

```bash
git revert HEAD
```

An editor opens with: `Revert "feat: add exciting new feature"`
Save and close.

**Check:**

```bash
git log --oneline -3
```

```
xyz7890 Revert "feat: add exciting new feature"
abc1234 feat: add exciting new feature
...
```

The bad code is gone, but the HISTORY shows what happened. Transparent and safe.

**+30 XP!**

### When to use what:

| Situation | Use This | Safe for pushed code? |
|-----------|----------|----------------------|
| Undo local commit | `git reset` | ❌ No |
| Undo pushed commit | `git revert` | ✅ Yes |
| Undo merged PR | `git revert -m 1 <hash>` | ✅ Yes |

**+30 XP!**

> **Youssef:** "`git revert` is the professional way to undo. `git reset --hard` on a shared branch is career suicide."

---

## 🔬 LAB 4: Git Bisect — Bug Detective Binary Search (80 XP)

> *The most underrated Git command. You have 100 commits. Something broke. Instead of checking each one, `git bisect` uses BINARY SEARCH to find the bug in ~7 steps.*

> **Fatima:** "Something broke between last Monday and today. We have 50 commits in between. I'm not checking all of them."
>
> **Sara:** "You don't have to. `git bisect`. It'll find the broken commit in about 6 steps."
>
> **Omar:** "That sounds like math."
>
> **Sara:** "It IS math. Binary search. $\log_2(50) \approx 6$"
>
> **Omar:** 😵

### Step 1: Create a history with a hidden bug

```bash
echo "Version 1 - all good" > feature.txt
git add feature.txt && git commit -m "v1: initial feature"

echo "Version 2 - still good" > feature.txt
git add feature.txt && git commit -m "v2: improve performance"

echo "Version 3 - still good" > feature.txt
git add feature.txt && git commit -m "v3: add caching"

echo "Version 4 - BUG INTRODUCED HERE" > feature.txt
git add feature.txt && git commit -m "v4: refactor internals"

echo "Version 5 - bug still here" > feature.txt
git add feature.txt && git commit -m "v5: update tests"

echo "Version 6 - bug still here" > feature.txt
git add feature.txt && git commit -m "v6: documentation update"

echo "Version 7 - bug still here" > feature.txt
git add feature.txt && git commit -m "v7: minor cleanup"
```

**+15 XP**

### Step 2: Start bisecting

```bash
git bisect start
```

**Mark the current as bad (the bug exists now):**

```bash
git bisect bad
```

**Find the known-good commit (v1):**

```bash
git log --oneline
```

Copy the hash of `v1: initial feature`:

```bash
git bisect good <v1-hash>
```

**+15 XP**

### Step 3: Git binary searches for you

Git checks out a middle commit. Check the file:

```bash
cat feature.txt
```

- If it says *"all good"*, *"still good"*, or *"add caching"* → `git bisect good`
- If it says *"BUG INTRODUCED"* or *"bug still here"* → `git bisect bad`

**Keep going.** Git narrows it down each time. After 2-3 steps:

```
<hash> is the first bad commit
commit <hash>
    v4: refactor internals
```

**FOUND IT!** v4 introduced the bug.

**+30 XP!**

### Step 4: Exit bisect

```bash
git bisect reset
```

**+20 XP**

🏅 **ACHIEVEMENT UNLOCKED: Bug Hunter — Found a bug with bisect!**

> **Fatima:** "I just found a week-old bug in 3 commands instead of 50 manual checks. I love this tool."
> **Omar:** "I usually just guess which commit broke it."
> **Fatima:** "...and how's that working out?"
> **Omar:** "Not great."

---

## 🔬 LAB 5: Git Tags — Version Your Releases (50 XP)

> **Youssef:** "Nothing goes to production without a version tag. No tag = no deploy. Period."

### Step 1: Create a lightweight tag

```bash
git tag v1.0.0
```

```bash
git tag
```
→ Shows `v1.0.0`

**+10 XP**

### Step 2: Create an annotated tag (preferred for releases)

```bash
git tag -a v1.1.0 -m "Release v1.1.0: dark mode, search, priority, login"
```

```bash
git show v1.1.0
```
→ Shows tag message, author, date, and the commit it points to.

**+15 XP**

### Step 3: Push tags to GitHub

```bash
git push origin --tags
```

**+10 XP**

### Semantic Versioning: `vMAJOR.MINOR.PATCH`

```
v1.0.0 → v1.0.1    PATCH: bug fix (nothing breaks)
v1.0.0 → v1.1.0    MINOR: new feature (backwards compatible)
v1.0.0 → v2.0.0    MAJOR: breaking change (things might break!)
```

| Change | Bump | Example |
|--------|------|---------|
| Fix crash | PATCH | `v1.0.0` → `v1.0.1` |
| Add search | MINOR | `v1.0.1` → `v1.1.0` |
| New API format | MAJOR | `v1.1.0` → `v2.0.0` |

**+15 XP**

> **Youssef:** "Client asks 'which version are we on?' You answer with the tag. No tags = no answer = unhappy client."

---

## 🔬 LAB 6: Git Add -p — Partial Staging (40 XP)

> *Sometimes you changed 10 things in a file but only want to commit 3. `git add -p` lets you stage individual chunks.*

### Step 1: Make multiple changes in one file

Edit `app.js` — add at the TOP (after line 1):

```javascript
// App version: 2.1.0
```

And add at the BOTTOM:

```javascript
// DEBUG MODE - REMOVE BEFORE PRODUCTION!!!
console.log('DEBUGGING: all variables', JSON.stringify(tasks));
```

### Step 2: Stage interactively

```bash
git add -p app.js
```

Git shows each "hunk" (chunk of changes) and asks:

```
Stage this hunk [y,n,q,a,d,s,e,?]?
```

| Key | Meaning |
|-----|---------|
| `y` | Yes, stage this chunk |
| `n` | No, skip this |
| `s` | Split into smaller chunks |
| `q` | Quit |

**Stage the version comment (`y`), SKIP the debug line (`n`).**

**+15 XP**

### Step 3: Verify the split

```bash
git diff --staged
```
→ Only the version comment is staged.

```bash
git diff
```
→ Only the debug line is unstaged.

**+10 XP**

**Commit the clean part:**

```bash
git commit -m "docs: add app version comment"
```

**Discard the debug junk:**

```bash
git restore app.js
```

**+15 XP**

> **Sara:** "I use `git add -p` every single day. It forces you to review what you're committing, chunk by chunk."
> **Ahmed:** "Same. It's like a self-code-review."

---

## 🔬 LAB 7: Git Aliases — Create Shortcuts (30 XP)

> **Sara:** "Tired of typing `git log --oneline --graph --all --decorate` every time? Me too."

```bash
git config --global alias.st "status"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.cm "commit -m"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 --oneline"
git config --global alias.unstage "restore --staged"
git config --global alias.undo "reset --soft HEAD~1"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.wip "stash push -m"
```

**Now use them:**

```bash
git st                     # git status
git lg                     # Beautiful graph log
git last                   # Last commit
git undo                   # Undo last commit (keep changes)
```

**+20 XP!**

**See all aliases:**

```bash
# Windows:
git config --global --list | findstr alias

# Mac/Linux:
git config --global --list | grep alias
```

**+10 XP**

> **Omar:** "Can I alias `git push --force` to something?"
> **Youssef:** "I will personally revoke your Git access."

---

## 💥 FINAL BOSS: Omar Deleted His Branch — Save Him with Reflog (140 XP)

> *This is it. The FINAL boss. Omar did the ONE thing everyone told him not to do.*

> **#general — Omar:**
> "HELP!! I accidentally deleted my branch and it had 3 HOURS of work! I didn't push it! 😭😭😭"
>
> **Ahmed:** "Did you commit before deleting?"
>
> **Omar:** "Yes! But the branch is GONE!"
>
> **Sara:** "Mehdi. This is your moment. Save Omar's work with `git reflog`."
>
> **Youssef:** 🍿

### What is Reflog?

`git reflog` is Git's SECRET diary. It records EVERY action — even things `git log` doesn't show. Deleted branches, bad resets, lost commits — reflog remembers ALL of it.

### Step 1: Simulate Omar's disaster

```bash
git checkout -b omar/super-important-work
```

```bash
echo "// Omar's amazing code that took 3 hours" > omars-masterpiece.js
echo "function amazingFeature() {" >> omars-masterpiece.js
echo "  return 'This is my best work ever';" >> omars-masterpiece.js
echo "}" >> omars-masterpiece.js
git add omars-masterpiece.js
git commit -m "feat: Omar's incredible feature (3 hours of work)"

echo "// Even more amazing code" >> omars-masterpiece.js
echo "function evenBetter() { return 42; }" >> omars-masterpiece.js
git add omars-masterpiece.js
git commit -m "feat: add even more amazing functionality"

echo "// The crown jewel" >> omars-masterpiece.js
echo "function crownJewel() { return 'perfection'; }" >> omars-masterpiece.js
git add omars-masterpiece.js
git commit -m "feat: the crown jewel of Omar's career"
```

**Now ACCIDENTALLY delete the branch:**

```bash
git checkout main
git branch -D omar/super-important-work
```

❌ Branch DELETED. It's not in `git log`. It's not in `git branch`.

**Omar's work appears to be GONE.**

**+30 XP**

### Step 2: The Reflog to the Rescue

```bash
git reflog
```

**Output:**

```
abc1234 HEAD@{0}: checkout: moving from omar/super-important-work to main
def5678 HEAD@{1}: commit: feat: the crown jewel of Omar's career
ghi9012 HEAD@{2}: commit: feat: add even more amazing functionality
jkl3456 HEAD@{3}: commit: feat: Omar's incredible feature (3 hours of work)
...
```

**IT'S STILL THERE!** Reflog remembers everything!

**+30 XP**

### Step 3: Recover the branch

Copy the hash from `HEAD@{1}` (the last commit on Omar's branch):

```bash
git checkout -b omar/recovered def5678
```

Replace `def5678` with the actual hash from YOUR reflog.

**Check:**

```bash
git log --oneline -3
```

→ ALL three of Omar's commits are back!

```bash
cat omars-masterpiece.js
```

→ The code is INTACT!

**+50 XP!**

🏅 **ACHIEVEMENT UNLOCKED: Git Hero — Saved a teammate's lost work with reflog!**

> **Omar:** "MEHDI YOU'RE MY HERO!! 😭🎉"
> **Sara:** "And THAT, team, is why reflog exists."
> **Ahmed:** "And why we PUSH our branches before going home."
> **Youssef:** "Omar, from now on: commit early, commit often, and PUSH."
> **Omar:** "Yes sir. Yes sir. Yes sir."

**Clean up:**

```bash
git checkout main
git branch -D omar/recovered
```

### Reflog Recovery Cheat Sheet:

| Lost because of... | How to recover |
|--------------------|----------------|
| Deleted branch | `git reflog` → find hash → `git checkout -b name <hash>` |
| Bad `reset --hard` | `git reflog` → find pre-reset hash → `git reset --hard <hash>` |
| Bad rebase | `git reflog` → find pre-rebase hash → `git reset --hard <hash>` |
| Accidental `git checkout .` | ❌ Gone if never committed |

> ⚠️ Reflog entries expire after **90 days**. Don't wait forever to recover!

**+30 XP**

---

## ❓ FINAL QUIZ — Day 6 (The Hardest One)

1. What's the difference between `merge` and `rebase`? When do you use each?
2. You have 8 commits. 3 of them are "fix typo." How do you squash them?
3. What's the Golden Rule of Rebase?
4. Why is `git revert` safer than `git reset` for pushed commits?
5. Explain `git bisect` to a non-developer in one sentence.
6. What's the difference between `git tag v1.0` and `git tag -a v1.0 -m "msg"`?
7. Omar deleted an unpushed branch. What command reveals the lost commits?
8. **HARDEST:** You accidentally ran `git reset --hard HEAD~5` and lost 5 commits. They were NOT pushed. How do you get them back?

---

## 🧠 Day 6 Summary

| Command | Power Level | What It Does |
|---------|-------------|-------------|
| `git rebase main` | ⚡⚡ | Replay commits on top of main (clean history) |
| `git rebase -i HEAD~N` | ⚡⚡⚡ | Edit/squash/reorder/delete commits |
| `git revert <hash>` | ⚡ | Safely undo a pushed commit |
| `git bisect` | ⚡⚡ | Binary search for bug-causing commit |
| `git tag -a v1.0 -m "msg"` | ⚡ | Mark a release version |
| `git add -p` | ⚡⚡ | Stage parts of a file selectively |
| `git config alias.X "Y"` | ⚡ | Create shortcut commands |
| `git reflog` | ⚡⚡⚡ | Recover ANYTHING (the ultimate safety net) |

---

## 🏆 Day 6 Scorecard

```
LAB 1: Git rebase ................. 100 XP
LAB 2: Interactive rebase/squash .. 100 XP
LAB 3: Git revert ................. 60 XP
LAB 4: Git bisect ................. 80 XP
LAB 5: Git tags ................... 50 XP
LAB 6: Git add -p ................. 40 XP
LAB 7: Git aliases ................ 30 XP
BOSS: Reflog recovery ............. 140 XP
────────────────────────────────────────
TOTAL                              600 XP

YOUR SCORE: ____ / 600
RUNNING TOTAL: ____ / 3000
```

---

## 📝 Quiz Answers

1. **Merge** creates a merge commit (preserves branch history). **Rebase** replays commits on top of main (linear history). Use merge for shared/public branches, rebase for local feature branches before pushing.
2. `git rebase -i HEAD~8` → Change "fix typo" commits from `pick` to `fixup`
3. **NEVER rebase commits that have been pushed to a shared branch.**
4. `revert` creates a NEW commit → history is preserved, teammates aren't affected. `reset` rewrites history → teammates' repos break.
5. "Git bisect plays a guessing game with your code to find exactly which change broke things, testing halfway points until it narrows down the culprit."
6. `git tag v1.0` is lightweight (just a pointer). `git tag -a v1.0 -m "msg"` is annotated (stores author, date, message — preferred for releases).
7. `git reflog` — it shows ALL actions, including commits on deleted branches.
8. `git reflog` → find the hash before the reset (should be `HEAD@{1}`) → `git reset --hard <that-hash>` → all 5 commits restored!

---

## 🏆🏆🏆 COURSE COMPLETE!

```
╔══════════════════════════════════════════════════╗
║           🏆 FINAL SCORECARD 🏆                 ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Day 1: First Day at Work .......... ___ / 300   ║
║  Day 2: You Broke Something ........ ___ / 400   ║
║  Day 3: The Multiverse ............. ___ / 600   ║
║  Day 4: Going Online ............... ___ / 500   ║
║  Day 5: Sprint Week ................ ___ / 600   ║
║  Day 6: The Power Tools ............ ___ / 600   ║
║                                                  ║
║  GRAND TOTAL:  _____ / 3000                      ║
║                                                  ║
║  Your Rank:                                      ║
║  🌱 0-500     Git Seedling                       ║
║  🌿 501-1200  Git Apprentice                     ║
║  ⚔️ 1201-2000 Git Warrior                        ║
║  🔥 2001-2700 Git Master                         ║
║  👑 2701-3000 Git Legend                          ║
║                                                  ║
║  🏅 Achievements Unlocked: ___ / 12              ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### 🏅 All Achievements:

| # | Achievement | How to Unlock |
|---|------------|---------------|
| 1 | 🏅 First Commit | Day 1: Make your first commit |
| 2 | 🏅 Rapid Fire | Day 1: 3 commits in 5 minutes |
| 3 | 🏅 Clean History | Day 2: Fix a commit message with amend |
| 4 | 🏅 Undo Master | Day 2: Survive the Undo Gauntlet |
| 5 | 🏅 Conflict Survivor | Day 3: Resolve a merge conflict |
| 6 | 🏅 Conflict Master | Day 3: Resolve 3 conflicts in a row (bonus) |
| 7 | 🏅 Cloud Warrior | Day 4: First push to GitHub |
| 8 | 🏅 PR Pro | Day 4: Complete PR workflow |
| 9 | 🏅 Team Player | Day 4: Handle push rejection |
| 10 | 🏅 Sprint Survivor | Day 5: Complete sprint simulation |
| 11 | 🏅 History Rewriter | Day 6: Squash commits with interactive rebase |
| 12 | 🏅 Git Hero | Day 6: Save Omar's work with reflog |

---

> **Sara:** "Congratulations, Mehdi. You're not a junior anymore."
>
> **Ahmed:** "Welcome to the team. For real this time."
>
> **Fatima:** "I'll still find bugs in your code, but at least your Git game is solid."
>
> **Youssef:** "Tag your releases. Always."
>
> **Lina:** "The client is happy. Ship it."
>
> **Omar:** "Can we do the course again? I think I missed a few things..."
>
> **Everyone:** 😂

---

## 📎 Quick Reference

**[Git Company Cheatsheet →](git-company-cheatsheet.md)** — Everything you learned, on one page.
