#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
cd "$root"
python3 -m venv .venv-build
.venv-build/bin/pip install --quiet -r requirements.txt pyinstaller
.venv-build/bin/pyinstaller --clean --onefile --name proovit-verify proovit_verify.py
echo "Binaire Linux : $root/dist/proovit-verify"
