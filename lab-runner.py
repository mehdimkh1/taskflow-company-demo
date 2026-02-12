"""
🏢 Git for Real Teams — Interactive Lab Runner
================================================
A CLI tool that validates your lab exercises, tracks XP, 
and gives real-time feedback as you work through the course.

Usage:
    python lab-runner.py              Interactive menu
    python lab-runner.py day 1        Jump to Day 1
    python lab-runner.py progress     See your progress
    python lab-runner.py reset        Reset all progress

No dependencies required — just Python 3.7+ and Git.
"""

import os
import sys
import subprocess
import json
import time
import shutil

# ─── COLORS ────────────────────────────────────────────
class C:
    GOLD   = "\033[93m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    MAGENTA = "\033[95m"
    DIM    = "\033[90m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

# ─── STATE ─────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "lab_progress.json")
SANDBOX_DIR = os.path.join(SCRIPT_DIR, "sandbox")

state = {
    "xp": 0,
    "day": 1,
    "lab": 1,
    "achievements": [],
    "completed_labs": [],
    "rank": "Seedling",
}

# ─── HELPERS ───────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause(msg="Press ENTER to continue..."):
    input(f"\n  {C.DIM}{msg}{C.RESET}")

def banner(text):
    width = max(len(text) + 4, 50)
    print(f"\n{C.GOLD}  {'═' * width}")
    print(f"  ║ {text:^{width - 4}} ║")
    print(f"  {'═' * width}{C.RESET}\n")

def slow_print(text, delay=0.015):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_xp():
    rank = get_rank()
    print(f"\n  {C.GOLD}⭐ XP: {state['xp']} / 3000  |  Rank: {rank}{C.RESET}")

def award_xp(amount, reason):
    state["xp"] += amount
    print(f"  {C.GREEN}  +{amount} XP — {reason}{C.RESET}")

def achievement(name):
    if name not in state["achievements"]:
        state["achievements"].append(name)
        print(f"\n  {C.MAGENTA}  🏅 ACHIEVEMENT UNLOCKED: {name}{C.RESET}\n")

def mission(text):
    print(f"  {C.BOLD}🎯 MISSION: {text}{C.RESET}")

def story(text):
    print(f"  {C.CYAN}  {text}{C.RESET}")

def instruction(text):
    print(f"\n  {C.BOLD}  {text}{C.RESET}")

def success(text):
    print(f"  {C.GREEN}  ✅ {text}{C.RESET}")

def fail(text):
    print(f"  {C.RED}  ❌ {text}{C.RESET}")

def hint(text):
    print(f"  {C.DIM}  💡 Hint: {text}{C.RESET}")

def show_command(cmd):
    print(f"\n  {C.CYAN}  $ {cmd}{C.RESET}\n")

def wait_for_command(prompt_text="  Type the command: "):
    return input(f"  {C.CYAN}{prompt_text}{C.RESET}").strip()

def get_rank():
    xp = state["xp"]
    if xp >= 2800:   return "🏆 Git Legend"
    if xp >= 2200:   return "⚔️ Git Warrior"
    if xp >= 1500:   return "🔥 Git Adept"
    if xp >= 700:    return "🌿 Git Apprentice"
    return "🌱 Seedling"

# ─── GIT HELPERS ───────────────────────────────────────
def run_git(*args, cwd=None):
    try:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=cwd or SANDBOX_DIR,
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def is_git_repo(path=None):
    p = path or SANDBOX_DIR
    return os.path.isdir(os.path.join(p, ".git"))

def check_file(filename, cwd=None):
    return os.path.exists(os.path.join(cwd or SANDBOX_DIR, filename))

def read_local_file(filename, cwd=None):
    path = os.path.join(cwd or SANDBOX_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return ""

def write_local_file(filename, content, cwd=None):
    path = os.path.join(cwd or SANDBOX_DIR, filename)
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else (cwd or SANDBOX_DIR), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_current_branch(cwd=None):
    ok, out = run_git("branch", "--show-current", cwd=cwd)
    return out.strip() if ok else ""

def get_branches(cwd=None):
    ok, out = run_git("branch", cwd=cwd)
    if ok:
        return [b.strip().lstrip("* ") for b in out.strip().split("\n") if b.strip()]
    return []

def get_commit_messages(count=5, cwd=None):
    ok, out = run_git("log", f"--oneline", f"-{count}", cwd=cwd)
    return out.strip() if ok else ""

def get_commit_count(cwd=None):
    ok, out = run_git("rev-list", "--count", "HEAD", cwd=cwd)
    try:
        return int(out.strip()) if ok else 0
    except:
        return 0

# ─── SAVE / LOAD ──────────────────────────────────────
def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load():
    global state
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            state = json.load(f)
        return True
    return False

def reset():
    global state
    state = {"xp": 0, "day": 1, "lab": 1, "achievements": [], "completed_labs": [], "rank": "Seedling"}
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    if os.path.exists(SANDBOX_DIR):
        shutil.rmtree(SANDBOX_DIR)

def mark_lab_done(day, lab):
    key = f"d{day}l{lab}"
    if key not in state["completed_labs"]:
        state["completed_labs"].append(key)
    save()

def is_lab_done(day, lab):
    return f"d{day}l{lab}" in state["completed_labs"]

# ─── SANDBOX SETUP ─────────────────────────────────────
def setup_sandbox():
    """Create the sandbox directory with sample project files."""
    os.makedirs(SANDBOX_DIR, exist_ok=True)

    if not check_file("index.html"):
        write_local_file("index.html",
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n'
            '    <title>TaskFlow - Task Manager</title>\n    <link rel="stylesheet" href="style.css">\n'
            '</head>\n<body>\n    <header>\n        <h1>TaskFlow</h1>\n        '
            '<p>Manage your tasks efficiently</p>\n    </header>\n\n    <main>\n'
            '        <div id="task-list">\n            <h2>My Tasks</h2>\n'
            '        </div>\n    </main>\n\n    <script src="app.js"></script>\n</body>\n</html>\n')

    if not check_file("style.css"):
        write_local_file("style.css",
            'body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n'
            '    background-color: #f5f5f5;\n}\n\nheader {\n    text-align: center;\n    padding: 20px;\n'
            '    background-color: #2c3e50;\n    color: white;\n    border-radius: 8px;\n}\n\n'
            '#task-list {\n    max-width: 600px;\n    margin: 20px auto;\n    padding: 20px;\n'
            '    background: white;\n    border-radius: 8px;\n}\n\n.task-item {\n    padding: 10px;\n'
            '    border-bottom: 1px solid #eee;\n}\n')

    if not check_file("app.js"):
        write_local_file("app.js",
            '// TaskFlow - Main Application\n\nconst tasks = [];\n\n'
            'function addTask(title) {\n    tasks.push({ id: tasks.length + 1, title, completed: false });\n'
            '    renderTasks();\n}\n\nfunction renderTasks() {\n'
            '    const list = document.getElementById("task-list");\n    list.innerHTML = "<h2>My Tasks</h2>";\n'
            '    tasks.forEach(task => {\n        const div = document.createElement("div");\n'
            '        div.className = "task-item";\n        div.textContent = task.title;\n'
            '        list.appendChild(div);\n    });\n}\n\nconsole.log("TaskFlow loaded!");\n')

    if not check_file("server.py"):
        write_local_file("server.py",
            '# TaskFlow Backend API\n\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\nimport json\n\n'
            'tasks = [\n    {"id": 1, "title": "Set up project", "completed": True},\n'
            '    {"id": 2, "title": "Build login page", "completed": False},\n]\n\n'
            'class TaskHandler(BaseHTTPRequestHandler):\n    def do_GET(self):\n'
            '        if self.path == "/api/tasks":\n            self.send_response(200)\n'
            '            self.send_header("Content-Type", "application/json")\n'
            '            self.end_headers()\n            self.wfile.write(json.dumps(tasks).encode())\n\n'
            'if __name__ == "__main__":\n    server = HTTPServer(("localhost", 8000), TaskHandler)\n'
            '    print("Server running on http://localhost:8000")\n    server.serve_forever()\n')

    if not check_file("database.py"):
        write_local_file("database.py",
            '# Database module for TaskFlow\n\nimport sqlite3\n\nDB_FILE = "taskflow.db"\n\n'
            'def init_db():\n    conn = sqlite3.connect(DB_FILE)\n    cursor = conn.cursor()\n'
            '    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (\n'
            '        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        title TEXT NOT NULL,\n'
            '        completed BOOLEAN DEFAULT 0\n    )""")\n    conn.commit()\n    conn.close()\n\n'
            'if __name__ == "__main__":\n    init_db()\n    print("Database ready!")\n')

# ═══════════════════════════════════════════════════════
# DAY 1: FIRST DAY AT WORK
# ═══════════════════════════════════════════════════════
def day_1():
    clear()
    banner("DAY 1: FIRST DAY AT WORK  🌱  300 XP")

    print(f"""
  {C.DIM}  Monday morning. You walk into TechCorp's office.
  The coffee machine is broken. Omar has already accidentally
  deleted a folder. Sara walks over and says:{C.RESET}

  {C.BOLD}  "Welcome to the team. First things first — 
   let's get you set up with Git."{C.RESET}
""")
    pause()

    # ─── LAB 1: Identity Setup ───
    clear()
    banner("DAY 1 — LAB 1: IDENTITY SETUP  (10 XP)")
    mission("Tell Git who you are.")

    story('"Git needs to know who you are. Every commit')
    story(' you make will have your name on it — forever."')
    story(' — Sara')

    instruction("Set your name (use YOUR actual name):")
    show_command('git config --global user.name "Your Name"')

    while True:
        cmd = wait_for_command()
        if cmd.startswith("git config") and "user.name" in cmd:
            os.system(cmd)
            success("Name configured!")
            award_xp(5, "Identity: name")
            break
        else:
            hint('Type: git config --global user.name "Your Name"')

    instruction("Now set your email:")
    show_command('git config --global user.email "you@example.com"')

    while True:
        cmd = wait_for_command()
        if cmd.startswith("git config") and "user.email" in cmd:
            os.system(cmd)
            success("Email configured!")
            award_xp(5, "Identity: email")
            break
        else:
            hint('Type: git config --global user.email "your@email.com"')

    mark_lab_done(1, 1)

    print(f"""
  {C.DIM}  Omar tries: git config --global user.name Omar the Great
  Sara: "...use quotes, Omar."
  Omar: 😅{C.RESET}
""")
    pause()

    # ─── LAB 2: Create the Repository ───
    clear()
    banner("DAY 1 — LAB 2: CREATE THE REPOSITORY  (20 XP)")
    mission("Put the TaskFlow project under version control.")

    story('"The TaskFlow project has files but NO Git.')
    story(' Your job: initialize a Git repository."  — Sara')

    # Set up sandbox
    setup_sandbox()

    print(f"\n  {C.BOLD}  The project files are ready in the sandbox folder.{C.RESET}")
    print(f"  {C.DIM}  Files: index.html, style.css, app.js, server.py, database.py{C.RESET}\n")

    instruction("Initialize a Git repository:")
    show_command("git init")

    while True:
        cmd = wait_for_command()
        if cmd.strip() == "git init":
            if not is_git_repo():
                ok, out = run_git("init")
                if ok:
                    print(f"  {C.DIM}  {out.strip()}{C.RESET}")
                    success("Git repository created!")
                    award_xp(20, "First repo initialized")
                else:
                    fail(out)
            else:
                success("Repository already initialized!")
                award_xp(20, "Repository ready")
            break
        else:
            hint("Type exactly: git init")

    mark_lab_done(1, 2)
    pause()

    # ─── LAB 3: The Three Zones ───
    clear()
    banner("DAY 1 — LAB 3: STAGING & COMMITTING  (40 XP)")
    mission("Stage files and make your first commit.")

    print(f"""
  {C.BOLD}  Git has 3 zones:{C.RESET}

  {C.RED}  📂 WORKING DIR{C.RESET}    →    {C.GOLD}📋 STAGING{C.RESET}    →    {C.GREEN}📦 COMMITTED{C.RESET}
     (your files)        (ready to save)      (saved!)
                    {C.CYAN}git add{C.RESET}          {C.GOLD}git commit{C.RESET}

  {C.DIM}  Ahmed's way of explaining it:{C.RESET}
  {C.BOLD}  "It's like mailing a package.
   1. Pick items from your room    (edit files)
   2. Put them in the box          (git add)
   3. Seal and label the box       (git commit)"{C.RESET}
""")

    instruction("First, check what Git sees:")
    show_command("git status")

    while True:
        cmd = wait_for_command()
        if "status" in cmd:
            ok, out = run_git("status")
            print(f"\n  {C.RED}  {out.replace(chr(10), chr(10) + '  ')}{C.RESET}")
            print(f"\n  {C.BOLD}  All files are RED = Git sees them but they're not staged.{C.RESET}")
            award_xp(5, "First status check")
            break
        else:
            hint("Type: git status")

    instruction("Stage ALL files at once:")
    show_command("git add .")

    while True:
        cmd = wait_for_command()
        if "git add" in cmd:
            run_git("add", ".")
            success("All files staged!")
            award_xp(5, "Files staged")
            break
        else:
            hint("Type: git add .")

    instruction("Check status again — see the difference:")
    show_command("git status")

    while True:
        cmd = wait_for_command()
        if "status" in cmd:
            ok, out = run_git("status")
            print(f"\n  {C.GREEN}  {out.replace(chr(10), chr(10) + '  ')}{C.RESET}")
            print(f"\n  {C.BOLD}  Now they're GREEN = staged and ready to be committed!{C.RESET}")
            break
        else:
            hint("Type: git status")

    print(f"""
  {C.BOLD}  Pro Commit Message Format (required at TechCorp):{C.RESET}

  {C.CYAN}  type: description{C.RESET}

  {C.GREEN}feat:{C.RESET}  New feature       {C.GREEN}fix:{C.RESET}   Bug fix
  {C.GREEN}docs:{C.RESET}  Documentation     {C.GREEN}style:{C.RESET} CSS/formatting
  {C.GREEN}test:{C.RESET}  Adding tests      {C.GREEN}chore:{C.RESET} Maintenance
""")

    instruction("Make your first commit:")
    show_command('git commit -m "feat: initialize TaskFlow project"')

    while True:
        cmd = wait_for_command()
        if "commit" in cmd and "-m" in cmd:
            msg = "feat: initialize TaskFlow project"
            try:
                msg = cmd.split("-m")[-1].strip().strip('"').strip("'") or msg
            except:
                pass
            run_git("commit", "-m", msg)
            success("FIRST COMMIT! Your code is now saved in history!")
            award_xp(30, "First commit at TechCorp")
            achievement("First Commit")
            break
        else:
            hint('Type: git commit -m "feat: initialize TaskFlow project"')

    mark_lab_done(1, 3)
    pause()

    # ─── LAB 4: Making Changes ───
    clear()
    banner("DAY 1 — LAB 4: TRACK CHANGES  (30 XP)")
    mission("Edit a file, see the diff, commit the change.")

    story('"Lina just messaged: the client wants the app header')
    story(' to say \'TaskFlow Pro\' instead of \'TaskFlow\'."  — Sara')

    instruction("Edit index.html — change the heading:")
    show_command('Replace <h1>TaskFlow</h1> with <h1>TaskFlow Pro</h1>')

    print(f"  {C.DIM}  (I'll simulate the edit for you...){C.RESET}")
    time.sleep(0.5)

    content = read_local_file("index.html")
    content = content.replace("<h1>TaskFlow</h1>", "<h1>TaskFlow Pro</h1>")
    content = content.replace("<title>TaskFlow - Task Manager</title>", "<title>TaskFlow Pro - Task Manager</title>")
    write_local_file("index.html", content)
    success("File edited!")

    instruction("See what changed:")
    show_command("git diff")

    while True:
        cmd = wait_for_command()
        if "diff" in cmd:
            ok, out = run_git("diff")
            for line in out.split("\n"):
                if line.startswith("+") and not line.startswith("+++"):
                    print(f"  {C.GREEN}  {line}{C.RESET}")
                elif line.startswith("-") and not line.startswith("---"):
                    print(f"  {C.RED}  {line}{C.RESET}")
                elif line.strip():
                    print(f"  {C.DIM}  {line}{C.RESET}")
            print(f"\n  {C.BOLD}  RED = removed  |  GREEN = added{C.RESET}")
            award_xp(10, "Read your first diff")
            break
        else:
            hint("Type: git diff")

    instruction("Stage and commit the change:")
    show_command("git add index.html")

    while True:
        cmd = wait_for_command()
        if "add" in cmd:
            run_git("add", "index.html")
            break
        else:
            hint("Type: git add index.html")

    show_command('git commit -m "feat: rename app to TaskFlow Pro"')

    while True:
        cmd = wait_for_command()
        if "commit" in cmd:
            msg = "feat: rename app to TaskFlow Pro"
            try:
                msg = cmd.split("-m")[-1].strip().strip('"').strip("'") or msg
            except:
                pass
            run_git("commit", "-m", msg)
            success("Change committed!")
            award_xp(20, "Edit → diff → commit workflow")
            break
        else:
            hint('Type: git commit -m "feat: rename app to TaskFlow Pro"')

    mark_lab_done(1, 4)
    pause()

    # ─── LAB 5: View History ───
    clear()
    banner("DAY 1 — LAB 5: EXPLORE HISTORY  (20 XP)")
    mission("Navigate your commit timeline.")

    instruction("See your commit history:")
    show_command("git log --oneline")

    while True:
        cmd = wait_for_command()
        if "log" in cmd:
            ok, out = run_git("log", "--oneline")
            print(f"\n  {C.GREEN}  {out.replace(chr(10), chr(10) + '  ')}{C.RESET}")
            print(f"\n  {C.BOLD}  Each line = one commit. The code is 'abc123' = the commit ID.{C.RESET}")
            award_xp(10, "Explored history")
            break
        else:
            hint("Type: git log --oneline")

    instruction("See details of the last commit:")
    show_command("git show --stat HEAD")

    while True:
        cmd = wait_for_command()
        if "show" in cmd:
            ok, out = run_git("show", "--stat", "HEAD")
            print(f"\n  {C.GREEN}  {out.replace(chr(10), chr(10) + '  ')}{C.RESET}")
            success("You can inspect any commit in detail!")
            award_xp(10, "Inspected a commit")
            achievement("Time Traveler")
            break
        else:
            hint("Type: git show --stat HEAD")

    mark_lab_done(1, 5)
    pause()

    # ─── LAB 6: Team Simulation ───
    clear()
    banner("DAY 1 — LAB 6: TEAM SIMULATION  (50 XP)")
    mission("Watch what happens when teammates commit.")

    story('"While you were working, Ahmed pushed a database')
    story(' update. Sara added a dark mode stylesheet."')

    print(f"\n  {C.DIM}  (Simulating teammate activity...){C.RESET}")
    time.sleep(1)

    # Simulate Ahmed's work
    write_local_file("database.py",
        '# Database module for TaskFlow\n# Updated by Ahmed\n\nimport sqlite3\n\nDB_FILE = "taskflow.db"\n\n'
        'def init_db():\n    conn = sqlite3.connect(DB_FILE)\n    cursor = conn.cursor()\n'
        '    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (\n'
        '        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        title TEXT NOT NULL,\n'
        "        description TEXT DEFAULT '',\\n        completed BOOLEAN DEFAULT 0,\\n"
        "        assigned_to TEXT DEFAULT '',\\n"
        '        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n'
        '    )""")\n    conn.commit()\n    conn.close()\n\n'
        'def add_task(title, desc="", assigned=""):\n    conn = sqlite3.connect(DB_FILE)\n'
        '    cursor = conn.cursor()\n    cursor.execute("INSERT INTO tasks (title, description, assigned_to) VALUES (?, ?, ?)", (title, desc, assigned))\n'
        '    conn.commit()\n    conn.close()\n\n'
        'if __name__ == "__main__":\n    init_db()\n    print("Database ready!")\n')
    run_git("add", "database.py")
    run_git("commit", "-m", "feat: add task fields - description, assigned_to, timestamps")

    # Simulate Sara's work
    with open(os.path.join(SANDBOX_DIR, "style.css"), "a", encoding="utf-8") as f:
        f.write("\n/* Dark Mode - Added by Sara */\nbody.dark-mode {\n    background-color: #1a1a2e;\n    color: #e0e0e0;\n}\n")
    run_git("add", "style.css")
    run_git("commit", "-m", "style: add dark mode CSS variables")

    print(f"  {C.GREEN}  Ahmed committed: database improvements{C.RESET}")
    print(f"  {C.GREEN}  Sara committed: dark mode styles{C.RESET}")

    instruction("See the full team history:")
    show_command("git log --oneline")

    while True:
        cmd = wait_for_command()
        if "log" in cmd:
            ok, out = run_git("log", "--oneline")
            print(f"\n  {C.GREEN}  {out.replace(chr(10), chr(10) + '  ')}{C.RESET}")
            print(f"\n  {C.BOLD}  See? Multiple people's commits in one timeline!{C.RESET}")
            print(f"  {C.BOLD}  This is how Git works in a real team.{C.RESET}")
            award_xp(30, "Team timeline understood")
            break
        else:
            hint("Type: git log --oneline")

    instruction("See who changed what in a specific file:")
    show_command("git log --oneline -- database.py")

    while True:
        cmd = wait_for_command()
        if "log" in cmd and "database" in cmd:
            ok, out = run_git("log", "--oneline", "--", "database.py")
            print(f"\n  {C.GREEN}  {out.replace(chr(10), chr(10) + '  ')}{C.RESET}")
            success("File-specific history! Know who touched what file.")
            award_xp(20, "File-specific history")
            break
        else:
            hint("Type: git log --oneline -- database.py")

    mark_lab_done(1, 6)
    pause()

    # ─── POP QUIZ ───
    clear()
    banner("📝 DAY 1 POP QUIZ  (30 XP)")

    questions = [
        {
            "q": "What does 'git add .' do?",
            "options": ["a) Commits all files", "b) Stages all changed files", "c) Creates a new branch", "d) Pushes to GitHub"],
            "answer": "b",
            "xp": 10
        },
        {
            "q": "What color are STAGED files in 'git status'?",
            "options": ["a) Red", "b) Yellow", "c) Green", "d) Blue"],
            "answer": "c",
            "xp": 10
        },
        {
            "q": "What's the correct commit message format at TechCorp?",
            "options": ["a) fixed stuff", "b) fix: resolve login crash", "c) FIX LOGIN", "d) update"],
            "answer": "b",
            "xp": 10
        }
    ]

    quiz_xp = 0
    for i, q in enumerate(questions, 1):
        print(f"\n  {C.BOLD}  Q{i}: {q['q']}{C.RESET}")
        for opt in q["options"]:
            print(f"    {opt}")
        ans = input(f"\n  {C.CYAN}  Your answer (a/b/c/d): {C.RESET}").strip().lower()
        if ans == q["answer"]:
            success("Correct!")
            quiz_xp += q["xp"]
        else:
            fail(f"The answer was: {q['answer']}")

    if quiz_xp > 0:
        award_xp(quiz_xp, f"Quiz score: {quiz_xp}/{sum(q['xp'] for q in questions)}")

    if quiz_xp == 30:
        achievement("Quiz Ace")

    pause()

    # ─── BOSS FIGHT ───
    clear()
    banner("☠️  BOSS FIGHT: THE RAPID COMMIT CHALLENGE  (80 XP)")

    print(f"""
  {C.RED}
  Sara: "Quick test. You have 90 seconds to create a file,
  stage it, commit it, edit it, check the diff, and commit
  again. This is what a normal morning looks like. Ready?"
  {C.RESET}""")
    pause("Press ENTER to start the timer...")

    start_time = time.time()

    # Step 1
    print(f"\n  {C.GOLD}  TASK 1/4: Create a file called 'notes.txt'{C.RESET}")
    show_command('echo "Sprint planning notes" > notes.txt')
    while True:
        cmd = wait_for_command()
        if "notes" in cmd.lower():
            write_local_file("notes.txt", "Sprint planning notes\n")
            success("File created!")
            break
        else:
            hint("Type anything with 'notes' to create the file")

    # Step 2
    print(f"\n  {C.GOLD}  TASK 2/4: Stage and commit it{C.RESET}")
    show_command("git add notes.txt")
    while True:
        cmd = wait_for_command()
        if "add" in cmd:
            run_git("add", "notes.txt")
            break
        else:
            hint("Type: git add notes.txt")

    show_command('git commit -m "docs: add sprint planning notes"')
    while True:
        cmd = wait_for_command()
        if "commit" in cmd:
            run_git("commit", "-m", "docs: add sprint planning notes")
            success("Committed!")
            break
        else:
            hint('Type: git commit -m "docs: add sprint planning notes"')

    # Step 3
    print(f"\n  {C.GOLD}  TASK 3/4: Add a line to notes.txt{C.RESET}")
    show_command('echo "- Review PR #42" >> notes.txt')
    while True:
        cmd = wait_for_command()
        if "notes" in cmd.lower() or "echo" in cmd.lower():
            with open(os.path.join(SANDBOX_DIR, "notes.txt"), "a") as f:
                f.write("- Review PR #42\n")
            success("File updated!")
            break
        else:
            hint("Type anything to add to the file")

    # Step 4
    print(f"\n  {C.GOLD}  TASK 4/4: Stage + commit the update{C.RESET}")
    show_command("git add notes.txt")
    while True:
        cmd = wait_for_command()
        if "add" in cmd:
            run_git("add", "notes.txt")
            break
        else:
            hint("Type: git add notes.txt")

    show_command('git commit -m "docs: update sprint notes with PR review"')
    while True:
        cmd = wait_for_command()
        if "commit" in cmd:
            run_git("commit", "-m", "docs: update sprint notes with PR review")
            break
        else:
            hint('git commit -m "docs: update sprint notes"')

    elapsed = time.time() - start_time

    clear()
    if elapsed < 90:
        print(f"""
  {C.GREEN}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║     ☠️  BOSS DEFEATED IN {elapsed:.0f} SECONDS!  🎉     ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
  {C.RESET}""")
        award_xp(80, "Boss Fight: Rapid Commit!")
        achievement("Rapid Fire")
    else:
        print(f"""
  {C.GOLD}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║     Time: {elapsed:.0f}s — Over 90s, but you made it!  ║
    ║     Practice makes perfect.                      ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
  {C.RESET}""")
        award_xp(50, "Boss Fight: completed (over time)")

    pause()

    # ─── DAY COMPLETE ───
    clear()
    banner("DAY 1 COMPLETE! 🎉")
    print(f"""
{C.GREEN}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║  TODAY YOU LEARNED:                               ║
    ║                                                  ║
    ║  ✅ git config     Set your identity              ║
    ║  ✅ git init       Create a repository            ║
    ║  ✅ git add        Stage files                    ║
    ║  ✅ git commit     Save snapshots                 ║
    ║  ✅ git status     Check what's happening         ║
    ║  ✅ git diff       See what changed               ║
    ║  ✅ git log        View history                   ║
    ║  ✅ git show       Inspect commits                ║
    ║                                                  ║
    ║  Sara: "Not bad for day one. Don't be late       ║ 
    ║   tomorrow — we're covering UNDO commands."      ║
    ║                                                  ║
    ║  Omar: "Wait, how do I close Vim?"               ║
    ║  Ahmed: 😐                                       ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
{C.RESET}""")

    state["day"] = max(state["day"], 2)
    save()
    show_xp()
    pause("Press ENTER to return to the course menu...")


# ═══════════════════════════════════════════════════════
# DAY 2: FIXING MISTAKES
# ═══════════════════════════════════════════════════════
def day_2():
    clear()
    banner("DAY 2: FIXING MISTAKES  🔧  400 XP")

    print(f"""
  {C.DIM}  Tuesday morning. Slack is blowing up:{C.RESET}

  {C.RED}  Omar: "I broke everything. EVERYTHING."
  Sara:  "What did you do?"
  Omar:  "I don't know. I just typed stuff."
  Ahmed: "This is why we learn undo commands."{C.RESET}

  {C.BOLD}  Today you learn recovery spells.
  Things WILL go wrong. Here's how to fix them.{C.RESET}
""")
    pause()

    # Ensure sandbox is ready
    setup_sandbox()
    if not is_git_repo():
        run_git("init")
        run_git("add", ".")
        run_git("commit", "-m", "feat: initialize TaskFlow project")

    # ─── LAB 1: Undo Working Changes ───
    clear()
    banner("DAY 2 — LAB 1: UNDO UNSTAGED CHANGES  (30 XP)")
    mission("Revert a file to its last committed version.")

    story('"Omar just overwrote server.py with \'hello world\'."')
    story('"Let\'s save him." — Sara')

    instruction("Corrupt the server file (on purpose):")
    show_command('echo "OOPS I BROKE IT" > server.py')

    while True:
        cmd = wait_for_command()
        if "server" in cmd.lower() or "oops" in cmd.lower() or "broke" in cmd.lower():
            write_local_file("server.py", "OOPS I BROKE IT\n")
            success("Server corrupted! 😱")
            break
        else:
            hint("Type anything to corrupt the file")

    instruction("See the damage:")
    show_command("git diff server.py")

    while True:
        cmd = wait_for_command()
        if "diff" in cmd:
            ok, out = run_git("diff", "server.py")
            for line in out.split("\n"):
                if line.startswith("+") and not line.startswith("+++"):
                    print(f"  {C.RED}  {line}{C.RESET}")
                elif line.startswith("-") and not line.startswith("---"):
                    print(f"  {C.GREEN}  {line}{C.RESET}")
            break
        else:
            hint("Type: git diff server.py")

    instruction("RESTORE it to the last committed version:")
    show_command("git restore server.py")

    while True:
        cmd = wait_for_command()
        if "restore" in cmd:
            run_git("restore", "server.py")
            content = read_local_file("server.py")
            if "OOPS" not in content:
                success("RESTORED! Server is back to normal! 🎉")
            else:
                success("Restored!")
            award_xp(30, "git restore mastered")
            break
        else:
            hint("Type: git restore server.py")

    print(f"""
  {C.DIM}  Omar: "Wait, that's it? Just two words?"
  Sara:  "Yes. Git always has a backup of the last commit.
          git restore brings it back."
  Omar:  "I love Git."{C.RESET}
""")

    mark_lab_done(2, 1)
    pause()

    # ─── LAB 2: Unstage ───
    clear()
    banner("DAY 2 — LAB 2: UNSTAGE FILES  (20 XP)")
    mission("Remove a file from staging without losing changes.")

    instruction("Create and stage a test file:")
    write_local_file("test-junk.txt", "This shouldn't be committed\n")
    run_git("add", "test-junk.txt")

    print(f"  {C.BOLD}  You accidentally staged 'test-junk.txt'.{C.RESET}")
    print(f"  {C.BOLD}  It shouldn't be committed. UNSTAGE it:{C.RESET}")

    show_command("git restore --staged test-junk.txt")

    while True:
        cmd = wait_for_command()
        if "restore" in cmd and "staged" in cmd:
            run_git("restore", "--staged", "test-junk.txt")
            success("Unstaged! The file still exists but won't be committed.")
            award_xp(20, "Unstage mastered")
            break
        else:
            hint("Type: git restore --staged test-junk.txt")

    # Clean up
    junk = os.path.join(SANDBOX_DIR, "test-junk.txt")
    if os.path.exists(junk):
        os.remove(junk)

    mark_lab_done(2, 2)
    pause()

    # ─── LAB 3: Amend ───
    clear()
    banner("DAY 2 — LAB 3: FIX LAST COMMIT  (30 XP)")
    mission("Fix a commit message typo without creating a new commit.")

    write_local_file("config.txt", "App Config: debug=false\n")
    run_git("add", "config.txt")
    run_git("commit", "-m", "add confg file")

    print(f"  {C.RED}  Oops! The message says 'confg' instead of 'config'.{C.RESET}")

    ok, out = run_git("log", "--oneline", "-1")
    print(f"  {C.DIM}  Current: {out.strip()}{C.RESET}")

    instruction("Fix it with amend:")
    show_command('git commit --amend -m "chore: add config file"')

    while True:
        cmd = wait_for_command()
        if "amend" in cmd:
            msg = "chore: add config file"
            try:
                msg = cmd.split("-m")[-1].strip().strip('"').strip("'") or msg
            except:
                pass
            run_git("commit", "--amend", "-m", msg)
            ok, out = run_git("log", "--oneline", "-1")
            success(f"Fixed! Now says: {out.strip()}")
            award_xp(30, "Amend mastered")
            achievement("Clean History")
            break
        else:
            hint('Type: git commit --amend -m "chore: add config file"')

    mark_lab_done(2, 3)
    pause()

    # ─── LAB 4: Reset ───
    clear()
    banner("DAY 2 — LAB 4: UNDO A COMMIT  (40 XP)")
    mission("Undo the last commit entirely.")

    print(f"""
  {C.BOLD}  git reset --soft HEAD~1{C.RESET}

  {C.CYAN}reset{C.RESET}   = go back in time
  {C.CYAN}--soft{C.RESET}  = keep your files (just undo the commit)
  {C.CYAN}HEAD~1{C.RESET}  = go back 1 commit

  {C.DIM}  The file stays. The commit disappears. Like it never happened.{C.RESET}
""")

    instruction("Undo the config file commit:")
    show_command("git reset --soft HEAD~1")

    while True:
        cmd = wait_for_command()
        if "reset" in cmd and "soft" in cmd:
            run_git("reset", "--soft", "HEAD~1")
            success("Commit undone! File is still here, just not committed.")

            ok, out = run_git("status")
            if "config" in out:
                print(f"  {C.GREEN}  config.txt is staged but uncommitted{C.RESET}")

            award_xp(40, "Soft reset mastered")
            break
        else:
            hint("Type: git reset --soft HEAD~1")

    # Re-commit to keep state clean
    run_git("commit", "-m", "chore: add config file")

    mark_lab_done(2, 4)
    pause()

    # ─── LAB 5: .gitignore ───
    clear()
    banner("DAY 2 — LAB 5: THE IGNORE SHIELD  (30 XP)")
    mission("Tell Git to ignore files that shouldn't be tracked.")

    story('"Some files should NEVER go to Git:"')
    story('"passwords, databases, personal notes, node_modules."')
    story('"Sara will fire you if you commit the .env file." — Ahmed')

    instruction("Create some files that should be ignored:")
    write_local_file(".env", "SECRET_KEY=abc123\nDB_PASSWORD=hunter2\n")
    write_local_file("debug.log", "ERROR: something broke at 3am\n")
    write_local_file("personal-notes.txt", "Ahmed smells like coffee\n")

    print(f"  {C.DIM}  Created: .env, debug.log, personal-notes.txt{C.RESET}")

    instruction("Create a .gitignore file:")
    show_command("Create .gitignore with patterns")

    print(f"""
  {C.BOLD}  Common .gitignore patterns:{C.RESET}

  {C.CYAN}.env{C.RESET}              ← passwords, API keys
  {C.CYAN}*.log{C.RESET}             ← log files
  {C.CYAN}__pycache__/{C.RESET}      ← Python cache
  {C.CYAN}node_modules/{C.RESET}     ← Node packages
  {C.CYAN}*.db{C.RESET}              ← database files
  {C.CYAN}personal-*{C.RESET}        ← personal files matching pattern
""")

    while True:
        cmd = wait_for_command("  Type 'create' to make the .gitignore: ")
        if cmd.lower() in ["create", "yes", "ok", "y", "gitignore", ".gitignore"]:
            write_local_file(".gitignore", ".env\n*.log\n__pycache__/\nnode_modules/\n*.db\npersonal-*\n")
            success(".gitignore created!")
            break
        else:
            hint("Type: create")

    run_git("add", ".gitignore")
    run_git("commit", "-m", "chore: add .gitignore for secrets and junk files")

    instruction("Verify — check status (the ignored files should not appear):")
    show_command("git status")

    while True:
        cmd = wait_for_command()
        if "status" in cmd:
            ok, out = run_git("status")
            if ".env" not in out and "debug.log" not in out:
                success("Ignored files are INVISIBLE to Git! 🛡️")
                print(f"  {C.BOLD}  .env, *.log, and personal-* are all hidden.{C.RESET}")
            else:
                print(f"  {C.DIM}  {out}{C.RESET}")
            award_xp(30, "Ignore shield activated")
            break
        else:
            hint("Type: git status")

    mark_lab_done(2, 5)
    pause()

    # ─── DAY 2 QUIZ ───
    clear()
    banner("📝 DAY 2 QUIZ  (30 XP)")

    questions = [
        {
            "q": "You edited app.js but haven't staged it. How do you undo?",
            "options": ["a) git reset app.js", "b) git restore app.js", "c) git undo app.js", "d) git revert app.js"],
            "answer": "b", "xp": 10
        },
        {
            "q": "You staged a file by mistake. How do you UNSTAGE it?",
            "options": ["a) git restore --staged file", "b) git unstage file", "c) git remove file", "d) git reset --hard"],
            "answer": "a", "xp": 10
        },
        {
            "q": "What does .gitignore do?",
            "options": ["a) Deletes files", "b) Tells Git which files to never track", "c) Hides files from your computer", "d) Backs up files"],
            "answer": "b", "xp": 10
        }
    ]

    quiz_xp = 0
    for i, q in enumerate(questions, 1):
        print(f"\n  {C.BOLD}  Q{i}: {q['q']}{C.RESET}")
        for opt in q["options"]:
            print(f"    {opt}")
        ans = input(f"\n  {C.CYAN}  Your answer (a/b/c/d): {C.RESET}").strip().lower()
        if ans == q["answer"]:
            success("Correct!")
            quiz_xp += q["xp"]
        else:
            fail(f"The answer was: {q['answer']}")

    if quiz_xp > 0:
        award_xp(quiz_xp, f"Quiz: {quiz_xp}/{sum(q['xp'] for q in questions)}")

    # ─── DAY COMPLETE ───
    clear()
    banner("DAY 2 COMPLETE!")
    print(f"""
{C.GREEN}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║  UNDO SPELLS MASTERED:                           ║
    ║                                                  ║
    ║  ✅ git restore <file>         Undo changes      ║
    ║  ✅ git restore --staged       Unstage a file    ║
    ║  ✅ git commit --amend         Fix last commit   ║
    ║  ✅ git reset --soft HEAD~1    Undo a commit     ║
    ║  ✅ .gitignore                 Hide files        ║
    ║                                                  ║
    ║  Omar: "So I can break anything and fix it?"     ║
    ║  Sara: "Within reason. DON'T test that theory."  ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
{C.RESET}""")

    achievement("Undo Master")
    state["day"] = max(state["day"], 3)
    save()
    show_xp()
    pause("Press ENTER to return to the course menu...")


# ═══════════════════════════════════════════════════════
# PLACEHOLDER: Days 3-6 (follow along with the markdown)
# ═══════════════════════════════════════════════════════
def day_placeholder(day_num, title, xp_total):
    clear()
    banner(f"DAY {day_num}: {title}")

    day_md = {
        3: "day-03-branching-merging.md",
        4: "day-04-github-remotes.md",
        5: "day-05-team-workflows.md",
        6: "day-06-advanced-tricks.md",
    }

    filename = day_md.get(day_num, "")
    filepath = os.path.join(SCRIPT_DIR, filename)

    print(f"""
  {C.BOLD}  This day has {xp_total} XP of interactive labs!{C.RESET}

  {C.CYAN}  📖 Open the companion guide:{C.RESET}
  {C.GREEN}  {filename}{C.RESET}

  {C.DIM}  The guide has full step-by-step instructions with:
  • Labs with checkpoints
  • Pop quizzes
  • Boss fights
  • Achievement unlocks{C.RESET}

  {C.BOLD}  Follow the labs in the guide, then come back
  here to mark the day complete.{C.RESET}
""")

    if os.path.exists(filepath):
        print(f"  {C.GREEN}  ✅ Guide file found!{C.RESET}")
    else:
        print(f"  {C.RED}  ⚠️  Guide file not found at: {filename}{C.RESET}")

    print(f"\n  {C.DIM}  When you finish all labs in the guide:{C.RESET}")
    choice = input(f"\n  {C.CYAN}  Type 'done' when finished, or 'back' to return: {C.RESET}").strip().lower()

    if choice == "done":
        award_xp(xp_total, f"Day {day_num} complete!")
        state["day"] = max(state["day"], day_num + 1)
        save()
        success(f"Day {day_num} marked complete!")
        show_xp()
    
    pause("Press ENTER to return to the course menu...")

def day_3():
    day_placeholder(3, "BRANCHING & MERGING  🌿  600 XP", 600)

def day_4():
    day_placeholder(4, "GITHUB & REMOTES  ☁️  500 XP", 500)

def day_5():
    day_placeholder(5, "TEAM WORKFLOWS  👥  600 XP", 600)

def day_6():
    day_placeholder(6, "ADVANCED TRICKS  🧙  600 XP", 600)


# ═══════════════════════════════════════════════════════
# PROGRESS SCREEN
# ═══════════════════════════════════════════════════════
def show_progress():
    clear()
    banner("YOUR PROGRESS")

    total_xp = 3000
    pct = int((state["xp"] / total_xp) * 100)
    bar_len = 35
    filled = int(bar_len * pct / 100)
    bar = f"{C.GREEN}{'█' * filled}{C.DIM}{'░' * (bar_len - filled)}{C.RESET}"

    rank = get_rank()
    day = min(state["day"], 7)
    
    print(f"""
  {C.BOLD}  Rank:     {C.GOLD}{rank}{C.RESET}
  {C.BOLD}  XP:       {C.GOLD}{state['xp']} / {total_xp}{C.RESET}  [{bar}] {pct}%
  {C.BOLD}  Day:      {C.CYAN}{day - 1} / 6 completed{C.RESET}
  {C.BOLD}  Labs:     {C.CYAN}{len(state['completed_labs'])} completed{C.RESET}
  {C.BOLD}  Badges:   {C.MAGENTA}{len(state['achievements'])} / 12{C.RESET}
""")

    # Day progress
    days = [
        "Day 1: First Day at Work",
        "Day 2: Fixing Mistakes",
        "Day 3: Branching & Merging",
        "Day 4: GitHub & Remotes",
        "Day 5: Team Workflows",
        "Day 6: Advanced Tricks",
    ]
    
    print(f"  {C.BOLD}  TRAINING SCHEDULE:{C.RESET}\n")
    for i, d in enumerate(days, 1):
        if i < state["day"]:
            status = f"{C.GREEN}✅"
        elif i == state["day"]:
            status = f"{C.CYAN}▶️ "
        else:
            status = f"{C.DIM}🔒"
        print(f"    {status}  {d}{C.RESET}")

    # Achievements
    if state["achievements"]:
        print(f"\n  {C.BOLD}  ACHIEVEMENTS:{C.RESET}\n")
        for a in state["achievements"]:
            print(f"    {C.MAGENTA}🏅 {a}{C.RESET}")

    # Rank ladder
    print(f"\n  {C.BOLD}  RANK LADDER:{C.RESET}\n")
    ranks = [
        ("🌱 Seedling",       "0 XP",    0),
        ("🌿 Apprentice",     "700 XP",  700),
        ("🔥 Adept",          "1500 XP", 1500),
        ("⚔️ Warrior",        "2200 XP", 2200),
        ("🏆 Legend",         "2800 XP", 2800),
    ]
    for emoji_name, xp_req, threshold in ranks:
        if state["xp"] >= threshold:
            print(f"    {C.GREEN}{emoji_name} ({xp_req}) ✅{C.RESET}")
        else:
            print(f"    {C.DIM}{emoji_name} ({xp_req}){C.RESET}")

    pause("\n  Press ENTER to go back...")


# ═══════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════
def main_menu():
    load()

    while True:
        clear()
        rank = get_rank()
        day = min(state["day"], 7)
        day_text = f"Day {state['day']}" if state["day"] <= 6 else "All Complete!"

        print(f"""
{C.GOLD}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║   🏢  GIT FOR REAL TEAMS                         ║
    ║   Company-Level Training by TechCorp             ║
    ║                                                  ║
    ╠══════════════════════════════════════════════════╣
    ║                                                  ║
    ║   1.  ▶️   Continue ({day_text:15s})         ║
    ║   2.  🗺️   Day Select                            ║
    ║   3.  📊  Progress & Achievements                ║
    ║   4.  📖  Open Course Guide                      ║
    ║   5.  🔄  Reset Everything                       ║
    ║   6.  ❌  Quit                                   ║
    ║                                                  ║
    ║   {rank:40s}  ║
    ║   XP: {state['xp']} / 3000                             ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
{C.RESET}""")

        choice = input(f"  {C.CYAN}Choose (1-6): {C.RESET}").strip()

        if choice == "1":
            run_day(state["day"])
        elif choice == "2":
            day_select()
        elif choice == "3":
            show_progress()
        elif choice == "4":
            print(f"\n  {C.GREEN}  Open these files in VS Code:{C.RESET}")
            print(f"  {C.CYAN}  • git-course-overview.md{C.RESET}")
            print(f"  {C.CYAN}  • day-01-getting-started.md{C.RESET}")
            print(f"  {C.CYAN}  • day-02-fixing-mistakes.md{C.RESET}")
            print(f"  {C.CYAN}  • day-03-branching-merging.md{C.RESET}")
            print(f"  {C.CYAN}  • day-04-github-remotes.md{C.RESET}")
            print(f"  {C.CYAN}  • day-05-team-workflows.md{C.RESET}")
            print(f"  {C.CYAN}  • day-06-advanced-tricks.md{C.RESET}")
            print(f"  {C.CYAN}  • git-company-cheatsheet.md{C.RESET}")
            pause()
        elif choice == "5":
            confirm = input(f"  {C.RED}  Are you sure? Type 'yes' to reset: {C.RESET}").strip().lower()
            if confirm == "yes":
                reset()
                success("All progress reset!")
                pause()
        elif choice == "6":
            print(f"\n  {C.GOLD}  See you at the office tomorrow! 🏢{C.RESET}\n")
            sys.exit(0)

def day_select():
    days_info = [
        ("First Day at Work",    "init, add, commit, status, diff, log",    300),
        ("Fixing Mistakes",      "restore, amend, reset, .gitignore",       400),
        ("Branching & Merging",  "branch, checkout, merge, conflicts",      600),
        ("GitHub & Remotes",     "push, pull, clone, pull requests",        500),
        ("Team Workflows",       "stash, blame, cherry-pick, sprint sim",   600),
        ("Advanced Tricks",      "rebase, bisect, tags, reflog, aliases",   600),
    ]

    while True:
        clear()
        banner("DAY SELECT")

        for i, (name, skills, xp) in enumerate(days_info, 1):
            if i < state["day"]:
                status = f"{C.GREEN}✅"
            elif i == state["day"]:
                status = f"{C.CYAN}▶️ "
            else:
                status = f"{C.DIM}🔒"
            lock = f" {C.DIM}(locked){C.RESET}" if i > state["day"] else ""
            print(f"  {status}  Day {i}: {name} ({xp} XP){C.RESET}{lock}")
            print(f"       {C.DIM}{skills}{C.RESET}")

        choice = input(f"\n  {C.CYAN}Choose day (1-6) or 'back': {C.RESET}").strip().lower()

        if choice == "back" or choice == "b":
            return

        try:
            day = int(choice)
            if 1 <= day <= state["day"]:
                run_day(day)
                return
            elif 1 <= day <= 6:
                print(f"\n  {C.RED}  Day {day} is locked! Complete Day {state['day']} first.{C.RESET}")
                pause()
        except ValueError:
            pass

def run_day(day_num):
    day_funcs = {
        1: day_1,
        2: day_2,
        3: day_3,
        4: day_4,
        5: day_5,
        6: day_6,
    }
    if day_num in day_funcs:
        day_funcs[day_num]()
    elif day_num > 6:
        graduation()

def graduation():
    clear()
    achievement("Git Hero")

    print(f"""
{C.GOLD}
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║   🎓  TRAINING COMPLETE  🎓                      ║
    ║                                                  ║
    ║   FINAL SCORE: {state['xp']} / 3000 XP{' ' * (22 - len(str(state['xp'])))}║
    ║   RANK: {get_rank():38s}  ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
{C.RESET}

  {C.GREEN}  ACHIEVEMENTS:{C.RESET}
""")
    for a in state["achievements"]:
        print(f"    {C.MAGENTA}🏅 {a}{C.RESET}")

    print(f"""
{C.BOLD}
  CHARACTER SIGN-OFFS:

  Sara:    "You're ready to review PRs now. Proud of you."
  Ahmed:   "Your commit messages are... acceptable." (high praise)
  Lina:    "Closing your onboarding ticket. Welcome to the team!"
  Youssef: "Next up: CI/CD pipelines. But that's another course."
  Fatima:  "I found 0 bugs in your last commit. Record." 
  Omar:    "Can we do the training again? I missed Day 2."
{C.RESET}

  {C.DIM}  Thank you for completing Git for Real Teams! 🏢
  You went from 'what is git?' to professional workflows.
  Now go build something amazing.{C.RESET}
""")
    save()
    pause("Press ENTER to return to menu...")


# ═══════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════
def main():
    if os.name == "nt":
        os.system("")  # Enable ANSI on Windows

    # Command line args
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "progress":
            load()
            show_progress()
            return
        elif arg == "reset":
            reset()
            print("Progress reset!")
            return
        elif arg == "day" and len(sys.argv) > 2:
            load()
            try:
                day = int(sys.argv[2])
                run_day(day)
                return
            except ValueError:
                pass

    main_menu()

if __name__ == "__main__":
    main()
