---
name: bicep-azure
description: 'Bicep coding standards, patterns, and governance for Azure deployments across Learning, Project, and Client workspaces. USE FOR: Bicep Azure code generation, module scaffolding, deployment stacks, parameter files, tagging, naming conventions, validation, security, Bicep style, Bicep best practices, ARM template alternatives, subscription-scoped deployments. DO NOT USE FOR: Terraform deployments (use terraform-azure), non-Azure IaC, ARM JSON templates.'
user-invocable: true
argument-hint: '[workspace or project context]'
---

# SKILL: Bicep on Azure

## Goal

Provide authoritative Bicep coding standards, patterns, and governance for all Azure deployments. This skill consolidates guidance from workspace-level governance documents, shared-contract rules, and real-world patterns observed across the Learning, Project, and Client workspaces.

## When to Use

- Generating or reviewing Bicep code for Azure resources
- Scaffolding a new Bicep project or module
- Applying deployment scope, parameter, naming, or tagging patterns
- Configuring deployment stacks and wrapper scripts
- Validating Bicep configurations against governance standards
- Advising on Bicep best practices, security, or cost optimization

## Source References

This skill synthesizes guidance from:

- `instructions/Azure Governance Guidelines.instructions.md` — cross-workspace naming, tagging, cost, security
- `LearningAzure/.github/skills/bicep-scaffolding/SKILL.md` — lab-specific scaffolding rules (R-130 through R-138)
- `LearningAzure/.github/skills/shared-contract/SKILL.md` — cross-cutting lab rules (R-001 through R-030)
- `LearningAzure/Governance-Lab.md` — Learning workspace governance
- `LearningAzure/.assets/shared/bicep/bicep.ps1` — shared deployment wrapper script
- Real Bicep modules from `LearningAzure/AZ-104/hands-on-labs/` — proven patterns in production labs

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
├── bicep.ps1          # Deployment wrapper script (shared, never modify)
└── modules/
    └── <module>.bicep # Individual module files
