---
name: bicep-azure
description: 'Bicep coding standards, patterns, and governance for Azure deployments across Project and Tenant workspaces. USE FOR: Bicep Azure code generation, module scaffolding, deployment stacks, parameter files, tagging, naming conventions, validation, security, Bicep style, Bicep best practices, ARM template alternatives, subscription-scoped deployments. DO NOT USE FOR: Terraform deployments (use terraform-azure), non-Azure IaC, ARM JSON templates.'
user-invocable: true
argument-hint: '[workspace or project context]'
---

# SKILL: Bicep on Azure

## Goal

Provide Bicep implementation standards and patterns for Azure deployments. Governance **values** (naming, tags, regions, SKUs, lifecycle, security) are owned by `instructions/Azure Governance Guidelines.instructions.md`; this skill covers **how** to implement them in Bicep. Sections below point to the governance document by section number instead of copying its values.

## When to Use

- Generating or reviewing Bicep code for Azure resources
- Scaffolding a new Bicep project or module
- Applying deployment scope, parameter, naming, or tagging patterns
- Configuring deployment stacks and wrapper scripts
- Validating Bicep configurations against governance standards
- Advising on Bicep best practices, security, or cost optimization

## Source References

This skill synthesizes guidance from:

- `instructions/Azure Governance Guidelines.instructions.md` — governance values (authoritative)
- `instructions/General Coding Guidelines.instructions.md` — code header format

---

## 1. General Principles

- Use Bicep as the preferred ARM abstraction for Azure resource deployments.
- Prioritize readability, clarity, and maintainability in all templates.
- Write concise, idiomatic Bicep that is easy to understand.
- Use `bicep build` to validate syntax before deployment.
- Use `bicepconfig.json` for lint/compile configuration.
- Ensure idempotency — multiple deployments should produce the same result.
- Follow the principle of least privilege for all RBAC and network rules.
- Prefer Bicep over raw ARM JSON templates in all cases.

---

## 2. File Structure

### Standard Project Layout

```
bicep/
├── main.bicep         # Root module (subscription or resource group scope)
├── main.bicepparam    # Parameter values file
├── bicepconfig.json   # Lint and compile configuration
├── bicep.ps1          # Deployment wrapper script (use the workspace's shared copy when one exists)
└── modules/
    └── <module>.bicep # Individual module files
```

### File Responsibilities

| File               | Content                                                       |
| ------------------ | ------------------------------------------------------------- |
| `main.bicep`       | Root orchestration — target scope, parameters, resource group, module calls |
| `main.bicepparam`  | Parameter values using `using './main.bicep'` syntax          |
| `bicepconfig.json` | Bicep linter and compiler settings                            |
| `bicep.ps1`        | Deployment wrapper — copy the workspace's shared wrapper when one exists instead of writing a new one |
| `modules/*.bicep`  | Individual module files — one concern per module              |

---

## 3. Deployment Scope and Stacks

### Subscription-Scoped Deployments

Use `targetScope = 'subscription'` for deployments that create resource groups:

```bicep
targetScope = 'subscription'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: commonTags
}

module networking 'modules/networking.bicep' = {
  name: 'networking-deployment'
  scope: rg
  params: {
    commonTags: commonTags
  }
}
```

### Wrapper Script Commands

A deployment wrapper (`bicep.ps1`) typically supports these actions:

| Command    | Purpose                           |
| ---------- | --------------------------------- |
| `validate` | Syntax and schema validation      |
| `plan`     | Deployment preview (what-if)      |
| `apply`    | Create or update deployment stack |
| `destroy`  | Delete deployment stack           |
| `show`     | Show stack details                |
| `list`     | List all stacks                   |
| `output`   | Show stack outputs                |

```powershell
# Validate
.\bicep.ps1 validate

# Preview
.\bicep.ps1 plan

# Deploy
.\bicep.ps1 apply

# Cleanup
.\bicep.ps1 destroy
```

The wrapper derives the stack name from the parameters file and validates subscription context before any deployment action. The `destroy` action must follow the destroy sequence in §9.

