#!/usr/bin/env python3
"""
Generate and load the weekly-ops-audit launchd plist (Mac only).
Schedule: every Friday at 1pm — matches the original kwoekel setup.
"""
import os
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent.resolve()
USERNAME = os.environ.get("USER", "user")
LABEL = f"com.{USERNAME}.weekly-ops-audit"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"

PLIST = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>{REPO_DIR}/scheduled-tasks/weekly-ops-audit/run.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Weekday</key><integer>5</integer>
            <key>Hour</key><integer>13</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>{REPO_DIR}/scheduled-tasks/weekly-ops-audit/run.log</string>
    <key>StandardErrorPath</key>
    <string>{REPO_DIR}/scheduled-tasks/weekly-ops-audit/run.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
"""

def main():
    # Unload existing if present
    if PLIST_PATH.exists():
        subprocess.run(["launchctl", "unload", str(PLIST_PATH)],
                       capture_output=True)

    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(PLIST)
    subprocess.run(["launchctl", "load", str(PLIST_PATH)], check=True)
    print(f"  ✅ Weekly ops audit scheduled: {LABEL}")
    print(f"     Runs: every Friday at 1pm")
    print(f"     Plist: {PLIST_PATH}")

if __name__ == "__main__":
    main()
