---
name: terraform-azure
description: 'Terraform coding standards, patterns, and governance for Azure deployments across Learning, Project, and Client workspaces. USE FOR: Terraform Azure code generation, module scaffolding, provider configuration, state management, variable patterns, tagging, naming conventions, validation, security, Terraform style, Terraform best practices, AzureRM provider, Terraform Azure governance. DO NOT USE FOR: local Hyper-V labs (use terraform-ad-lab), Bicep deployments (use bicep-azure), non-Azure Terraform providers.'
user-invocable: true
argument-hint: '[workspace or project context]'
---

# SKILL: Terraform on Azure

## Goal

Provide authoritative Terraform coding standards, patterns, and governance for all Azure deployments. This skill consolidates guidance from workspace-level governance documents, community best practices, and real-world patterns observed across the Learning, Project, and Client workspaces.

## When to Use

- Generating or reviewing Terraform code for Azure resources
- Scaffolding a new Terraform project or module
- Applying provider, state, variable, naming, or tagging patterns
- Validating Terraform configurations against governance standards
- Advising on Terraform best practices, security, or cost optimization

## Source References

This skill synthesizes guidance from:

- `instructions/Terraform Style Guidelines.instructions.md` — formatting, naming, best practices
- `instructions/Azure Governance Guidelines.instructions.md` — cross-workspace naming, tagging, cost, security
- `LearningAzure/.github/skills/terraform-scaffolding/SKILL.md` — lab-specific scaffolding rules (R-120 through R-128)
- `LearningAzure/.github/skills/shared-contract/SKILL.md` — cross-cutting lab rules (R-001 through R-030)
- `LearningAzure/Governance-Lab.md` — Learning workspace governance
- `TCU/.github/instructions/terraform-governance.instructions.md` — Client workspace governance
- [terraform.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/terraform.instructions.md) — community Terraform conventions
- [terraform-azure.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/terraform-azure.instructions.md) — community Azure Terraform best practices

---

## 1. General Principles

- Use Terraform to provision and manage Azure infrastructure declaratively.
- Prioritize readability, clarity, and maintainability in all configurations.
- Write concise, efficient, idiomatic HCL that is easy to understand.
- Use `terraform fmt` standard formatting (2-space indentation) before all reviews.
- Run `terraform validate` to check syntax before planning.
- Use `tflint` for linting and `tfsec` or equivalent for security scanning.
- Ensure idempotency — multiple applies should produce the same result.
- Follow the principle of least privilege for all RBAC and network rules.

---

## 2. File Structure

### Standard Project Layout

```
terraform/
├── main.tf            # Primary resource definitions or thin orchestration
├── variables.tf       # Input variable declarations
├── outputs.tf         # Output value declarations
├── providers.tf       # Provider and version configuration
├── locals.tf          # Local values (optional — use when computed values exist)
├── data.tf            # Data sources (optional)
├── terraform.tfvars   # Non-sensitive variable values
├── terraform.lock.hcl # Provider lock file (commit this)
└── modules/
    └── <module-name>/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### File Responsibilities

| File              | Content                                                             |
| ----------------- | ------------------------------------------------------------------- |
| `providers.tf`    | `terraform {}` block with `required_version` and `required_providers`, provider configuration |
| `main.tf`         | Thin orchestration: locals, resource group, module calls, or direct resources |
| `variables.tf`    | All input variables with `description`, `type`, and optional `validation` |
| `outputs.tf`      | Outputs with `description`; use `sensitive = true` for secrets      |
| `locals.tf`       | Computed values, common tags, name construction                     |
| `data.tf`         | Data sources for existing resources                                 |
| `terraform.tfvars`| Non-sensitive defaults; never store secrets here                    |

If `main.tf` or `variables.tf` grows too large, split by resource type (e.g., `main.networking.tf`, `variables.networking.tf`).

### Learning Workspace Layout (Labs)

```
<EXAM>/hands-on-labs/<domain>/lab-<topic>/
├── README.md
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── terraform.tfvars
│   └── modules/
│       └── <module>/
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
└── validation/
    └── <validation-script>.ps1
```

---

## 3. Provider Configuration

### AzureRM Provider (Standard)

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }

  subscription_id = var.subscription_id
}
```

### Rules

- Use AzureRM by default. Use AzAPI only if AzureRM lacks a required feature.
- Pin provider versions with pessimistic constraint (`~>`).
- Target latest stable Terraform and Azure provider versions.
- Include the `random` provider when the deployment contains soft-delete resources requiring unique names.
- Subscription ID must come from a variable or `ARM_SUBSCRIPTION_ID` environment variable — never hardcode in the provider block.

### Learning Workspace Override

Learning labs use `lab_subscription_id` variable name and include a subscription guard (see §11).

---

## 4. Naming Conventions

