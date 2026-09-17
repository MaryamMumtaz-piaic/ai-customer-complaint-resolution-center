"""
ComplaintIQ - Single command launcher
Usage: python run.py
"""
import subprocess, sys, os, time, threading, webbrowser, venv, shutil
from pathlib import Path

ROOT     = Path(__file__).parent
BACKEND  = ROOT / "backend"
FRONTEND = ROOT / "frontend"
VENV     = BACKEND / "venv"
PYTHON   = VENV / "Scripts" / "python.exe" if sys.platform == "win32" else VENV / "bin" / "python"
UVICORN  = VENV / "Scripts" / "uvicorn.exe" if sys.platform == "win32" else VENV / "bin" / "uvicorn"
PIP      = VENV / "Scripts" / "pip.exe"     if sys.platform == "win32" else VENV / "bin" / "pip"

CYAN  = "\033[96m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
RED   = "\033[91m"; BLUE  = "\033[94m"; MAGENTA = "\033[95m"; RESET = "\033[0m"; BOLD = "\033[1m"

def banner():
    print(f"\n{CYAN}{BOLD}  ========================================")
    print(f"    ComplaintIQ - AI Complaint Center")
    print(f"    Starting all services...{RESET}")
    print(f"{CYAN}{BOLD}  ========================================{RESET}\n")

def setup():
    # Create venv if needed
    if not VENV.exists():
        print(f"{YELLOW}  [SETUP] Creating virtual environment...{RESET}")
        venv.create(str(VENV), with_pip=True)

    # Install deps if needed
    if not UVICORN.exists():
        print(f"{YELLOW}  [SETUP] Installing backend dependencies (first run only)...{RESET}")
        subprocess.run([str(PIP), "install", "-r", str(BACKEND / "requirements.txt"), "--quiet"], check=True)
        print(f"{GREEN}  [SETUP] Done!{RESET}")

    # Create .env if missing
    env_file = BACKEND / ".env"
    env_example = BACKEND / ".env.example"
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"{YELLOW}  [WARN] Created backend/.env — set your OPENAI_API_KEY!{RESET}")

def stream(proc, prefix, color):
    """Stream stdout from a process with a colored prefix."""
    for line in iter(proc.stdout.readline, ""):
        print(f"{color}  [{prefix}]{RESET} {line}", end="")

def main():
    banner()
    setup()

    print(f"{GREEN}  [1/2] Backend  → http://localhost:8000      (API){RESET}")
    print(f"{GREEN}  [2/2] Frontend → http://localhost:5500      (UI){RESET}")
    print(f"{BLUE}        API Docs → http://localhost:8000/docs{RESET}")
    print(f"\n{YELLOW}  Ctrl+C to stop everything.{RESET}")
    print(f"{CYAN}  ========================================{RESET}\n")

    # Start backend
    backend_proc = subprocess.Popen(
        [str(UVICORN), "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"],
        cwd=str(BACKEND),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Start frontend
    frontend_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "5500", "--directory", str(FRONTEND)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Stream logs in background threads
    threading.Thread(target=stream, args=(backend_proc,  "BACKEND ", BLUE),    daemon=True).start()
    threading.Thread(target=stream, args=(frontend_proc, "FRONTEND", MAGENTA), daemon=True).start()

    # Open browser after short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:5500")
        print(f"\n{GREEN}  [OK] Browser opened → http://localhost:5500{RESET}")
    threading.Thread(target=open_browser, daemon=True).start()

    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}  Stopping servers...{RESET}")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print(f"{CYAN}  Stopped. Goodbye!{RESET}\n")

if __name__ == "__main__":
    main()