---

## 4. Naming Conventions

### 4.1 Governance Values

- Resource group pattern, closed value lists, and validation regex: governance §2.
- Resource type abbreviations, Global and Suffix columns, and name patterns: governance §4.1–4.2.
- Length and character rules: governance §4.3.
- Random suffix rules: governance §4.4.

### 4.2 Bicep Style Rules

- Use `camelCase` for Bicep parameter names, variables, and resource symbolic names.
- Build names in variables so each name is defined once.

### 4.3 Global Names and Random Suffix

`uniqueString()` is deterministic, so `uniqueString(resourceGroup().id)` alone returns the same value after a destroy and recreate and does not meet governance §4.4. Include `dateCreated` in the seed: the suffix stays stable across redeploys and changes when the deployment is recreated with a new `dateCreated`. A same-day recreate keeps the same suffix, so the purge in §9 must run (or use a new `dateCreated`).

```bicep
@description('Optional 3-4 letter tenant uniqueness prefix for globally unique names (governance §4.1)')
@maxLength(4)
param tenantPrefix string = ''

var suffix = take(uniqueString(resourceGroup().id, dateCreated), 4)
var tenantPart = empty(tenantPrefix) ? '' : '${tenantPrefix}-'
var keyVaultName = '${tenantPart}kv-${workspace}-${suffix}'
var storageName = '${tenantPrefix}st${workspace}data01'
```

---

## 5. Tagging Standards

Tag keys, closed value lists, and rules: governance §3.

### 5.1 Common Tags Pattern

```bicep
var commonTags = {
  Environment: environment     // 'Lab', 'Dev', 'Staging', 'Prod'
  Category: category           // 'Project', 'Tenant'
  Workspace: workspaceTag
  Purpose: purpose
  Owner: owner
  DateCreated: dateCreated     // Static YYYY-MM-DD — never use utcNow()
  DeploymentMethod: 'Bicep'
}
```

### 5.2 Bicep Implementation Rules

- Apply tags to all taggable resources via `commonTags`.
- Pass `commonTags` as an explicit parameter to all modules.
- Set `dateCreated` once in `main.bicepparam` and never change it on later deployments.

---

## 6. Parameters and Code Style

### 6.1 Parameter Declarations

Every parameter must have:

- `@description()` decorator — clear, concise purpose
- Explicit type
- `@allowed()` decorator when values are constrained
- `@secure()` decorator for sensitive values

```bicep
@description('Azure region for resource deployment (governance §5)')
@allowed([
  'centralus'
  'eastus'
  'eastus2'
  'northcentralus'
  'southcentralus'
  'westcentralus'
  'westus'
  'westus2'
  'westus3'
])
param location string = 'centralus'

@description('Resource owner name')
param owner string = 'Greg Tate'

@description('Static date for DateCreated tag (YYYY-MM-DD)')
param dateCreated string

@description('Administrator password for virtual machines')
@secure()
param adminPassword string
```

### 6.2 Parameter File (`.bicepparam`)

```bicep
using './main.bicep'

param location = 'centralus'
param owner = 'Greg Tate'
param dateCreated = '<YYYY-MM-DD>'
```

### 6.3 Local Variables

Use variables for computed values and repeated expressions:

```bicep
var resourceGroupName = 'project-${workspace}-${environmentSegment}-${purposeSegment}'

var commonTags = {
  Environment: 'Dev'
  Category: 'Project'
  Workspace: 'DocumentWriter'
  Purpose: 'Storage'
  Owner: owner
  DateCreated: dateCreated
  DeploymentMethod: 'Bicep'
}
```

### 6.4 Naming Style

- Use `camelCase` for parameter names, variable names, and resource symbolic names.
- Use `@description()` on every parameter — not inline comments.
- Group parameters logically: scope/location first, then domain-specific, then secrets last.

---

## 7. Modules

### 7.1 When to Use Modules

Use modules when 2+ related resource types are deployed together.

