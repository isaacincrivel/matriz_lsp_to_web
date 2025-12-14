# Script PowerShell para baixar bibliotecas JavaScript necessárias
# Execute: .\download-libs.ps1

$libsPath = "libs"
if (-not (Test-Path $libsPath)) {
    New-Item -ItemType Directory -Path $libsPath
}

Write-Host "Baixando bibliotecas JavaScript..." -ForegroundColor Green

# PapaParse
Write-Host "Baixando PapaParse..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js" -OutFile "$libsPath\papaparse.min.js"

# FileSaver.js
Write-Host "Baixando FileSaver.js..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js" -OutFile "$libsPath\FileSaver.min.js"

# XLSX.js
Write-Host "Baixando XLSX.js..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js" -OutFile "$libsPath\xlsx.full.min.js"

Write-Host "`n✅ Todas as bibliotecas foram baixadas com sucesso!" -ForegroundColor Green
Write-Host "Localização: $PWD\$libsPath" -ForegroundColor Cyan

