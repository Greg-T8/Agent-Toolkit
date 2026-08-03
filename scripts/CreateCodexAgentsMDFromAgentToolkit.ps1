$sourceDirectory = "$env:USERPROFILE\LocalCode\Agent-Toolkit\instructions"
$targetFile = Join-Path $env:USERPROFILE '.codex\AGENTS.md'

$instructionFiles = @(
    'General Coding Guidelines.instructions.md'
    'Azure Governance Guidelines.instructions.md'
    'PowerShell Style Guidelines.instructions.md'
    'Python Style Guidelines.instructions.md'
    'Shell Style Guidelines.instructions.md'
    'Terraform Style Guidelines.instructions.md'
)

New-Item `
    -ItemType Directory `
    -Path (Split-Path -Path $targetFile) `
    -Force | Out-Null

$sections = foreach ($fileName in $instructionFiles) {
    $sourceFile = Join-Path $sourceDirectory $fileName

    if (-not (Test-Path -LiteralPath $sourceFile)) {
        Write-Warning "Instruction file not found: $sourceFile"
        continue
    }

    $sectionName = $fileName -replace '\.instructions\.md$', ''

    "## $sectionName"
    ''
    Get-Content -LiteralPath $sourceFile -Raw
    ''
}

@(
    '# Shared engineering instructions'
    ''
    'Apply the general instructions to every task.'
    'Apply language-, platform-, and technology-specific instructions only when relevant.'
    'Treat any Copilot `applyTo` metadata as a description of the intended scope.'
    ''
    $sections
) | Set-Content -LiteralPath $targetFile -Encoding utf8

Write-Host "Created Codex instructions: $targetFile"