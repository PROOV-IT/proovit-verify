$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
py -m venv .venv-build
& .\.venv-build\Scripts\python.exe -m pip install --quiet -r requirements.txt pyinstaller
& .\.venv-build\Scripts\pyinstaller.exe --clean --onefile --name proovit-verify proovit_verify.py
Write-Host "Binaire Windows : $Root\dist\proovit-verify.exe"