### 4.1 Resource Group Naming by Workspace

| Workspace | Pattern                                                        | Example                                |
| --------- | -------------------------------------------------------------- | -------------------------------------- |
| Learning  | `<exam>-<domain>-<topic>-tf`                                   | `az104-networking-vnet-peering-tf`     |
| Project   | `project-<workspace>-<environment>-<purpose>[-<instance>]-tf`  | `project-docwriter-lab-compute-tf`     |
| Client    | `client-<client>-<environment>-<purpose>[-<instance>]`         | `client-tcu-lab-network-01`            |

### 4.2 Resource Naming

Pattern: `<prefix>-<descriptive-name>[-<instance>]`

Use Azure CAF-aligned abbreviations:

| Resource Type           | Prefix   | Example                |
| ----------------------- | -------- | ---------------------- |
| Virtual Network         | `vnet`   | `vnet-core-01`         |
| Subnet                  | `snet`   | `snet-app-01`          |
| Network Security Group  | `nsg`    | `nsg-web-01`           |
| Virtual Machine         | `vm`     | `vm-web-01`            |
| Storage Account         | `st`     | `stdocwriterdata01`    |
| Key Vault               | `kv`     | `kv-secrets-01`        |
| App Service Plan        | `asp`    | `asp-web-01`           |
| App Service             | `app`    | `app-api-01`           |
| Function App            | `func`   | `func-processor-01`    |
| SQL Server              | `sql`    | `sql-main-01`          |
| Log Analytics           | `log`    | `log-monitor-01`       |
| Application Insights    | `appi`   | `appi-web-01`          |
| Container Registry      | `acr`    | `acrdocwriter01`       |
| OpenAI Account          | `oai`    | `oai-gpt-01`           |
| AI Services             | `ais`    | `ais-shared-01`        |
| Cognitive Services      | `cog`    | `cog-docwriter-7k3m`   |

### 4.3 Style Rules

- All segments use **lowercase with hyphens** as delimiters.
- Resources disallowing hyphens (Storage Accounts, Container Registries) use contiguous lowercase alphanumeric.
- Use `snake_case` for Terraform identifiers (variables, locals, resource names, module names).
- Use descriptive resource labels: `azurerm_resource_group.main` not `azurerm_resource_group.rg1`.
- Deployment moniker (`-tf`) is mandatory and always last for resource groups.

### 4.4 Static Names by Default

All resource names must be static and predictable. Random suffixes are **only** permitted for resources subject to soft-delete name reservation:

| Resource           | Retention | Random Suffix Required |
| ------------------ | --------- | ---------------------- |
| Cognitive Services | 48 hrs    | Yes                    |
| Key Vault          | 7–90 days | Yes                    |
| API Management     | 48 hrs    | Yes                    |
| Recovery Vault     | 14 days   | Yes                    |

Random suffix format: 4 lowercase alphanumeric characters via `random_string`.

```hcl
resource "random_string" "suffix" {
  length  = 4
  upper   = false
  special = false
}
```

---

## 5. Tagging Standards

### 5.1 Common Tags Pattern

```hcl
locals {
  common_tags = {
    Environment      = var.environment
    Category         = var.category         # "Learning", "Project", "Client"
    Workspace        = var.workspace
    Purpose          = var.purpose
    Owner            = var.owner
    DateCreated      = var.date_created     # Static YYYY-MM-DD — never use timestamp()
    DeploymentMethod = "Terraform"
    ManagedBy        = "terraform"
  }
}
```

### 5.2 Tag Rules

- `DateCreated` must be a static string. Never use `timestamp()` or any dynamic function.
- Tag keys use **PascalCase**.
- Apply tags to all taggable resources via `local.common_tags`.
- Pass `common_tags` as an explicit input to all modules.
- Workspace-specific governance may add required tags (e.g., `ExamCode`, `Client`, `CostCenter`).

### 5.3 Learning Workspace Tags

```hcl
locals {
  common_tags = {
    Environment      = "Lab"
    Project          = "<EXAM>"         # "AI-102", "AZ-104"
    Domain           = "<Domain>"       # "Networking", "Compute"
    Purpose          = "<Purpose>"      # "VNet Peering"
    Owner            = var.owner
    DateCreated      = var.date_created
    DeploymentMethod = "Terraform"
  }
}
```

---

## 6. Variables and Code Style

### 6.1 Variable Declarations

Every variable must have:

- `description` — clear, concise purpose
- `type` — explicit type declaration
- `validation` — where appropriate for safety

