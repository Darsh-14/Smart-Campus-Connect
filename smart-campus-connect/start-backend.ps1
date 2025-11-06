Write-Host "Starting Smart Campus Connect Backend..." -ForegroundColor Green
Set-Location src\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
