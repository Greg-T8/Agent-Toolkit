---
name: terraform-ad-lab
description: 'Build a local Active Directory lab on Hyper-V using Terraform. Scaffolds Terraform modules, unattended answer files, and PowerShell bootstrap scripts that create a domain controller and member servers on a Windows Hyper-V host. USE FOR: AD lab, Active Directory lab, Terraform Hyper-V, local domain lab, domain controller lab, Windows Server lab, WinRM Hyper-V, AD DS lab, lab environment, on-prem AD, local lab, terraform hyperv provider, unattended install lab, domain join automation, PowerShell Direct bootstrap. DO NOT USE FOR: Azure AD/Entra ID, cloud VMs, Azure Virtual Machines, AKS, cloud Terraform providers.'
user-invocable: true
argument-hint: '[lab name or domain name]'
---

# SKILL: Terraform Active Directory Lab on Local Hyper-V

## Goal

Scaffold and configure a Terraform project that deploys a local Active Directory lab on a Windows Hyper-V host. The lab consists of a domain controller VM and one or more member server VMs, all provisioned with unattended Windows installs and domain-joined via PowerShell Direct.

## When to Use

- Setting up a local AD DS lab for testing, studying, or certification prep
- Automating Windows Server VM creation on a local Hyper-V host with Terraform
- Need a repeatable domain environment that can be torn down and rebuilt
- Bootstrapping Active Directory forest creation and domain joins without manual steps

## Architecture Overview

```
Hyper-V Host (Windows)
├── Terraform (taliesins/hyperv provider over WinRM)
│   ├── Module: hyperv       → VMs, VHDs, virtual switches, DVD drives
│   └── Module: active-directory → Guest bootstrap via PowerShell Direct
├── Answer File ISOs         → Unattended Windows Server install
└── PowerShell Bootstrap     → AD forest promotion + domain join
```

**Data flow:** Terraform creates Gen2 VMs with OS disks and answer-file ISOs → VMs auto-install Windows → Terraform triggers a PowerShell script → script uses PowerShell Direct (VMBus, no network needed) to promote the DC and join members to the domain.

---

## Prerequisites

Before running this skill, the Hyper-V host must satisfy these requirements:

### Software
- Windows 10/11 Pro or Windows Server with the Hyper-V role enabled
- Terraform >= 1.5.0
- PowerShell 7+ (pwsh)
- A Windows Server installation ISO (e.g., Windows Server 2025 Evaluation)
- Answer file ISOs (one for the DC, one for member servers) — created with `oscdimg` or `mkisofs`

### Hyper-V Virtual Switches
At minimum, one **Internal** virtual switch for domain traffic. Optionally an **External** switch for internet access.

### WinRM Host Configuration
The `taliesins/hyperv` provider connects to the local Hyper-V host over WinRM. The host must be configured correctly or Terraform will fail to authenticate. Apply every step below:

| # | Issue | Fix |
|---|-------|-----|
| 1 | WinRM service not running | `winrm quickconfig -quiet` and set the service to start automatically |
| 2 | Network profile is Public | `Set-NetConnectionProfile -InterfaceAlias "vEthernet (*)" -NetworkCategory Private` — Hyper-V virtual switches default to Public, which blocks WinRM |
| 3 | Unencrypted traffic blocked (HTTP mode) | Enable on both service and client: `winrm set winrm/config/service '@{AllowUnencrypted="true"}'` and `winrm set winrm/config/client '@{AllowUnencrypted="true"}'` |
| 4 | Basic authentication disabled | `winrm set winrm/config/service/auth '@{Basic="true"}'` |
| 5 | UAC remote token filtering blocks admin | Set registry: `New-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System -Name LocalAccountTokenFilterPolicy -Value 1 -PropertyType DWord -Force` |
| 6 | Microsoft-linked account fails | Use the built-in `Administrator` account — Microsoft-linked accounts fail Task Scheduler registration used by the provider |
| 7 | IP 127.0.0.1 causes Kerberos SPN mismatch | Use `localhost` as the host value instead of `127.0.0.1` |
| 8 | Operations timeout on large VHDs | Set `hyperv_timeout` to `"300s"` or more |