```hcl
variable "location" {
  description = "Azure region for resource deployment"
  type        = string
  default     = "eastus"

  validation {
    condition     = contains(["eastus", "eastus2", "westus2", "centralus"], var.location)
    error_message = "Location must be a supported US region."
  }
}

variable "date_created" {
  description = "Date the resources were created (YYYY-MM-DD format)"
  type        = string

  validation {
    condition     = can(regex("^\\d{4}-\\d{2}-\\d{2}$", var.date_created))
    error_message = "Date must be in YYYY-MM-DD format."
  }
}
```

### 6.2 Sensitive Variables

- Mark with `sensitive = true`.
- Never store secrets in `.tfvars` files or state.
- Prefer Managed Identities over passwords or keys.
- Use `ephemeral` secrets with write-only parameters when supported (Terraform v1.11+).
- Where secrets are required, store in Key Vault unless directed otherwise.

### 6.3 Local Values

- Use locals for computed values and complex expressions.
- Extract repeated expressions for DRY consistency.
- Use `locals.tf` when local values exist.
- Use precise typing for locals.

```hcl
locals {
  resource_group_name  = "project-docwriter-tf"
  resource_name_prefix = "${var.project_name}-${var.environment}"
  common_tags          = { ... }
}
```

### 6.4 Attribute Ordering in Resource Blocks

1. `depends_on` (if explicit dependency required)
2. `count` or `for_each` (instantiation logic)
3. Required attributes first, then optional
4. `tags` near the end
5. `lifecycle` block last

Separate sections with blank lines. Group related attributes together.

---

## 7. Modules

### 7.1 When to Use Modules

Use modules when 2+ related resource types are deployed together.

- One concern per module (domain grouping)
- Self-contained with clear inputs/outputs
- Thin orchestration in root `main.tf`
- **Anti-pattern**: consolidating unrelated resource types into a single module
- **Anti-pattern**: wrapping a single resource in a module

### 7.2 Module File Pattern

```
modules/<module-name>/
├── main.tf        # Resource definitions
├── variables.tf   # Inputs — must accept tags map + resource IDs from other modules
└── outputs.tf     # Resource IDs, endpoints, principal IDs
```

### 7.3 Module Best Practices

- Keep modules focused — single responsibility principle.
- Version modules if stored in Git repos.
- Provide examples in an `examples/` directory when distributing.
- Include a `README.md` explaining usage.
- Define clear input/output contracts.
- Pass identity references (e.g., `principal_id`) as explicit inputs for RBAC.
- Prefer explicit module parameters over data source lookups inside modules.
- Avoid circular dependencies between modules.
- Azure Verified Modules (AVM) are recommended when available and align with Microsoft's Well-Architected Framework.

---

## 8. State Management

### By Workspace

| Workspace | Backend                         | Notes                                |
| --------- | ------------------------------- | ------------------------------------ |
| Learning  | Local state only                | Never configure remote backend       |
| Project   | Local or remote (Azure Storage) | Use Terraform workspaces as needed   |
| Client    | Remote (Azure Storage)          | State locking via blob lease         |

### Rules

- Never commit `.tfstate` files to version control; ensure `.gitignore` coverage.
- Commit `terraform.lock.hcl` to ensure consistent providers.
- Use remote state with locking for shared/production environments.
- Enable encryption at rest and in transit for remote state.
- Only read state files — all changes must be made via Terraform CLI or HCL.

---

## 9. Security

- Never hardcode secrets in Terraform files or state.
- Use Managed Identities instead of service principals where possible.
- Mark sensitive variables with `sensitive = true`.
- Mark sensitive outputs with `sensitive = true`.
- Use Key Vault with RBAC authorization for secret storage.
- Enable encryption for storage accounts and disks.
- Use private endpoints where applicable (required for production; optional for lab/dev).
- Public network access is acceptable in lab/dev environments only.
- Implement least privilege with Azure RBAC.
- Use `.gitignore` to exclude files containing sensitive information.
- Regularly scan with `tfsec`, `trivy`, or `checkov` for security issues.

---

## 10. Soft-Delete and Purge Management

### Disable Patterns (Lab/Dev)

For non-production environments, disable soft-delete when the provider allows it:

```hcl
# Cognitive Account
purge_soft_delete_on_destroy = false     # Unique names eliminate purge need

# Key Vault feature flags
cognitive_account {
  purge_soft_delete_on_destroy = false
}

# Log Analytics
permanently_delete_on_destroy = true

# Recovery Vault
purge_protected_items_from_vault_on_destroy = true

# General
soft_delete_enabled = false
```

### Random Suffix for Soft-Delete Resources

```hcl
resource "random_string" "suffix" {
  length  = 4
  upper   = false
  special = false
}

resource "azurerm_cognitive_account" "example" {
  name = "cog-${var.topic}-${random_string.suffix.result}"
  ...
}
```

---

## 11. Subscription Safety

### Subscription Guard (Learning Workspace)

