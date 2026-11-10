---
applyTo: "**/*.tf,**/*.tfvars,**/*.bicep,**/*.bicepparam"
description: "Overarching Azure resource governance — naming, tagging, regions, cost, lifecycle, and security standards for all workspaces."
---

# Azure Resource Governance

> **Author:** Greg Tate
> **Effective:** March 4, 2026
> **Last Modified:** 2026-11-10

Universal governance standards for all Azure deployments across Project and
Tenant workspaces. This document owns the governance **values and
requirements**. Technology-specific implementation (Terraform, Bicep) lives in
dedicated skills and instructions, which reference this document by section
instead of copying its values. This document is **deployment-type agnostic**.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
indicate requirement levels. MUST and MUST NOT are mandatory. SHOULD and
SHOULD NOT are defaults that may be departed from with a documented reason.
MAY is optional.

Workspace-specific governance may extend or override these standards for its
scope, subject to §10.

These standards apply to new deployments. Existing resources created under
earlier versions keep their names and settings; do not rename or recreate a
resource solely to conform.

---

## 1. Workspace Categories

| Category | Folder Pattern             | RG Prefix  | Description                                             |
| -------- | -------------------------- | ---------- | ------------------------------------------------------- |
| Project  | `Projects/*`               | `project-` | Personal or open-source projects                        |
| Tenant   | `Projects/AzureGovernance` | `tenant-`  | Tenant-wide governance (policy, monitoring, networking) |

When a folder matches more than one pattern, the most specific pattern wins
(`Projects/AzureGovernance` is **Tenant**).

---

## 2. Resource Group Naming

### 2.1 Pattern

```text
<category>-<workspace>-<environment>-<purpose>[-<instance>]
```

| Segment         | Description                                                    | Values                                        |
| --------------- | -------------------------------------------------------------- | --------------------------------------------- |
| `<category>`    | Workspace category prefix (see §1)                             | `project`, `tenant`                           |
| `<workspace>`   | Short workspace identifier, 1–12 characters                    | e.g. `docwriter`, `homelab`, `governance`     |
| `<environment>` | Target environment (closed list)                               | `lab`, `dev`, `staging`, `prod`               |
| `<purpose>`     | Functional role of the resource group                          | e.g. `network`, `compute`, `data`, `security` |
| `<instance>`    | Optional two-digit suffix when multiples exist, including side-by-side copies deployed with different tools | `01`, `02` |

### 2.2 Examples

| Resource Group Name                 | Category | Description                                   |
| ----------------------------------- | -------- | --------------------------------------------- |
| `project-docwriter-lab-compute`     | Project  | DocumentWriter VMs                            |
| `project-docwriter-dev-data-01`     | Project  | DocumentWriter storage                        |
| `project-docwriter-dev-data-02`     | Project  | Side-by-side copy deployed with another tool  |
| `tenant-governance-prod-monitoring` | Tenant   | Central Log Analytics                         |

### 2.3 Rules

1. Segments MUST contain only lowercase letters and digits. Hyphens appear
   only as delimiters between segments.
2. Names MUST match
   `^(project|tenant)-[a-z0-9]{1,12}-(lab|dev|staging|prod)-[a-z0-9]+(-[0-9]{2})?$`.
3. Names MUST NOT use the `rg-` prefix or a deployment-tool moniker
   (`-tf`, `-bicep`). The `DeploymentMethod` tag (§3) records the tool.

---

## 3. Common Tags

Every resource group and taggable resource MUST include these tags:

