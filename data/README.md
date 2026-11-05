# Data model

Synthetic finance data for **Lusalpina Group**, a fictional chocolate and coffee group. The model follows the structure of the SAP S/4HANA Universal Journal (ACDOCA for actuals, ACDOCP for plan), simplified for this project.

| Company code | Company | Country | Local currency | Business |
|---|---|---|---|---|
| CH01 | Lusalpina Switzerland AG | CH | CHF | Chocolate production and sales (group headquarters) |
| PT01 | Lusalpina Portugal, S.A. | PT | EUR | Coffee roasting and retail cafés |

Group currency: **CHF**. Actuals: 2024–2025. Budget: 2025.

## Overview

```
          company    gl_account    cost_center    profit_center
               \          |              |              /
        journal_entry (actuals)     budget (plan)

        pl_hierarchy → gl_account        exchange_rate → currency conversion
```

Two fact tables with **different grain** share the same dimensions:
- `journal_entry`: one row per **document line item** (like ACDOCA)
- `budget`: one row per **month × GL account × cost center** (like ACDOCP)

They are combined for actual vs budget analysis in SAP Datasphere (Sprint 5).

## Conventions

- **Sign:** debit = positive, credit = negative. Revenue is a credit, so it is **negative**. P&L reports flip the sign once, at the top of the hierarchy.
- **Balanced documents:** every `journal_entry` document sums to zero (both halves are generated: P&L and balance sheet).
- **Empty cost centers are valid:** revenue and balance sheet lines have no cost center.
- **Currency:** `amount_local` is in the company's currency, `amount_group` in CHF. Actuals use the monthly average rate (type `M`), budget uses one fixed planning rate (type `P`), following SAP exchange rate types.

## Tables

### Dimensions

**`company`** (SAP: T001)

| Column | Type | Description |
|---|---|---|
| `company_code` | string | Key, e.g. `CH01` |
| `company_name` | string | Legal name |
| `country` | string | ISO country code |
| `local_currency` | string | `CHF` or `EUR` |

**`gl_account`** (SAP: SKA1 + SKAT)

| Column | Type | Description |
|---|---|---|
| `gl_account` | string | Key, 8 digits |
| `account_name` | string | English text |
| `account_type` | string | `P&L` or `Balance sheet` |

**`cost_center`** (SAP: CSKS + CSKT)

| Column | Type | Description |
|---|---|---|
| `cost_center` | string | Key, e.g. `PT01-SALES` |
| `cost_center_name` | string | English text |
| `company_code` | string | → `company` |
| `profit_center` | string | → `profit_center` |

**`profit_center`** (SAP: CEPC)

| Column | Type | Description |
|---|---|---|
| `profit_center` | string | Key, e.g. `PC-COFFEE` |
| `profit_center_name` | string | English text |

**`pl_hierarchy`** (SAP: Financial Statement Version), parent-child

| Column | Type | Description |
|---|---|---|
| `node_id` | string | Key: a structure node (e.g. `GROSS_MARGIN`) or a GL account |
| `parent_node_id` | string | Parent node, empty for the top node (`EBIT`) |
| `node_name` | string | Display text |
| `sort_order` | integer | Display order among siblings |

**`exchange_rate`** (SAP: TCURR)

| Column | Type | Description |
|---|---|---|
| `rate_type` | string | `M` (monthly average, actuals) or `P` (planning rate, budget) |
| `from_currency` | string | `EUR` |
| `to_currency` | string | `CHF` |
| `fiscal_year` | integer | Year |
| `posting_period` | integer | Month (1–12) |
| `rate` | decimal(9,5) | 1 EUR = `rate` CHF |

### Facts

**`journal_entry`** (SAP: ACDOCA)

| Column | Type | Description | SAP field |
|---|---|---|---|
| `company_code` | string | → `company` | RBUKRS |
| `fiscal_year` | integer | Year | GJAHR |
| `document_number` | string | Groups the lines of one posting | BELNR |
| `line_item` | integer | Line number within the document | DOCLN |
| `posting_date` | date | Posting date | BUDAT |
| `posting_period` | integer | Month (1–12) | POPER |
| `document_type` | string | e.g. customer invoice, vendor invoice | BLART |
| `gl_account` | string | → `gl_account` | RACCT |
| `cost_center` | string | → `cost_center` (may be empty) | RCNTR |
| `profit_center` | string | → `profit_center` | PRCTR |
| `amount_local` | decimal(15,2) | Amount in company currency | HSL |
| `local_currency` | string | Company currency | RHCUR |
| `amount_group` | decimal(15,2) | Amount in group currency | KSL |
| `group_currency` | string | Always `CHF` | RKCUR |

Key: `company_code` + `fiscal_year` + `document_number` + `line_item` (SAP restarts document numbering per company and year).

**`budget`** (SAP: ACDOCP)

| Column | Type | Description |
|---|---|---|
| `company_code` | string | → `company` |
| `fiscal_year` | integer | Year |
| `posting_period` | integer | Month (1–12) |
| `gl_account` | string | → `gl_account` (P&L accounts only) |
| `cost_center` | string | → `cost_center` (may be empty) |
| `profit_center` | string | → `profit_center` |
| `amount_local` | decimal(15,2) | Planned amount in company currency |
| `local_currency` | string | Company currency |
| `amount_group` | decimal(15,2) | Planned amount in CHF (planning rate) |
| `group_currency` | string | Always `CHF` |

## Master data

**Profit centers:** `PC-CHOCOLATE`, `PC-COFFEE`, `PC-RETAIL`, `PC-CORPORATE` (headquarters and admin costs).

**Cost centers:**

| Cost center | Name | Profit center |
|---|---|---|
| CH01-PROD | Chocolate production | PC-CHOCOLATE |
| CH01-SALES | Sales Switzerland | PC-CHOCOLATE |
| CH01-MKT | Marketing Switzerland | PC-CHOCOLATE |
| CH01-ADMIN | Administration Switzerland | PC-CORPORATE |
| PT01-PROD | Coffee roasting | PC-COFFEE |
| PT01-SALES | Sales Portugal | PC-COFFEE |
| PT01-RETAIL | Retail cafés | PC-RETAIL |
| PT01-ADMIN | Administration Portugal | PC-CORPORATE |

**Chart of accounts and P&L structure:**

```
EBIT
├── Gross margin
│   ├── Revenue
│   │   ├── 41000000  Revenue – Chocolate
│   │   ├── 41100000  Revenue – Coffee
│   │   └── 41200000  Revenue – Retail
│   └── Cost of goods sold
│       ├── 51000000  Raw materials – Cocoa
│       ├── 51100000  Raw materials – Coffee beans
│       ├── 51200000  Packaging
│       └── 51300000  Production overhead (energy, maintenance)
└── Operating expenses
    ├── 61000000  Salaries
    ├── 62000000  Rent
    ├── 63000000  Marketing
    ├── 64000000  Freight & logistics
    └── 65000000  Travel expenses
```

Balance sheet accounts (counterpart of each posting, outside the P&L): `11001000` Bank, `12100000` Trade receivables, `21100000` Trade payables.
