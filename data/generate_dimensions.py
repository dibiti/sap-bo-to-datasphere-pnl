"""Generate the master data (dimension) tables for Lusalpina Group as CSV files.

Table definitions: see data/README.md.
"""

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path(__file__).parent / "generated"


def build_profit_center() -> pd.DataFrame:
    """Solved example: one row per profit center."""
    rows = [
        ("PC-CHOCOLATE", "Chocolate"),
        ("PC-COFFEE", "Coffee"),
        ("PC-RETAIL", "Retail"),
        ("PC-CORPORATE", "Corporate"),
    ]
    return pd.DataFrame(rows, columns=["profit_center", "profit_center_name"])


def build_company() -> pd.DataFrame:
    rows = [
       ("CH01", "Lusalpina Switzerland AG", "CH", "CHF"),
       ("PT01", "Lusalpina Portugal, S.A.", "PT", "EUR"),
    ]
    return pd.DataFrame(rows, columns=["company_code", "company_name", "country", "local_currency"])


def build_gl_account() -> pd.DataFrame:
    rows = [
        ("11001000", "Bank", "Balance sheet"),
        ("12100000", "Trade receivables", "Balance sheet"),
        ("21100000", "Trade payables", "Balance sheet"),
        ("41000000", "Revenue - Chocolate", "P&L"),
        ("41100000", "Revenue - Coffee", "P&L"),
        ("41200000", "Revenue - Retail", "P&L"),
        ("51000000", "Raw materials - Cocoa", "P&L"),
        ("51100000", "Raw materials - Coffee beans", "P&L"),
        ("51200000", "Packaging", "P&L"),
        ("51300000", "Production overhead", "P&L"),
        ("61000000", "Salaries", "P&L"),
        ("62000000", "Rent", "P&L"),
        ("63000000", "Marketing", "P&L"),
        ("64000000", "Freight & logistics", "P&L"),
        ("65000000", "Travel expenses", "P&L"),
    ]
    return pd.DataFrame(rows, columns=["gl_account", "account_name", "account_type"])


def build_cost_center() -> pd.DataFrame:
    rows = [
        ("CH01-PROD", "Chocolate production", "CH01", "PC-CHOCOLATE"),
        ("CH01-SALES", "Sales Switzerland", "CH01", "PC-CHOCOLATE"),
        ("CH01-MKT", "Marketing Switzerland", "CH01", "PC-CHOCOLATE"),
        ("CH01-ADMIN", "Administration Switzerland", "CH01", "PC-CORPORATE"),
        ("PT01-PROD", "Coffee roasting", "PT01", "PC-COFFEE"),
        ("PT01-SALES", "Sales Portugal", "PT01", "PC-COFFEE"),
        ("PT01-RETAIL", "Retail cafés", "PT01", "PC-RETAIL"),
        ("PT01-ADMIN", "Administration Portugal", "PT01", "PC-CORPORATE"),
    ]
    return pd.DataFrame(rows, columns=["cost_center", "cost_center_name", "company_code", "profit_center"])


def parent_of_account(gl_account: str) -> str:
    if gl_account.startswith("41"):
        return "REVENUE"
    elif gl_account.startswith("51"):
        return "COGS"
    else:
        return "OPEX"


def build_pl_hierarchy() -> pd.DataFrame:
    """Parent-child P&L structure: 5 structure nodes + 12 P&L accounts (leaves)."""
    columns = ["node_id", "parent_node_id", "node_name", "sort_order"]

    # Step 1: structure nodes, written by hand
    structure = pd.DataFrame(
        [
            ("EBIT", None, "EBIT", 1),
            ("GROSS_MARGIN", "EBIT", "Gross margin", 1),
            ("REVENUE", "GROSS_MARGIN", "Revenue", 1),
            ("COGS", "GROSS_MARGIN", "Cost of goods sold", 2),
            ("OPEX", "EBIT", "Operating expenses", 2)
        ],
        columns=columns,
    )

    # Step 2: account leaves, derived from the gl_account table
    accounts = build_gl_account()
    pl_accounts = accounts[accounts["account_type"] == "P&L"]  # WHERE
    leaves = pd.DataFrame({
        "node_id": pl_accounts["gl_account"],
        "parent_node_id": pl_accounts["gl_account"].map(parent_of_account),  # CASE WHEN
        "node_name": pl_accounts["account_name"],
    })
    # ROW_NUMBER() OVER (PARTITION BY parent_node_id)
    leaves["sort_order"] = leaves.groupby("parent_node_id").cumcount() + 1

    # Step 3: UNION ALL
    return pd.concat([structure, leaves], ignore_index=True)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    builders = {
        "profit_center": build_profit_center,
        "company": build_company,
        "gl_account": build_gl_account,
        "cost_center": build_cost_center,
        "pl_hierarchy": build_pl_hierarchy,
    }

    for table_name, build in builders.items():
        try:
            df = build()
        except NotImplementedError:
            print(f"{table_name:<15} skipped (TODO)")
            continue
        df.to_csv(OUTPUT_DIR / f"{table_name}.csv", index=False)
        print(f"{table_name:<15} {len(df):>3} rows")


if __name__ == "__main__":
    main()
