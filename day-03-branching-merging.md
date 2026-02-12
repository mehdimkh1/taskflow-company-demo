# 🌳 Day 3: The Multiverse — Branching & Merging

> *Wednesday. The office is buzzing. Lina just announced a new sprint with 4 features due Friday. Sara, Ahmed, Youssef, and you all need to work on different things SIMULTANEOUSLY without breaking each other's code. Time to learn Git's greatest superpower: branches.*

**⏱️ Time: ~50 minutes**
**Difficulty: 🟡🔴 Medium-Hard**
**⭐ XP Available: 600**

**📍 Prerequisites:** Complete Days 1-2. Be inside `realcompanysteup` on `main`.

---

## 📖 THE STORY SO FAR

> **#sprint-planning — Lina:**
> "OK team, here's this week's sprint:
> - 🎨 Sara → Redesign the header
> - ⚙️ Ahmed → Add POST endpoint to API
> - 🌙 Mehdi → Add dark mode
> - 📊 Omar → Add task counter
>
> NOBODY works directly on `main`. Create branches. I don't want another repeat of last month."
>
> **Youssef:** "What happened last month?"
>
> **Sara:** "Omar pushed directly to main and deleted the entire CSS file."
>
> **Omar:** "It was ONE time..."
>
> **Ahmed:** "The site was white for 6 hours. SIX."

---

## 📖 STORY BREAK: What Are Branches?

> *Sara draws on the whiteboard:*

```
Imagine 4 chefs in a kitchen:

🍳 Main Kitchen (main branch) = The restaurant menu that customers eat from
  
🧪 Sara's Test Kitchen = She experiments with a new recipe
🧪 Ahmed's Test Kitchen = He experiments with a new sauce  
🧪 Mehdi's Test Kitchen = You try making a new dessert
🧪 Omar's Test Kitchen = He... sets something on fire probably

When a recipe works → you add it to the main menu (MERGE)
If it fails → you throw it away (DELETE branch). Main menu is never affected!
```

**In Git terms:**

```
main:     A ── B ── C                            (stable, always works)
                     ├── D ── E                   (Sara: feature/header)
                     ├── F ── G                   (Ahmed: feature/api-post)
                     └── H                        (Mehdi: feature/dark-mode)
```

---

## 🔬 LAB 1: Your First Branch (40 XP)

### Step 1: See where you are

```bash
git branch
```

**Expected:**
```
* main
```

The `*` means "you are here." **+5 XP**

### Step 2: Create your feature branch

> **Sara:** "The naming convention is: `feature/description`, `bugfix/description`, or `hotfix/description`. Always lowercase, use hyphens."

```bash
git checkout -b feature/dark-mode
```

This does TWO things:
1. Creates a branch called `feature/dark-mode`
2. Switches you to it

**Verify:**

```bash
git branch
```

```
* feature/dark-mode
  main
```

**+15 XP!**

### Step 3: Confirm you're on the new branch

```bash
git status
```

→ First line says `On branch feature/dark-mode`

**+5 XP!**

> **Omar:** "What happens if I name my branch `omar is the best developer`?"
> **Sara:** "No spaces in branch names. Also, no."

### Branch naming at TechCorp:

| Type | Format | Example |
|------|--------|---------|
| New feature | `feature/description` | `feature/dark-mode` |
| Bug fix | `bugfix/description` | `bugfix/login-crash` |
| Urgent fix | `hotfix/description` | `hotfix/payment-error` |
| Release prep | `release/version` | `release/v2.0` |

**+15 XP for learning the conventions!**

---

## 🔬 LAB 2: Work on Your Branch (60 XP)

> *Time to build dark mode!*

### Step 1: Add dark mode CSS

Edit `style.css` — add at the bottom:

```css
/* ===== Dark Mode ===== */
.dark-mode {
    background-color: #1a1a2e;
    color: #eee;
}

.dark-mode header {
    background-color: #16213e;
}

.dark-mode #task-list {
    background-color: #0f3460;
    color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.dark-mode .task-item {
    border-bottom-color: #333;
}
```

### Step 2: Add the toggle function

Edit `app.js` — add at the bottom:

```javascript
// ===== Dark Mode Toggle =====
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const btn = document.getElementById('dark-mode-btn');
    const isDark = document.body.classList.contains('dark-mode');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
    localStorage.setItem('darkMode', isDark);
}

// Load saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
```

