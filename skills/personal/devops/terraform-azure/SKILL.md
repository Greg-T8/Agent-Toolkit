---
name: terraform-azure
description: 'Terraform coding standards, patterns, and governance for Azure deployments across Project and Tenant workspaces. USE FOR: Terraform Azure code generation, module scaffolding, provider configuration, state management, variable patterns, tagging, naming conventions, validation, security, Terraform style, Terraform best practices, AzureRM provider, Terraform Azure governance. DO NOT USE FOR: local Hyper-V labs (use terraform-ad-lab), Bicep deployments (use bicep-azure), non-Azure Terraform providers.'
user-invocable: true
argument-hint: '[workspace or project context]'
---

# SKILL: Terraform on Azure

## Goal

Provide Terraform implementation standards and patterns for Azure deployments. Governance **values** (naming, tags, regions, SKUs, lifecycle, security) are owned by `instructions/Azure Governance Guidelines.instructions.md`; this skill covers **how** to implement them in Terraform. Sections below point to the governance document by section number instead of copying its values.

## When to Use

- Generating or reviewing Terraform code for Azure resources
- Scaffolding a new Terraform project or module
- Applying provider, state, variable, naming, or tagging patterns
- Validating Terraform configurations against governance standards
- Advising on Terraform best practices, security, or cost optimization

## Source References

This skill synthesizes guidance from:

- `instructions/Azure Governance Guidelines.instructions.md` — governance values (authoritative)
- `instructions/Terraform Style Guidelines.instructions.md` — formatting, naming, best practices
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

For lab and dev deployments, add the soft-delete flags from §10 to the `features {}` block.

### Rules

- Use AzureRM by default. Use AzAPI only if AzureRM lacks a required feature.
- Pin provider versions with pessimistic constraint (`~>`).
- Target latest stable Terraform and Azure provider versions.
- Include the `random` provider when the deployment contains resource types marked **Suffix** in governance §4.2.
- Subscription ID must come from a variable or `ARM_SUBSCRIPTION_ID` environment variable — never hardcode in the provider block.

---

## 4. Naming Conventions

### 4.1 Governance Values

- Resource group pattern, closed value lists, and validation regex: governance §2.
- Resource type abbreviations, Global and Suffix columns, and name patterns: governance §4.1–4.2.
- Length and character rules: governance §4.3.
- Random suffix rules: governance §4.4.

### 4.2 Terraform Style Rules

- Use `snake_case` for Terraform identifiers (variables, locals, resource names, module names).
- Use descriptive resource labels: `azurerm_resource_group.main` not `azurerm_resource_group.rg1`.
- Build names in `locals.tf` so each name is defined once.

### 4.3 Global Names and Random Suffix

`random_string` meets the governance §4.4 stability rule: the value persists in state across applies and is regenerated after `terraform destroy`.

```hcl
variable "tenant_prefix" {
  description = "Optional 3-4 letter tenant uniqueness prefix for globally unique names (governance §4.1)"
  type        = string
  default     = ""

  validation {
    condition     = can(regex("^([a-z]{3,4})?$", var.tenant_prefix))
    error_message = "Tenant prefix must be empty or 3-4 lowercase letters."
  }
}

resource "random_string" "suffix" {
  length  = 4
  upper   = false
  special = false
}

locals {
  tenant_part    = var.tenant_prefix == "" ? "" : "${var.tenant_prefix}-"
  key_vault_name = "${local.tenant_part}kv-${var.workspace}-${random_string.suffix.result}"
  storage_name   = "${var.tenant_prefix}st${var.workspace}data01"
}
```

---

## 5. Tagging Standards

Tag keys, closed value lists, and rules: governance §3.

### 5.1 Common Tags Pattern

```hcl
locals {
  common_tags = {
    Environment      = var.environment       # "Lab", "Dev", "Staging", "Prod"
    Category         = var.category          # "Project", "Tenant"
    Workspace        = var.workspace_tag
    Purpose          = var.purpose
    Owner            = var.owner
    DateCreated      = var.date_created      # Static YYYY-MM-DD — never use timestamp()
    DeploymentMethod = "Terraform"
  }
}
```

### 5.2 Terraform Implementation Rules

- Apply tags to all taggable resources via `local.common_tags`.
- Pass `common_tags` as an explicit input to all modules.
- Set `date_created` once in `terraform.tfvars` and never change it on later applies.

---

## 6. Variables and Code Style

### 6.1 Variable Declarations

Every variable must have:

- `description` — clear, concise purpose
- `type` — explicit type declaration
- `validation` — where appropriate for safety

