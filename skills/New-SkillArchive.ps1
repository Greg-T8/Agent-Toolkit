# ---------------------------------------------------------------------------
# Description   : Create ChatGPT plugin or skill archives from selected skills
# Context       : Agent-Toolkit - configurable, portable skill distribution
# Author        : Greg Tate & coding agent
# Last Modified : 2026-11-27
# Revision History:
#   2026-11-27 - Locate bundle definitions and icons in bundle directories
#   2026-11-27 - Support an optional bundle routing skill
#   2026-11-25 - Rename packager to New-SkillArchive.ps1
#   2026-11-25 - Default to the consolidated Agent Toolkit bundle
#   2026-11-25 - Allow a display name without plugin icons
#   2026-11-25 - Support a separate plugin display name
#   2026-11-25 - Support a separate composer icon
#   2026-11-25 - Include the bundle changelog in the generated skill
#   2026-11-25 - Include optional plugin icon from bundle configuration
#   2026-11-24 - Add ChatGPT plugin ZIP output
#   2026-11-24 - Initial manifest-driven unified skill packaging
# ---------------------------------------------------------------------------
<#
.SYNOPSIS
    Create ChatGPT plugin or skill archives from selected skills.

.DESCRIPTION
    Reads a JSON bundle definition, validates selected skill directories, and
    embeds their complete contents under references/skills. Generates a root
    SKILL.md that routes requests to the embedded guidance. Preserves license
    files and records source Git revisions and file hashes in bundle-manifest.json.
    Creates a plugin ZIP under skills/_bundles by default. Use -Format Skill
    for the previous standalone .skill archive.
    Requires PowerShell 7. Supports -WhatIf without creating output or staging.

.PARAMETER ConfigPath
    JSON bundle definition. Relative paths resolve from the caller's directory.
    Skill paths inside the JSON always resolve from this script's skills directory.

.PARAMETER OutputDirectory
    Destination directory. Relative paths resolve from the caller's directory.

.PARAMETER Layout
    For Skill format, Root places SKILL.md at the archive root; Folder encloses
    the contents in a named directory. Plugin format always uses its root layout.

.PARAMETER Format
    Plugin (default) creates a ZIP for the ChatGPT plugin uploader; Skill creates
    a standalone .skill archive with the selected Layout.

.EXAMPLE
    ./skills/New-SkillArchive.ps1 -WhatIf

.EXAMPLE
    ./skills/New-SkillArchive.ps1 -ConfigPath ./skills/bundles/agent-toolkit/agent-toolkit.json

.CONTEXT
    Agent-Toolkit - manual ChatGPT skill import from maintained source folders.

.AUTHOR
    Greg Tate & coding agent
#>
#requires -Version 7.0

[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot 'bundles/agent-toolkit/agent-toolkit.json'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '_bundles'),
    [ValidateSet('Plugin', 'Skill')]
    [string]$Format = 'Plugin',
    [ValidateSet('Root', 'Folder')]
    [string]$Layout = 'Root'
)

# Resolve caller-relative arguments before the execution wrapper changes location.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ConfigPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ConfigPath)
$OutputDirectory = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDirectory)

#region MAIN
# Coordinate validation, planning, packaging, and structured results.
$Main = {
    . $Helpers

    # Build the entire file plan before permitting any output changes.
    $Definition = Get-BundleDefinition -Path $ConfigPath
    $Plan = New-BundlePlan -Definition $Definition
    if ($Definition.Contains('routingSkill') -and $Definition.routingSkill -cnotin @($Plan.Name)) {
        throw "Bundle routingSkill '$($Definition.routingSkill)' must name a selected skill."
    }
    New-SkillArchive -Definition $Definition -Plan $Plan
}
#endregion

