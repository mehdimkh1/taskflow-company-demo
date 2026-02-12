# ☁️ Day 4: Going Online — GitHub & Remotes

> *Thursday. TaskFlow has been living on your laptop. What happens if your laptop dies? What if Sara needs your dark mode code RIGHT NOW? It's time to put the project on GitHub — the cloud for code.*

**⏱️ Time: ~45 minutes**
**Difficulty: 🟡 Medium**
**⭐ XP Available: 500**

**📍 Prerequisites:** Complete Days 1-3. Have a [GitHub account](https://github.com) (free).

---

## 📖 THE STORY SO FAR

> **#general — Youssef (DevOps):**
> "Team, it's 2026 and our project isn't on GitHub. We're one coffee spill away from losing everything. Let's fix that TODAY."
>
> **Sara:** "Agreed. And once it's on GitHub, we're using Pull Requests for everything."
>
> **Omar:** "What's a Pull Request?"
>
> **Ahmed:** "It's how adults write code, Omar."
>
> **Omar:** 😢
>
> **Sara:** "Ahmed, be nice. Mehdi — I'll walk you both through it."
>
> **Fatima:** "Can we also set up branch protection so nobody pushes directly to main?"
>
> **Youssef:** *looks at Omar* "Yes. Definitely yes."

---

## 📖 STORY BREAK: Local vs Remote

```
YOUR LAPTOP (Local)                GITHUB (Remote / Cloud)
┌──────────────────┐              ┌──────────────────┐
│  realcompanysteup/│              │  taskflow/        │
│  ├── index.html  │   git push   │  ├── index.html  │
│  ├── server.py   │  ─────────→  │  ├── server.py   │
│  ├── app.js      │              │  ├── app.js       │
│  └── ...         │  ←─────────  │  └── ...         │
│                  │   git pull   │                    │
└──────────────────┘              └──────────────────┘
     You work here                 ✅ Backup online
                                   ✅ Teammates can access
                                   ✅ Code reviews happen here
                                   ✅ Deployment starts here
```

**Three commands to remember:**
| Command | Direction | Analogy |
|---------|-----------|---------|
| `git push` | You → GitHub | Upload your latest work |
| `git pull` | GitHub → You | Download teammates' work |
| `git clone` | GitHub → New Folder | Copy entire repo for the first time |

---

## 🔬 LAB 1: Create a GitHub Repository (30 XP)

> **Youssef:** "Mehdi, create the GitHub repo. I'll walk you through it."

### Step 1: Go to GitHub

1. Open [github.com](https://github.com) and sign in
2. Click the **"+"** button (top right) → **"New repository"**
3. Fill in:
   - **Name:** `taskflow`
   - **Description:** `Task management app by TechCorp`
   - **Visibility:** Public (or Private — your choice)
   - ❌ Do NOT check "Add a README" (we already have one!)
   - ❌ Do NOT add .gitignore (we already have one!)
4. Click **"Create repository"**

**+15 XP**

### Step 2: Connect your local repo to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/taskflow.git
```

> 💡 Replace `YOUR_USERNAME` with your actual GitHub username!

**What this did:**
- `remote add` = "connect to a remote server"
- `origin` = a nickname for this GitHub URL (used by convention worldwide)

**Verify the connection:**

```bash
git remote -v
```

```
origin  https://github.com/YOUR_USERNAME/taskflow.git (fetch)
origin  https://github.com/YOUR_USERNAME/taskflow.git (push)
```

**+15 XP!**

> **Omar:** "Can I call it something other than `origin`?"
> **Youssef:** "You CAN, but don't. Everyone uses `origin`. It's like naming your WiFi."

---

## 🔬 LAB 2: Push to GitHub — First Upload (50 XP)

> **Sara:** "Moment of truth. Push the entire project to GitHub."

```bash
git push -u origin main
```

**What each part means:**
- `push` — upload commits
- `-u` — "set this as the default" (so next time you just type `git push`)
- `origin` — push to GitHub (the remote you just added)
- `main` — push the `main` branch

> You may get asked to log in. GitHub uses Personal Access Tokens now — follow the prompts or set up SSH keys.

**Expected output:**
```
Enumerating objects: ...
Counting objects: 100% ...
Writing objects: 100% ...
To https://github.com/YOUR_USERNAME/taskflow.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**Go to `github.com/YOUR_USERNAME/taskflow` in your browser.**

🎉 Your code is in the cloud!

**+40 XP!**
🏅 **ACHIEVEMENT UNLOCKED: Cloud Warrior — First push to GitHub!**

**+10 XP** for checking it in the browser!

---

## 🔬 LAB 3: Push Changes (30 XP)

> **Ahmed:** "I just added a new database function. Let me push it."

Edit `database.py` — add at the bottom:

```python
def delete_task(task_id):
    """Delete a task by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} deleted.")
```

```bash
git add database.py
git commit -m "feat: add delete_task function to database module"
git push
```

→ Just `git push` now! (The `-u` from before set the default.)

**+20 XP**

**Check GitHub** — refresh the page. The new commit is there! **+10 XP**

---

## 🔬 LAB 4: Pull Changes — Download Teammates' Work (60 XP)

> **Scenario:** Sara pushed a change from HER laptop. You need to download it.

> **Sara:** "I just pushed a welcome message to the frontend. Everyone pull."

### Simulate Sara's push by editing directly on GitHub:

1. Go to your repo on GitHub
2. Click on `index.html`
3. Click the **pencil icon** ✏️ (edit)
4. Find the `<main>` section and add this line inside it:
   ```html
       <p class="welcome-msg">👋 Welcome to TaskFlow! Start managing your tasks.</p>
   ```
5. Scroll down → Commit message: `feat: add welcome message to frontend`
6. Click **"Commit changes"**

### Now pull it to your laptop:

```bash
git pull
```

**Expected:**
```
Updating abc1234..def5678
Fast-forward
 index.html | 1 +
 1 file changed, 1 insertion(+)
```

**Open `index.html` locally** — Sara's welcome message is there! 

**+40 XP!**

> **Omar:** "So `git pull` is like downloading the latest episode of a TV show?"
> **Sara:** "...sure. Yeah. Let's go with that."

### The Golden Rule:

> **⭐ START EVERY WORK DAY WITH `git pull`!**
> This ensures you have the latest code before you start working. If you don't, you'll get conflicts.

**+20 XP for understanding the golden rule!**

---

## ❓ POP QUIZ #1

1. What does `origin` mean in `git push origin main`?
2. What's the difference between `git push` and `git push -u origin main`?
3. You made 3 commits locally. How many get pushed with `git push`?
4. What happens if you `git push` but someone else pushed before you?

*(Answers at the bottom)*

---

## 🔬 LAB 5: The Pull Request Workflow — How Pros Do It (120 XP)

> *This is the core workflow at every tech company. Nobody pushes to main directly. You create a Pull Request (PR) and teammates review it.*

> **Sara:** "From now on, the workflow is:
> 1. Create branch locally
> 2. Make your changes
> 3. Push the branch to GitHub
> 4. Create a Pull Request
> 5. Someone reviews your code
> 6. Merge the PR
> 7. Update your local main
>
> No exceptions. Not even for you, Ahmed."
>
> **Ahmed:** "I've been doing this for 5 years."
>
> **Sara:** "...not even for Omar, then."
>
> **Omar:** "Hey!"

### Step 1: Create a feature branch

> **Lina:** "@mehdi your ticket: Add a search bar to filter tasks."

```bash
git checkout -b feature/search-bar
```

**+10 XP**

### Step 2: Build the feature

Edit `index.html` — add before the `<div id="task-list">`:

```html
        <div id="search-container">
            <input type="text" id="search-input" placeholder="🔍 Search tasks..." onkeyup="searchTasks()">
        </div>
```

Edit `app.js` — add:

```javascript
// ===== Search Filter =====
function searchTasks() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const items = document.querySelectorAll('.task-item');
    items.forEach(item => {
        const visible = item.textContent.toLowerCase().includes(query);
        item.style.display = visible ? 'flex' : 'none';
    });
}
```

Edit `style.css` — add:

```css
/* Search Bar */
#search-container {
    max-width: 600px;
    margin: 15px auto;
}

#search-input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s;
}

#search-input:focus {
    border-color: #2c3e50;
    outline: none;
}
```

### Step 3: Commit

```bash
git add .
git commit -m "feat: add search bar with real-time task filtering"
```

**+20 XP**

### Step 4: Push the BRANCH (not main!)

```bash
git push -u origin feature/search-bar
```

→ This pushes your branch to GitHub. It does NOT affect main.

**+15 XP**

### Step 5: Create a Pull Request on GitHub

1. Go to your repo on GitHub
2. You'll see a yellow banner: **"feature/search-bar had recent pushes"** → Click **"Compare & pull request"**
3. Fill in the PR template:

   **Title:** `feat: add search bar with real-time task filtering`

   **Description:**
   ```markdown
   ## What does this PR do?
   Adds a search bar that filters tasks as the user types.
   
   ## Changes
   - `index.html` — Added search input element
   - `app.js` — Added `searchTasks()` function with real-time filtering
   - `style.css` — Added search bar styling with focus effect
   
   ## How to test
   1. Open `index.html` in browser
   2. Type in the search bar
   3. Tasks should filter in real-time
   
   ## Screenshots
   (You'd normally attach screenshots here)
   
   ## Checklist
   - [x] Code works locally
   - [x] Follows naming conventions
   - [x] Commit messages use conventional format
   ```

4. Click **"Create pull request"**

**+25 XP!**

> **Fatima:** "Nice PR description, Mehdi. This is how it should always be done."
> **Omar:** "My last PR description was 'fixed stuff'. Is that bad?"
> **Fatima:** "Yes, Omar. Yes it is."

### Step 6: Review & Merge

In a real company, a teammate reviews and approves. For now:

1. On the PR page, click **"Merge pull request"**
2. Click **"Confirm merge"**
3. Click **"Delete branch"** (cleans up on GitHub)

**+25 XP**

### Step 7: Update your local repo

```bash
git checkout main
git pull
```

→ Your search bar is now on `main`, both locally and on GitHub.

**Delete the local branch too:**

```bash
git branch -d feature/search-bar
```

**+25 XP!**

🏅 **ACHIEVEMENT UNLOCKED: PR Pro — Completed full Pull Request workflow!**

---

## 🔬 LAB 6: Clone — How New Teammates Join (40 XP)

> **Scenario:** Fatima needs the project on her machine. She doesn't have it. She needs to CLONE.

> **Fatima:** "OK I need to test this locally. How do I get the repo?"
> **Youssef:** "`git clone`. It copies everything — all branches, all history."

**Simulate this by cloning your own repo to a new folder:**

```bash
cd ..
git clone https://github.com/YOUR_USERNAME/taskflow.git taskflow-fatima
cd taskflow-fatima
```

**Explore:**

```bash
git log --oneline -5
```
→ Full history! **+10 XP**

```bash
git remote -v
```
→ `origin` is already set! **+10 XP**

```bash
git branch -a
```
→ Shows local AND remote branches! **+10 XP**

**Go back to your original folder:**

```bash
cd ../realcompanysteup
```

**+10 XP**

> **Omar:** "Wait, so when I clone, I get EVERYTHING? Even the embarrassing commits?"
> **Ahmed:** "Yes. Everything. Forever."
> **Omar:** 😰

---

## 💥 BOSS FIGHT: The Simultaneous Push Problem (100 XP)

> *This happens in real teams ALL THE TIME. You and Omar both work on different things, but you both push at the same time. One of you gets an error.*

> **The scenario:**
> 1. You make a commit and try to push
> 2. But Omar ALREADY pushed something before you
> 3. GitHub rejects YOUR push: "your branch is behind"

### Step 1: Simulate Omar pushing first

Edit a file on GitHub directly (simulating Omar's push):

1. Go to `README.md` on GitHub → Edit ✏️
2. Add: `## Contributors\n- Omar (Intern)\n`
3. Commit: `docs: add contributors section - Omar`

### Step 2: Make a LOCAL change (you don't know about Omar's push)

```bash
echo "" >> README.md
echo "## License" >> README.md
echo "MIT License - TechCorp 2026" >> README.md
git add README.md
git commit -m "docs: add license info to README"
```

### Step 3: Try to push

```bash
git push
```

**💥 ERROR!**

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not have locally.
```

> **Omar:** "I pushed first! I win!"
> **Sara:** "That's not how it works, Omar."

**+20 XP** for understanding the error!

### Step 4: The Fix — Pull, then Push

```bash
git pull
```

Git will try to auto-merge. If both edited different parts of README, it works:

```
Auto-merging README.md
Merge made by the 'ort' strategy.
```

If same section → you get a conflict. Resolve it like Day 3! 

**Now push:**

```bash
git push
```

→ Success! ✅

**+40 XP!**

### The Lesson:

> **Youssef:** "This will happen every single day in a team. The fix is ALWAYS:
> ```
> git pull    ← Get their changes first
> git push    ← Then push yours
> ```
> Or better yet: **pull every morning before starting work.**"

**+40 XP!**

🏅 **ACHIEVEMENT UNLOCKED: Team Player — Handled a push rejection!**

---

## 🏋️ BONUS CHALLENGE: Multiple Branches on GitHub (50 bonus XP)

Create 3 branches, push ALL of them to GitHub, and verify they appear:

```bash
git checkout -b experiment/feature-a
echo "Feature A" > feature-a.txt
git add . && git commit -m "feat: experiment A"
git push -u origin experiment/feature-a

git checkout main
git checkout -b experiment/feature-b
echo "Feature B" > feature-b.txt
git add . && git commit -m "feat: experiment B"
git push -u origin experiment/feature-b

git checkout main
git checkout -b experiment/feature-c
echo "Feature C" > feature-c.txt
git add . && git commit -m "feat: experiment C"
git push -u origin experiment/feature-c
```

Go to GitHub → Click "branches" → You should see all 3!

Clean up (delete from GitHub via the web, then locally):

```bash
git checkout main
git branch -D experiment/feature-a experiment/feature-b experiment/feature-c
```

🏅 **ACHIEVEMENT UNLOCKED: Branch Pusher — 3 branches on GitHub!**

---

## ❓ FINAL QUIZ — Day 4

1. What's the difference between `git push` and `git push -u origin main`?
2. You run `git push` and get "rejected: fetch first." What happened and how do you fix it?
3. What is a Pull Request? Why not just merge locally and push?
4. What does `git clone` give you that downloading a ZIP from GitHub doesn't?
5. **HARD:** Sara pushes to `main` at 2:00 PM. You push at 2:01 PM. You get rejected. You run `git pull`. What exactly happens behind the scenes?
6. **HARDER:** What's the difference between `git pull` and `git fetch`?

---

## 🧠 Day 4 Summary

| Command | What It Does | When |
|---------|-------------|------|
| `git remote add origin <url>` | Connect to GitHub | First-time setup |
| `git push -u origin main` | First push (set default) | Initial upload |
| `git push` | Upload commits | After committing |
| `git pull` | Download commits | Start of every work day |
| `git clone <url>` | Copy entire repo | Joining a project |
| `git push -u origin <branch>` | Push a feature branch | Before creating PR |

### The PR Workflow:
```
1. git checkout -b feature/name     ← Create branch
2. (write code, commit)              ← Do your work
3. git push -u origin feature/name   ← Push branch
4. Create PR on GitHub              ← Request review
5. Teammates review                 ← Code quality check
6. Merge on GitHub                  ← Click the button
7. git checkout main && git pull    ← Update local
8. git branch -d feature/name      ← Clean up
```

---

## 🏆 Day 4 Scorecard

```
LAB 1: Create GitHub repo ......... 30 XP
LAB 2: First push ................. 50 XP
LAB 3: Push changes ............... 30 XP
LAB 4: Pull changes ............... 60 XP
LAB 5: Pull Request workflow ....... 120 XP
LAB 6: Clone a repo ............... 40 XP
BOSS: Simultaneous push ........... 100 XP
BONUS: Multiple branches .......... +50 XP
────────────────────────────────────────
TOTAL (without bonus)          500 XP

YOUR SCORE: ____ / 500
RUNNING TOTAL: ____ / 1800
```

---

## 📝 Quiz Answers

**Quiz #1:**
1. `origin` is a nickname for the GitHub URL. Just a shortcut.
2. `-u origin main` sets the default. After that, `git push` alone knows where to push.
3. All 3. `git push` sends ALL local commits that aren't on the remote yet.
4. Git rejects your push. You must `git pull` first (to get their changes), then `git push`.

**Final Quiz:**
1. `-u origin main` sets the default remote/branch. After that, `git push` alone works without specifying.
2. Someone pushed before you. Your local `main` is behind. Fix: `git pull` then `git push`.
3. A PR is a request to merge your branch, with code review. Just merging locally skips the review — teammates can't check your code for bugs/style issues.
4. `git clone` gives you: full history, all branches, all commits, Git tracking, and `origin` configured. A ZIP is just a snapshot of files — no history, no Git.
5. `git pull` = `git fetch` (download their commits) + `git merge` (combine with yours). Git creates a merge commit combining your license commit with Omar's contributor commit.
6. `git fetch` downloads remote changes but does NOT apply them. `git pull` = fetch + merge. Fetch is safer because you can inspect before merging.

---

## ⏭️ Next Episode

**[Day 5: Sprint Week 🏢 →](day-05-team-workflows.md)**

> Tomorrow: the full TechCorp sprint begins. Stashing work when emergencies hit, blaming code authors, cherry-picking fixes, and the daily workflow every professional developer follows. Fatima files 5 bugs. Omar breaks production. Ahmed saves the day. Business as usual. 🔥