```

### File Responsibilities

| File               | Content                                                       |
| ------------------ | ------------------------------------------------------------- |
| `main.bicep`       | Root orchestration — target scope, parameters, resource group, module calls |
| `main.bicepparam`  | Parameter values using `using './main.bicep'` syntax          |
| `bicepconfig.json` | Bicep linter and compiler settings                            |
| `bicep.ps1`        | Shared deployment wrapper — copy from `.assets/shared/bicep/bicep.ps1`, never create custom |
| `modules/*.bicep`  | Individual module files — one concern per module              |

### Learning Workspace Layout (Labs)

```
<EXAM>/hands-on-labs/<domain>/lab-<topic>/
├── README.md
├── bicep/
│   ├── main.bicep
│   ├── main.bicepparam
│   ├── bicepconfig.json
│   ├── bicep.ps1
│   └── modules/
│       └── <module>.bicep
└── validation/
    └── <validation-script>.ps1
```

---

## 3. Deployment Scope and Stacks

### Subscription-Scoped Deployments

Use `targetScope = 'subscription'` for labs and projects that create resource groups:

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

### Deployment Stack Naming (Learning Workspace)

Pattern: `stack-<domain>-<topic>` — no exam code in stack name.

### Wrapper Script Commands

The shared `bicep.ps1` supports these actions:

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

The wrapper script auto-derives the stack name from the parameters file and validates subscription context before any deployment action.

Cleanup destroy command:

```powershell
az stack sub delete --name $stackName --yes --force-deletion-types $forceTypes
```

---

## 4. Naming Conventions

### 4.1 Resource Group Naming by Workspace

| Workspace | Pattern                                                          | Example                                    |
| --------- | ---------------------------------------------------------------- | ------------------------------------------ |
| Learning  | `<exam>-<domain>-<topic>-bicep`                                  | `az104-compute-enable-boot-diagnostics-bicep` |
| Project   | `project-<workspace>-<environment>-<purpose>[-<instance>]-bicep` | `project-docwriter-dev-data-01-bicep`      |
| Client    | `client-<client>-<environment>-<purpose>[-<instance>]-bicep`     | `client-tcu-prod-security-01-bicep`        |

### 4.2 Resource Naming

Pattern: `<prefix>-<descriptive-name>[-<instance>]`

Use Azure CAF-aligned abbreviations:

| Resource Type           | Prefix   | Example                |
| ----------------------- | -------- | ---------------------- |
| Virtual Network         | `vnet`   | `vnet-core-01`         |
| Subnet                  | `snet`   | `snet-app-01`          |
| Network Security Group  | `nsg`    | `nsg-web-01`           |
| Network Interface       | `nic`    | `nic-vm-web-01`        |
| Virtual Machine         | `vm`     | `vm-web-01`            |
| Storage Account         | `st`     | `staz104bootdiag`      |
| Key Vault               | `kv`     | `kv-secrets-01`        |
| App Service Plan        | `asp`    | `asp-web-01`           |
| Function App            | `func`   | `func-processor-01`    |
| Log Analytics           | `log`    | `log-monitor-01`       |
| Application Insights    | `appi`   | `appi-web-01`          |
| OpenAI Account          | `oai`    | `oai-gpt-01`           |
| Cognitive Services      | `cog`    | `cog-lang-7k3m`        |
| Recovery Services Vault | `rsv`    | `rsv-backup-4h8n`      |
| Bastion Host            | `bas`    | `bas-hub-01`           |

### 4.3 Style Rules

- All segments use **lowercase with hyphens** as delimiters.
- Resources disallowing hyphens (Storage Accounts, Container Registries) use contiguous lowercase alphanumeric.
- Deployment moniker (`-bicep`) is mandatory and always last for resource groups.
- Use `camelCase` for Bicep parameter names and local variables.

### 4.4 Static Names by Default

All resource names must be static and predictable. Random suffixes are **only** permitted for resources subject to soft-delete name reservation:

| Resource           | Retention | Random Suffix Required |
| ------------------ | --------- | ---------------------- |
| Cognitive Services | 48 hrs    | Yes                    |
| Key Vault          | 7–90 days | Yes                    |
| API Management     | 48 hrs    | Yes                    |
| Recovery Vault     | 14 days   | Yes                    |

Random suffix format: `uniqueString(resourceGroup().id)` truncated or scoped.

```bicep
var suffix = uniqueString(resourceGroup().id)
var cogName = 'cog-${topic}-${suffix}'
```

---

## 5. Tagging Standards

### 5.1 Common Tags Pattern

```bicep
var commonTags = {
  Environment: environment
  Category: category           // 'Learning', 'Project', 'Client'
  Workspace: workspace
  Purpose: purpose
  Owner: owner
  DateCreated: dateCreated     // Static YYYY-MM-DD — never use utcNow()
  DeploymentMethod: 'Bicep'
  ManagedBy: 'bicep'
}
```

### 5.2 Tag Rules

- `DateCreated` must be a static string. Never use `utcNow()` or any dynamic function.
- Tag keys use **PascalCase**.
- Apply tags to all taggable resources via `commonTags`.
- Pass `commonTags` as an explicit parameter to all modules.
- Workspace-specific governance may add required tags.

### 5.3 Learning Workspace Tags

```bicep
var commonTags = {
  Environment: 'Lab'
  Project: '<EXAM>'            // 'AI-102', 'AZ-104'
  Domain: '<Domain>'           // 'Networking', 'Compute'
  Purpose: '<Purpose>'         // 'Enable Boot Diagnostics'
  Owner: owner
  DateCreated: dateCreated
  DeploymentMethod: 'Bicep'
}
```

---

## 6. Parameters and Code Style

### 6.1 Parameter Declarations

Every parameter must have:

- `@description()` decorator — clear, concise purpose
- Explicit type
- `@allowed()` decorator when values are constrained
- `@secure()` decorator for sensitive values

```bicep
@description('Azure region for resource deployment')
param location string = 'eastus'

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

param location = 'eastus'
param owner = 'Greg Tate'
param dateCreated = '<YYYY-MM-DD>'
```

### 6.3 Local Variables

Use variables for computed values and repeated expressions:

```bicep
var resourceGroupName = 'az104-${domain}-${topic}-bicep'

var commonTags = {
  Environment: 'Lab'
  Project: 'AZ-104'
  Domain: 'Compute'
  Purpose: 'Enable Boot Diagnostics'
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

- Never hardcode secrets in Bicep files.
- Use `@secure()` decorator for sensitive parameters.
- Prefer Managed Identities over passwords or keys.
- Use Key Vault with RBAC authorization for secret storage.
- Enable encryption for storage accounts and disks.
- Use private endpoints where applicable (required for production; optional for lab/dev).
- Public network access is acceptable in lab/dev environments only.
- Implement least privilege with Azure RBAC.
- Never output sensitive values without marking them appropriately.

### Password Implementation

Use `uniqueString()`, a static pattern, or supply in `.bicepparam`. Mark with `@secure()`.

Target pattern for labs: `AzureLab2026!`

```bicep
@description('Administrator password')
@secure()
param adminPassword string
```

---

## 9. Soft-Delete and Purge Management

### Disable Pattern (Lab/Dev)

```bicep
resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' = {
  ...
  properties: {
    ...
    enableSoftDelete: false
  }
}
```

For Cognitive Services:

```bicep
// softDeleteState is not always available — check API version support
```

### Random Suffix for Soft-Delete Resources

```bicep
var suffix = uniqueString(resourceGroup().id)
var cogName = 'cog-${topic}-${suffix}'
var kvName = 'kv-${topic}-${suffix}'
```

---

## 10. Subscription Safety

### Subscription Validation

The shared `bicep.ps1` wrapper validates subscription context automatically before `apply`, `destroy`, and `plan` actions. It checks against the configured lab subscription ID.

### Validation Sequence

```powershell
# Switch to correct profile
Use-AzProfile Lab

# Validate syntax
.\bicep.ps1 validate

# Capacity tests for constrained services (R-019)
# Preview deployment
.\bicep.ps1 plan

# Deploy
.\bicep.ps1 apply
```

---

## 11. Cost Governance

### Default SKUs (Non-Production)

| Resource Type   | Default SKU           |
| --------------- | --------------------- |
| Virtual Machine | `Standard_B2s`        |
| Storage Account | `Standard_LRS`        |
| Load Balancer   | `Basic`               |
| Public IP       | `Basic`               |
| SQL Database    | `Basic` / `S0`        |
| Managed Disk    | `Standard_HDD`        |
| Bastion         | `Developer`           |
| AI Services     | `F0` → `S0` fallback  |

### Auto-Shutdown Schedule

All VMs must include auto-shutdown via `Microsoft.DevTestLab/schedules`:

| Setting   | Default Value          |
| --------- | ---------------------- |
| Time      | `0800` (8:00 AM)       |
| Time Zone | `Central Standard Time`|

### Cleanup Policy

- Destroy lab/dev resources within 7 days.
- Track via `DateCreated` tag.
- README cleanup section must reference the 7-day policy.

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
| `Microsoft.KeyVault/vaults`     | `2024-04-01-preview`  |
| `Microsoft.CognitiveServices/*` | `2024-10-01`          |

---

## 14. Code Header

Include in all `.bicep` files using `//` comment syntax:

```bicep
// -------------------------------------------------------------------------
// Program: <filename>
// Description: <purpose>
// Context: <workspace context>
// Author: Greg Tate
// Date: <YYYY-MM-DD>
// -------------------------------------------------------------------------
```

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
- **SHOULD NOT** create custom `bicep.ps1` wrapper scripts — always copy from shared.
- **SHOULD** avoid overly complex conditional logic that obscures intent.
- **Anti-pattern**: using ARM JSON templates when Bicep is available.
- **Anti-pattern**: inlining all resources in `main.bicep` instead of using modules.

---

## 17. Governance Override Hierarchy

When rules conflict, apply this precedence (highest wins):

1. **Workspace-specific governance** (e.g., `Governance-Lab.md`)
2. **Azure Governance Guidelines** (`instructions/Azure Governance Guidelines.instructions.md`)
3. **This skill** (general Bicep on Azure patterns)
4. **General Coding Guidelines** (`instructions/General Coding Guidelines.instructions.md`)

---

## 18. Region Rules

| Setting          | Value                                     |
| ---------------- | ----------------------------------------- |
| Default (Lab)    | `centralus` (supports Bastion Developer)  |
| Default (Other)  | `eastus`                                  |
| Fallback         | `eastus2` → `westus2` → `northcentralus` |
| Allowed          | Any US region                             |

Use default region unless capacity requires fallback. Document the choice if deviating.