---

## Procedure

### Step 1 — Scaffold the Project Structure

Create the following directory layout:

```
<project>/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
├── versions.tf
├── terraform.tfvars
├── modules/
│   ├── hyperv/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── locals.tf
│   │   └── versions.tf
│   └── active-directory/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── scripts/
    ├── Invoke-DomainBootstrap.ps1
    ├── autounattend-dc.xml
    └── autounattend-node.xml
```

### Step 2 — Configure the Provider

Use the `taliesins/hyperv` provider pinned to `~> 1.2.0`. Connect over WinRM HTTP to localhost with NTLM authentication.

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    hyperv = {
      source  = "registry.terraform.io/taliesins/hyperv"
      version = "~> 1.2.0"
    }
  }
}

# providers.tf
provider "hyperv" {
  host        = var.hyperv_host     # "localhost"
  port        = var.hyperv_port     # 5985 for HTTP
  user        = var.hyperv_user
  password    = var.hyperv_password
  https       = var.hyperv_https    # false for HTTP
  insecure    = var.hyperv_insecure # true for HTTP
  use_ntlm    = var.hyperv_use_ntlm # true
  script_path = var.hyperv_script_path
  timeout     = var.hyperv_timeout  # "300s"
}
```

**Critical:** Never set `hyperv_user` or `hyperv_password` in `terraform.tfvars`. Blank values override environment variables due to Terraform variable precedence. Use `TF_VAR_hyperv_user` and `TF_VAR_hyperv_password` environment variables instead, or let Terraform prompt interactively.

### Step 3 — Define the Hyper-V Module

The `hyperv` module creates VMs, OS disks, and attaches ISOs.

#### VM Naming (locals.tf)

```hcl
locals {
  bytes_per_gib = 1073741824
  dc_name       = format("%s-DC01", var.vm_prefix)
  vm_names      = [for i in range(var.vm_count) : format("%s-SRV%02d", var.vm_prefix, i + 1)]
  answer_iso_dc   = "${var.vm_path}/AnswerISO/autounattend-dc.iso"
  answer_iso_node  = "${var.vm_path}/AnswerISO/autounattend-node.iso"
}
```

#### Domain Controller VM

Create one `hyperv_machine_instance` for the DC with:
- **Generation 2**, Secure Boot enabled, UEFI boot order: `["IDE", "CD", "Floppy", "Network"]`
- **Dynamic memory** with startup/min/max bounds
- **Two NICs**: one on an External switch (management/internet), one on an Internal switch (domain traffic)
- **Two DVD drives**: one for the Windows Server ISO, one for the DC answer-file ISO
- **One OS VHD**: dynamic VHDX

```hcl
resource "hyperv_vhd" "dc_os_disk" {
  path = "${var.vm_path}/${local.dc_name}/${local.dc_name}-OS.vhdx"
  size = var.os_disk_size_gb * local.bytes_per_gib
}

