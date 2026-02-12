# 🌱 Day 1: First Day at Work

> *Monday morning. You walk into TechCorp's office for the first time. The coffee machine is broken. Omar (the other new intern) has already accidentally deleted a folder. Sara walks over and says: "Welcome to the team. First things first — let's get you set up with Git."*

**⏱️ Time: ~40 minutes**
**Difficulty: 🟢 Easy**
**⭐ XP Available: 300**

---

## 📖 THE STORY SO FAR

Lina (Product Manager) sent this Slack message this morning:

> **#general — Lina:**
> "Welcome Mehdi and Omar! 🎉 You're joining us on TaskFlow — our task management app for a client. Sara will onboard you today. The project files exist but we never put them in Git (I know, I know 😅). That's your first job."
>
> **Sara:** "I'll walk them through it. @mehdi @omar open your terminals."
>
> **Ahmed:** "Please learn proper commit messages. I beg you. 🙏"
>
> **Omar:** "What's a terminal?"
>
> **Ahmed:** 😐

---

## 🔬 LAB 1: Identity Setup (10 XP)

> *Sara stands behind your desk: "Git needs to know who you are. Every commit you make will have your name on it — forever. So don't use 'asdf' as your name."*

**Run these commands (use YOUR actual name and email):**

```bash
git config --global user.name "Mehdi"
```

```bash
git config --global user.email "mehdi@techcorp.com"
```

### ✅ CHECKPOINT: Did it stick?

```bash
git config user.name
```
→ Should print your name. **+5 XP**

```bash
git config user.email
```
→ Should print your email. **+5 XP**

> **Omar** tries: `git config --global user.name Omar the Great`
> **Sara:** "...use quotes, Omar."
> **Omar:** 😅

---

## 🔬 LAB 2: Create the Repository (20 XP)

> *Sara: "The TaskFlow project is in the `realcompanysteup` folder. It has code but NO Git. Your job: put it under version control."*

**Navigate to the project:**

```bash
cd realcompanysteup
```

**Cast the spell:**

```bash
git init
```

**Expected output:**
```
Initialized empty Git repository in .../realcompanysteup/.git/
```

🎉 **+20 XP!**

> **Fatima (QA):** "Wait, so before this, we had ZERO version control? How were we tracking bugs?"
> **Ahmed:** "We weren't. That's why the database has three backup copies named `database_FINAL_v2_copy.py`."
> **Everyone:** 😂

---

## 📖 STORY BREAK: The Three Zones

> *Sara draws this on the whiteboard. She says: "If you understand this, you understand 80% of Git."*

```
📂 WORKING DIRECTORY      →    📋 STAGING AREA       →    📦 REPOSITORY
(Your files on disk)            (Ready to save)            (Saved forever)

You edit files here        → git add puts files     → git commit saves
                              here (packing box)       them permanently
                                                       (sealed & shipped)
```

**Think of it like moving apartments:**
1. 📂 You have stuff all over your room → *Working Directory*
2. 📋 You put selected items in a box → *`git add` = Staging*
3. 📦 You tape the box shut and label it → *`git commit` = Committed*

You can't ship a box without taping it. You can't tape it without putting stuff in it.

---

## ❓ POP QUIZ #1

**Before moving on, answer these** (answers at the bottom of this page):

1. What command creates a new Git repository?
2. Name the three "zones" that Git uses.
3. Which command moves a file from Working Directory → Staging Area?
4. What's the difference between `git add` and `git commit`?

---

## 🔬 LAB 3: First Staging (30 XP)

> *Sara: "Check what Git sees right now."*

```bash
git status
```

**Expected output:**

```
On branch main
No commits yet

Untracked files:
        README.md
        app.js
        database.py
        index.html
        server.py
        style.css
```

All files are **RED** — Git sees them but isn't tracking them.

> **Omar:** "Why are they red? Did I break something?"
> **Sara:** "No, Omar. Red means untracked. Green means staged. Breathe."

### Option A — Stage one file at a time (for learning):

```bash
git add README.md
```

Check status:

```bash
git status
```

→ `README.md` is now **GREEN**! The rest are still red.

**+10 XP** — You staged your first file!

### Option B — Stage everything at once (what pros do):

```bash
git add .
```

The `.` means "everything in this directory."

```bash
git status
```

→ ALL files are **GREEN** now!

**+20 XP for staging all files!**

> **Omar** runs `git add ..` (two dots). Everything breaks.
> **Sara:** "One dot, Omar. ONE. DOT."

---

## 🔬 LAB 4: The First Commit (40 XP)