### Step 3: Add button to HTML

Edit `index.html` — add after the `<p>` tag in the header:

```html
        <button id="dark-mode-btn" onclick="toggleDarkMode()">🌙 Dark Mode</button>
```

### Step 4: Commit your work

```bash
git add .
git commit -m "feat: add dark mode with toggle, CSS, and localStorage"
```

🎉 **+40 XP!**

### Step 5: The Magic of Branches — switch back to main

```bash
git checkout main
```

**Open `style.css`, `app.js`, `index.html`** — your dark mode is GONE! 😱

> **Don't panic.** Switch back:

```bash
git checkout feature/dark-mode
```

→ Dark mode is back! **Branches are parallel universes.**

**+20 XP!**

---

## 🔬 LAB 3: Simulate Teammates Working (80 XP)

> *While you built dark mode, the team was busy too. Let's simulate everyone's work.*

### 🎨 Sara's branch: Header redesign

```bash
git checkout main
git checkout -b feature/header-redesign
```

Edit `index.html` — change the `<header>` section:

```html
    <header>
        <h1>✅ TaskFlow</h1>
        <p>Your team's favorite task manager</p>
    </header>
```

Edit `style.css` — add:

```css
header h1 {
    font-size: 2.5em;
    margin: 0;
}
```

```bash
git add .
git commit -m "style: redesign header with emoji and larger title"
```

**+20 XP**

### ⚙️ Ahmed's branch: POST endpoint

```bash
git checkout main
git checkout -b feature/post-endpoint
```

Edit `server.py` — add inside the class, after the `do_GET` method:

```python
    def do_POST(self):
        if self.path == '/api/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_task = json.loads(post_data.decode())
            new_task['id'] = len(tasks) + 1
            new_task['completed'] = False
            tasks.append(new_task)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_task).encode())
```

```bash
git add server.py
git commit -m "feat: add POST /api/tasks endpoint for creating tasks"
```

**+20 XP**

### 📊 Omar's branch: Task counter (with mistakes, of course)

```bash
git checkout main
git checkout -b feature/task-counter
```

Edit `app.js` — add at the bottom:

```javascript
// Task Counter - by Omar
function updateTaskCount() {
    const count = tasks.length;
    document.title = `TaskFlow (${count} tasks)`;
}
```

```bash
git add .
git commit -m "add counter for tasks in page title"
```

> **Ahmed reviews Omar's commit:** "No prefix. It should be `feat: add task counter`. Please fix it."

```bash
git commit --amend -m "feat: add task counter in page title"
```

**+20 XP**

### See all branches:

```bash
git branch
```

```
* feature/task-counter
  feature/dark-mode
  feature/header-redesign
  feature/post-endpoint
  main
```

**5 branches!** Just like a real sprint. **+20 XP** (but only from completing this section fully!)

---

## 🔬 LAB 4: Merging — Bring It All Together (60 XP)

> **Lina:** "Sara's header redesign is approved. Merge it to main."

### Step 1: Merge Sara's branch

```bash
git checkout main
git merge feature/header-redesign
```

**Expected:** Fast-forward merge. No conflicts because nobody else touched those files.

```
Updating abc1234..def5678
Fast-forward
 index.html | ...
 style.css  | ...
 2 files changed, ...
```

**+15 XP**

### Step 2: Merge Ahmed's branch

```bash
git merge feature/post-endpoint
```

**Expected:** Fast-forward again. Ahmed only changed `server.py`.

**+15 XP**

### Step 3: Merge Omar's branch

```bash
git merge feature/task-counter
```

**Expected:** Might say "Merge made by the 'ort' strategy" — this creates a merge commit because `main` moved since Omar's branch was created.

**+15 XP**

### Step 4: Merge YOUR branch

```bash
git merge feature/dark-mode
```

**+15 XP**

### See the beautiful history:

```bash
git log --oneline --graph --all
```

→ You'll see all the branches merging into main. This is what real projects look like!

---

## 🔬 LAB 5: Clean Up Merged Branches (20 XP)

> **Youssef:** "Delete your merged branches. A clean repo is a happy repo."

```bash
git branch -d feature/dark-mode
git branch -d feature/header-redesign
git branch -d feature/post-endpoint
git branch -d feature/task-counter
```

