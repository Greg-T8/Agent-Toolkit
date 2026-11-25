# ---------------------------------------------------------------------------
# Description   : Refresh and package the coding-guidelines skill bundle
# Context       : Agent-Toolkit - portable ChatGPT skill distribution
# Author        : Greg Tate & coding agent
# Last Modified : 2026-11-25
# Revision History:
#   2026-11-25 - Initial version
# ---------------------------------------------------------------------------
<#
.SYNOPSIS
    Refresh and package the coding-guidelines skill bundle.

.DESCRIPTION
    Copies the selected instruction files into the personal skill and invokes
    the shared packager with the dedicated coding-guidelines bundle manifest.

.PARAMETER OutputDirectory
    Destination directory for the generated plugin archive.

.CONTEXT
    Agent-Toolkit - manual ChatGPT skill import from maintained source files.

.AUTHOR
    Greg Tate & coding agent
#>
#requires -Version 7.0

[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '_bundles')
)

# Resolve the dedicated bundle inputs relative to this script.
$SyncScriptPath    = Join-Path $PSScriptRoot 'Sync-CodingGuidelines.ps1'
$PackageScriptPath = Join-Path $PSScriptRoot 'Package-Skills.ps1'
$BundleConfigPath  = Join-Path $PSScriptRoot 'bundles\coding-guidelines.json'

# Keep the build sequence to synchronization followed by shared packaging.
$Main = {
    . $Helpers

    Invoke-CodingGuidelineSync
    New-CodingGuidelineBundle
}

# Keep child-process details out of the high-level build sequence.
$Helpers = {
    function Invoke-CodingGuidelineSync {
        # Refresh the embedded references before the packager enumerates the skill.
        & $SyncScriptPath
    }

    function New-CodingGuidelineBundle {
        # Use the shared packager with only the dedicated coding-guidelines manifest.
        & $PackageScriptPath -ConfigPath $BundleConfigPath -OutputDirectory $OutputDirectory
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