> *Sara: "Time to seal the box. A commit needs a message that describes WHAT you did. Ahmed — tell them the rules."*
>
> *Ahmed takes off his headphones:*
> *"Your commit message should explain what changed. Not 'stuff'. Not 'update'. Not 'asdfgh'. If I see any of those, I will personally revert your commits."*

```bash
git commit -m "Initial commit: add TaskFlow project files"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial commit: add TaskFlow project files
 6 files changed, ...
```

🎉 **+30 XP!**
🏅 **ACHIEVEMENT UNLOCKED: First Commit!**

### ✅ CHECKPOINT: Verify it

```bash
git log
```

→ You see your commit with author, date, and message.

**Cleaner view:**

```bash
git log --oneline
```

→ `abc1234 Initial commit: add TaskFlow project files`

**+10 XP** for verifying!

---

## 🔬 LAB 5: Make Changes & Commit Again (40 XP)

> *Lina sends a Slack message:*
> *"@mehdi can you add setup instructions to the README? The client asked how to run the app."*

**Open `README.md` in your editor and add at the bottom:**

```markdown

## Setup Instructions
1. Clone the repository
2. Run `python server.py` to start the backend
3. Open `index.html` in your browser
```

**See what Git detected:**

```bash
git status
```

→ `README.md` is **modified** (red)

**See EXACTLY what changed, line by line:**

```bash
git diff
```

→ Lines with `+` are additions. Lines with `-` are deletions. This is how code review works!

**+10 XP** for checking your diff!

**Stage and commit:**

```bash
git add README.md
git commit -m "docs: add setup instructions to README"
```

**+20 XP!**

> 💡 **Notice the commit message format:** `docs: add setup instructions`
>
> At TechCorp, we use **Conventional Commits**:
> | Prefix | When to use | Example |
> |--------|-----------|---------|
> | `feat:` | New feature | `feat: add dark mode` |
> | `fix:` | Bug fix | `fix: resolve login crash` |
> | `docs:` | Documentation | `docs: update README` |
> | `style:` | Formatting/CSS | `style: fix button color` |
> | `refactor:` | Restructuring code | `refactor: extract helpers` |
> | `chore:` | Maintenance | `chore: update dependencies` |

**+10 XP** for using proper message format!

---

## 🔬 LAB 6: Team Simulation — Multiple Commits (50 XP)

> *Sara: "In a real team, different people commit different things. Let's simulate that."*

### Ahmed's commit:

Edit `database.py` — change the first comment:

From: `# Database module for TaskFlow`
To: `# Database module for TaskFlow v1.0`

```bash
git add database.py
git commit -m "docs: update database module version to v1.0"
```

**+10 XP**

### Sara's commit:

Edit `style.css` — add at the bottom:

```css
.priority-high {
    border-left: 4px solid red;
}
```

```bash
git add style.css
git commit -m "style: add high-priority task indicator"
```

**+10 XP**

### Youssef's commit:

Edit `server.py` — add a comment at the bottom:

```python
# TODO: Add health check endpoint - Youssef
```

```bash
git add server.py
git commit -m "chore: add TODO for health check endpoint"
```

**+10 XP**

### Check the full history:

```bash
git log --oneline
```

**Expected (numbers will differ):**
```
def5678 chore: add TODO for health check endpoint
abc1234 style: add high-priority task indicator
9876543 docs: update database module version to v1.0
1234567 docs: add setup instructions to README
abcdef0 Initial commit: add TaskFlow project files
```

**5 commits!** This looks like a real project history. **+20 XP!**

---

## 🔬 LAB 7: Detective Work — Reading History (30 XP)

> *Fatima (QA): "OK Mehdi, I need you to tell me what changed in the last 3 commits. Can you do that?"*

### Challenge 1: See the last 3 commits

```bash
git log --oneline -3
```

**+10 XP**

### Challenge 2: See what EXACTLY changed in the most recent commit

```bash
git show HEAD
```

→ Shows the full diff of the latest commit.

**+10 XP**

### Challenge 3: See all commits with stats (which files, how many lines)

```bash
git log --stat -3
```

→ Shows `file | lines changed` for each commit.

**+10 XP**

> **Fatima:** "Good. If I ever ask 'what changed?', this is how you find out. `git log` and `git show` are your best friends."

---

## 💥 BOSS FIGHT: The Rapid Commit Challenge (80 XP)

> *Sara: "OK rookie, let's see if you actually learned something. Here's a timed challenge."*
>
> **⏱️ Try to finish in under 5 minutes!**

