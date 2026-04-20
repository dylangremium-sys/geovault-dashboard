# Dried Fruit Ledger - Instruction Manual

This desktop app tracks dried-fruit orders with a local backend:

- **SQLite database** (`ledger.db`) for products and orders
- **CSV export snapshot** (`ledger_data.csv`) for spreadsheet compatibility
- Tkinter desktop interface (offline only, no internet/API required)

---

## 1) What this app does

- Stores products and orders locally in `ledger.db`
- Lets you manage product **Code + SKU + Weight + Cost + Name**
- Accepts orders by either **Code** or **SKU**
- Automatically calculates:
  - total weight
  - total cost
  - total revenue
  - profit
- Shows a **Live Ledger** table in real time
- Provides a **Weekly Report** (last 7 days)
- Exports all orders to `ledger_data.csv` on demand (and after order save)

---

## 2) Data model and backend

### Products

Each product has:

- `code` (unique)
- `sku` (unique)
- `name`
- `unit_cost`
- `unit_weight_kg`

### Orders

Each order stores:

- `order_date`
- `customer_name`
- `address`
- `product_code`
- `sku`
- `product_name`
- `quantity`
- `unit_weight_kg`
- `total_weight_kg`
- `total_cost`
- `total_revenue`
- `profit`

The database file is created automatically at first run.

---

## 3) Default preloaded products

The app preloads the full catalog:

- VIL1001, VIL2001, VIL3001, VIL4001, VIL5001, VIL6001
- MUS1001, MUS2001, MUS3001, MUS4001, MUS5001
- CAN1001, CAN5001, CAN6001
- HER1001, HER2001, HER3001, HER4001, HER5001, HER6001, HER7001

Defaults:

- `sku` initially matches `code`
- `unit_weight_kg` initially `1.000`
- You should update SKU/weight in Product Management to your real values

---

## 4) Input formats supported

### A) Single-line format

```text
Name, Address, CodeOrSKU, Qty, Price
```

Example:

```text
Jane Doe, 12 Oak Lane, MUS2001, 3, 35
```

### B) Multi-line block format

Use this when name/address come on separate lines and the last line is:

```text
CodeOrSKU, Qty, Price
```

Example:

```text
Elva Nic Phadin
37 Garryowen Rd
Dublin 10
D10 TP28
MUS1001, 5, 250EUR
```

You can also use SKU in the last line:

```text
MUSH-BTN-001, 5, 250EUR
```

Notes:

- Currency suffixes accepted at end of price: `EUR`, `GBP`, `USD`, `€`, `$`, `£`
- Quantity must be a whole number > 0
- Code/SKU matching is case-insensitive in input

---

## 5) Buttons and interface

- **Process Order**
  - Parses input
  - Resolves product by code or SKU
  - Saves order to SQLite
  - Refreshes live ledger
  - Exports CSV snapshot
- **Reset Input**
  - Clears the order text box
- **View Weekly Report**
  - Shows order count, total revenue, total profit (last 7 days)
- **Export CSV Snapshot**
  - Writes all orders to `ledger_data.csv`
- **Refresh**
  - Reloads live ledger from the database
- **Save Product** (Product Management section)
  - Creates or updates product code/SKU/weight/cost/name

Status messages appear in the **Status** panel on the left.

---

## 6) CSV export format

`ledger_data.csv` headers:

`Date, Name, Address, Code, SKU, Product, Qty, UnitWeightKg, TotalWeightKg, Cost, Revenue, Profit`

This file is a spreadsheet-friendly export of your backend data.

---

## 7) Running the app

From the folder containing `dried_fruit_ledger.py`:

```bash
python3 dried_fruit_ledger.py
```

If your system uses `python` instead:

```bash
python dried_fruit_ledger.py
```

---

## 8) First-time setup workflow (recommended)

1. Open app
2. Use **Product Management** to set:
   - true SKU values
   - true unit weight (kg)
   - current cost
3. Save each product
4. Start processing orders by Code or SKU

---

## 9) Troubleshooting

- **Unknown product code/SKU**
  - Add/update it in Product Management first.
- **Invalid format**
  - Use one of the two supported input formats exactly.
- **CSV open in another app**
  - Close Excel/Sheets if file-lock issues occur, then export again.
- **Tkinter missing**
  - Install a Python build that includes Tk support.

