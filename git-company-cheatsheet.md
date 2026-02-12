# 📋 TechCorp Git Cheatsheet — Everything on One Page

> *Print this. Pin it to your desk. You WILL need it.*

---

## 🟢 SETUP & CONFIG

```bash
git init                                    # Initialize new repo
git config --global user.name "Name"        # Set your name
git config --global user.email "email"      # Set your email
git config --global core.editor "code -w"   # Use VS Code as editor
git config --global init.defaultBranch main # Default branch = main
```

---

## 🔵 DAILY COMMANDS

```bash
git status                     # What changed? (run this CONSTANTLY)
git add <file>                 # Stage a file
git add .                      # Stage ALL changes
git add -p <file>              # Stage parts of a file (interactive chunks)
git commit -m "message"        # Commit staged changes
git commit --amend             # Edit last commit (message + files)
git commit --amend --no-edit   # Add to last commit (keep message)
git diff                       # See unstaged changes
git diff --staged              # See staged changes
git log --oneline              # Compact commit history
git log --oneline --graph --all  # Visual branch graph
```

---

## 🟡 BRANCHING & MERGING

```bash
git branch                     # List branches
git branch <name>              # Create branch
git branch -d <name>           # Delete branch (safe)
git branch -D <name>           # Force-delete branch
git checkout <branch>          # Switch to branch
git checkout -b <name>         # Create + switch
git merge <branch>             # Merge branch into current
```

### Merge Conflict Resolution:

```bash
# 1. Open conflicted file, find:
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> branch-name

# 2. Keep what you want, delete markers
# 3. Stage + commit
git add <file>
git commit -m "fix: resolve merge conflict in <file>"
```

---

## 🟣 REMOTE / GITHUB

```bash
git remote add origin <url>           # Connect to GitHub
git push -u origin main               # First push (sets upstream)
git push                              # Push commits
git pull                              # Pull latest changes
git clone <url>                       # Clone a repository
git fetch                             # Download updates (don't merge)
```

### Pull Request Workflow:

```bash
git checkout -b feature/name          # 1. Create feature branch
# ... make changes, commit ...
git push origin feature/name          # 2. Push branch
# 3. Open PR on GitHub
# 4. Get code review
# 5. Merge on GitHub
git checkout main && git pull         # 6. Update local main
git branch -d feature/name            # 7. Clean up
```

---

## 🔴 UNDO & FIX

```bash
# Undo unstaged changes (restore file to last commit):
git restore <file>

# Unstage a file (keep changes):
git restore --staged <file>

# Undo last commit (keep changes staged):
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged):
git reset HEAD~1

# NUKE last commit (⚠️ DESTROYS CHANGES):
git reset --hard HEAD~1

# Edit last commit message:
git commit --amend -m "new message"

# Safely undo a PUSHED commit:
git revert <hash>
```

---

## ⚡ ADVANCED

### Rebase (Clean Linear History)

```bash
git rebase main                       # Replay commits on top of main
git rebase -i HEAD~N                  # Interactive: squash/reword/drop
```

**Interactive rebase keywords:**

| Key | What it does |
|-----|-------------|
| `pick` | Keep commit |
| `squash` | Combine + keep both messages |
| `fixup` | Combine + discard this message |
| `reword` | Change commit message |
| `edit` | Pause to modify |
| `drop` | Delete commit |

> ⚠️ **NEVER rebase pushed commits on shared branches!**

### Bisect (Find Bug with Binary Search)

```bash
git bisect start                      # Start bisecting
git bisect bad                        # Current is broken
git bisect good <hash>                # This commit was working
# ... test each checkout, mark good/bad ...
git bisect reset                      # Exit bisect
```

### Tags (Version Releases)

```bash
git tag v1.0.0                        # Lightweight tag
git tag -a v1.0.0 -m "Release 1.0"   # Annotated tag (preferred)
git push origin --tags                # Push all tags
git tag                               # List all tags
```

**Semantic Versioning:** `vMAJOR.MINOR.PATCH`
- PATCH: bug fix (v1.0.0 → v1.0.1)
- MINOR: new feature (v1.0.0 → v1.1.0)
- MAJOR: breaking change (v1.0.0 → v2.0.0)

### Stash (Save Work Temporarily)

```bash
git stash                             # Stash current changes
git stash push -m "description"       # Stash with label
git stash list                        # See all stashes
git stash pop                         # Restore latest stash
git stash apply stash@{N}             # Apply specific stash
git stash drop stash@{N}              # Remove specific stash
```

### Cherry-Pick (Copy Specific Commits)

```bash
git cherry-pick <hash>                # Apply one commit to current branch
```

### Blame (Who Wrote This?)

```bash
git blame <file>                      # Show author of each line
```

### Reflog (Recover ANYTHING)

```bash
git reflog                            # See ALL actions (the ultimate diary)
# Recover deleted branch:
git checkout -b <branch-name> <hash-from-reflog>
# Undo bad reset:
git reset --hard <hash-from-reflog>
```

> Reflog entries expire after **90 days**.

---

## 🛡️ .gitignore Patterns

```
# Common patterns:
__pycache__/          # Python cache
*.pyc                 # Compiled Python
node_modules/         # Node dependencies
.env                  # Environment variables (SECRETS!)
*.log                 # Log files
.DS_Store             # macOS junk
Thumbs.db             # Windows junk
.vscode/              # Editor settings (optional)
dist/                 # Build output
*.sqlite3             # Database files
```

---

## ✅ COMMIT MESSAGE FORMAT

```
<type>: <short description>

Types:
  feat:     New feature
  fix:      Bug fix
  docs:     Documentation
  style:    Formatting (no code change)
  refactor: Code restructure (no behavior change)
  test:     Add/fix tests
  chore:    Maintenance tasks

Examples:
  feat: add dark mode toggle
  fix: resolve login timeout on slow connections
  docs: update API endpoint descriptions
  refactor: extract validation into helper function
```

---

## 🔄 DAILY ROUTINE

```bash
# Morning:
git checkout main
git pull
git checkout -b feature/todays-work

# During the day:
git add -p .                           # Review + stage chunks
git commit -m "feat: description"      # Commit frequently!

# End of day:
git push origin feature/todays-work    # Push your branch
# Open PR on GitHub if ready
```

---

## 🚨 EMERGENCY: HOTFIX

```bash
git stash                              # Save current work
git checkout main
git pull
git checkout -b hotfix/critical-bug
# ... fix the bug ...
git add . && git commit -m "fix: critical bug description"
git push origin hotfix/critical-bug
# Open PR → merge ASAP
git checkout main && git pull
git checkout <your-branch>
git stash pop                          # Resume your work
```

---

## 🎖️ USEFUL ALIASES

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

---

> *"Commit early. Commit often. Push before you leave."* — The entire TechCorp team 🚀
