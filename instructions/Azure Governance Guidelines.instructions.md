---
applyTo: "**/*.tf,**/*.tfvars,**/*.bicep,**/*.bicepparam"
description: "Overarching Azure resource governance — naming, tagging, and cost standards for all workspaces."
---

# Azure Resource Governance

> **Author:** Greg Tate
> **Effective:** March 4, 2026

Universal governance standards for all Azure deployments across Learning,
Project, and Client workspaces. Technology-specific guidance (Terraform, Bicep)
lives in dedicated skills and instructions — this document is
**deployment-type agnostic**.

Workspace-specific governance documents (e.g., `Governance-Lab.md`,
`terraform-governance.instructions.md`) may extend or override these
standards for their scope. When a workspace-level rule conflicts with this
document, the **workspace-level rule wins** within that workspace.

---

## 1. Workspace Categories

| Category   | Folder Pattern              | RG Prefix     | Description                                    |
| ---------- | --------------------------- | ------------- | ---------------------------------------------- |
| Learning   | `Learning/*`                | *exam-based*  | Exam study labs — governed by `Governance-Lab.md` |
| Project    | `Projects/*`                | `project-`    | Personal or open-source projects               |
| Client     | `Clients/*`                 | `client-`     | Client-specific engagements                    |

> Learning workspaces defer to `Governance-Lab.md` for resource-group
> naming. The standards below apply to **Project** and **Client**
> workspaces, and serve as defaults for any new workspace category.

---

## 2. Resource Group Naming

### 2.1 Pattern

```text
<category>-<workspace>-<environment>-<purpose>[-<instance>]-<deployment>
```

| Segment         | Description                                                         | Example Values                              |
| --------------- | ------------------------------------------------------------------- | ------------------------------------------- |
| `<category>`    | Workspace category prefix (see §1)                                  | `project`, `client`                         |
| `<workspace>`   | Short identifier for the workspace / client / project               | `docwriter`, `tcu`, `homelab`               |
| `<environment>` | Target environment                                                  | `lab`, `dev`, `staging`, `prod`             |
| `<purpose>`     | Functional role of the resource group                               | `network`, `compute`, `data`, `security`    |
| `<instance>`    | Optional numeric suffix when multiples exist                        | `01`, `02`                                  |
| `<deployment>`  | Deployment tool indicator — **always the final segment**            | `tf`, `bicep`                               |

### 2.2 Examples

| Resource Group Name                            | Category | Description                          |
| ---------------------------------------------- | -------- | ------------------------------------ |
| `project-docwriter-lab-compute-tf`             | Project  | DocumentWriter VMs (Terraform)       |
| `project-docwriter-dev-data-01-bicep`          | Project  | DocumentWriter storage (Bicep)       |
| `client-tcu-lab-network-01-tf`                 | Client   | TCU networking (Terraform)           |
| `client-tcu-prod-security-01-bicep`            | Client   | TCU Key Vault & identities (Bicep)   |

### 2.3 Learning Workspaces (Reference)

Learning workspaces follow the pattern defined in `Governance-Lab.md`:

```text
<exam>-<domain>-<topic>-<deployment>
```

Examples: `az104-networking-vnet-peering-tf`, `ai102-generative-ai-dalle-image-gen-bicep`

### 2.4 Rules

1. All segments use **lowercase with hyphens** as delimiters.
2. The deployment moniker (`-tf` or `-bicep`) is **mandatory** and always last.
3. Do **not** use the `rg-` prefix — it is retired across all workspaces.
4. Keep `<workspace>` short — abbreviate when the full name exceeds ~12 characters.

---

## 3. Common Tags

Every Azure resource group and taggable resource **must** include these tags:

| Tag                | Required | Description                                              | Example Values              |
| ------------------ | -------- | -------------------------------------------------------- | --------------------------- |
| `Environment`      | Yes      | Deployment environment                                   | `Lab`, `Dev`, `Staging`, `Prod` |
| `Category`         | Yes      | Workspace category                                       | `Learning`, `Project`, `Client` |
| `Workspace`        | Yes      | Workspace or project identifier                          | `LearningAzure`, `DocumentWriter`, `TCU` |
| `Purpose`          | Yes      | Brief description of the resource group's role           | `Networking`, `AI Foundry`, `SQL Database` |
| `Owner`            | Yes      | Resource owner display name                              | `Greg Tate`                 |
| `DateCreated`      | Yes      | Static creation date — never use dynamic functions       | `2026-03-04`                |
| `DeploymentMethod` | Yes      | IaC tool used                                            | `Terraform`, `Bicep`        |
| `ManagedBy`        | Yes      | Automation or team responsible                           | `terraform`, `bicep`, `manual` |

### 3.1 Optional Tags

These tags are encouraged when applicable:

| Tag                | When to Use                                      | Example Values              |
| ------------------ | ------------------------------------------------ | --------------------------- |
| `ExamCode`         | Learning workspaces (exam labs)                  | `AI-102`, `AZ-104`         |
| `Domain`           | Learning workspaces (functional domain)          | `Networking`, `Generative AI` |
| `Client`           | Client workspaces                                | `tcu`                       |
| `CostCenter`       | Client workspaces with billing requirements      | `IT-OPS-001`               |
| `ExpiresOn`        | Temporary or lab resources                       | `2026-03-11`               |
| `AutoShutdownExempt` | VMs exempt from auto-shutdown                  | `approved`                  |

### 3.2 Tag Rules

1. `DateCreated` must be a static string (`YYYY-MM-DD`). Never use
   `timestamp()`, `utcNow()`, or any dynamic function.
2. Tag keys use **PascalCase**.
3. Tag values are **free-form** but should be consistent within a workspace.
4. Workspace-specific governance may add required tags beyond this set.

---

## 4. Resource Naming Conventions

### 4.1 General Pattern

```text
<prefix>-<descriptive-name>[-<instance>]
```

- `<prefix>` — Azure CAF-aligned abbreviation for the resource type (see §4.2).
- `<descriptive-name>` — short, meaningful label for the resource's purpose.
- `<instance>` — optional numeric suffix (`01`, `02`) when multiples exist.

### 4.2 Common Resource Prefixes

| Resource Type               | Prefix   | Example Name                   |
| --------------------------- | -------- | ------------------------------ |
| Resource Group              | *(none)* | Uses §2 naming pattern         |
| Virtual Network             | `vnet`   | `vnet-core-01`                 |
| Subnet                      | `snet`   | `snet-app-01`                  |
| Network Security Group      | `nsg`    | `nsg-web-01`                   |
| Network Interface           | `nic`    | `nic-vm-web-01`                |
| Public IP Address           | `pip`    | `pip-lb-frontend`              |
| Load Balancer               | `lb`     | `lb-web-frontend`              |
| Application Gateway         | `agw`    | `agw-api-01`                   |
| Virtual Machine             | `vm`     | `vm-web-01`                    |
| Availability Set            | `avail`  | `avail-web-tier`               |
| VM Scale Set                | `vmss`   | `vmss-worker-01`               |
| Managed Disk                | `disk`   | `disk-vm-web-01-os`            |
| Storage Account             | `st`     | `stdocwriterdata01` (no hyphens) |
| Key Vault                   | `kv`     | `kv-app-secrets-01`            |
| App Service Plan            | `asp`    | `asp-web-01`                   |
| App Service                 | `app`    | `app-api-01`                   |
| Function App                | `func`   | `func-processor-01`            |
| SQL Server                  | `sql`    | `sql-main-01`                  |
| SQL Database                | `sqldb`  | `sqldb-orders-01`              |
| Cosmos DB Account           | `cosmos` | `cosmos-catalog-01`            |
| Container Registry          | `acr`    | `acrdocwriterlab01` (no hyphens) |
| Container App               | `ca`     | `ca-api-01`                    |
| Container App Environment   | `cae`    | `cae-shared-01`                |
| AKS Cluster                 | `aks`    | `aks-workload-01`              |
| Log Analytics Workspace     | `log`    | `log-monitor-01`               |
| Application Insights        | `appi`   | `appi-web-01`                  |
| Recovery Services Vault     | `rsv`    | `rsv-backup-01`                |
| Private Endpoint            | `pep`    | `pep-kv-01`                    |
| Private DNS Zone            | *(FQDN)* | `privatelink.blob.core.windows.net` |
| User-Assigned Managed Identity | `id`  | `id-app-web-01`                |
| Bastion Host                | `bas`    | `bas-hub-01`                   |
| NAT Gateway                 | `ng`     | `ng-egress-01`                 |
| Route Table                 | `rt`     | `rt-spoke-01`                  |
| OpenAI Account              | `oai`    | `oai-gpt-01`                   |
| AI Services (Multi-service) | `ais`    | `ais-shared-01`                |
| AI Search                   | `srch`   | `srch-knowledge-01`            |
| API Management              | `apim`   | `apim-gateway-01`              |
| Event Hub Namespace         | `evhns`  | `evhns-ingest-01`              |
| Service Bus Namespace       | `sbns`   | `sbns-messaging-01`            |

> This table covers the most common resource types. For resources not listed,
> follow the [Azure CAF abbreviation reference](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations).

### 4.3 Naming Rules

1. Use **lowercase with hyphens** for all resource names, except where Azure
   disallows hyphens (Storage Accounts, Container Registries — use
   contiguous lowercase alphanumeric).
2. Keep names concise — descriptive but not verbose.
3. Use `<prefix>-<descriptive-name>[-<instance>]` consistently.
4. For resources requiring global uniqueness, append a short deterministic or
   random suffix only when necessary (see §4.4).

### 4.4 Unique Naming — When to Use Random Suffixes

Use **static, predictable names by default**. Random suffixes are only
permitted for resources that enter a soft-deleted state and cannot be
immediately recreated with the same name.

**Decision criteria (check in order):**

