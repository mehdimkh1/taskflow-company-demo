# 🔥 Day 2: You Broke Something

> *Tuesday. You arrive at work feeling confident. You start editing files... and then everything goes wrong. You delete code you shouldn't have. You commit with a typo. You stage the wrong file. Welcome to every developer's first week.*

**⏱️ Time: ~40 minutes**
**Difficulty: 🟡 Medium**
**⭐ XP Available: 400**

**📍 Prerequisites:** Complete Day 1. Be inside the `realcompanysteup` folder.

---

## 📖 THE STORY SO FAR

> **#general — Sara:**
> "Morning team. Mehdi, today I'll teach you the 'undo' commands. You WILL mess things up — every developer does. The trick is knowing how to fix it."
>
> **Fatima (QA):** "Speaking of messing up, who pushed that broken CSS last night?"
>
> **Omar:** "...that might have been me."
>
> **Ahmed:** "Omar, you committed a file called `asdfgh.py`. What even IS that?"
>
> **Omar:** "I was testing if Git worked."
>
> **Sara:** "And this is why we need today's lesson."

---

## 🔬 LAB 1: "Oh No, I Changed the Wrong File!" (40 XP)

> *You accidentally edited `app.js` with garbage code. You haven't staged it yet. How do you undo?*

**Make a bad edit to `app.js`** — add at the bottom:

```javascript
// OOPS I deleted the login function
// TODO delete this later maybe
function oopsie() { return "I broke everything"; }
```

**Inspect the damage:**

```bash
git status
```
→ `app.js` is modified (red). **+5 XP**

```bash
git diff app.js
```
→ You see the garbage lines you added. **+5 XP**

> **Sara:** "OK, don't panic. The file is modified but NOT staged. That means you can throw away the changes."

**The undo spell:**

```bash
git restore app.js
```

**Verify it's fixed:**

```bash
git status
```
→ Clean! No changes.

```bash
git diff app.js
```
→ Nothing. The file is back to the last committed version.

🎉 **+20 XP!**

> **Omar** accidentally runs `git restore .` and loses ALL his work for the morning.
> **Omar:** "WHERE DID MY CODE GO?!"
> **Sara:** "That's why you commit often, Omar. Uncommitted work can be lost."
> **Life lesson: Commit early, commit often.**

**⚠️ DANGER ZONE:** `git restore` PERMANENTLY deletes your uncommitted changes. There's no "undo" for the undo. Make sure you really want to discard!

---

## 🔬 LAB 2: "I Staged the Wrong File!" (40 XP)

> *You edited `style.css` with an experiment, ran `git add .` out of habit — but you're NOT ready to commit this yet.*

**Edit `style.css`** — add at the bottom:

```css
/* Experimental - not ready yet */
.new-feature {
    color: purple;
    font-size: 999px;
    animation: spin 0.1s infinite;
}
```

**Stage it by accident:**

```bash
git add style.css
```

**Check status:**

```bash
git status
```
→ `style.css` is **GREEN** (staged). Uh oh — you don't want to commit this.

> **Sara:** "Green means staged. But you can UN-stage without losing work."

**Unstage it (keep your changes in the file):**

```bash
git restore --staged style.css
```

**Check again:**

```bash
git status
```
→ `style.css` is **RED** (modified, not staged). Your changes are still in the file — they're just not staged anymore.

🎉 **+20 XP!**

**Now discard the experimental CSS too:**

```bash
git restore style.css
```

**+10 XP** for cleaning up!

> 💡 **Cheat Sheet:**
> - `git restore <file>` → "Throw away my changes" (file goes back to last commit)
> - `git restore --staged <file>` → "Unstage this, but keep my changes in the file"

**+10 XP** for understanding the difference!

---

## ❓ POP QUIZ #1

**What command would you use in each situation?**

| Situation | Command |
|-----------|---------|
| You edited a file and want to undo (NOT staged) | ??? |
| You ran `git add` but want to unstage | ??? |
| You want to unstage AND throw away changes | ??? |

*(Answers at the bottom)*

---

## 🔬 LAB 3: "Typo in My Commit Message!" (40 XP)

> *Ahmed is reviewing commit messages. He's not happy.*

**Make a commit with a typo:**

