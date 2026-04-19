# Dried Fruit Ledger - Instruction Manual

This desktop app tracks dried fruit orders locally using Tkinter and CSV storage.

## 1) What this app does

- Stores orders in `ledger_data.csv` (offline/local only)
- Calculates **Cost**, **Revenue**, and **Profit** automatically from product code + quantity + retail price
- Shows a **Live Ledger** table in real time
- Provides a **Weekly Report** (last 7 days)

No internet connection is required.

---

## 2) Product catalog

The app has a built-in catalog keyed by code:

- VIL1001, VIL2001, VIL3001, VIL4001, VIL5001, VIL6001
- MUS1001, MUS2001, MUS3001, MUS4001, MUS5001
- CAN1001, CAN5001, CAN6001
- HER1001, HER2001, HER3001, HER4001, HER5001, HER6001, HER7001

The right side of the app shows each code and cost per unit.

---

## 3) Input formats supported

### A) Single-line format

```text
Name, Address, Code, Qty, Price
```

Example:

```text
Jane Doe, 12 Oak Lane, MUS2001, 3, 35
```

### B) Multi-line block format (for real-world pasted orders)

Use this when name/address come on separate lines and the last line is:

```text
Code, Qty, Price
```

Example:

```text
Elva Nic Phadin
37 Garryowen Rd
Dublin 10
D10 TP28
MUS1001, 5, 250EUR
```

Notes:

- Currency suffixes are accepted at the end of price (`EUR`, `GBP`, `USD`, `€`, `$`, `£`)
- Quantity must be a whole number
- Code is case-insensitive in input (it is normalized to uppercase)

---

## 4) Buttons and interface

- **Process Order**: parses input, validates data, saves to CSV, and updates the live ledger
- **Reset Input**: clears the input text box
- **View Weekly Report**: opens totals for the last 7 days
- **Refresh**: reloads the live ledger from disk

Status messages appear in the **Status** panel on the left.

---

## 5) CSV data storage

Orders are saved in `ledger_data.csv` in the same directory as the script.

If the file does not exist, it is created at startup with headers:

`Date, Name, Address, Code, Product, Qty, Cost, Revenue, Profit`

---

## 6) Running the app

From the folder containing `dried_fruit_ledger.py`:

```bash
python3 dried_fruit_ledger.py
```

If your system uses `python` instead:

```bash
python dried_fruit_ledger.py
```

---

## 7) Troubleshooting

- **Unknown product code**
  - Check code spelling against the product list.
- **Invalid format**
  - Use one of the two supported input formats exactly.
- **CSV open in another app**
  - Close Excel/Sheets if file-lock issues occur, then try again.
- **Tkinter missing**
  - Install a Python build that includes Tk support.