**Mission: Create 3 files, make 3 separate commits, then verify the history.**

### Step 1: Create a config file

```bash
echo "PORT=8000" > config.txt
echo "DEBUG=true" >> config.txt
echo "DB_FILE=taskflow.db" >> config.txt
```

Stage and commit:

```bash
git add config.txt
git commit -m "feat: add application config file"
```

### Step 2: Create a changelog

```bash
echo "# Changelog" > CHANGELOG.md
echo "## v1.0.0 - Initial Release" >> CHANGELOG.md
echo "- Basic task management" >> CHANGELOG.md
echo "- REST API" >> CHANGELOG.md
```

Stage and commit:

```bash
git add CHANGELOG.md
git commit -m "docs: add changelog for v1.0.0"
```

### Step 3: Create a contribution guide

```bash
echo "# Contributing" > CONTRIBUTING.md
echo "1. Fork the repo" >> CONTRIBUTING.md
echo "2. Create a feature branch" >> CONTRIBUTING.md
echo "3. Submit a pull request" >> CONTRIBUTING.md
```

Stage and commit:

```bash
git add CONTRIBUTING.md
git commit -m "docs: add contributing guidelines"
```

### Step 4: Verify EVERYTHING

```bash
git log --oneline
```

**Do you see 8 total commits?** If yes:

🎉 **+50 XP!**
🏅 **ACHIEVEMENT UNLOCKED: Rapid Fire — 3 commits in 5 minutes!**

### Bonus: Can you answer these without scrolling up?

```bash
git log --oneline --author="Mehdi" | wc -l
```

How many commits did "you" make? **+15 XP** if correct!

```bash
git log --oneline --grep="docs"
```

How many commits have "docs" in the message? **+15 XP** if correct!

---

## ❓ POP QUIZ #2 (Answers below)

**Circle / write down your answers before checking:**

1. What does `git status` show you?
2. What's the difference between `git diff` and `git log`?
3. What does the `.` in `git add .` mean?
4. What's wrong with this commit message: `git commit -m "update"`?
5. Your file is RED in `git status`. What does that mean?
6. Your file is GREEN in `git status`. What does that mean?
7. **HARD:** What happens if you run `git commit` without running `git add` first?

---

## 🧠 Day 1 Summary

| Command | What It Does | Memory Trick |
|---------|-------------|--------------|
| `git init` | Create a new repo | "Initialize" = start |
| `git status` | See what changed | Check the weather before going out |
| `git add .` | Stage all changes | Put items in the box |
| `git add <file>` | Stage one file | Pick one item for the box |
| `git diff` | See line-by-line changes | "What did I touch?" |
| `git commit -m "msg"` | Save a snapshot | Tape the box shut with a label |
| `git log --oneline` | View commit history | Read your diary |
| `git show HEAD` | See latest commit's details | "Show me what just happened" |

---

## 🏆 Day 1 Scorecard

```
LAB 1: Identity setup .............. 10 XP
LAB 2: Create repository ........... 20 XP
LAB 3: First staging ............... 30 XP
LAB 4: First commit ................ 40 XP
LAB 5: Changes & second commit ..... 40 XP
LAB 6: Team simulation ............. 50 XP
LAB 7: Detective work .............. 30 XP
BOSS: Rapid commit challenge ........ 80 XP
────────────────────────────────────────
TOTAL                              300 XP

YOUR SCORE: ____ / 300
```

**Your rank after Day 1:** 🌱 Git Seedling → 🌿 Git Apprentice (if you got 300!)

---

## 📝 Quiz Answers

**Quiz #1:**
1. `git init`
2. Working Directory → Staging Area → Repository
3. `git add`
4. `git add` puts files in the staging area (ready to commit). `git commit` saves the snapshot permanently.

**Quiz #2:**
1. Which files have been modified, staged, or are untracked
2. `git diff` shows line-by-line changes in files. `git log` shows commit history.
3. "All files in the current directory"
4. It's too vague. What was updated? A good message: `docs: update setup instructions`
5. Modified but NOT staged (or untracked)
6. Staged and ready to be committed
7. Nothing happens! Git says "nothing to commit." You MUST `git add` before `git commit`.

---

## ⏭️ Next Episode

**[Day 2: You Broke Something 🔥 →](day-02-fixing-mistakes.md)**

> Tomorrow: you accidentally delete code, write bad commits, and break things. Don't worry — Git can fix ALL of it. Also, Omar force-pushes something and Ahmed has a meltdown. Fun times. 😈