```bash
git branch
```

→ Only `main` remains. **+20 XP!**

> **Omar:** "Wait, does deleting the branch delete my code?"
> **Sara:** "No! The commits are already merged into main. The branch was just a pointer."
> **Omar:** *deletes branch* *code is still there* "Oh cool! 😄"

---

## ❓ POP QUIZ #2

1. What's the command to create a branch AND switch to it in one step?
2. What does "fast-forward" merge mean?
3. Why do we delete branches after merging?
4. Can two people work on the same branch? Should they?

*(Answers at the bottom)*

---

## 💥 BOSS FIGHT: The Merge Conflict (200 XP)

> *This is the moment every developer dreads. Two people changed THE SAME LINE of the same file. Git doesn't know which version to keep. YOU must decide.*

> **Lina:** "OK... we have a problem. Sara and Ahmed BOTH changed the title in `index.html`. Git is confused. Mehdi — resolve this."
>
> **Sara:** "I changed it to `TaskFlow Pro`."
> **Ahmed:** "I changed it to `TaskFlow 2.0`."
> **Sara:** "Mine is better."
> **Ahmed:** "Mine has a version number."
> **Fatima:** *eating popcorn* 🍿

### Step 1: Create Sara's branch

```bash
git checkout -b conflict/sara-title
```

Edit `index.html` — change the `<h1>`:

From:
```html
        <h1>✅ TaskFlow</h1>
```
To:
```html
        <h1>✅ TaskFlow Pro</h1>
```

```bash
git add index.html
git commit -m "feat: rename to TaskFlow Pro"
```

### Step 2: Create Ahmed's branch (from main)

```bash
git checkout main
git checkout -b conflict/ahmed-title
```

Edit `index.html` — change the SAME `<h1>`:

From:
```html
        <h1>✅ TaskFlow</h1>
```
To:
```html
        <h1>✅ TaskFlow 2.0</h1>
```

```bash
git add index.html
git commit -m "feat: rebrand to TaskFlow 2.0"
```

### Step 3: Merge Sara's branch first (no conflict)

```bash
git checkout main
git merge conflict/sara-title
```

→ Fast-forward. Works fine. **+20 XP**

### Step 4: Now merge Ahmed's — 💥 CONFLICT!

```bash
git merge conflict/ahmed-title
```

**Output:**
```
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

> **Omar:** "THE COMPUTER IS YELLING AT US!"
> **Sara:** "It's not yelling. It's asking for help."

**+20 XP** for triggering a conflict without running away!

### Step 5: See the conflict

```bash
git status
```

→ Shows `both modified: index.html`

**Open `index.html`** — you'll see conflict markers:

```html
<<<<<<< HEAD
        <h1>✅ TaskFlow Pro</h1>
=======
        <h1>✅ TaskFlow 2.0</h1>
>>>>>>> conflict/ahmed-title
```

**What these markers mean:**

```
<<<<<<< HEAD
    (What's on YOUR current branch — main, which has Sara's change)
=======
    (What's on the INCOMING branch — Ahmed's change)
>>>>>>> conflict/ahmed-title
```

**+30 XP** for understanding the markers!

### Step 6: RESOLVE — You Decide!

> **Lina:** "Just combine them. Call it `TaskFlow Pro 2.0`. Happy?"
> **Sara & Ahmed:** "...fine."

**Edit `index.html`** — replace the ENTIRE conflict block with:

```html
        <h1>✅ TaskFlow Pro 2.0</h1>
```

**Make sure ALL conflict markers are deleted!** (`<<<<<<<`, `=======`, `>>>>>>>`)

**+30 XP**

### Step 7: Complete the merge

```bash
git add index.html
git commit -m "merge: combine Pro and 2.0 branding into TaskFlow Pro 2.0"
```

**+50 XP!**
🏅 **ACHIEVEMENT UNLOCKED: Conflict Survivor — Resolved a merge conflict!**

### Step 8: Clean up

```bash
git branch -d conflict/sara-title
git branch -d conflict/ahmed-title
```

**+20 XP**

### Step 9: Verify the final result

```bash
git log --oneline --graph -8
```

You should see the merge commit at the top with the branch history below.

**+30 XP**

> **Fatima:** *finishes popcorn* "Well handled, Mehdi."
> **Omar:** "Could I have done that?"
> **Sara:** "Let's not find out."

---

## 🏋️ BONUS CHALLENGE: Triple Conflict (Unlocks 🏅 Conflict Master)

> **Only attempt this if you want the extra achievement!**

Create THREE branches that ALL change `style.css` body background:

1. Branch `test/red`: Change `background-color` to `#ff0000`
2. Branch `test/blue`: Change `background-color` to `#0000ff`
3. Branch `test/green`: Change `background-color` to `#00ff00`