| Tag                | Description                                                         | Values                                         |
| ------------------ | ------------------------------------------------------------------- | ---------------------------------------------- |
| `Environment`      | Deployment environment; PascalCase form of the RG `<environment>`   | `Lab`, `Dev`, `Staging`, `Prod`                |
| `Category`         | Workspace category                                                  | `Project`, `Tenant`                            |
| `Workspace`        | Workspace or project identifier                                     | e.g. `DocumentWriter`, `AzureGovernance`       |
| `Purpose`          | Role of the resource group                                          | e.g. `Networking`, `AI Foundry`, `SQL Database` |
| `Owner`            | Resource owner display name                                         | `Greg Tate`                                    |
| `DateCreated`      | Date of the resource group's first deployment (`YYYY-MM-DD`)        | `2026-03-04`                                   |
| `DeploymentMethod` | Tool that deploys and manages the resource                          | `Terraform`, `Bicep`, `AzureCLI`, `PowerShell` |

### 3.1 Optional Tags

| Tag                  | When to Use                     | Example Values |
| -------------------- | ------------------------------- | -------------- |
| `ExpiresOn`          | Temporary or lab resources      | `2026-03-11`   |
| `AutoShutdownExempt` | VMs exempt from auto-shutdown   | `approved`     |

### 3.2 Tag Rules

1. `DateCreated` MUST be a static `YYYY-MM-DD` string. It MUST NOT use
   `timestamp()`, `utcNow()`, or any other dynamic function.
2. `Purpose` and `DateCreated` are set once per resource group and applied
   unchanged to every resource in it. `DateCreated` MUST NOT change on
   redeploy or when resources are added later.
3. Tag keys use **PascalCase**.
4. `Environment`, `Category`, and `DeploymentMethod` are closed lists. Other
   values are free-form but SHOULD be consistent within a workspace.
5. Workspace-specific governance MAY add required tags.

---

## 4. Resource Naming Conventions

### 4.1 Patterns

Resource-group-scoped resources (**Global = No** in §4.2):

```text
<type>-<descriptive-name>[-<instance>]
```

Globally unique resources (**Global = Yes** in §4.2):

```text
[<tenant>-]<type>-<workspace>-<descriptive-name>[-<instance>]
```

- `<type>` — CAF abbreviation from §4.2.
- `<tenant>` — optional 3–4 lowercase letter uniqueness prefix, typically
  matching the tenant name. Use the value set in project-level instructions.
  If none is set, ask the user, and omit the prefix if they decline.
- `<workspace>` — the RG `<workspace>` segment (§2.1).
- `<descriptive-name>` — short, meaningful label for the resource's purpose.
- `<instance>` — optional two-digit suffix (`01`, `02`). For types marked
  **Suffix** in §4.2, the random suffix (§4.4) takes its place.

### 4.2 Resource Type Abbreviations

**Global:** Yes = the name must be unique across Azure; "no hyphens" = letters
and digits only. **Suffix:** the name stays reserved after deletion (§4.4, §7).

