# ---------------------------------------------------------------------------
# Description   : Refresh coding guidance and package the Agent Toolkit bundle
# Context       : Agent-Toolkit - portable ChatGPT skill distribution
# Author        : Greg Tate & coding agent
# Last Modified : 2026-11-25
# Revision History:
#   2026-11-25 - Consolidate all skills into the Agent Toolkit build
#   2026-11-25 - Initial version
# ---------------------------------------------------------------------------
<#
.SYNOPSIS
    Refresh coding guidance and package the Agent Toolkit bundle.

.DESCRIPTION
    Copies the selected instruction files into the personal skill and invokes
    the shared packager with the consolidated Agent Toolkit bundle manifest.
    Supports -WhatIf without synchronizing references or writing an archive.

.PARAMETER OutputDirectory
    Destination directory for the generated plugin archive.

.CONTEXT
    Agent-Toolkit - manual ChatGPT skill import from maintained source files.

.AUTHOR
    Greg Tate & coding agent
#>
#requires -Version 7.0

[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '_bundles')
)

# Resolve the consolidated bundle inputs relative to this script.
$SyncScriptPath         = Join-Path $PSScriptRoot 'Sync-CodingGuidelines.ps1'
$SkillArchiveScriptPath = Join-Path $PSScriptRoot 'New-SkillArchive.ps1'
$BundleConfigPath       = Join-Path $PSScriptRoot 'bundles\agent-toolkit.json'

# Keep the build sequence to synchronization followed by shared packaging.
$Main = {
    . $Helpers

    Invoke-CodingGuidelineSync
    New-SkillBundle
}

# Keep child-process details out of the high-level build sequence.
$Helpers = {
    function Invoke-CodingGuidelineSync {
        # Refresh the embedded references before the packager enumerates the skill.
        & $SyncScriptPath
    }

    function New-SkillBundle {
        # Package every selected skill using the consolidated manifest.
        & $SkillArchiveScriptPath -ConfigPath $BundleConfigPath -OutputDirectory $OutputDirectory
    }
}

# Execute from the skills directory so the shared packager receives stable paths.
try {
    Push-Location -Path $PSScriptRoot
    & $Main
}
finally {
    Pop-Location
}
