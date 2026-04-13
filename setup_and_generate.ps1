$ErrorActionPreference = "Stop"

$venvDir = ".venv311"
$python311 = (& py -3.11 -c "import sys; print(sys.executable)" 2>$null)

if (-not $python311) {
    throw "Python 3.11 was not found. Install it with winget: winget install -e --id Python.Python.3.11 --scope user"
}

if (-not (Test-Path $venvDir)) {
    & py -3.11 -m venv $venvDir
}

& "$venvDir\Scripts\python.exe" -m pip install --upgrade pip
& "$venvDir\Scripts\python.exe" -m pip install -r requirements.txt
& "$venvDir\Scripts\python.exe" .\generate_models.py

Write-Host "Done. Open STEP files from .\exports in AutoCAD."