| Resource Type                    | Abbr.    | Global          | Suffix | Example Name                          |
| -------------------------------- | -------- | --------------- | ------ | ------------------------------------- |
| Resource Group                   | *(none)* | —               |        | Uses §2 pattern                       |
| Virtual Network                  | `vnet`   | No              |        | `vnet-core-01`                        |
| Subnet                           | `snet`   | No              |        | `snet-app-01`                         |
| Network Security Group           | `nsg`    | No              |        | `nsg-web-01`                          |
| Network Interface                | `nic`    | No              |        | `nic-vm-web-01`                       |
| Public IP Address                | `pip`    | No              |        | `pip-vm-web-01`                       |
| Load Balancer (internal)         | `lbi`    | No              |        | `lbi-app-01`                          |
| Load Balancer (external)         | `lbe`    | No              |        | `lbe-web-01`                          |
| Application Gateway              | `agw`    | No              |        | `agw-api-01`                          |
| Virtual Machine                  | `vm`     | No              |        | `vm-web-01`                           |
| Availability Set                 | `avail`  | No              |        | `avail-web-tier`                      |
| VM Scale Set                     | `vmss`   | No              |        | `vmss-worker-01`                      |
| Managed Disk (OS)                | `osdisk` | No              |        | `osdisk-vm-web-01`                    |
| Managed Disk (data)              | `disk`   | No              |        | `disk-vm-web-01`                      |
| Storage Account                  | `st`     | Yes, no hyphens |        | `gtlstdocwriterdata01`                |
| Key Vault                        | `kv`     | Yes             | Yes    | `gtl-kv-docwriter-7k3m`               |
| App Service Plan                 | `asp`    | No              |        | `asp-web-01`                          |
| Web App                          | `app`    | Yes             |        | `gtl-app-docwriter-api`               |
| Function App                     | `func`   | Yes             |        | `gtl-func-docwriter-processor`        |
| SQL Server                       | `sql`    | Yes             |        | `gtl-sql-docwriter-main`              |
| SQL Database                     | `sqldb`  | No              |        | `sqldb-orders-01`                     |
| Cosmos DB Account                | `cosmos` | Yes             |        | `gtl-cosmos-docwriter-catalog`        |
| Container Registry               | `cr`     | Yes, no hyphens |        | `gtlcrdocwriter01`                    |
| Container App                    | `ca`     | No              |        | `ca-api-01`                           |
| Container Apps Environment       | `cae`    | No              |        | `cae-shared-01`                       |
| AKS Cluster                      | `aks`    | No              |        | `aks-workload-01`                     |
| Log Analytics Workspace          | `log`    | No              |        | `log-monitor-01`                      |
| Application Insights             | `appi`   | No              |        | `appi-web-01`                         |
| Recovery Services Vault          | `rsv`    | No              |        | `rsv-backup-01`                       |
| Private Endpoint                 | `pep`    | No              |        | `pep-kv-01`                           |
| Private DNS Zone                 | *(FQDN)* | —               |        | `privatelink.blob.core.windows.net`   |
| User-Assigned Managed Identity   | `id`     | No              |        | `id-app-web-01`                       |
| Bastion Host                     | `bas`    | No              |        | `bas-hub-01`                          |
| NAT Gateway                      | `ng`     | No              |        | `ng-egress-01`                        |
| Route Table                      | `rt`     | No              |        | `rt-spoke-01`                         |
| Azure OpenAI                     | `oai`    | Yes             | Yes    | `gtl-oai-docwriter-gpt-7k3m`          |
| Foundry Tools (multi-service)    | `ais`    | Yes             | Yes    | `gtl-ais-docwriter-shared-7k3m`       |
| Foundry Account                  | `aif`    | Yes             | Yes    | `gtl-aif-docwriter-agents-7k3m`       |
| Foundry Project                  | `proj`   | No              |        | `proj-docwriter-01`                   |
| Foundry Hub                      | `hub`    | No              | Yes    | `hub-docwriter-7k3m`                  |
| Machine Learning Workspace       | `mlw`    | No              | Yes    | `mlw-docwriter-7k3m`                  |
| AI Search                        | `srch`   | Yes             |        | `gtl-srch-docwriter-knowledge`        |
| API Management                   | `apim`   | Yes             | Yes    | `gtl-apim-docwriter-gateway-7k3m`     |
| App Configuration Store          | `appcs`  | Yes             | Yes    | `gtl-appcs-docwriter-config-7k3m`     |
| Event Hubs Namespace             | `evhns`  | Yes             |        | `gtl-evhns-docwriter-ingest`          |
| Service Bus Namespace            | `sbns`   | Yes             |        | `gtl-sbns-docwriter-messaging`        |

> For resource types not listed, use the
> [Azure CAF abbreviation reference](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations).

### 4.3 Naming Rules

1. Names MUST use lowercase letters, digits, and hyphens. Types marked
   "no hyphens" MUST use lowercase letters and digits only.
2. Names MUST fit Azure's length and character rules for the resource type
   ([resource name rules](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules)).
   The limits most often exceeded:
   - Windows VM names: 15 characters (computer name limit)
   - Key Vault and Storage Account names: 24 characters
3. If a name would exceed its limit, omit `<descriptive-name>` first, then
   shorten `<workspace>`.
4. Keep names concise — descriptive but not verbose.