- One concern per module (domain grouping)
- Self-contained with clear inputs/outputs
- Thin orchestration in root `main.bicep`
- **Anti-pattern**: consolidating unrelated resource types into a single module

### 7.2 Module File Pattern

Each module is a `.bicep` file in `modules/`:

- Accepts `location`, `tags` (object), and cross-module references as parameters.
- Outputs resource IDs, endpoints, principal IDs.
- Uses `@description()` decorators on all parameters.

```bicep
// modules/networking.bicep

@description('Common tags applied to all networking resources')
param commonTags object

@description('Location for networking resources')
param location string = resourceGroup().location

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-core-01'
  location: location
  tags: commonTags
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
  }
}

@description('Virtual network resource ID')
output vnetId string = vnet.id

@description('Virtual network name')
output vnetName string = vnet.name
```

### 7.3 Module Consumption from Root

```bicep
module networking 'modules/networking.bicep' = {
  name: 'networking-deployment'
  scope: rg
  params: {
    commonTags: commonTags
  }
}

module compute 'modules/compute.bicep' = {
  name: 'compute-deployment'
  scope: rg
  params: {
    commonTags: commonTags
    subnetId: networking.outputs.subnetId
  }
}
```

### 7.4 Module Best Practices

- Keep modules focused — single responsibility principle.
- Define clear input/output contracts.
- Pass identity references (e.g., `principalId`) as explicit inputs for RBAC.
- Use `dependsOn` only when implicit dependencies are insufficient.
- Always scope module deployments explicitly (e.g., `scope: rg`).

---

## 8. Security

Security requirements: governance §8. Bicep implementation:

- Never hardcode secrets in Bicep files.
- Use `@secure()` decorator for sensitive parameters.
- Prefer Managed Identities over passwords or keys.
- Key Vaults must set `enableRbacAuthorization: true`.
- Enable encryption for storage accounts and disks.
- Use private endpoints only when specifically requested.
- VM network access and outbound connectivity: follow governance §8.7–8.8. Lab NSG rules for RDP/SSH must use a single owner `/32` source supplied by parameter, never `*` or `Internet`.
- Implement least privilege with Azure RBAC.
- Never output sensitive values without marking them appropriately.

### Password Implementation

Supply passwords through a `@secure()` parameter at deploy time. Never set a default value or commit the password to `.bicepparam`.

```bicep
@description('Administrator password')
@secure()
param adminPassword string
```

---

## 9. Soft-Delete and Purge Management

Behavior and lab/dev handling per resource type: governance §7.

### Resource Settings (Lab/Dev)

- Key Vault: soft-delete cannot be disabled; do not set `enableSoftDelete: false`. Leave `enablePurgeProtection` unset.
- App Configuration: leave `enablePurgeProtection` unset.
- Recovery Services Vault: set `securitySettings.softDeleteSettings.softDeleteState: 'Disabled'`; never `AlwaysON`.

```bicep
resource keyVault 'Microsoft.KeyVault/vaults@2026-02-01' = {
  name: keyVaultName
  location: location
  tags: commonTags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
  }
}
```

### Destroy Sequence (Lab/Dev)

Deleting a deployment stack soft-deletes resources but does not purge them. Run the steps that apply to the deployed resource types:

```powershell
# 1. Permanently delete workspaces first; they can't be purged once soft-deleted
az monitor log-analytics workspace delete --resource-group $rgName --workspace-name $logName --force --yes
az ml workspace delete --resource-group $rgName --name $mlwName --permanently-delete --yes

# 2. Delete the deployment stack
az stack sub delete --name $stackName --yes --force-deletion-types $forceTypes

# 3. Purge soft-deleted resources that reserve their names
az keyvault purge --name $kvName --location $location
az cognitiveservices account purge --name $aiName --resource-group $rgName --location $location
az apim deletedservice purge --service-name $apimName --location $location
az appconfig purge --name $appcsName --location $location --yes
```

---

## 10. Subscription Safety

### Subscription Validation