resource "hyperv_machine_instance" "domain_controller" {
  name                = local.dc_name
  path                = var.vm_path
  generation          = 2
  state               = "Running"
  processor_count     = var.dc_processor_count
  checkpoint_type     = "Disabled"

  dynamic_memory      = true
  memory_startup_bytes = var.dc_memory_startup_bytes
  memory_minimum_bytes = var.dc_memory_minimum_bytes
  memory_maximum_bytes = var.dc_memory_maximum_bytes

  vm_firmware {
    enable_secure_boot   = "On"
    secure_boot_template = "MicrosoftWindows"
    boot_order {
      boot_type            = "HardDiskDrive"
      controller_number    = 0
      controller_location  = 0
    }
    boot_order {
      boot_type            = "DvdDrive"
      controller_number    = 0
      controller_location  = 1
    }
    boot_order {
      boot_type            = "NetworkAdapter"
      network_adapter_name = "Management"
    }
  }

  hard_disk_drives {
    controller_type     = "Scsi"
    controller_number   = 0
    controller_location = 0
    path                = hyperv_vhd.dc_os_disk.path
  }

  dvd_drives {
    controller_number   = 0
    controller_location = 1
    path                = var.iso_path  # Windows Server ISO
  }

  dvd_drives {
    controller_number   = 0
    controller_location = 2
    path                = local.answer_iso_dc
  }

  network_adaptors {
    name        = "Management"
    switch_name = var.management_switch_name
  }

  network_adaptors {
    name        = "Internal"
    switch_name = var.internal_switch_name
  }

  lifecycle {
    ignore_changes = [dvd_drives]
  }
}
```

#### Member Server VMs

Use `for_each = toset(local.vm_names)` to create member servers. Start them in `state = "Off"` so the bootstrap script can control power-on sequencing.

```hcl
resource "hyperv_vhd" "node_os_disk" {
  for_each = toset(local.vm_names)
  path     = "${var.vm_path}/${each.value}/${each.value}-OS.vhdx"
  size     = var.os_disk_size_gb * local.bytes_per_gib
}

resource "hyperv_machine_instance" "member_server" {
  for_each            = toset(local.vm_names)
  name                = each.value
  path                = var.vm_path
  generation          = 2
  state               = "Off"
  processor_count     = var.processor_count
  checkpoint_type     = "Disabled"
  # ... same pattern: dynamic memory, firmware, disk, DVD drives, NICs

  lifecycle {
    ignore_changes = [dvd_drives, state]
  }

  depends_on = [hyperv_machine_instance.domain_controller]
}
```

**Key `lifecycle` patterns:**
- `ignore_changes = [dvd_drives]` — Users eject ISOs after install; Terraform should not try to re-attach them.
- `ignore_changes = [state]` on member servers — The bootstrap script powers them on; Terraform should not revert them to `Off`.

### Step 4 — Define the Active Directory Module

The `active-directory` module calls a PowerShell bootstrap script via `terraform_data` and `local-exec`.

```hcl
resource "terraform_data" "ad_bootstrap" {
  count = var.enable_guest_bootstrap ? 1 : 0

  triggers_replace = [
    var.domain_name,
    var.domain_controller_name,
    join(",", var.member_server_names),
    sha256(var.guest_admin_password),
    sha256(var.domain_safe_mode_password),
  ]

  provisioner "local-exec" {
    command     = "pwsh -File '${var.bootstrap_script_path}' -DomainName '${var.domain_name}' -DomainControllerName '${var.domain_controller_name}' -MemberServerNames '${join(",", var.member_server_names)}' -GuestAdminUsername '${var.guest_admin_username}' -DomainControllerIPv4 '${var.domain_controller_ipv4}' -PrefixLength ${var.prefix_length}"
    interpreter = ["pwsh", "-NoProfile", "-Command"]

    environment = {
      GUEST_ADMIN_PASSWORD       = var.guest_admin_password
      DOMAIN_SAFE_MODE_PASSWORD  = var.domain_safe_mode_password
    }
  }
}
```

**Security pattern:** Passwords are passed as environment variables, never on the command line. Trigger hashes use `sha256()` to detect changes without storing secrets in Terraform state.

### Step 5 — Write the Bootstrap Script

`Invoke-DomainBootstrap.ps1` uses **PowerShell Direct** (`Invoke-Command -VMName`) to configure VMs over the VMBus — no network connectivity required.

#### Orchestration Flow

```
1. Start member VMs (they were created as "Off")
2. Wait for all VMs to finish Windows install (parallel background jobs)
3. Configure DC: static IP → DNS to 127.0.0.1 → Install AD DS → Install-ADDSForest
4. Wait for AD services to come online
5. Configure members: static IP → DNS to DC → Rename-Computer → Reboot
6. Domain join members: Add-Computer -DomainName → Reboot
7. Verify all members report domain membership
```

#### Critical Patterns

**PowerShell Direct for guest access:**
```powershell
$cred = New-Object PSCredential($GuestAdminUsername, (ConvertTo-SecureString $env:GUEST_ADMIN_PASSWORD -AsPlainText -Force))
Invoke-Command -VMName $VMName -Credential $cred -ScriptBlock { ... }
```

**Wait for OS install with retries:**
```powershell
$maxRetries = 45
$delay = 20  # seconds
for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        Invoke-Command -VMName $VMName -Credential $cred -ScriptBlock { $env:COMPUTERNAME }
        break
    } catch {
        Start-Sleep -Seconds $delay
    }
}
```

**Idempotent DC promotion:**
```powershell
$cs = Get-CimInstance Win32_ComputerSystem
if ($cs.PartOfDomain -and $cs.Domain -ieq $DomainName) {
    Write-Host "Already a DC in $DomainName — skipping"
    return
}
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSForest -DomainName $DomainName -SafeModeAdministratorPassword $dsrmPwd -Force -NoRebootOnCompletion:$false
```

**Handle reboot disconnections:** AD promotion and domain join both reboot the VM, which drops the PowerShell Direct session. Catch and tolerate these known errors:
```powershell
catch {
    if ($_.Exception.Message -match 'broken pipe|transport connection|socket.*ended') {
        Write-Host "Expected reboot disconnection — continuing"
    } else {
        throw
    }
}
```

**Idempotent domain join:**
```powershell
$cs = Get-CimInstance Win32_ComputerSystem
if ($cs.PartOfDomain -and $cs.Domain -ieq $DomainName) {
    Write-Host "$VMName already joined to $DomainName — skipping"
    return
}
Add-Computer -DomainName $DomainName -Credential $domainCred -Force -Restart
```

**Adapter selection heuristic:** Select the internal adapter (no default gateway) for static IP assignment:
```powershell
$adapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
    Where-Object { -not (Get-NetIPConfiguration -InterfaceIndex $_.ifIndex).IPv4DefaultGateway }