```bash
echo "<!-- Footer section -->" >> index.html
git add index.html
git commit -m "feat: add fotter to HTML page"
```

> **Ahmed** sees your commit: "fotter? FOTTER?! It's FOOTER. Fix this before anyone else sees it."

**Fix the message (WITHOUT creating a new commit):**

```bash
git commit --amend -m "feat: add footer section to HTML page"
```

**Verify:**

```bash
git log --oneline -3
```

→ The old message is gone. Only the corrected one exists.

🎉 **+20 XP!**
🏅 **ACHIEVEMENT UNLOCKED: Clean History — Fixed a commit message!**

> ⚠️ **WARNING:** Only amend commits that are LOCAL (not pushed to GitHub). Amending pushed commits causes chaos for teammates.

### BONUS: Forgot a file? Add it to the last commit!

```bash
echo "/* Footer styles */" >> style.css
echo ".footer { text-align: center; padding: 20px; }" >> style.css
git add style.css
git commit --amend --no-edit
```

→ `style.css` is now included in your last commit. Same message, same commit, extra file.

**+20 XP!**

---

## 🔬 LAB 4: "I Committed Too Early!" — Git Reset (60 XP)

> *Fatima (QA): "Mehdi, why did you commit that? It's not finished!"*
> *You: "I panicked and hit commit..."*
> *Sara: "Time to learn `git reset`."*

### Scenario: Undo the last commit (keep changes)

**Make a premature commit:**

```bash
echo "// Half-finished notification code" >> app.js
echo "function notify() { /* TODO */ }" >> app.js
git add app.js
git commit -m "feat: add notifications"
```

> **Fatima:** "That function is empty. You can commit empty functions?!"
> **Sara:** "Technically yes. But please don't."

**UNDO the commit — but KEEP your changes staged:**

```bash
git reset --soft HEAD~1
```

**Check:**

```bash
git status
```
→ `app.js` is staged (green), but there's no commit. You can keep working and commit later.

**+20 XP!**

### What does `HEAD~1` mean?

```
HEAD    = your most recent commit
HEAD~1  = one commit before HEAD (the parent)
HEAD~2  = two commits back (grandparent)
HEAD~3  = three commits back
```

### The Three Levels of Reset:

```bash
# Level 1: Gentle — undo commit, keep changes STAGED
git reset --soft HEAD~1

# Level 2: Medium — undo commit, keep changes UNSTAGED  
git reset HEAD~1

# Level 3: NUCLEAR — undo commit AND DELETE ALL CHANGES ⚠️
git reset --hard HEAD~1
```

> **Omar:** "What happens if I use `--hard`?"
> **Sara:** "Your changes are gone FOREVER. It's like throwing a box into a volcano."
> **Omar:** "Cool! I'll try it—"
> **Sara:** "DON'T."

**Let's try the medium reset:**

```bash
git commit -m "feat: add notifications"
git reset HEAD~1
```

```bash
git status
```
→ `app.js` is modified (red). Changes are in the file, but unstaged.

**+20 XP!**

**Clean up:**

```bash
git restore app.js
```

**+20 XP for understanding all 3 reset levels!**

---

## 🔬 LAB 5: Omar's Disaster — Setting Up .gitignore (60 XP)

> *This is where things get real.*

> **#general — Youssef (DevOps):**
> "WHO COMMITTED `taskflow.db` TO THE REPO?! Database files should NEVER be in Git!"
>
> **Omar:** "I ran `git add .` like Sara told me to..."
>
> **Ahmed:** "He also committed `personal-notes.txt` with his lunch plans and a file called `test_delete_me.pyc`."
>
> **Sara:** "OK, this is exactly why we need a `.gitignore` file. Mehdi, set this up."
>
> **Youssef:** "Please. Before Omar commits his browser history next."

### Step 1: Create the junk files

```bash
echo "compiled bytecode" > database.pyc
echo "SELECT * FROM tasks" > taskflow.db
echo "Lunch: shawarma at 1pm" > personal-notes.txt
echo "my password is 123456" > secrets.env
echo "temporary test" > test_output.log
```

**Check status:**

```bash
git status
```

→ 5 junk files show up. We need to prevent this!

