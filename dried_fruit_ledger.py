import csv
import os
import re
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

PRODUCT_CATALOG = {
    "VIL1001": ("Dried Carrot Slices", 0.35),
    "VIL2001": ("Dried Potato Cubes", 0.20),
    "VIL3001": ("Dried Onion Flakes", 0.35),
    "VIL4001": ("Dried Tomato Pieces", 0.35),
    "VIL5001": ("Dried Bell Pepper Mix", 0.35),
    "VIL6001": ("Dried Sweet Corn Kernels", 0.35),
    "MUS1001": ("Dried Button Mushrooms", 3.00),
    "MUS2001": ("Dried Shiitake", 25.00),
    "MUS3001": ("Dried Oyster", 4.00),
    "MUS4001": ("Dried Porcini", 35.00),
    "MUS5001": ("Mixed Wild", 5.00),
    "CAN1001": ("Dried Apple Slices", 5.00),
    "CAN5001": ("Dried Pineapple Rings", 4.00),
    "CAN6001": ("Dried Mango Strips", 20.00),
    "HER1001": ("Dried Basil", 4.00),
    "HER2001": ("Dried Oregano", 1.20),
    "HER3001": ("Dried Thyme", 3.50),
    "HER4001": ("Dried Rosemary", 1.20),
    "HER5001": ("Dried Parsley", 10.00),
    "HER6001": ("Dried Dill", 7.00),
    "HER7001": ("Dried Mint", 1.50),
}

CSV_FILE = "ledger_data.csv"
HEADERS = ["Date", "Name", "Address", "Code", "Product", "Qty", "Cost", "Revenue", "Profit"]
PRIMARY_BG = "#f3f6fa"
CARD_BG = "#ffffff"


class DriedFruitLedgerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Dried Fruit Ledger")
        self.root.geometry("1180x730")
        self.root.configure(bg=PRIMARY_BG)

        self._init_csv()
        self._create_styles()
        self._create_widgets()
        self._load_ledger()
        self._log("Application ready. Enter order text and click Process Order.")

    def _init_csv(self) -> None:
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(HEADERS)

    def _create_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Ledger.Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Ledger.Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Positive.Treeview", foreground="#0f8a3e")
        style.configure("Negative.Treeview", foreground="#b32020")

    def _create_widgets(self) -> None:
        app_frame = tk.Frame(self.root, bg=PRIMARY_BG)
        app_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        left_panel = tk.Frame(app_frame, bg=CARD_BG, bd=1, relief=tk.SOLID)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        left_panel.configure(width=390)
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(app_frame, bg=CARD_BG, bd=1, relief=tk.SOLID)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_left_panel(left_panel)
        self._build_right_panel(right_panel)

    def _build_left_panel(self, panel: tk.Frame) -> None:
        title = tk.Label(
            panel,
            text="Dried Fruit Ledger",
            bg=CARD_BG,
            font=("Segoe UI", 17, "bold"),
            padx=14,
            pady=14,
        )
        title.pack(anchor="w")

        instructions_title = tk.Label(
            panel,
            text="Quick Start Instructions",
            bg=CARD_BG,
            font=("Segoe UI", 11, "bold"),
            padx=14,
        )
        instructions_title.pack(anchor="w", pady=(0, 4))

        instructions = (
            "1) Paste order details into the box below.\n"
            "2) Supported formats:\n"
            "   - Single line: Name, Address, Code, Qty, Price\n"
            "   - Multi-line blocks ending with: Code, Qty, Price (EUR/GBP/$ accepted)\n"
            "3) Click Process Order.\n"
            "4) Live Ledger updates instantly.\n"
            "5) Use Reset Input to clear the text box."
        )
        instructions_lbl = tk.Label(
            panel,
            text=instructions,
            bg=CARD_BG,
            fg="#333333",
            justify=tk.LEFT,
            font=("Segoe UI", 9),
            padx=14,
        )
        instructions_lbl.pack(anchor="w")

        format_hint = (
            "Example block:\n"
            "Elva Nic Phadin\n"
            "37 Garryowen Rd\n"
            "Dublin 10\n"
            "D10 TP28\n"
            "MUS1001, 5, 250EUR"
        )
        hint_lbl = tk.Label(
            panel,
            text=format_hint,
            bg="#f7f9fc",
            justify=tk.LEFT,
            font=("Consolas", 9),
            padx=10,
            pady=8,
        )
        hint_lbl.pack(fill=tk.X, padx=14, pady=(10, 8))

        input_label = tk.Label(
            panel,
            text="Paste Order Text",
            bg=CARD_BG,
            font=("Segoe UI", 10, "bold"),
            padx=14,
        )
        input_label.pack(anchor="w")

        self.input_box = tk.Text(
            panel,
            height=13,
            wrap=tk.WORD,
            font=("Consolas", 10),
            relief=tk.SOLID,
            bd=1,
        )
        self.input_box.pack(fill=tk.X, padx=14, pady=(6, 10))

        buttons_frame = tk.Frame(panel, bg=CARD_BG)
        buttons_frame.pack(fill=tk.X, padx=14, pady=(0, 8))

        process_btn = tk.Button(
            buttons_frame,
            text="Process Order",
            command=self.process_order,
            bg="#1f8f5f",
            fg="white",
            activebackground="#18724c",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=7,
        )
        process_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        reset_btn = tk.Button(
            buttons_frame,
            text="Reset Input",
            command=self.reset_input,
            bg="#e2852d",
            fg="white",
            activebackground="#c96f1b",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=7,
        )
        reset_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        report_btn = tk.Button(
            panel,
            text="View Weekly Report",
            command=self.view_weekly_report,
            bg="#2b6ed2",
            fg="white",
            activebackground="#1e55a7",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        report_btn.pack(fill=tk.X, padx=14, pady=(2, 10))

        log_title = tk.Label(
            panel,
            text="Status",
            bg=CARD_BG,
            font=("Segoe UI", 10, "bold"),
            padx=14,
        )
        log_title.pack(anchor="w")

        self.status_box = tk.Text(
            panel,
            height=8,
            wrap=tk.WORD,
            bg="#171a21",
            fg="#9ef2b1",
            insertbackground="#9ef2b1",
            font=("Consolas", 9),
            relief=tk.SOLID,
            bd=1,
        )
        self.status_box.pack(fill=tk.BOTH, expand=True, padx=14, pady=(6, 14))
        self.status_box.configure(state=tk.DISABLED)

    def _build_right_panel(self, panel: tk.Frame) -> None:
        top = tk.Frame(panel, bg=CARD_BG)
        top.pack(fill=tk.X, padx=14, pady=(12, 6))

        ledger_title = tk.Label(
            top,
            text="Live Ledger (Latest 100 Orders)",
            bg=CARD_BG,
            font=("Segoe UI", 13, "bold"),
        )
        ledger_title.pack(side=tk.LEFT)

        refresh_btn = tk.Button(
            top,
            text="Refresh",
            command=self._load_ledger,
            bg="#dce4ef",
            fg="#222222",
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=10,
        )
        refresh_btn.pack(side=tk.RIGHT)

        table_frame = tk.Frame(panel, bg=CARD_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(4, 14))

        columns = ("Date", "Name", "Address", "Code", "Product", "Qty", "Cost", "Revenue", "Profit")
        self.ledger_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Ledger.Treeview")

        widths = {
            "Date": 130,
            "Name": 120,
            "Address": 180,
            "Code": 78,
            "Product": 170,
            "Qty": 48,
            "Cost": 70,
            "Revenue": 78,
            "Profit": 70,
        }
        for col in columns:
            self.ledger_tree.heading(col, text=col)
            anchor = tk.CENTER if col in {"Qty", "Code"} else tk.W
            self.ledger_tree.column(col, width=widths[col], anchor=anchor, stretch=False)

        self.ledger_tree.tag_configure("positive", foreground="#0f8a3e")
        self.ledger_tree.tag_configure("negative", foreground="#b32020")

        y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.ledger_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.ledger_tree.xview)
        self.ledger_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.ledger_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        catalog_frame = tk.Frame(panel, bg="#f7f9fc", bd=1, relief=tk.SOLID)
        catalog_frame.pack(fill=tk.X, padx=14, pady=(0, 14))

        catalog_title = tk.Label(
            catalog_frame,
            text="Product Catalog (Cost per Unit)",
            bg="#f7f9fc",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8,
        )
        catalog_title.pack(anchor="w")

        catalog_text = tk.Text(
            catalog_frame,
            height=6,
            wrap=tk.NONE,
            font=("Consolas", 9),
            bg="#f7f9fc",
            relief=tk.FLAT,
        )
        catalog_text.pack(fill=tk.X, padx=10, pady=(0, 8))
        for code, (name, cost) in PRODUCT_CATALOG.items():
            catalog_text.insert(tk.END, f"{code:<8}  {name:<28}  {cost:>5.2f}\n")
        catalog_text.configure(state=tk.DISABLED)

    def reset_input(self) -> None:
        self.input_box.delete("1.0", tk.END)
        self._log("Input cleared.")

    def _log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_box.configure(state=tk.NORMAL)
        self.status_box.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_box.see(tk.END)
        self.status_box.configure(state=tk.DISABLED)

    @staticmethod
    def _parse_money(value: str) -> float:
        cleaned = value.strip().upper().replace(",", "")
        cleaned = re.sub(r"(EUR|GBP|USD|€|\$|£)$", "", cleaned).strip()
        return float(cleaned)

    @staticmethod
    def _normalize_lines(raw_data: str) -> list[str]:
        lines = [line.strip() for line in raw_data.splitlines()]
        return [line for line in lines if line]

    def _parse_order(self, raw_data: str) -> tuple[str, str, str, int, float]:
        lines = self._normalize_lines(raw_data)
        if not lines:
            raise ValueError("No input provided.")

        if len(lines) == 1 and lines[0].count(",") >= 4:
            parts = [part.strip() for part in lines[0].split(",")]
            if len(parts) != 5:
                raise ValueError("Single-line format must be: Name, Address, Code, Qty, Price")
            name, address, code, qty_raw, price_raw = parts
            qty = int(qty_raw)
            price = self._parse_money(price_raw)
            return name, address, code.upper(), qty, price

        trailing_line = lines[-1]
        trailing_parts = [part.strip() for part in trailing_line.split(",")]
        if len(trailing_parts) != 3:
            raise ValueError(
                "Multi-line format must end with: Code, Qty, Price (example: MUS1001, 5, 250EUR)"
            )
        code, qty_raw, price_raw = trailing_parts
        code = code.upper()
        qty = int(qty_raw)
        price = self._parse_money(price_raw)

        if len(lines) < 2:
            raise ValueError("Multi-line format requires at least a name line before code/qty/price line.")
        name = lines[0]
        address = " ".join(lines[1:-1]).strip()
        if not address:
            raise ValueError("Address is required.")

        return name, address, code, qty, price

    def process_order(self) -> None:
        raw_data = self.input_box.get("1.0", tk.END).strip()
        if not raw_data:
            messagebox.showwarning("Input Required", "Paste an order before processing.")
            return

        try:
            name, address, code, qty, retail_unit_price = self._parse_order(raw_data)

            if qty <= 0:
                raise ValueError("Quantity must be greater than zero.")
            if retail_unit_price < 0:
                raise ValueError("Retail price cannot be negative.")
            if code not in PRODUCT_CATALOG:
                raise ValueError(f"Unknown product code: {code}")

            product_name, unit_cost = PRODUCT_CATALOG[code]
            total_cost = unit_cost * qty
            total_revenue = retail_unit_price * qty
            profit = total_revenue - total_cost

            order_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        order_date,
                        name,
                        address,
                        code,
                        product_name,
                        qty,
                        f"{total_cost:.2f}",
                        f"{total_revenue:.2f}",
                        f"{profit:.2f}",
                    ]
                )

            self._log(
                f"Saved order for {name} | {code} ({qty} units) | Revenue {total_revenue:.2f} | Profit {profit:.2f}"
            )
            self._load_ledger()
            messagebox.showinfo(
                "Order Processed",
                f"Product: {product_name}\nTotal Revenue: {total_revenue:.2f}\nTotal Profit: {profit:.2f}",
            )
        except ValueError as exc:
            self._log(f"Validation error: {exc}")
            messagebox.showerror("Invalid Order", str(exc))
        except Exception as exc:
            self._log(f"Unexpected error: {exc}")
            messagebox.showerror("Error", f"Could not process order.\n{exc}")

    def _load_ledger(self) -> None:
        for item in self.ledger_tree.get_children():
            self.ledger_tree.delete(item)

        try:
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
        except FileNotFoundError:
            rows = []

        for row in rows[-100:][::-1]:
            profit_value = float(row["Profit"])
            tag = "positive" if profit_value >= 0 else "negative"
            self.ledger_tree.insert(
                "",
                tk.END,
                values=(
                    row["Date"],
                    row["Name"],
                    row["Address"],
                    row["Code"],
                    row["Product"],
                    row["Qty"],
                    row["Cost"],
                    row["Revenue"],
                    row["Profit"],
                ),
                tags=(tag,),
            )

    def view_weekly_report(self) -> None:
        seven_days_ago = datetime.now() - timedelta(days=7)
        total_revenue = 0.0
        total_profit = 0.0
        order_count = 0

        try:
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order_date = datetime.strptime(row["Date"], "%Y-%m-%d %H:%M")
                    if order_date >= seven_days_ago:
                        order_count += 1
                        total_revenue += float(row["Revenue"])
                        total_profit += float(row["Profit"])
        except FileNotFoundError:
            pass

        report = tk.Toplevel(self.root)
        report.title("Weekly Report (Last 7 Days)")
        report.geometry("420x260")
        report.configure(bg=CARD_BG)
        report.transient(self.root)
        report.grab_set()

        tk.Label(
            report,
            text="Weekly Ledger Report",
            bg=CARD_BG,
            font=("Segoe UI", 14, "bold"),
            pady=14,
        ).pack()

        details = tk.Frame(report, bg=CARD_BG)
        details.pack(fill=tk.X, padx=28, pady=4)
        tk.Label(details, text=f"Orders processed: {order_count}", bg=CARD_BG, font=("Segoe UI", 11)).pack(
            anchor="w", pady=2
        )
        tk.Label(details, text=f"Total revenue: {total_revenue:.2f}", bg=CARD_BG, font=("Segoe UI", 11)).pack(
            anchor="w", pady=2
        )

        profit_color = "#0f8a3e" if total_profit >= 0 else "#b32020"
        tk.Label(
            details,
            text=f"Total profit: {total_profit:.2f}",
            bg=CARD_BG,
            fg=profit_color,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=2)

        tk.Button(
            report,
            text="Close",
            command=report.destroy,
            bg="#dce4ef",
            relief=tk.FLAT,
            padx=14,
            pady=7,
        ).pack(pady=16)


def main() -> None:
    root = tk.Tk()
    app = DriedFruitLedgerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