```

### Step 6 — Create Unattended Answer Files

Create two answer files (one for DC, one for member servers) and burn them to ISO.

**Key differences:**
| Setting | DC Answer File | Member Answer File |
|---------|---------------|--------------------|
| `ComputerName` | Fixed name (e.g., `LAB-DC01`) | `*` (auto-generated, renamed later by bootstrap) |

**Common settings for both:**
- UEFI 4-partition disk layout: EFI (260 MB), MSR (16 MB), WinRE (1 GB), OS (remaining)
- Windows Server Datacenter (Desktop Experience) image
- Administrator auto-logon (1 time)
- FirstLogonCommands: enable RDP + open firewall rule + disable IE Enhanced Security

```xml
<!-- Disk configuration for UEFI Gen2 VMs -->
<DiskConfiguration>
  <Disk wcm:action="add">
    <DiskID>0</DiskID>
    <WillWipeDisk>true</WillWipeDisk>
    <CreatePartitions>
      <CreatePartition wcm:action="add"><Order>1</Order><Type>EFI</Type><Size>260</Size></CreatePartition>
      <CreatePartition wcm:action="add"><Order>2</Order><Type>MSR</Type><Size>16</Size></CreatePartition>
      <CreatePartition wcm:action="add"><Order>3</Order><Type>Primary</Type><Size>1024</Size></CreatePartition>
      <CreatePartition wcm:action="add"><Order>4</Order><Type>Primary</Type><Extend>true</Extend></CreatePartition>
    </CreatePartitions>
    <ModifyPartitions>
      <ModifyPartition wcm:action="add"><Order>1</Order><PartitionID>1</PartitionID><Format>FAT32</Format><Label>System</Label></ModifyPartition>
      <ModifyPartition wcm:action="add"><Order>2</Order><PartitionID>2</PartitionID></ModifyPartition>
      <ModifyPartition wcm:action="add"><Order>3</Order><PartitionID>3</PartitionID><Format>NTFS</Format><Label>WinRE</Label><TypeID>de94bba4-06d1-4d40-a16a-bfd50179d6ac</TypeID></ModifyPartition>
      <ModifyPartition wcm:action="add"><Order>4</Order><PartitionID>4</PartitionID><Format>NTFS</Format><Label>Windows</Label><Letter>C</Letter></ModifyPartition>
    </ModifyPartitions>
  </Disk>