### Step 2: Create `.gitignore`

```bash
echo "# ===== Python =====" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "" >> .gitignore
echo "# ===== Database =====" >> .gitignore
echo "*.db" >> .gitignore
echo "" >> .gitignore
echo "# ===== Secrets (NEVER commit these!) =====" >> .gitignore
echo "*.env" >> .gitignore
echo "secrets.*" >> .gitignore
echo "" >> .gitignore
echo "# ===== Personal files =====" >> .gitignore
echo "personal-*" >> .gitignore
echo "*.log" >> .gitignore
echo "" >> .gitignore
echo "# ===== IDE/Editor =====" >> .gitignore
echo ".vscode/" >> .gitignore
echo ".idea/" >> .gitignore
echo "" >> .gitignore
echo "# ===== OS junk =====" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "Thumbs.db" >> .gitignore
```

**Check status NOW:**

```bash
git status
```

→ The junk files are GONE! Only `.gitignore` appears. Magic! ✨

**+20 XP!**

**Commit it:**

```bash
git add .gitignore
git commit -m "chore: add .gitignore for Python, DB, secrets, and IDE files"
```

**+20 XP!**

**Clean up the junk files:**

```bash
rm database.pyc taskflow.db personal-notes.txt secrets.env test_output.log
```

**+20 XP!**

> **Youssef:** "Beautiful. Now nobody can accidentally commit a database or password file."
> **Omar:** "But what if I WANT to commit my lunch plans?"
> **Everyone:** "NO."

---

## 🔬 LAB 6: Investigating Commits — Git Show (30 XP)

> *Fatima: "Mehdi, something changed in the last commit. What was it?"*

**See the most recent commit in full detail:**

```bash
git show HEAD
```

→ Shows author, date, message, and the EXACT diff. **+10 XP**

**See a specific file's changes across all commits:**

```bash
git log --oneline -5 -- README.md
```

→ Shows only commits that touched `README.md`. **+10 XP**

**See what the README looked like 3 commits ago:**

```bash
git show HEAD~3:README.md
```

→ Time travel! You can read ANY file at ANY point in history. **+10 XP**

> **Omar:** "Wait... Git remembers EVERYTHING? Even the stuff I deleted?"
> **Sara:** "Yes. Everything."
> **Omar:** 😰

---

## 💥 BOSS FIGHT: The Undo Gauntlet (130 XP)

> **Sara:** "OK, final test. I'm going to put you through five undo scenarios. No help. No hints. Can you survive?"
>
> **⏱️ Try to finish in under 8 minutes!**

### Round 1: Discard uncommitted changes (20 XP)

```bash
echo "GARBAGE CODE DO NOT USE" >> server.py
```

**Your mission:** Get `server.py` back to its last committed state.

<details>
<summary>🔑 Click for hint (costs 10 XP!)</summary>

```bash
git restore server.py
```
</details>

Verify with `git status` — should be clean. **+20 XP (or +10 if you used the hint)**

---

### Round 2: Unstage a file (20 XP)

```bash
echo "/* EXPERIMENTAL */" >> style.css
git add style.css
```

**Your mission:** Unstage `style.css` (but keep the changes in the file).

<details>
<summary>🔑 Click for hint (costs 10 XP!)</summary>

```bash
git restore --staged style.css
```
</details>

Verify: `git status` should show `style.css` as modified (red), not staged (green). **+20 XP**

Then clean up: `git restore style.css`

---

### Round 3: Fix a commit message (20 XP)

```bash
echo "<!-- contact page -->" > contact.html
git add contact.html
git commit -m "add contakt page"
```

**Your mission:** Fix "contakt" → "contact" without creating a new commit.

<details>
<summary>🔑 Click for hint (costs 10 XP!)</summary>

```bash
git commit --amend -m "feat: add contact page"
```
</details>

Verify: `git log --oneline -1` should show the corrected message. **+20 XP**

---

### Round 4: Undo a commit (keep changes) (30 XP)

```bash
echo "// work in progress, not ready" >> app.js
git add app.js
git commit -m "feat: WIP stuff"
```

**Your mission:** Undo this commit. Keep the changes staged.

<details>
<summary>🔑 Click for hint (costs 15 XP!)</summary>

