import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from ledger_backend import LedgerBackend
from ledger_parser import parse_order_text

PRIMARY_BG = "#f3f6fa"
CARD_BG = "#ffffff"


class DriedFruitLedgerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.backend = LedgerBackend()
        self.root = root
        self.root.title("Dried Fruit Ledger")
        self.root.geometry("1380x770")
        self.root.configure(bg=PRIMARY_BG)

        self._create_styles()
        self._create_widgets()
        self._load_ledger()
        self._load_products()
        self._log("Application ready. Enter order text and click Process Order.")

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
        left_panel.configure(width=420)
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
            "   - Single line: Name, Address, Code/SKU, Qty, Price\n"
            "   - Multi-line blocks ending with: Code/SKU, Qty, Price\n"
            "3) Click Process Order.\n"
            "4) Live Ledger updates instantly.\n"
            "5) Set product SKU and weight in Product Management.\n"
            "6) Use Reset Input to clear the text box."
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
            "MUS1001, 5, 250EUR\n\n"
            "You can use SKU too (example):\n"
            "MUSH-BTN-001, 5, 250EUR"
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
            height=9,
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

        export_btn = tk.Button(
            panel,
            text="Export CSV Snapshot",
            command=self.export_csv_snapshot,
            bg="#495d73",
            fg="white",
            activebackground="#344557",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        export_btn.pack(fill=tk.X, padx=14, pady=(0, 10))

        product_title = tk.Label(
            panel,
            text="Product Management (Code + SKU + Weight)",
            bg=CARD_BG,
            font=("Segoe UI", 10, "bold"),
            padx=14,
        )
        product_title.pack(anchor="w")

        form = tk.Frame(panel, bg=CARD_BG)
        form.pack(fill=tk.X, padx=14, pady=(6, 10))

        tk.Label(form, text="Code", bg=CARD_BG, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        self.product_code_var = tk.StringVar()
        tk.Entry(form, textvariable=self.product_code_var, width=12).grid(row=1, column=0, padx=(0, 6), pady=(2, 6))

        tk.Label(form, text="SKU", bg=CARD_BG, font=("Segoe UI", 9)).grid(row=0, column=1, sticky="w")
        self.product_sku_var = tk.StringVar()
        tk.Entry(form, textvariable=self.product_sku_var, width=14).grid(row=1, column=1, padx=(0, 6), pady=(2, 6))

        tk.Label(form, text="Weight kg", bg=CARD_BG, font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w")
        self.product_weight_var = tk.StringVar(value="1.000")
        tk.Entry(form, textvariable=self.product_weight_var, width=10).grid(
            row=1, column=2, padx=(0, 6), pady=(2, 6)
        )

        tk.Label(form, text="Unit Cost", bg=CARD_BG, font=("Segoe UI", 9)).grid(row=0, column=3, sticky="w")
        self.product_cost_var = tk.StringVar()
        tk.Entry(form, textvariable=self.product_cost_var, width=10).grid(row=1, column=3, pady=(2, 6))

        tk.Label(form, text="Product Name", bg=CARD_BG, font=("Segoe UI", 9)).grid(
            row=2, column=0, sticky="w", pady=(2, 0)
        )
        self.product_name_var = tk.StringVar()
        tk.Entry(form, textvariable=self.product_name_var, width=42).grid(
            row=3, column=0, columnspan=3, sticky="we", pady=(2, 2), padx=(0, 6)
        )
        save_product_btn = tk.Button(
            form,
            text="Save Product",
            command=self.save_product,
            bg="#5a3ec8",
            fg="white",
            activebackground="#432ea0",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=8,
            pady=5,
        )
        save_product_btn.grid(row=3, column=3, sticky="we", pady=(2, 2))

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
            height=6,
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
            text="Live Ledger (Latest 150 Orders)",
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

        columns = (
            "Date",
            "Name",
            "Address",
            "Code",
            "SKU",
            "Product",
            "Qty",
            "UnitWtKg",
            "TotalWtKg",
            "Cost",
            "Revenue",
            "Profit",
        )
        self.ledger_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Ledger.Treeview")

        widths = {
            "Date": 130,
            "Name": 120,
            "Address": 210,
            "Code": 80,
            "SKU": 110,
            "Product": 150,
            "Qty": 48,
            "UnitWtKg": 78,
            "TotalWtKg": 82,
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
            text="Product Catalog (Code | SKU | Weight kg | Cost)",
            bg="#f7f9fc",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8,
        )
        catalog_title.pack(anchor="w")

        catalog_table_frame = tk.Frame(catalog_frame, bg="#f7f9fc")
        catalog_table_frame.pack(fill=tk.X, padx=10, pady=(0, 8))

        catalog_cols = ("Code", "SKU", "Name", "WtKg", "Cost")
        self.catalog_tree = ttk.Treeview(catalog_table_frame, columns=catalog_cols, show="headings", height=6)
        for col in catalog_cols:
            self.catalog_tree.heading(col, text=col)
        self.catalog_tree.column("Code", width=80, stretch=False)
        self.catalog_tree.column("SKU", width=100, stretch=False)
        self.catalog_tree.column("Name", width=190, stretch=False)
        self.catalog_tree.column("WtKg", width=64, stretch=False)
        self.catalog_tree.column("Cost", width=60, stretch=False)

        catalog_scroll = ttk.Scrollbar(catalog_table_frame, orient=tk.VERTICAL, command=self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand=catalog_scroll.set)
        self.catalog_tree.grid(row=0, column=0, sticky="nsew")
        catalog_scroll.grid(row=0, column=1, sticky="ns")
        catalog_table_frame.grid_columnconfigure(0, weight=1)

    def reset_input(self) -> None:
        self.input_box.delete("1.0", tk.END)
        self._log("Input cleared.")

    def _log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_box.configure(state=tk.NORMAL)
        self.status_box.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_box.see(tk.END)
        self.status_box.configure(state=tk.DISABLED)

    def process_order(self) -> None:
        raw_data = self.input_box.get("1.0", tk.END).strip()
        if not raw_data:
            messagebox.showwarning("Input Required", "Paste an order before processing.")
            return

        try:
            parsed = parse_order_text(raw_data)
            saved = self.backend.create_order(
                customer_name=parsed.customer_name,
                address=parsed.address,
                code_or_sku=parsed.code_or_sku,
                quantity=parsed.quantity,
                unit_price=parsed.unit_price,
            )
            self.backend.export_orders_csv("ledger_data.csv")

            self._log(
                "Saved order for "
                f"{saved['name']} | {saved['code']} / {saved['sku']} ({saved['qty']} units) | "
                f"Revenue {saved['revenue']:.2f} | Profit {saved['profit']:.2f}"
            )
            self._load_ledger()
            messagebox.showinfo(
                "Order Processed",
                "Product: "
                f"{saved['product']}\n"
                f"SKU: {saved['sku']}\n"
                f"Total Weight: {saved['total_weight_kg']:.3f} kg\n"
                f"Total Revenue: {saved['revenue']:.2f}\n"
                f"Total Profit: {saved['profit']:.2f}",
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

        rows = self.backend.list_recent_orders(limit=150)
        for row in rows:
            profit_value = float(row["profit"])
            tag = "positive" if profit_value >= 0 else "negative"
            self.ledger_tree.insert(
                "",
                tk.END,
                values=(
                    row["order_date"],
                    row["customer_name"],
                    row["address"],
                    row["product_code"],
                    row["sku"],
                    row["product_name"],
                    row["quantity"],
                    f'{float(row["unit_weight_kg"]):.3f}',
                    f'{float(row["total_weight_kg"]):.3f}',
                    f'{float(row["total_cost"]):.2f}',
                    f'{float(row["total_revenue"]):.2f}',
                    f'{float(row["profit"]):.2f}',
                ),
                tags=(tag,),
            )

    def _load_products(self) -> None:
        for item in self.catalog_tree.get_children():
            self.catalog_tree.delete(item)

        for product in self.backend.get_products():
            self.catalog_tree.insert(
                "",
                tk.END,
                values=(
                    product.code,
                    product.sku,
                    product.name,
                    f"{product.unit_weight_kg:.3f}",
                    f"{product.unit_cost:.2f}",
                ),
            )

    def save_product(self) -> None:
        try:
            code = self.product_code_var.get()
            sku = self.product_sku_var.get()
            name = self.product_name_var.get()
            unit_cost = float(self.product_cost_var.get())
            unit_weight_kg = float(self.product_weight_var.get())
            product = self.backend.upsert_product(
                code=code, sku=sku, name=name, unit_cost=unit_cost, unit_weight_kg=unit_weight_kg
            )
            self._load_products()
            self._log(
                f"Saved product {product.code} / {product.sku} | {product.name} | "
                f"Weight {product.unit_weight_kg:.3f} kg | Cost {product.unit_cost:.2f}"
            )
            messagebox.showinfo("Product Saved", f"{product.code} / {product.sku} updated successfully.")
        except ValueError as exc:
            self._log(f"Product validation error: {exc}")
            messagebox.showerror("Invalid Product", str(exc))
        except Exception as exc:
            self._log(f"Unexpected product save error: {exc}")
            messagebox.showerror("Error", f"Could not save product.\n{exc}")

    def export_csv_snapshot(self) -> None:
        try:
            path = self.backend.export_orders_csv("ledger_data.csv")
            self._log(f"Exported CSV snapshot to {path}")
            messagebox.showinfo("CSV Exported", f"Ledger snapshot exported:\n{path}")
        except Exception as exc:
            self._log(f"CSV export failed: {exc}")
            messagebox.showerror("Export Failed", f"Could not export CSV.\n{exc}")

    def view_weekly_report(self) -> None:
        totals = self.backend.weekly_totals(days=7)
        total_revenue = totals["total_revenue"]
        total_profit = totals["total_profit"]
        order_count = totals["order_count"]

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
