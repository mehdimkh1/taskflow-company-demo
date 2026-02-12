<p align="center">
  <img src="https://img.shields.io/badge/Days-6-blue?style=for-the-badge" alt="6 Days" />
  <img src="https://img.shields.io/badge/XP-3000-gold?style=for-the-badge" alt="3000 XP" />
  <img src="https://img.shields.io/badge/Labs-35-green?style=for-the-badge" alt="35 Labs" />
  <img src="https://img.shields.io/badge/Boss_Fights-6-red?style=for-the-badge" alt="6 Boss Fights" />
  <img src="https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python" alt="Python 3.7+" />
</p>

# 🏢 Git for Real Teams

**A 6-day gamified Git training course that simulates working at a real software company.**

You're the new developer at **TechCorp**. Your teammates are Sara (Senior Frontend), Ahmed (Backend Lead), Lina (PM), Youssef (DevOps), Fatima (QA), and Omar (the intern who breaks everything). Over 6 days, you'll learn Git the way professionals use it — through hands-on labs, boss fights, and real-world scenarios.

> *"I hear and I forget. I see and I remember. I do and I understand."*

---

## 🎮 Quick Start

```bash
# Clone the repo
git clone https://github.com/mehdimkh1/taskflow-company-demo.git
cd taskflow-company-demo

# Launch the interactive lab runner
python lab-runner.py
```

**No dependencies required** — just Python 3.7+ and Git.

---

## 📋 Curriculum

| Day | Topic | XP | Labs | What You'll Master |
|-----|-------|-----|------|---------------------|
| **1** | [First Day at Work](day-01-getting-started.md) | 300 | 7 | `init`, `add`, `commit`, `status`, `diff`, `log` |
| **2** | [Fixing Mistakes](day-02-fixing-mistakes.md) | 400 | 6 | `restore`, `amend`, `reset`, `.gitignore` |
| **3** | [Branching & Merging](day-03-branching-merging.md) | 600 | 6 | `branch`, `checkout`, `merge`, conflict resolution |
| **4** | [GitHub & Remotes](day-04-github-remotes.md) | 500 | 6 | `push`, `pull`, `clone`, pull requests, forks |
| **5** | [Team Workflows](day-05-team-workflows.md) | 600 | 6 | `stash`, `blame`, `cherry-pick`, sprint simulation |
| **6** | [Advanced Tricks](day-06-advanced-tricks.md) | 600 | 4 | `rebase`, `bisect`, `tag`, `reflog`, aliases |

**Bonus resources:**
- [Course Overview & Story](git-course-overview.md) — Meet the team, see the rank system
- [Company Cheatsheet](git-company-cheatsheet.md) — Quick reference card for all commands

---

## 🧭 How It Works

### Two ways to learn:

**1. Interactive Lab Runner** (recommended)
```bash
python lab-runner.py          # Start from where you left off
python lab-runner.py day 1    # Jump to a specific day
python lab-runner.py progress # Check your stats
```
The lab runner validates your commands in real-time, tracks XP, unlocks achievements, and creates a sandbox environment to practice safely.

**2. Read-Along Guides**
Open any `day-XX-*.md` file and follow the step-by-step labs manually. Each guide includes all instructions, examples, quizzes, and boss fight challenges.

### Progression System

```
🌱 Seedling        0 XP      Day 1: You're new here
🌿 Apprentice    700 XP      Day 2-3: Making progress
🔥 Adept       1,500 XP      Day 4: GitHub unlocked
⚔️  Warrior     2,200 XP      Day 5: Team player
🏆 Legend      2,800 XP      Day 6: Git master
```

### 12 Achievements to Unlock

| Badge | Achievement | How to Earn |
|-------|-------------|-------------|
| 🏅 | First Commit | Make your first commit |
| 🏅 | Time Traveler | Use `git log` and `git show` |
| 🏅 | Quiz Ace | Score 100% on a quiz |
| 🏅 | Rapid Fire | Beat the speed boss fight |
| 🏅 | Undo Master | Master all undo commands |
| 🏅 | Clean History | Use `git commit --amend` |
| 🏅 | Branch Navigator | Create & switch branches |
| 🏅 | Conflict Resolver | Solve a merge conflict |
| 🏅 | Cloud Pusher | Push to GitHub |
| 🏅 | Team Player | Complete a pull request |
| 🏅 | Firefighter | Handle a production hotfix |
| 🏅 | Git Hero | Complete the full course |

---

## 📁 Project Structure

```
├── lab-runner.py                   # Interactive CLI lab runner
├── git-course-overview.md          # Story, characters, rank system
├── day-01-getting-started.md       # Day 1: Git basics
├── day-02-fixing-mistakes.md       # Day 2: Undo commands
├── day-03-branching-merging.md     # Day 3: Branches & merging
├── day-04-github-remotes.md        # Day 4: GitHub & remotes
├── day-05-team-workflows.md        # Day 5: Team collaboration
├── day-06-advanced-tricks.md       # Day 6: Advanced Git
├── git-company-cheatsheet.md       # Quick reference card
├── CONTRIBUTING.md                 # How to contribute
├── LICENSE                         # MIT License
│
├── index.html                      # Sample project files
├── style.css                       # (used in labs)
├── app.js
├── server.py
└── database.py
```

---

## 🎯 Who Is This For?

| Audience | Why This Course |
|----------|-----------------|
| **Complete beginners** | Start from "what is Git?" with zero assumptions |
| **CS students** | Hands-on labs beat any lecture |
| **Bootcamp grads** | Fill the Git gap that bootcamps skip |
| **Teams onboarding** | Standard training path for new hires |
| **Self-learners** | Gamification keeps you motivated |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- Bug fixes and typo corrections
- New labs or quiz questions
- Translations to other languages
- Improvements to the lab runner

---

## 📜 License

[MIT License](LICENSE) — use this course freely for personal or organizational training.

---

<p align="center">
  <b>Built with ❤️ for developers who learn by doing.</b><br>
  <sub>Created by <a href="https://github.com/mehdimkh1">Mehdi Mekhatria</a></sub>
</p>