```bash
git reset --soft HEAD~1
```
</details>

Verify: `git status` shows `app.js` staged but NOT committed. **+30 XP**

Then clean up: `git restore --staged app.js && git restore app.js`

---

### Round 5: The FULL undo chain — do all of these in order (40 XP)

```bash
echo "BAD CODE" >> database.py
git add database.py
git commit -m "uhh"
```

**Missions (in order):**
1. Undo the commit (keep changes staged)
2. Unstage the file (keep changes in file)
3. Discard the changes from the file
4. Verify everything is clean

<details>
<summary>🔑 Click for hint (costs 20 XP!)</summary>

```bash
git reset --soft HEAD~1              # Undo commit → staged
git restore --staged database.py     # Unstage → modified
git restore database.py             # Discard changes → clean
git status                          # Verify: clean!
```
</details>

If `git status` shows a clean working tree: **+40 XP!**
🏅 **ACHIEVEMENT UNLOCKED: Undo Master — Survived the Gauntlet!**

---

## ❓ FINAL QUIZ — Day 2

**Answer without looking at notes:**

1. What's the difference between `git restore file` and `git restore --staged file`?
2. You committed but the message has a typo. What command fixes it?
3. You committed too early and want to undo. Name the three reset levels and what each does.
4. What goes in a `.gitignore` file and WHY?
5. You want to see what `server.py` looked like 5 commits ago. What command?
6. **HARD:** Omar committed `passwords.env` to the repo. He then added `*.env` to `.gitignore`. Is the file safe now?

*(Answers below)*

---

## 🧠 Day 2 Summary

| Situation | Command | Danger Level |
|-----------|---------|-------------|
| Bad changes, not staged | `git restore <file>` | 🟡 Changes lost |
| Accidentally staged | `git restore --staged <file>` | 🟢 Safe |
| Bad commit message | `git commit --amend -m "new"` | 🟢 Safe (if local) |
| Forgot a file in commit | `git add file && git commit --amend --no-edit` | 🟢 Safe (if local) |
| Committed too early | `git reset --soft HEAD~1` | 🟢 Safe |
| Undo commit + unstage | `git reset HEAD~1` | 🟡 Careful |
| ☢️ DELETE everything | `git reset --hard HEAD~1` | 🔴 DANGEROUS |
| Ignore junk files | `.gitignore` | 🟢 Essential |

---

## 🏆 Day 2 Scorecard

```
LAB 1: Undo bad changes ............ 40 XP
LAB 2: Unstage files ............... 40 XP
LAB 3: Amend commit message ........ 40 XP
LAB 4: Git reset levels ............ 60 XP
LAB 5: .gitignore setup ............ 60 XP
LAB 6: Investigating commits ....... 30 XP
BOSS: The Undo Gauntlet ............ 130 XP
────────────────────────────────────────
TOTAL                              400 XP

YOUR SCORE: ____ / 400
RUNNING TOTAL: ____ / 700
```

---

## 📝 Quiz Answers

**Quiz #1:**
| Situation | Command |
|-----------|---------|
| Undo changes (not staged) | `git restore <file>` |
| Unstage a file | `git restore --staged <file>` |
| Unstage AND throw away | `git restore --staged <file>` then `git restore <file>` |

**Final Quiz:**
1. `restore file` discards changes. `restore --staged file` removes from staging but keeps changes.
2. `git commit --amend -m "corrected message"`
3. `--soft` (undo commit, keep staged), `--mixed`/default (undo commit, unstage), `--hard` (undo commit + DELETE changes)
4. File patterns to exclude from tracking — prevent junk, secrets, compiled files from entering the repo.
5. `git show HEAD~5:server.py`
6. **NO!** `.gitignore` only prevents FUTURE tracking. Files already committed are still in the repo. Omar needs to run `git rm --cached passwords.env` to remove it from tracking.

---

## ⏭️ Next Episode

**[Day 3: The Multiverse 🌳 →](day-03-branching-merging.md)**

> Tomorrow: branches. This is where Git gets POWERFUL. Sara works on CSS, Ahmed works on the API, you work on a new feature — all at the same time, nobody's code touches anyone else's. Until it does. And then... the merge conflict boss fight. 💥
