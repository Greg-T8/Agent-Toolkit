---
name: mermaid-styling
description: Mermaid diagram styling aligned with the Azure Well-Architected Framework. Defines the base theme, class definitions, and visual hierarchy rules for all lab architecture diagrams.
user-invokable: true
---

# Mermaid Diagram Styling

Standardized styling for Mermaid architecture diagrams in hands-on labs. Colors are organized by Azure resource category and inspired by the five pillars of the [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/):

| WAF Pillar               | Mapped Categories            |
| ------------------------ | ---------------------------- |
| Reliability              | Recovery, Networking         |
| Security                 | Security, Identity           |
| Cost Optimization        | Governance                   |
| Operational Excellence   | Monitoring                   |
| Performance Efficiency   | Compute, Storage             |

All fills are soft pastels for readability; strokes are moderately bold for definition without visual noise.

---

## M-001: Base Theme

Apply this `init` block at the top of every Mermaid diagram. It sets a neutral, non-distracting canvas.

````markdown
```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#F5F5F5",
    "primaryColor": "#E8E8E8",
    "primaryTextColor": "#333333",
    "primaryBorderColor": "#999999",
    "lineColor": "#666666",
    "clusterBkg": "#FAFAFA",
    "clusterBorder": "#CCCCCC",
    "edgeLabelBackground": "#F5F5F5",
    "fontFamily": "Segoe UI, Roboto, Arial, sans-serif",
    "fontSize": "14px"
  }
}}%%
```
````

---

## M-002: AZ-104 Class Definitions

Include these class definitions in every AZ-104 diagram. Each class uses a soft fill, a moderately bold stroke, and dark text for accessibility.

````markdown
```mermaid
classDef compute    fill:#DCC8EB,stroke:#7B4FA0,color:#2D1045,stroke-width:1.5px;
classDef network    fill:#C2E6CE,stroke:#3D8B57,color:#102B18,stroke-width:1.5px;
classDef security   fill:#F2C0C4,stroke:#B5333D,color:#3A0A0E,stroke-width:1.5px;
classDef storage    fill:#FDE0B8,stroke:#C07A1A,color:#2A1800,stroke-width:1.5px;
classDef recovery   fill:#B8D8F2,stroke:#2A6BAD,color:#0D2240,stroke-width:1.5px;
classDef identity   fill:#B0E2E8,stroke:#1A7C86,color:#082628,stroke-width:1.5px;
classDef monitor    fill:#FFE4AA,stroke:#A07A00,color:#2A1C00,stroke-width:1.5px;
classDef governance fill:#D5D5D5,stroke:#6B6B6B,color:#1A1A1A,stroke-width:1.5px;
```
````

| Class        | Fill (soft) | Stroke (moderate) | WAF Alignment            |
| ------------ | ----------- | ----------------- | ------------------------ |
| `compute`    | `#DCC8EB`   | `#7B4FA0`        | Performance Efficiency   |
| `network`    | `#C2E6CE`   | `#3D8B57`        | Reliability              |
| `security`   | `#F2C0C4`   | `#B5333D`        | Security                 |
| `storage`    | `#FDE0B8`   | `#C07A1A`        | Performance Efficiency   |
| `recovery`   | `#B8D8F2`   | `#2A6BAD`        | Reliability              |
| `identity`   | `#B0E2E8`   | `#1A7C86`        | Security                 |
| `monitor`    | `#FFE4AA`   | `#A07A00`        | Operational Excellence   |
| `governance` | `#D5D5D5`   | `#6B6B6B`        | Cost Optimization        |

---

## M-003: AI-102 Class Definitions

Include these class definitions in every AI-102 diagram.

````markdown
```mermaid
classDef aiCore    fill:#CCADE0,stroke:#4A2275,color:#1A0A2D,stroke-width:1.5px;
classDef aiOpenAI  fill:#EABED8,stroke:#8A2F7A,color:#2D0A25,stroke-width:1.5px;
classDef aiSearch  fill:#ADE0E0,stroke:#1A7A7A,color:#082525,stroke-width:1.5px;
classDef aiML      fill:#B5CEE8,stroke:#2A5F93,color:#0D2240,stroke-width:1.5px;
classDef aiBot     fill:#BDDAED,stroke:#2A6F9F,color:#0D2240,stroke-width:1.5px;
```
````

| Class      | Fill (soft) | Stroke (moderate) | Category          |
| ---------- | ----------- | ----------------- | ----------------- |
| `aiCore`   | `#CCADE0`   | `#4A2275`         | AI Services       |
| `aiOpenAI` | `#EABED8`   | `#8A2F7A`         | Generative AI     |
| `aiSearch` | `#ADE0E0`   | `#1A7A7A`         | Knowledge Mining  |
| `aiML`     | `#B5CEE8`   | `#2A5F93`         | Machine Learning  |
| `aiBot`    | `#BDDAED`   | `#2A6F9F`         | Bot / Copilot     |

---

## M-004: Container Styling

For VNet, subnet, and other grouping subgraphs, apply a prominent light-blue border to establish visual hierarchy:

````markdown
```mermaid
style VNET stroke:#4A90E2,stroke-width:2.5px
```
````

---

## M-005: Usage Pattern

Apply the class to each node using the `:::` syntax:

````markdown
```mermaid
vm["VM"]:::compute
vnet["VNet"]:::network
entra["Entra ID"]:::identity
openai["Azure OpenAI"]:::aiOpenAI
```
````

---

## M-006: Design Principles

These rules govern all diagram styling decisions:

1. **Soft fills** — Pastel tones reduce visual fatigue and keep focus on topology, not color.
2. **Moderate strokes** — Bold enough to define node boundaries; not so dark they dominate.
3. **Neutral canvas** — Background (`#F5F5F5`), line color (`#666666`), and cluster borders (`#CCCCCC`) stay understated so resource nodes stand out.
4. **Dark text on light fills** — Every class uses a dark `color` value for WCAG-accessible contrast against its pastel fill.
5. **Consistent stroke-width** — All resource classes use `1.5px`; container borders use `2.5px` for hierarchy.
6. **Category alignment** — Colors map logically to Azure Well-Architected Framework pillars so diagrams communicate architectural intent at a glance.