### 4.4 Random Suffixes

Use **static, predictable names by default**. A random suffix is permitted
only for resource types marked **Suffix** in §4.2, whose names stay reserved
after deletion (§7.1).

1. The suffix is 4 lowercase alphanumeric characters and replaces
   `<instance>` as the final segment (e.g. `gtl-kv-docwriter-7k3m`).
2. The suffix MUST stay the same across redeploys of the same deployment and
   MUST change when the deployment is destroyed and recreated. A value derived
   only from the resource group ID does not change on recreate and does not
   meet this rule.

---

## 5. Location Policy

| Setting                     | Value                                                                                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| Default Region              | `centralus`                                                                                             |
| Fallback Regions (in order) | `eastus2`, `westus2`, `northcentralus`                                                                  |
| Allowed Regions             | `centralus`, `eastus`, `eastus2`, `northcentralus`, `southcentralus`, `westcentralus`, `westus`, `westus2`, `westus3` |

1. Use `centralus` unless resource capacity or feature availability requires
   a fallback. Document the region choice in a comment when deviating from
   the default.
2. For AI model deployments (Azure OpenAI, Foundry), agents MUST confirm the
   model and deployment type are available in the target region before
   deploying, and use the fallback order if they are not.

---

## 6. Cost Governance

### 6.1 Default SKUs

Use the smallest practical SKU for non-production environments:

| Resource Type   | Default SKU                  | Notes                                                                 |
| --------------- | ---------------------------- | --------------------------------------------------------------------- |
| Virtual Machine | `Standard_B2s_v2`            | `Standard_B2ats_v2` for minimal workloads                             |
| Storage Account | `Standard_LRS`               |                                                                       |
| Load Balancer   | `Standard`                   | Basic was retired on 2025-09-30                                       |
| Public IP       | `Standard`                   | Basic was retired on 2025-09-30                                       |
| SQL Database    | Free offer (serverless)      | Auto-pause when the monthly free limit is reached; `Basic` / `S0` when the subscription's free databases are used up |
| Managed Disk    | `StandardSSD_LRS`            |                                                                       |
| Bastion         | `Developer`                  | Single-VNet lab/dev only. `Basic` for VNet peering, production, or regions without Developer |
| AI Services     | `F0` (free) where available  | `S0` when `F0` is unavailable or the subscription's one `F0` for that service already exists |
| AI Search       | `Free` / `Basic`             | `Basic` when the subscription's one `Free` service already exists     |

### 6.2 Auto-Shutdown Schedule

All virtual machines **MUST** include an auto-shutdown schedule:

| Setting   | Value                   |
| --------- | ----------------------- |
| Time      | `0800` (8:00 AM)        |
| Time Zone | `Central Standard Time` |

Exceptions MUST be documented and tagged `AutoShutdownExempt = "approved"`.
Workspace-specific governance MAY set a different shutdown time.

### 6.3 Cleanup Policy

- Lab and dev resources MUST be destroyed within **7 days** of creation.
- Track resource age via the `DateCreated` tag.
- Resources requiring long-term persistence MUST justify their existence in
  the workspace README.
- On destroy, purge or permanently delete soft-deleted resources (§7).
- The Tenant workspace SHOULD maintain a monthly budget alert on each lab and
  dev subscription.

### 6.4 Resource Limits (Per Deployment)

These soft limits prevent runaway costs in non-production environments:

| Resource         | Max |
| ---------------- | --- |
| Virtual Machines | 4   |
| Public IPs       | 5   |
| Storage Accounts | 3   |
| Virtual Networks | 4   |

Production environments MAY exceed these limits with documented
justification.

---

## 7. Soft-Delete & Purge Management

### 7.1 Soft-Delete Behavior