The deployment wrapper validates subscription context before `apply`, `destroy`, and `plan` actions. It checks against the configured subscription ID.

### Validation Sequence

```powershell
# Switch to correct profile
Use-AzProfile Lab

# Validate syntax
.\bicep.ps1 validate

# Capacity tests for constrained services
# Preview deployment
.\bicep.ps1 plan

# Deploy
.\bicep.ps1 apply
```

---

## 11. Cost Governance

Default SKUs, auto-shutdown schedule, cleanup policy, and resource limits: governance §6.

Bicep implementation:

- Use `Microsoft.DevTestLab/schedules` for VM auto-shutdown, with the time and time zone from governance §6.2.
- Expose SKUs as parameters with governance §6.1 values as defaults.
- README cleanup sections must reference the 7-day policy (governance §6.3).

---

## 12. Dependencies

### Implicit Dependencies

Bicep automatically infers dependencies when one resource references another. Prefer implicit dependencies.

### Explicit dependsOn

Use `dependsOn` only when implicit dependencies are insufficient:

```bicep
resource bastion 'Microsoft.Network/bastionHosts@2024-10-01' = {
  name: bastionName
  ...
  dependsOn: [
    networkingModule    // Bastion requires VNet in Succeeded state
  ]
}
```

**Bastion exception**: Always declare explicit dependency so Bastion creation waits for all networking resources (race condition with Developer SKU).

---

## 13. API Versions

- Use current, stable API versions for all resources.
- Prefer the latest GA API version available at time of authoring.
- Document the API version choice if deviating from latest.
- Update API versions when authoring new code — don't carry forward stale versions.

Common current API versions:

| Resource Type                   | Example API Version    |
| ------------------------------- | ---------------------- |
| `Microsoft.Resources/resourceGroups` | `2024-03-01`      |
| `Microsoft.Network/*`           | `2024-05-01`          |
| `Microsoft.Compute/*`           | `2024-07-01`          |
| `Microsoft.Storage/*`           | `2024-01-01`          |
| `Microsoft.KeyVault/vaults`     | `2026-02-01` (earlier versions retire 2027-02-27) |
| `Microsoft.CognitiveServices/*` | `2024-10-01`          |

---

## 14. Code Header

Include the header defined in `instructions/General Coding Guidelines.instructions.md` at the top of all `.bicep` files, using `//` comments.

---

## 15. Outputs

- Include `@description()` on every output.
- Output resource group names, key endpoints, and resource IDs.
- Mark sensitive outputs appropriately.

```bicep
@description('Resource group name')
output resourceGroupName string = rg.name

@description('Virtual machine name')
output vmName string = compute.outputs.vmName

@description('Storage account name for boot diagnostics')
output storageAccountName string = storage.outputs.storageName
```

---

## 16. Anti-Patterns

- **MUST NOT** hardcode values that should be parameterized.
- **MUST NEVER** store secrets in Bicep files.
- **MUST NOT** disable security features for convenience.
- **MUST NOT** use default passwords or keys.
- **MUST NOT** use `utcNow()` for `DateCreated` tags.
- **SHOULD NOT** write a new `bicep.ps1` wrapper when the workspace already has a shared one.
- **SHOULD** avoid overly complex conditional logic that obscures intent.
- **Anti-pattern**: using ARM JSON templates when Bicep is available.
- **Anti-pattern**: inlining all resources in `main.bicep` instead of using modules.

---

## 17. Governance Override Hierarchy

When rules conflict, apply this precedence (highest wins):

1. **Explicit user instruction** for the current task — state any deviation from the standards
2. **Workspace-specific governance** (the workspace's own governance instructions)
3. **Azure Governance Guidelines** (`instructions/Azure Governance Guidelines.instructions.md`)
4. **This skill** (Bicep on Azure implementation patterns)
5. **General Coding Guidelines** (`instructions/General Coding Guidelines.instructions.md`)

---

## 18. Region Rules

Default, fallback, and allowed regions: governance §5. Use the allowed list in the `location` parameter's `@allowed()` decorator (§6.1).