1. **Resource enters soft-deleted state and name is reserved during
   retention?** (Cognitive Services, Key Vault, API Management)
   → **Use random suffix**
2. **Backup items block deletion and prevent name reuse?**
   (Recovery Vault with protected items)
   → **Use random suffix**
3. **Otherwise** → **No random suffix** — use a static name, even for
   globally unique resources (Storage Accounts, etc.)

**Random suffix format:** 4 lowercase alphanumeric characters.
Examples: `oai-gpt-7k3m`, `kv-secrets-9x2p`, `rsv-backup-4h8n`

---

## 5. Location Policy

| Setting          | Value                                          |
| ---------------- | ---------------------------------------------- |
| Default Region   | `centralus`                                    |
| Fallback Regions | `eastus2`, `westus2`, `northcentralus`         |
| Allowed Regions  | Any US region                                  |

Use `centralus` unless resource capacity or feature availability requires a
fallback. Document the region choice in a comment if deviating from the
default.

---

## 6. Cost Governance

### 6.1 Default SKUs

Use the smallest practical SKU for non-production environments:

| Resource Type     | Default SKU                 | Notes                           |
| ----------------- | --------------------------- | ------------------------------- |
| Virtual Machine   | `Standard_B2s`              | `B1s` for minimal workloads    |
| Storage Account   | `Standard_LRS`              |                                 |
| Load Balancer     | `Basic`                     |                                 |
| Public IP         | `Basic`                     |                                 |
| SQL Database      | `Basic` / `S0`              |                                 |
| Managed Disk      | `Standard_HDD`              |                                 |
| Bastion           | `Developer`                 | Required for all VM deployments |
| AI Services       | `F0` (free) where available | Upgrade to `S0` when `F0` unavailable |
| AI Search         | `Free` / `Basic`            |                                 |

### 6.2 Auto-Shutdown Schedule

All virtual machines **must** include an auto-shutdown schedule:

| Setting   | Value                    |
| --------- | ------------------------ |
| Time      | `0800` (8:00 AM)         |
| Time Zone | `Central Standard Time`  |

Exceptions must be documented and tagged with
`AutoShutdownExempt = "approved"`.

> **Client workspace override:** Client workspaces may define a different
> shutdown time. TCU uses `1600` (4:00 PM) per its own governance.

### 6.3 Cleanup Policy

- Destroy lab and dev resources within **7 days** of creation.
- Track resource age via the `DateCreated` tag.
- Resources requiring long-term persistence must justify their existence
  in the workspace README.

### 6.4 Resource Limits (Per Deployment)

These soft limits prevent runaway costs in non-production environments:

| Resource            | Max |
| ------------------- | --- |
| Virtual Machines    | 4   |
| Public IPs          | 5   |
| Storage Accounts    | 3   |
| Virtual Networks    | 4   |

Client and production workspaces may exceed these limits with documented
justification.

---

## 7. Soft-Delete & Purge Management

### 7.1 Soft-Delete Retention Periods

| Resource           | Retention | Manual Purge | Random Suffix Required                  |
| ------------------ | --------- | ------------ | --------------------------------------- |
| Cognitive Services | 48 hrs    | Yes          | Yes — name reserved during retention    |
| Key Vault          | 7–90 days | Yes          | Yes — name reserved during retention    |
| API Management     | 48 hrs    | Yes          | Yes — name reserved during retention    |
| Recovery Vault     | 14 days   | Yes          | Yes — backup items block name reuse     |
| App Insights       | 14 days   | No           | No — soft-delete can be disabled        |
| Log Analytics      | 14 days   | No           | No — soft-delete can be disabled        |

### 7.2 Disable Soft-Delete When Possible

For lab and dev environments, disable soft-delete during resource creation
when the provider allows it. This avoids name-collision issues on
recreate. Implementation details are deployment-tool specific — refer to
the relevant Terraform or Bicep skill.

---

## 8. Security Baseline

1. **Never hardcode secrets** — use Key Vault, environment variables, or
   pipeline secrets.
2. **Never commit state files or secrets** to version control.
3. **Mark sensitive outputs** appropriately in IaC code.
4. **Enable RBAC** over access policies for Key Vault where possible.
5. **Public network access** is acceptable in lab/dev environments only.
   Production must use private endpoints.

---

## 9. Documentation Requirements

Every deployment **must** include a README or equivalent documentation
covering at minimum:

1. Purpose and scope of the deployment
2. Prerequisites (subscriptions, permissions, tooling)
3. Deployment instructions
4. Validation / verification steps
5. Cleanup / teardown instructions

---

## 10. Override Hierarchy

When governance rules conflict, apply this precedence (highest wins):

1. **Workspace-specific governance** (e.g., `Governance-Lab.md`,
   `terraform-governance.instructions.md`)
2. **This document** (`Azure Governance Guidelines.instructions.md`)
3. **General Coding Guidelines** (`General Coding Guidelines.instructions.md`)

This ensures workspace-specific needs are respected while maintaining a
consistent baseline across all workspaces.