```hcl
data "azurerm_subscription" "current" {}

resource "terraform_data" "subscription_guard" {
  lifecycle {
    precondition {
      condition     = data.azurerm_subscription.current.subscription_id == var.lab_subscription_id
      error_message = "DEPLOYMENT BLOCKED — wrong subscription detected."
    }
  }
}
```

### Validation Sequence

```
terraform init
terraform validate
terraform fmt -check
# Capacity tests for constrained services
terraform plan
# Review plan output
terraform apply
```

Always review `terraform plan` output before applying, especially for production.

---

## 12. Cost Governance

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

All VMs must include auto-shutdown:

| Setting   | Default Value          | Client Override       |
| --------- | ---------------------- | --------------------- |
| Time      | `0800` (8:00 AM)       | TCU: `1600` (4:00 PM) |
| Time Zone | `Central Standard Time`| —                     |

Use `azurerm_dev_test_global_vm_shutdown_schedule`.

### Cleanup Policy

- Destroy lab/dev resources within 7 days.
- Track via `DateCreated` tag.
- Resources requiring persistence must justify in README.

---

## 13. Iteration and Dynamic Blocks

### for_each vs count

- Use `for_each` for collections (maps/sets) — provides stable resource addresses.
- Use `count` for 0-1 conditional resources.

```hcl
# Conditional resource
resource "azurerm_public_ip" "pip" {
  count = var.create_public_ip ? 1 : 0
  ...
}

# Multiple resources from a map
resource "azurerm_subnet" "subnets" {
  for_each = var.subnet_configs
  name     = each.key
  ...
}
```

### Dynamic Blocks

Use dynamic blocks for optional nested objects:

```hcl
resource "azurerm_network_security_group" "nsg" {
  ...
  dynamic "security_rule" {
    for_each = var.security_rules
    content {
      name                       = security_rule.value.name
      priority                   = security_rule.value.priority
      direction                  = security_rule.value.direction
      access                     = security_rule.value.access
      protocol                   = security_rule.value.protocol
      source_port_range          = security_rule.value.source_port_range
      destination_port_range     = security_rule.value.destination_port_range
      source_address_prefix      = security_rule.value.source_address_prefix
      destination_address_prefix = security_rule.value.destination_address_prefix
    }
  }
}
```

---

## 14. Dependencies and Lifecycle

### depends_on

- Terraform infers most dependencies automatically.
- Only use explicit `depends_on` when absolutely necessary.
- Remove redundant `depends_on` where the dependent resource is already referenced implicitly.
- Never depend on module outputs.
- **Bastion exception**: Always declare explicit dependency so Bastion creation waits for all networking resources (race condition with Developer SKU).

### lifecycle Blocks

```hcl
lifecycle {
  ignore_changes = [tags]                       # Prevent drift on externally managed tags
  prevent_destroy = true                         # Protect critical resources
}
```

- Use `ignore_changes` for attributes managed externally.
- Use `moved` blocks for renames to avoid resource replacement.
- Place `lifecycle` blocks at the end of resource definitions.

---

## 15. Code Header

Include in all `.tf` files:

```hcl
# -------------------------------------------------------------------------
# Program: <filename>
# Description: <purpose>
# Context: <workspace context>
# Author: Greg Tate
# Date: <YYYY-MM-DD>
# -------------------------------------------------------------------------
```

---

## 16. Anti-Patterns

- **MUST NOT** hardcode values that should be parameterized.
- **MUST NOT** use `local-exec` provisioners unless absolutely necessary.
- **MUST NEVER** store secrets in Terraform files or state.
- **MUST NOT** disable security features for convenience.
- **MUST NOT** use default passwords or keys.
- **MUST NOT** make manual changes to Terraform-managed resources.
- **MUST NOT** ignore state file corruption or inconsistencies.
- **SHOULD NOT** use `terraform import` as a regular workflow pattern.
- **SHOULD** avoid complex conditional logic that obscures intent.
- **SHOULD** avoid unnecessary data sources in reusable modules.
- **Anti-pattern**: branch-per-environment, repo-per-environment, or folder-per-environment layouts.

---

## 17. Governance Override Hierarchy

When rules conflict, apply this precedence (highest wins):

1. **Workspace-specific governance** (e.g., `Governance-Lab.md`, `terraform-governance.instructions.md`)
2. **Azure Governance Guidelines** (`instructions/Azure Governance Guidelines.instructions.md`)
3. **This skill** (general Terraform on Azure patterns)
4. **General Coding Guidelines** (`instructions/General Coding Guidelines.instructions.md`)

---

## 18. Testing

- Write test files using `.tftest.hcl` extension.
- Cover both positive and negative scenarios.
- Ensure tests are idempotent and repeatable.
- Use `terraform validate` for syntax checks.
- Use `terraform plan` for pre-deployment verification.
- Test in non-production environments first.