```hcl
variable "location" {
  description = "Azure region for resource deployment (governance §5)"
  type        = string
  default     = "centralus"

  validation {
    condition = contains([
      "centralus", "eastus", "eastus2", "northcentralus", "southcentralus",
      "westcentralus", "westus", "westus2", "westus3"
    ], var.location)
    error_message = "Location must be an allowed region from governance §5."
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
  resource_group_name  = "project-docwriter-dev-data"
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

### Backend

| Workspace         | Backend                         | Notes                                |
| ----------------- | ------------------------------- | ------------------------------------ |
| Project / Tenant  | Local or remote (Azure Storage) | Remote state uses blob-lease locking |

### Rules

- Never commit `.tfstate` files to version control; ensure `.gitignore` coverage.
- Commit `terraform.lock.hcl` to ensure consistent providers.
- Use remote state with locking for shared/production environments.
- Enable encryption at rest and in transit for remote state.
- Only read state files — all changes must be made via Terraform CLI or HCL.

---

## 9. Security

Security requirements: governance §8. Terraform implementation:

- Never hardcode secrets in Terraform files or state.
- Use Managed Identities instead of service principals where possible.
- Mark sensitive variables and outputs with `sensitive = true`.
- Key Vaults must use RBAC authorization. Set the `azurerm_key_vault` RBAC authorization argument to `true`; the argument was renamed during the 4.x releases, so confirm the name for the pinned provider version.
- Enable encryption for storage accounts and disks.
- Use private endpoints only when specifically requested.
- VM network access and outbound connectivity: follow governance §8.7–8.8. Lab NSG rules for RDP/SSH must use a single owner `/32` source supplied by variable, never `*` or `Internet`.
- Implement least privilege with Azure RBAC.
- Use `.gitignore` to exclude files containing sensitive information.
- Regularly scan with `tfsec`, `trivy`, or `checkov` for security issues.

---

## 10. Soft-Delete and Purge Management

Behavior and lab/dev handling per resource type: governance §7.

### Provider Flags (Lab/Dev)

Purge or permanently delete on `terraform destroy`:

```hcl
provider "azurerm" {
  features {
    api_management {
      purge_soft_delete_on_destroy = true
    }
    app_configuration {
      purge_soft_delete_on_destroy = true
    }
    cognitive_account {
      purge_soft_delete_on_destroy = true
    }
    key_vault {
      purge_soft_delete_on_destroy = true
    }
    log_analytics_workspace {
      permanently_delete_on_destroy = true
    }
    machine_learning {
      purge_soft_deleted_workspace_on_destroy = true
    }
    recovery_service {
      purge_protected_items_from_vault_on_destroy = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}
```

The `api_management`, `app_configuration`, `cognitive_account`, and `key_vault` purge flags default to `true`; set them explicitly so the intent is visible. The `log_analytics_workspace`, `machine_learning`, and `recovery_service` flags default to `false` and must be set.

### Resource Settings (Lab/Dev)

- Key Vault: soft-delete cannot be disabled; leave `purge_protection_enabled = false`.
- App Configuration: leave `purge_protection_enabled = false`.
- Recovery Services Vault: set `soft_delete_enabled = false`; never enable always-on soft delete.

### Random Suffix for Soft-Delete Resources

```hcl
resource "azurerm_cognitive_account" "openai" {
  name                  = "${local.tenant_part}oai-${var.workspace}-gpt-${random_string.suffix.result}"
  custom_subdomain_name = "${local.tenant_part}oai-${var.workspace}-gpt-${random_string.suffix.result}"
  ...
}
```

---

## 11. Subscription Safety

### Subscription Guard

```hcl
data "azurerm_subscription" "current" {}

resource "terraform_data" "subscription_guard" {
  lifecycle {
    precondition {
      condition     = data.azurerm_subscription.current.subscription_id == var.subscription_id
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

Default SKUs, auto-shutdown schedule, cleanup policy, and resource limits: governance §6.

Terraform implementation:

- Use `azurerm_dev_test_global_vm_shutdown_schedule` for VM auto-shutdown, with the time and time zone from governance §6.2.
- Expose SKUs as variables with governance §6.1 values as defaults.

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

Include the header defined in `instructions/General Coding Guidelines.instructions.md` at the top of all `.tf` files, using `#` comments.

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

1. **Explicit user instruction** for the current task — state any deviation from the standards
2. **Workspace-specific governance** (the workspace's own governance instructions)
3. **Azure Governance Guidelines** (`instructions/Azure Governance Guidelines.instructions.md`)
4. **This skill** (Terraform on Azure implementation patterns)
5. **General Coding Guidelines** (`instructions/General Coding Guidelines.instructions.md`)

---

## 18. Testing

- Write test files using `.tftest.hcl` extension.
- Cover both positive and negative scenarios.
- Ensure tests are idempotent and repeatable.
- Use `terraform validate` for syntax checks.
- Use `terraform plan` for pre-deployment verification.
- Test in non-production environments first.