| Resource                                     | Retention                        | Name Reserved | Lab/Dev Handling |
| -------------------------------------------- | -------------------------------- | ------------- | ---------------- |
| AI Services / Azure OpenAI / Foundry account | 48 hrs                           | Yes           | Purge on destroy; random suffix |
| Key Vault                                    | 7–90 days                        | Yes           | Soft-delete can't be disabled. Purge protection off; purge on destroy; random suffix |
| API Management                               | 48 hrs                           | Yes           | Purge on destroy; random suffix |
| App Configuration (Standard/Premium)         | 1–7 days, set at creation        | Yes           | Purge protection off; purge on destroy; random suffix |
| ML Workspace / Foundry Hub                   | 14 days                          | Yes           | Permanently delete on destroy; random suffix |
| Log Analytics Workspace                      | 14 days                          | Yes           | Force (permanent) delete on destroy; no suffix. Recreating the same name in the same RG within 14 days recovers the old workspace |
| Recovery Services Vault                      | Backup items 14 days (up to 180) | No — soft-deleted backup items block vault deletion | Soft-delete state `Disabled`, never `AlwaysOn` (irreversible); delete backup data before destroy; no suffix |

### 7.2 Lab and Dev Rules

1. Resources with **Name Reserved = Yes** MUST be purged or permanently
   deleted on destroy, and those marked Suffix in §4.2 MUST also use the
   random suffix (§4.4) as a safeguard against failed or delayed purges.
2. Log Analytics and ML workspaces MUST be permanently deleted at deletion
   time; a workspace already in soft-delete can't be purged directly.
3. Implementation details are deployment-tool specific — refer to the
   relevant Terraform or Bicep skill.

---

## 8. Security Baseline

1. Secrets MUST NOT be hardcoded — use Key Vault, environment variables, or
   pipeline secrets.
2. State files and secrets MUST NOT be committed to version control.
3. Sensitive outputs MUST be marked sensitive in IaC code.
4. Key Vaults MUST use RBAC authorization, not access policies.
5. Workloads SHOULD use managed identities instead of keys, connection
   strings, or client secrets.
6. Private endpoints are not required in any environment and MUST NOT be
   deployed unless specifically requested.
7. VM network access:
   - VMs MUST NOT allow inbound RDP, SSH, or other management ports from the
     internet (`Internet`, `*`, or `0.0.0.0/0`).
   - Lab/dev: VMs MAY have a Standard public IP for outbound access.
     Management access MUST use Azure Bastion or an NSG rule restricted to a
     single specified owner source IP (`/32`).
   - Production: VMs MUST NOT have public IPs. Outbound access MUST use a NAT
     Gateway or load balancer outbound rules, and management access MUST use
     Azure Bastion.
8. Subnets in new virtual networks are private by default (default outbound
   access was retired on 2026-03-31). Every VM that needs internet access
   MUST have an explicit outbound method from item 7.

---

## 9. Documentation Requirements

Every deployment **MUST** include a README or equivalent documentation
covering at minimum:

1. Purpose and scope of the deployment
2. Prerequisites (subscriptions, permissions, tooling)
3. Deployment instructions
4. Validation / verification steps
5. Cleanup / teardown instructions

---

## 10. Override Hierarchy

When governance rules conflict, apply this precedence (highest wins):

1. **Explicit user instruction** for the current task — the agent MUST state
   any deviation from these standards.
2. **Workspace-specific governance** (the workspace's own governance
   instructions)
3. **This document** (`Azure Governance Guidelines.instructions.md`)
4. **Technology skills** (`terraform-azure`, `bicep-azure`)
5. **General Coding Guidelines** (`General Coding Guidelines.instructions.md`)

Workspace-specific governance MAY make §8 stricter. It MUST NOT relax §8
unless the exception is documented in that workspace's governance.

---

## Revision History

- 2026-11-10 — Removed Learning and Client categories and the RG deployment
  moniker; added global naming pattern, tenant prefix, Global/Suffix
  columns, requirement keywords, closed value lists, VM access and egress
  rules, region list; replaced retired SKUs; corrected soft-delete table;
  aligned abbreviations with CAF.
- 2026-03-04 — Initial version.
