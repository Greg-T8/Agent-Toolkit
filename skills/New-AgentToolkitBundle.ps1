# ---------------------------------------------------------------------------
# Description   : Refresh coding guidance and package the Agent Toolkit bundle
# Context       : Agent-Toolkit - portable ChatGPT skill distribution
# Author        : Greg Tate & coding agent
# Last Modified : 2026-11-27
# Revision History:
#   2026-11-27 - Locate the configuration in its bundle directory
#   2026-11-27 - Check selection changes against version and changelog
#   2026-11-25 - Consolidate all skills into the Agent Toolkit build
#   2026-11-25 - Initial version
# ---------------------------------------------------------------------------
<#
.SYNOPSIS
    Refresh coding guidance and package the Agent Toolkit bundle.

.DESCRIPTION
    Checks selection changes against the previous archive, then copies the
    selected instruction files into the personal skill and invokes
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
$BundleConfigPath       = Join-Path $PSScriptRoot 'bundles\agent-toolkit\agent-toolkit.json'

# Keep the build sequence to synchronization followed by shared packaging.
$Main = {
    . $Helpers

    Confirm-BundleSelection
    Invoke-CodingGuidelineSync
    New-SkillBundle
}

# Keep child-process details out of the high-level build sequence.
$Helpers = {
    function Confirm-BundleSelection {
        # Require release notes before replacing an archive with a changed selection.
        $Definition = Get-Content -LiteralPath $BundleConfigPath -Raw -Encoding utf8 | ConvertFrom-Json
        $ArchivePath = Join-Path $OutputDirectory "$($Definition.name).plugin.zip"
        if (-not (Test-Path -LiteralPath $ArchivePath -PathType Leaf)) {
            Write-Warning "Selection baseline unavailable: archive not found at $ArchivePath."
            return
        }

        # Read the last local selection without extracting or changing the archive.
        try {
            $Archive = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path -LiteralPath $ArchivePath).Path)
            try {
                $Entry = $Archive.GetEntry("skills/$($Definition.name)/bundle-manifest.json")
                if ($null -eq $Entry) { throw 'Bundle manifest is missing.' }
                $Reader = [System.IO.StreamReader]::new($Entry.Open())
                try { $Previous = $Reader.ReadToEnd() | ConvertFrom-Json } finally { $Reader.Dispose() }
            }
            finally { $Archive.Dispose() }
            if (-not $Previous.version -or $null -eq $Previous.skills) { throw 'Bundle manifest lacks a version or skill inventory.' }
            $PreviousVersion = [version]$Previous.version
            if (@($Previous.skills | Where-Object { -not $_.Name -or -not $_.Path }).Count) { throw 'Bundle manifest contains an incomplete skill inventory.' }
        }
        catch {
            Write-Warning "Selection baseline unavailable: cannot read $ArchivePath. $($_.Exception.Message)"
            return
        }

        # Compare names separately from paths so moves are not treated as removals.
        $OldSkills = @{}
        $NewSkills = @{}
        foreach ($Skill in $Previous.skills) { $OldSkills[$Skill.Name] = $Skill.Path }
        foreach ($Path in $Definition.skills) { $NewSkills[($Path -split '/')[-1]] = $Path }
        $Added   = @($NewSkills.Keys | Where-Object { -not $OldSkills.ContainsKey($_) } | Sort-Object)
        $Removed = @($OldSkills.Keys | Where-Object { -not $NewSkills.ContainsKey($_) } | Sort-Object)
        $Moved   = @($NewSkills.Keys | Where-Object { $OldSkills.ContainsKey($_) -and $OldSkills[$_] -cne $NewSkills[$_] } | Sort-Object)
        foreach ($Name in $Added) { Write-Host "Added: $Name ($($NewSkills[$Name]))" }
        foreach ($Name in $Removed) { Write-Host "Removed: $Name ($($OldSkills[$Name]))" }
        foreach ($Name in $Moved) { Write-Host "Moved: $Name ($($OldSkills[$Name]) -> $($NewSkills[$Name]))" }
        if (-not ($Added.Count + $Removed.Count + $Moved.Count)) {
            Write-Host 'Bundle selection unchanged from the previous local archive.'
            return
        }

        # Require a newer version and names of additions and removals in its notes.
        if ($Definition.version -notmatch '^\d+\.\d+\.\d+$' -or [version]$Definition.version -le $PreviousVersion) {
            throw "Selection changed. Set a version greater than $PreviousVersion before building."
        }
        $ChangelogPath = [System.IO.Path]::ChangeExtension($BundleConfigPath, '.changelog.md')
        if (-not (Test-Path -LiteralPath $ChangelogPath -PathType Leaf)) { throw "Selection changed. Changelog not found: $ChangelogPath" }
        $Changelog = Get-Content -LiteralPath $ChangelogPath -Raw -Encoding utf8
        $Pattern = '(?ms)^##\s+' + [regex]::Escape($Definition.version) + '(?:\s+-\s+[^\r\n]+)?\s*\r?\n(.*?)(?=^##\s+|\z)'
        $Section = [regex]::Match($Changelog, $Pattern)
        if (-not $Section.Success) { throw "Selection changed. Add a changelog section for version $($Definition.version)." }
        $Missing = @($Added + $Removed | Where-Object { $Section.Groups[1].Value -notmatch ('(?<![a-zA-Z0-9-])' + [regex]::Escape($_) + '(?![a-zA-Z0-9-])') })
        if ($Missing.Count) { throw "Selection changed. Add these skill names to the version $($Definition.version) changelog section: $($Missing -join ', ')." }
    }

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
