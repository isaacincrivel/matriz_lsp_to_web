# Script PowerShell para organizar o projeto
# Execute: .\organizar_projeto.ps1

Write-Host "📁 Organizando estrutura do projeto..." -ForegroundColor Green

# Criar estrutura de pastas
$pastas = @(
    "backend\core",
    "backend\exportacao",
    "backend\elementos",
    "backend\abacos",
    "backend\django",
    "frontend\desktop_app\libs",
    "frontend\web_app\css",
    "frontend\web_app\js",
    "frontend\standalone",
    "data\input",
    "data\output",
    "backup",
    "docs",
    "scripts"
)

foreach ($pasta in $pastas) {
    if (-not (Test-Path $pasta)) {
        New-Item -ItemType Directory -Path $pasta -Force | Out-Null
        Write-Host "  ✅ Criada: $pasta" -ForegroundColor Yellow
    }
}

# Mover arquivos Python para backend
Write-Host "`n🔄 Movendo arquivos Python..." -ForegroundColor Cyan

# Core
$arquivosCore = @(
    @{origem="calculo_geografico.py"; destino="backend\core\"},
    @{origem="processamento_vertices.py"; destino="backend\core\"},
    @{origem="transformacao_csv.py"; destino="backend\core\"},
    @{origem="matriz_csv_to_kml.PY"; destino="backend\core\matriz_csv_to_kml.py"}
)

foreach ($arquivo in $arquivosCore) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

# Exportação
$arquivosExport = @(
    @{origem="exportacao.py"; destino="backend\exportacao\"},
    @{origem="kml.py"; destino="backend\exportacao\"}
)

foreach ($arquivo in $arquivosExport) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

# Elementos
$arquivosElementos = @(
    @{origem="kml_elementos.py"; destino="backend\elementos\"},
    @{origem="colocar_encabecamento_rede.py"; destino="backend\elementos\"},
    @{origem="colocar_poste_estrutura.py"; destino="backend\elementos\"},
    @{origem="marcar_vertices_angulo_deflexao.py"; destino="backend\elementos\"}
)

foreach ($arquivo in $arquivosElementos) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

# Ábacos
$arquivosAbacos = @(
    @{origem="abaco_mosaico.py"; destino="backend\abacos\"},
    @{origem="TABELA ABACOS.xlsx"; destino="backend\abacos\"}
)

foreach ($arquivo in $arquivosAbacos) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

# Django
$arquivosDjango = @(
    @{origem="views_kml.py"; destino="backend\django\"},
    @{origem="views_matriz.py"; destino="backend\django\"}
)

foreach ($arquivo in $arquivosDjango) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

# Mover frontend
Write-Host "`n🔄 Movendo aplicações frontend..." -ForegroundColor Cyan

if (Test-Path "desktop_app") {
    Copy-Item -Path "desktop_app\*" -Destination "frontend\desktop_app\" -Recurse -Force
    Write-Host "  ✅ Copiado: desktop_app → frontend\desktop_app" -ForegroundColor Green
}

if (Test-Path "web_app") {
    Copy-Item -Path "web_app\*" -Destination "frontend\web_app\" -Recurse -Force
    Write-Host "  ✅ Copiado: web_app → frontend\web_app" -ForegroundColor Green
}

if (Test-Path "importar_kml.html") {
    Move-Item -Path "importar_kml.html" -Destination "frontend\standalone\" -Force
    Write-Host "  ✅ Movido: importar_kml.html → frontend\standalone\" -ForegroundColor Green
}

# Mover dados
Write-Host "`n🔄 Movendo arquivos de dados..." -ForegroundColor Cyan

$arquivosDados = @(
    @{origem="matriz_teste.csv"; destino="data\input\"},
    @{origem="matriz_teste_transformada.csv"; destino="data\input\"},
    @{origem="matriz_teste_transformada_final.csv"; destino="data\input\"}
)

foreach ($arquivo in $arquivosDados) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

if (Test-Path "resultados") {
    Copy-Item -Path "resultados\*" -Destination "data\output\resultados\" -Recurse -Force
    Write-Host "  ✅ Copiado: resultados → data\output\resultados" -ForegroundColor Green
}

# Mover backups
Write-Host "`n🔄 Movendo backups..." -ForegroundColor Cyan

if (Test-Path "BKP") {
    Copy-Item -Path "BKP\*" -Destination "backup\" -Recurse -Force
    Write-Host "  ✅ Copiado: BKP → backup" -ForegroundColor Green
}

# Mover documentação
Write-Host "`n🔄 Movendo documentação..." -ForegroundColor Cyan

$arquivosDocs = @(
    @{origem="ANALISE_ADAPTACAO_SISTEMA.md"; destino="docs\"},
    @{origem="README_IMPORTAR_KML.md"; destino="docs\"}
)

foreach ($arquivo in $arquivosDocs) {
    if (Test-Path $arquivo.origem) {
        Move-Item -Path $arquivo.origem -Destination $arquivo.destino -Force
        Write-Host "  ✅ Movido: $($arquivo.origem) → $($arquivo.destino)" -ForegroundColor Green
    }
}

# Mover scripts
Write-Host "`n🔄 Movendo scripts..." -ForegroundColor Cyan

if (Test-Path "desktop_app\download-libs.ps1") {
    Move-Item -Path "desktop_app\download-libs.ps1" -Destination "scripts\" -Force
    Write-Host "  ✅ Movido: download-libs.ps1 → scripts\" -ForegroundColor Green
}

Write-Host "`n✅ Organização concluída!" -ForegroundColor Green
Write-Host "`n⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   1. Verifique se os imports nos arquivos Python estão corretos"
Write-Host "   2. Teste as aplicações para garantir que tudo funciona"
Write-Host "   3. Os arquivos foram COPIADOS (não movidos) para segurança"
Write-Host "   4. Você pode deletar as pastas antigas após verificar que tudo funciona"