Merge them ONE BY ONE into main, resolving each conflict.

**Final result:** Choose your favorite color (or make it a gradient!).

🏅 **ACHIEVEMENT UNLOCKED: Conflict Master — Resolved 3 conflicts in a row!**

Clean up all test branches when done.

---

## ❓ FINAL QUIZ — Day 3

1. Draw (or describe) what happens when you create a branch and make 2 commits on it.
2. What's the difference between `git checkout -b name` and `git branch name`?  
3. You merged `feature/x` into main. What does `git branch -d feature/x` do? Does it delete the code?
4. **HARD:** In a conflict, what does the code between `<<<<<<< HEAD` and `=======` represent?
5. **HARDER:** Why is it called "fast-forward" merge? What makes it different from a regular merge?
6. **HARDEST:** You have 3 teammates all working on different branches. They all finish at the same time. Does the order you merge them matter?

---

## 🧠 Day 3 Summary

| Command | What It Does | Analogy |
|---------|-------------|---------|
| `git branch` | List all branches | See all parallel universes |
| `git checkout -b name` | Create + switch to branch | Open a portal to a new universe |
| `git checkout name` | Switch to existing branch | Travel to another universe |
| `git merge branch` | Combine branch into current | Merge two universes |
| `git branch -d name` | Delete merged branch | Close the portal |
| `git log --graph --all` | Visual branch history | See the multiverse map |

### Conflict Resolution Cheat Sheet:
```
1. git merge branch          ← Conflict appears
2. Open conflicted file      ← Find <<<<<<< markers
3. Choose what to keep       ← Remove all markers
4. git add <file>            ← "I resolved this"
5. git commit                ← Complete the merge
```

---

## 🏆 Day 3 Scorecard

```
LAB 1: First branch ............... 40 XP
LAB 2: Work on branch ............. 60 XP
LAB 3: Simulate teammates ......... 80 XP
LAB 4: Merging branches ........... 60 XP
LAB 5: Clean up branches .......... 20 XP
BOSS: Merge conflict resolution .... 200 XP
BONUS: Triple conflict ............ +50 XP
────────────────────────────────────────
TOTAL                              600 XP

YOUR SCORE: ____ / 600
RUNNING TOTAL: ____ / 1300
```

---

## 📝 Quiz Answers

**Quiz #2:**
1. `git checkout -b branch-name`
2. Fast-forward means main just moved its pointer forward — no diverging history, no merge commit needed.
3. We delete them to keep the branch list clean. Merged commits remain in main.
4. Two people CAN work on the same branch, but they SHOULDN'T — it causes constant conflicts and overwriting.

**Final Quiz:**
1. Main stays at commit C. Your branch adds D and E after C: `main: A-B-C`, `feature: A-B-C-D-E`
2. `checkout -b` creates AND switches. `branch` only creates — you stay on your current branch.
3. Deletes the branch pointer, NOT the code. The commits are already in main from the merge.
4. That's what's on your CURRENT branch (the branch you're merging INTO).
5. "Fast-forward" happens when main hasn't changed since you branched off. Git just moves the main pointer forward to your latest commit. No merge commit needed. A regular merge happens when both branches have new commits — Git creates a merge commit combining both.
6. **Yes, sort of.** Each merge after the first might cause conflicts with the previously merged code. The first merge is always easiest (fast-forward if possible), and later merges may need conflict resolution.

---

## ⏭️ Next Episode

**[Day 4: Going Online ☁️ →](day-04-github-remotes.md)**

> Tomorrow: Your code goes to the cloud! You'll push TaskFlow to GitHub, learn to pull teammates' work, and create your first Pull Request. Youssef will also teach you why you NEVER force-push to main. (Spoiler: Omar does it anyway.) 🌐