#region HELPERS
# Keep source validation and archive construction separate from orchestration.
$Helpers = {
    function Get-BundleDefinition {
        # Read a deliberately small JSON configuration with explicit skill selections.
        param([string]$Path)

        # Reject misspelled keys so an intended option cannot be silently ignored.
        $Definition = Get-Content -LiteralPath $Path -Raw -Encoding utf8 |
            ConvertFrom-Json -AsHashtable
        if ($Definition -isnot [System.Collections.IDictionary]) {
            throw 'Bundle configuration must be a JSON object.'
        }
        foreach ($Key in $Definition.Keys) {
            if ($Key -notin @('name', 'displayName', 'description', 'version', 'skills', 'icon', 'composerIcon', 'routingSkill')) {
                throw "Unknown bundle configuration field '$Key'."
            }
        }

        # Require portable identity and a useful trigger description for the root skill.
        if ($Definition.name -isnot [string] -or $Definition.name -cnotmatch '^[a-z0-9]+(-[a-z0-9]+)*$' -or
            $Definition.name.Length -gt 64) {
            throw 'Bundle name must be at most 64 lowercase letters, digits, and single hyphens.'
        }
        if ($Definition.description -isnot [string] -or [string]::IsNullOrWhiteSpace($Definition.description) -or
            $Definition.description.Length -gt 1024) {
            throw 'Bundle description must contain 1 to 1024 characters.'
        }
        if ($Definition.Contains('displayName') -and
            ($Definition.displayName -isnot [string] -or [string]::IsNullOrWhiteSpace($Definition.displayName) -or
                $Definition.displayName.Length -gt 64)) {
            throw 'Bundle displayName must contain 1 to 64 characters.'
        }
        if ($Definition.version -isnot [string] -or $Definition.version -notmatch '^\d+\.\d+\.\d+$') {
            throw 'Bundle version must use major.minor.patch format.'
        }
        if ($Definition.skills -isnot [array] -or $Definition.skills.Count -eq 0) {
            throw 'Bundle skills must be a nonempty JSON array of directory paths.'
        }
        if ($Definition.Contains('routingSkill') -and
            ($Definition.routingSkill -isnot [string] -or $Definition.routingSkill -cnotmatch '^[a-z0-9]+(-[a-z0-9]+)*$' -or
                $Definition.routingSkill.Length -gt 64)) {
            throw 'Bundle routingSkill must be a lowercase skill name of at most 64 characters.'
        }
        foreach ($IconKey in @('icon', 'composerIcon')) {
            if (-not $Definition.Contains($IconKey)) { continue }
            if ($Definition[$IconKey] -isnot [string] -or $Definition[$IconKey] -notmatch '^bundles[/\\][a-zA-Z0-9][a-zA-Z0-9_-]*[/\\][a-zA-Z0-9][a-zA-Z0-9._-]*\.png$') {
                throw "Bundle $IconKey must be a PNG file in a bundle directory under bundles/."
            }
            $Icon = Get-Item -LiteralPath (Join-Path $PSScriptRoot $Definition[$IconKey])
            if ($Icon.PSIsContainer -or ($Icon.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -or
                ($Icon.Directory.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
                throw "Bundle $IconKey must be a physical PNG file."
            }
        }
        return $Definition
    }

    function Resolve-SkillDirectory {
        # Restrict selections to real directories below personal or community.
        param([string]$RelativePath)

        # Prevent path traversal, wildcard selection, and Windows alternate data streams.
        if ($RelativePath -notmatch '^(personal|community)[/\\]' -or
            $RelativePath -match '(^|[/\\])\.\.?([/\\]|$)|[:*?\[\]]') {
            throw "Skill path '$RelativePath' must be an explicit path under personal/ or community/."
        }
        $FullPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot $RelativePath))
        $Directory = Get-Item -LiteralPath $FullPath
        if (-not $Directory.PSIsContainer) {
            throw "Skill path '$RelativePath' is not a directory."
        }

        # Reject linked ancestors rather than silently exporting files outside the source tree.
        $Current = $Directory
        while ($Current.FullName -ne $PSScriptRoot) {
            if ($Current.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                throw "Linked source '$($Current.FullName)' is unsupported. Select a physical skill directory."
            }
            $Current = $Current.Parent
        }
        if (-not (Test-Path -LiteralPath (Join-Path $FullPath 'SKILL.md') -PathType Leaf)) {
            throw "Skill '$RelativePath' is missing SKILL.md."
        }
        return $Directory
    }

    function ConvertFrom-SkillScalar {
        # Decode quoted metadata without carrying YAML escaping into generated prose.
        param([string]$Value)

        # Handle the single-quoted and JSON-compatible double-quoted forms used by sources.
        $Value = $Value.Trim()
        if ($Value.StartsWith("'")) {
            if ($Value.Length -lt 2 -or -not $Value.EndsWith("'")) {
                throw 'Unterminated single-quoted skill metadata.'
            }
            return $Value.Substring(1, $Value.Length - 2).Replace("''", "'")
        }
        if ($Value.StartsWith('"')) {
            return ConvertFrom-Json -InputObject $Value -NoEnumerate
        }
        return $Value
    }

    function Get-SkillMetadata {
        # Check frontmatter boundaries and the required portable skill identity fields.
        param([System.IO.DirectoryInfo]$Directory)

        # Read only supported scalar identity and scalar or block description forms.
        $Text = Get-Content -LiteralPath (Join-Path $Directory.FullName 'SKILL.md') -Raw -Encoding utf8
        $Frontmatter = [regex]::Match($Text, '\A---\r?\n(?<yaml>[\s\S]*?)\r?\n---(?:\r?\n|\z)')
        if (-not $Frontmatter.Success) {
            throw "Skill '$($Directory.Name)' needs YAML frontmatter delimited by --- lines."
        }
        $NameField = [regex]::Matches($Frontmatter.Groups['yaml'].Value, '(?m)^name:[ \t]*(?<value>[^\r\n]+)')
        $DescriptionField = [regex]::Matches($Frontmatter.Groups['yaml'].Value, '(?m)^description:[ \t]*(?<value>[^\r\n]*)')
        if ($NameField.Count -ne 1 -or $DescriptionField.Count -ne 1) {
            throw "Skill '$($Directory.Name)' needs exactly one name and description field."
        }
        $Name = ConvertFrom-SkillScalar -Value $NameField[0].Groups['value'].Value
        if ($Name -cnotmatch '^[a-z0-9]+(-[a-z0-9]+)*$' -or $Name.Length -gt 64 -or $Name -cne $Directory.Name) {
            throw "Skill name '$Name' must be a lowercase slug matching directory '$($Directory.Name)'."
        }
        $Description = $DescriptionField[0].Groups['value'].Value.Trim()
        if ($Description -match '^[>|][-+]?([1-9])?$') {
            $Block = [regex]::Match($Frontmatter.Groups['yaml'].Value, '(?m)^description:[^\r\n]*\r?\n(?<body>(?:[ \t]+[^\r\n]*(?:\r?\n|$))+)')
            $Description = ($Block.Groups['body'].Value -replace '\s+', ' ').Trim()
        }
        else {
            $Description = ConvertFrom-SkillScalar -Value $Description
        }
        if ([string]::IsNullOrWhiteSpace($Description) -or $Description -in @('null', '~', '[]', '{}') -or
            $Description.StartsWith('#') -or $Description.Length -gt 1024) {
            throw "Skill '$Name' needs a nonempty description of at most 1024 characters."
        }
        return [pscustomobject]@{ Name = $Name; Description = $Description }
    }

    function Get-SkillFile {
        # Enumerate portable content while pruning repository metadata and generated caches.
        param([System.IO.DirectoryInfo]$Directory, [string]$RelativePath = '')

        # Preserve hidden resources; exclude only known metadata and generated content.
        foreach ($Item in Get-ChildItem -LiteralPath $Directory.FullName -Force | Sort-Object Name) {
            if ($Item.Name -in @('.git', '.github', '__pycache__', '.pytest_cache', '.mypy_cache',
                    '.ruff_cache', '.venv', 'venv', 'node_modules', '.DS_Store', 'Thumbs.db', 'Desktop.ini') -or
                $Item.Extension -in @('.pyc', '.pyo')) {
                continue
            }
            if ($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                throw "Linked content '$($Item.FullName)' is unsupported. Materialize it before packaging."
            }
            $ChildPath = ($RelativePath + '/' + $Item.Name).TrimStart('/')
            if ($Item.PSIsContainer) {
                Get-SkillFile -Directory $Item -RelativePath $ChildPath
            }
            else {
                [pscustomobject]@{ Source = $Item.FullName; RelativePath = $ChildPath }
            }
        }
    }

    function Get-SourceProvenance {
        # Record the current checkout honestly, including local changes to the selected source.
        param([System.IO.DirectoryInfo]$Directory)

        # Git metadata is optional for personal directories but required for community checkouts.
        $Repository = & git -C $Directory.FullName rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -ne 0) {
            return [ordered]@{ repository = $null; commit = $null; dirty = $null }
        }
        $Commit = & git -C $Directory.FullName rev-parse HEAD
        $Remote = & git -C $Directory.FullName config --get remote.origin.url
        $Dirty = @(& git -C $Directory.FullName status --porcelain -- .).Count -gt 0
        return [ordered]@{
            repository = ($Remote -join '')
            commit     = ($Commit -join '')
            dirty      = $Dirty
        }
    }

    function New-BundlePlan {
        # Validate every selection and collect source files before creating an archive.
        param([System.Collections.IDictionary]$Definition)

        # Track portable names so two repositories cannot silently overwrite the same skill.
        $Names = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
        foreach ($Selection in $Definition.skills) {
            if ($Selection -isnot [string] -or [string]::IsNullOrWhiteSpace($Selection)) {
                throw 'Each skills entry must be a nonempty directory path string.'
            }
            $Directory = Resolve-SkillDirectory -RelativePath $Selection
            $Metadata = Get-SkillMetadata -Directory $Directory
            if (-not $Names.Add($Metadata.Name)) {
                throw "Duplicate skill name '$($Metadata.Name)' in bundle selection."
            }
            $Files = @(Get-SkillFile -Directory $Directory)

            # Preserve ancestor licenses alongside each skill without altering its own files.
            $LicenseFiles = @()
            $Ancestor = $Directory.Parent
            $CommunityRoot = Join-Path $PSScriptRoot 'community'
            $PersonalRoot = Join-Path $PSScriptRoot 'personal'
            while ($Ancestor.FullName -notin @($PSScriptRoot, $CommunityRoot, $PersonalRoot)) {
                foreach ($License in Get-ChildItem -LiteralPath $Ancestor.FullName -File -Force |
                        Where-Object { $_.Name -match '^(LICENSE|LICENCE|COPYING|NOTICE)([.-].*)?$' }) {
                    if ($License.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                        throw "Linked license '$($License.FullName)' is unsupported."
                    }
                    $LicenseFiles += [pscustomobject]@{
                        Source       = $License.FullName
                        RelativePath = "licenses/$($LicenseFiles.Count)-$($License.Name)"
                    }
                }
                $Ancestor = $Ancestor.Parent
            }
            $Provenance = Get-SourceProvenance -Directory $Directory
            if ($Selection -match '^community[/\\]' -and $Provenance.commit -eq $null) {
                throw "Community skill '$Selection' must be in a Git checkout for provenance."
            }
            if ($Selection -match '^community[/\\]' -and $LicenseFiles.Count -eq 0 -and
                -not ($Files.RelativePath -match '(^|/)(LICENSE|LICENCE|COPYING)([.-].*)?$')) {
                throw "No license file found for '$Selection'. Review its licensing before packaging."
            }
            [pscustomobject]@{
                Name        = $Metadata.Name
                Description = $Metadata.Description
                Path        = $Selection.Replace('\', '/')
                Files       = $Files
                Licenses    = $LicenseFiles
                Provenance  = $Provenance
            }
        }
    }

    function New-BundleEntryPoint {
        # Generate a concise router that loads only guidance relevant to the user's request.
        param([System.Collections.IDictionary]$Definition, [object[]]$Plan)

        # Serialize the description as a quoted YAML-compatible JSON string.
        $Description = ConvertTo-Json -InputObject $Definition.description -Compress
        $Lines = @(
            '---', "name: $($Definition.name)", "description: $Description", '---', '',
            "# $($Definition.name)", '',
            'Use the following embedded guidance when it matches the request. Read the linked',
            'SKILL.md before applying it; load its supporting files only as needed.', '',
            '## Included guidance', ''
        )
        if ($Definition.Contains('routingSkill')) {
            $Lines += "For requests covered by this bundle, first read and follow the [$($Definition.routingSkill) routing guidance](references/skills/$($Definition.routingSkill)/SKILL.md).", ''
        }
        foreach ($Skill in $Plan) {
            $Lines += "- [$($Skill.Name)](references/skills/$($Skill.Name)/SKILL.md): $($Skill.Description)"
        }
        $Lines += @(
            '', '## Applying the guidance', '',
            '- Select only the guidance needed for the current task; combine it when useful.',
            '- Resolve embedded relative references from the containing skill directory.',
            '- Follow the user''s request and applicable host instructions when guidance conflicts.',
            '- Use tools actually available in ChatGPT. If a required capability is unavailable,',
            '  explain the limitation instead of claiming the workflow ran.',
            '- Treat scripts as supporting resources; inspect them before running them.',
            '- Source revisions, licenses, and file hashes are recorded in bundle-manifest.json.'
        )
        # Include release history from the matching configuration when available.
        $ChangelogPath = [System.IO.Path]::ChangeExtension($ConfigPath, '.changelog.md')
        if (Test-Path -LiteralPath $ChangelogPath -PathType Leaf) {
            $Lines += '', (Get-Content -LiteralPath $ChangelogPath -Raw -Encoding utf8).TrimEnd()
        }
        return ($Lines -join "`n") + "`n"
    }

    function Add-ArchiveText {
        # Write generated UTF-8 text directly to a ZIP entry without a staging tree.
        param([System.IO.Compression.ZipArchive]$Archive, [string]$Name, [string]$Text)

        # Dispose the writer even when a write fails.
        $Entry = $Archive.CreateEntry($Name)
        $Writer = [System.IO.StreamWriter]::new($Entry.Open(), [System.Text.UTF8Encoding]::new($false))
        try {
            $Writer.Write($Text)
        }
        finally {
            $Writer.Dispose()
        }
    }

    function New-SkillArchive {
        # Construct and verify a temporary ZIP before replacing the named bundle.
        param([System.Collections.IDictionary]$Definition, [object[]]$Plan)

        # Keep generated output away from sources, including when a custom destination is used.
        foreach ($SourceRoot in @('personal', 'community')) {
            $ProtectedRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot $SourceRoot))
            if ($OutputDirectory -eq $ProtectedRoot -or
                $OutputDirectory.StartsWith($ProtectedRoot + [System.IO.Path]::DirectorySeparatorChar,
                    [System.StringComparison]::OrdinalIgnoreCase)) {
                throw 'OutputDirectory must be outside personal/ and community/.'
            }
        }
        if ($Format -eq 'Plugin' -and $Layout -ne 'Root') {
            throw 'Plugin format requires the Root layout.'
        }
        $Extension = if ($Format -eq 'Plugin') { '.plugin.zip' } else { '.skill' }
        $BundlePath = Join-Path $OutputDirectory ($Definition.name + $Extension)
        if (-not $PSCmdlet.ShouldProcess($BundlePath, "Package $(@($Plan).Count) selected skills")) {
            return [pscustomobject]@{ Bundle = $BundlePath; Status = 'Skipped'; SkillCount = @($Plan).Count }
        }

        # Use a unique temporary file in the destination so validation precedes replacement.
        [System.IO.Directory]::CreateDirectory($OutputDirectory) | Out-Null
        $TemporaryPath = Join-Path $OutputDirectory ('.package-' + [guid]::NewGuid().ToString('N') + '.tmp')
        $Prefix = ''
        if ($Format -eq 'Plugin') {
            $Prefix = 'skills/' + $Definition.name + '/'
        }
        elseif ($Layout -eq 'Folder') {
            $Prefix = $Definition.name + '/'
        }
        $Inventory = [System.Collections.Generic.List[object]]::new()
        $Expected = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
        try {
            $Archive = [System.IO.Compression.ZipFile]::Open($TemporaryPath, 'Create')
            try {
                # Identify the plugin and expose the composed skill to the plugin host.
                if ($Format -eq 'Plugin') {
                    $PluginManifest = [ordered]@{
                        '$schema'   = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
                        name        = $Definition.name
                        version     = $Definition.version
                        description = $Definition.description
                    }
                    $Interface = @{}
                    foreach ($IconKey in @('icon', 'composerIcon')) {
                        if (-not $Definition.Contains($IconKey)) { continue }
                        $IconPath = Join-Path $PSScriptRoot $Definition[$IconKey]
                        $IconBytes = [System.IO.File]::ReadAllBytes($IconPath)
                        $AssetPath = if ($IconKey -eq 'icon') { 'assets/icon.png' } else { 'assets/composer-icon.png' }
                        $IconStream = $Archive.CreateEntry($AssetPath).Open()
                        try {
                            $IconStream.Write($IconBytes, 0, $IconBytes.Length)
                        }
                        finally {
                            $IconStream.Dispose()
                        }
                        $Expected.Add($AssetPath) | Out-Null
                        if ($IconKey -eq 'icon') { $Interface.logo = './assets/icon.png' }
                        else { $Interface.composerIcon = './assets/composer-icon.png' }
                    }
                    if ($Interface.ContainsKey('logo') -and -not $Interface.ContainsKey('composerIcon')) {
                        $Interface.composerIcon = $Interface.logo
                    }
                    if ($Interface.Count -gt 0) {
                        $PluginManifest.extensions = @{ 'com.openai' = @{ interface = $Interface } }
                    }
                    if ($Definition.Contains('displayName')) {
                        if (-not $PluginManifest.Contains('extensions')) {
                            $PluginManifest.extensions = @{ 'com.openai' = @{ interface = @{} } }
                        }
                        $PluginManifest.extensions['com.openai'].interface.displayName = $Definition.displayName
                    }
                    Add-ArchiveText -Archive $Archive -Name 'plugin.json' -Text (
                        ($PluginManifest | ConvertTo-Json -Depth 4) + "`n"
                    )
                    $Expected.Add('plugin.json') | Out-Null
                }
                Add-ArchiveText -Archive $Archive -Name ($Prefix + 'SKILL.md') -Text (
                    New-BundleEntryPoint -Definition $Definition -Plan $Plan
                )
                $Expected.Add($Prefix + 'SKILL.md') | Out-Null

                # Retain source bytes and directory structure; hash exactly the bytes archived.
                foreach ($Skill in $Plan) {
                    foreach ($File in @($Skill.Files) + @($Skill.Licenses)) {
                        $EntryName = $Prefix + "references/skills/$($Skill.Name)/$($File.RelativePath)"
                        if (-not $Expected.Add($EntryName)) {
                            throw "Duplicate archive path '$EntryName'."
                        }
                        $Bytes = [System.IO.File]::ReadAllBytes($File.Source)
                        $Stream = $Archive.CreateEntry($EntryName).Open()
                        try {
                            $Stream.Write($Bytes, 0, $Bytes.Length)
                        }
                        finally {
                            $Stream.Dispose()
                        }
                        $Hasher = [System.Security.Cryptography.SHA256]::Create()
                        try {
                            $Hash = [System.BitConverter]::ToString($Hasher.ComputeHash($Bytes)).Replace('-', '').ToLowerInvariant()
                        }
                        finally {
                            $Hasher.Dispose()
                        }
                        $Inventory.Add([ordered]@{ path = $EntryName.Substring($Prefix.Length); sha256 = $Hash })
                    }
                }

                # Keep provenance portable by recording source-relative paths rather than local absolute paths.
                $Manifest = [ordered]@{
                    name         = $Definition.name
                    version      = $Definition.version
                    generatedUtc = [datetime]::UtcNow.ToString('o')
                    skills       = @($Plan | Select-Object Name, Path, Provenance)
                    files        = $Inventory.ToArray()
                }
                Add-ArchiveText -Archive $Archive -Name ($Prefix + 'bundle-manifest.json') -Text (
                    ($Manifest | ConvertTo-Json -Depth 12) + "`n"
                )
                $Expected.Add($Prefix + 'bundle-manifest.json') | Out-Null
            }
            finally {
                $Archive.Dispose()
            }

            # Reopen the finished ZIP and verify every planned entry before publication.
            $Archive = [System.IO.Compression.ZipFile]::OpenRead($TemporaryPath)
            try {
                $Actual = @($Archive.Entries.FullName)
                if ($Actual.Count -ne $Expected.Count -or @($Actual | Where-Object { -not $Expected.Contains($_) }).Count) {
                    throw 'Archive entries do not match the validated file plan.'
                }
            }
            finally {
                $Archive.Dispose()
            }
            [System.IO.File]::Move($TemporaryPath, $BundlePath, $true)
            [pscustomobject]@{
                Bundle     = $BundlePath
                Status     = 'Packaged'
                SkillCount = @($Plan).Count
                EntryCount = $Expected.Count
                SizeBytes  = (Get-Item -LiteralPath $BundlePath).Length
            }
        }
        finally {
            # Delete only this invocation's exact temporary file; never remove source directories.
            if ([System.IO.File]::Exists($TemporaryPath)) {
                [System.IO.File]::Delete($TemporaryPath)
            }
        }
    }
}
#endregion

# Restore the caller's location on both success and failure.
try {
    Push-Location -LiteralPath $PSScriptRoot
    & $Main
}
finally {
    Pop-Location
}
