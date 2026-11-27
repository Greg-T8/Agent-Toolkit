# ---------------------------------------------------------------------------
# Description   : Copy selected coding instructions into the personal skill
# Context       : Agent-Toolkit - portable coding-guidelines skill bundle
# Author        : Greg Tate & coding agent
# Last Modified : 2026-11-27
# Revision History:
#   2026-11-27 - Follow Skills Atlas theme folders
#   2026-11-25 - Initial version
# ---------------------------------------------------------------------------
<#
.SYNOPSIS
    Copy selected coding instructions into the personal skill.

.DESCRIPTION
    Refreshes the general, PowerShell, and Shell instruction references so the
    coding-guidelines skill can be packaged without access to local files.

.CONTEXT
    Agent-Toolkit - prepare portable ChatGPT skill references.

.AUTHOR
    Greg Tate & coding agent
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Low')]
param()

# Resolve the maintained instruction source and skill reference destination.
$InstructionDirectory = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\instructions'))
$ReferenceDirectory = Join-Path $PSScriptRoot 'personal\code\coding-guidelines\references'

# Limit synchronization to the three requested instruction files.
$InstructionFiles = @(
    'General Coding Guidelines.instructions.md',
    'PowerShell Style Guidelines.instructions.md',
    'Shell Style Guidelines.instructions.md'
)

# Keep orchestration readable while the helper owns file checks and copying.
$Main = {
    . $Helpers

    Copy-CodingGuidelineInstruction
}

# Define the exact-source copy operation used by the script entry point.
$Helpers = {
    # Copy the selected instruction documents into the skill's references folder.
    function Copy-CodingGuidelineInstruction {
        [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Low')]
        param()

        # Stop before copying if any selected source document is unavailable.
        foreach ($InstructionFile in $InstructionFiles) {
            $SourcePath = Join-Path $InstructionDirectory $InstructionFile
            if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
                throw "Required instruction file '$SourcePath' was not found."
            }
        }

        # Create the reference folder only during an actual synchronization.
        if (-not (Test-Path -LiteralPath $ReferenceDirectory -PathType Container) -and
            -not $WhatIfPreference) {
            New-Item -Path $ReferenceDirectory -ItemType Directory -Force | Out-Null
        }

        # Copy each selected source with its original filename and content.
        foreach ($InstructionFile in $InstructionFiles) {
            $SourcePath = Join-Path $InstructionDirectory $InstructionFile
            $DestinationPath = Join-Path $ReferenceDirectory $InstructionFile
            if ($PSCmdlet.ShouldProcess($DestinationPath, 'Copy coding instruction')) {
                Copy-Item -LiteralPath $SourcePath -Destination $DestinationPath -Force
            }
        }

        [pscustomobject]@{
            ReferenceDirectory = $ReferenceDirectory
            InstructionCount  = $InstructionFiles.Count
        }
    }
}

# Execute from the skills directory so all maintained paths resolve consistently.
try {
    Push-Location -Path $PSScriptRoot
    & $Main
}
finally {
    Pop-Location
}