</DiskConfiguration>
```

**Burn answer files to ISO** (from an elevated prompt):
```powershell
oscdimg -n -o <answer-file-folder> <output-iso-path>
```

### Step 7 — Define Variables

Root `variables.tf` must include:

| Variable | Purpose | Notes |
|----------|---------|-------|
| `hyperv_host` | WinRM target | Default `"localhost"` (not `127.0.0.1`) |
| `hyperv_port` | WinRM port | `5985` for HTTP, `5986` for HTTPS |
| `hyperv_user` | Admin username | `sensitive = true`, non-empty validation |
| `hyperv_password` | Admin password | `sensitive = true`, non-empty validation |
| `vm_prefix` | Name prefix | e.g., `"LAB"` → `LAB-DC01`, `LAB-SRV01` |
| `vm_count` | Number of member servers | >= 1 |
| `vm_path` | VM storage root | e.g., `"D:\\Hyper-V\\ADLab"` |
| `iso_path` | Windows Server ISO | Full path on host |
| `domain_name` | AD domain FQDN | e.g., `"lab.local"` |
| `guest_admin_username` | Local admin on guest VMs | Usually `"Administrator"` |
| `guest_admin_password` | Local admin password | `sensitive = true` |
| `domain_safe_mode_password` | DSRM password | `sensitive = true` |
| `domain_controller_ipv4` | Static IP for DC | On internal network |
| `member_server_ipv4s` | Static IPs for members | List, one per VM |
| `enable_guest_bootstrap` | Toggle AD bootstrap | `true`/`false` |

**Credential validation pattern:**
```hcl
variable "hyperv_user" {
  type      = string
  sensitive = true
  validation {
    condition     = length(trimspace(var.hyperv_user)) > 0
    error_message = "hyperv_user must not be empty."
  }
}
```

### Step 8 — Apply and Verify

```bash
# Set credentials via environment variables
$env:TF_VAR_hyperv_user = 'HOSTNAME\Administrator'
$env:TF_VAR_hyperv_password = 'YourPassword'

# Initialize and apply
terraform init
terraform apply
```

After apply completes, verify domain membership:
```powershell
Invoke-Command -VMName LAB-SRV01 -Credential $domainCred -ScriptBlock {
    (Get-CimInstance Win32_ComputerSystem).Domain
}
# Expected output: lab.local
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Anonymous authentication not supported` | `hyperv_user`/`hyperv_password` blank in tfvars | Remove credentials from tfvars; use `TF_VAR_*` env vars |
| `WinRM cannot process the request` | WinRM not configured on host | Run the full WinRM checklist in Prerequisites |
| `The network path was not found` | Using `127.0.0.1` instead of `localhost` | Set `hyperv_host = "localhost"` |
| Terraform timeout creating VHDs | Default 30s timeout too short | Set `hyperv_timeout = "300s"` |
| Bootstrap hangs waiting for VM | Windows install didn't start | Verify ISO paths and answer file ISO is valid |
| `broken pipe` during AD promotion | Expected — DC reboots after forest install | Already handled in bootstrap script error catching |
| VMs re-created on every apply | `dvd_drives` or `state` not in `ignore_changes` | Add `lifecycle { ignore_changes = [dvd_drives, state] }` |

---

## Customization Points

- **VM count**: Change `vm_count` for more or fewer member servers
- **VM sizing**: Adjust processor count and memory variables per role
- **Network topology**: Add or remove virtual switches and NICs
- **OS version**: Swap the ISO and update the answer file image name
- **Additional roles**: Extend `Invoke-DomainBootstrap.ps1` to install DHCP, DNS zones, Certificate Services, etc.
- **Shared storage**: Add shared VHDX disks and SMB shares for failover cluster or Storage Spaces Direct labs
