# Contributing to Git for Real Teams

Thank you for your interest in making this course better! Whether you're fixing a typo or adding an entire new lab, your contribution matters.

## How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/taskflow-company-demo.git
cd taskflow-company-demo
```

### 2. Create a Branch

```bash
git checkout -b fix/your-improvement
```

Use prefixes: `fix/`, `feat/`, `docs/`, `lab/`

### 3. Make Changes

Follow the existing style:
- Labs use the `### Lab X:` heading format
- XP awards appear as `**+XX XP!**`
- Character dialogue uses `> **Name:** "quote"` format
- Boss fights use `## 💥 BOSS FIGHT:` heading

### 4. Submit a Pull Request

```bash
git add .
git commit -m "docs: improve Day 3 merge conflict explanation"
git push origin fix/your-improvement
```

Then open a PR on GitHub.

---

## What We're Looking For

| Type | Examples |
|------|----------|
| **Bug fixes** | Typos, broken commands, incorrect XP totals |
| **New labs** | Additional practice exercises for any day |
| **Quiz questions** | More quiz items with 4 options and 1 correct answer |
| **Translations** | Translate day files to other languages |
| **Lab runner** | New interactive day implementations in `lab-runner.py` |
| **Accessibility** | Improve instructions for screen readers, colorblind users |

## Style Guide

- **Commit messages:** Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`)
- **Language:** Casual but professional. Match the "TechCorp office" tone
- **Characters:** Keep them in character (Sara = mentor, Ahmed = precise, Omar = chaotic)
- **XP values:** Small task = 10-20 XP, lab = 30-50 XP, boss fight = 80-140 XP

## Code of Conduct

Be kind. This is a learning resource. Everyone starts somewhere.

---

Questions? Open an issue and we'll help you get started.
