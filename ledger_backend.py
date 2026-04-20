import csv
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

DB_FILE = "ledger.db"

DEFAULT_PRODUCTS: dict[str, tuple[str, float]] = {
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

CSV_HEADERS = [
    "Date",
    "Name",
    "Address",
    "Code",
    "SKU",
    "Product",
    "Qty",
    "UnitWeightKg",
    "TotalWeightKg",
    "Cost",
    "Revenue",
    "Profit",
]


@dataclass(slots=True)
class Product:
    code: str
    sku: str
    name: str
    unit_cost: float
    unit_weight_kg: float


class LedgerBackend:
    def __init__(self, db_path: str = DB_FILE) -> None:
        self.db_path = Path(db_path)
        self._init_db()
        self._seed_default_products()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL UNIQUE,
                    sku TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    unit_cost REAL NOT NULL CHECK(unit_cost >= 0),
                    unit_weight_kg REAL NOT NULL CHECK(unit_weight_kg > 0),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_date TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    product_code TEXT NOT NULL,
                    sku TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    unit_weight_kg REAL NOT NULL,
                    total_weight_kg REAL NOT NULL,
                    unit_cost REAL NOT NULL,
                    total_cost REAL NOT NULL,
                    unit_price REAL NOT NULL,
                    total_revenue REAL NOT NULL,
                    profit REAL NOT NULL,
                    FOREIGN KEY (product_code) REFERENCES products(code)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_orders_order_date
                ON orders(order_date)
                """
            )

    def _seed_default_products(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as connection:
            for code, (name, unit_cost) in DEFAULT_PRODUCTS.items():
                connection.execute(
                    """
                    INSERT INTO products (code, sku, name, unit_cost, unit_weight_kg, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(code) DO UPDATE SET
                        name = excluded.name,
                        unit_cost = excluded.unit_cost,
                        updated_at = excluded.updated_at
                    """,
                    (code, code, name, float(unit_cost), 1.0, now, now),
                )

    @staticmethod
    def _validate_product_inputs(code: str, sku: str, name: str, unit_cost: float, unit_weight_kg: float) -> None:
        if not code.strip():
            raise ValueError("Product code is required.")
        if not sku.strip():
            raise ValueError("SKU is required.")
        if not name.strip():
            raise ValueError("Product name is required.")
        if unit_cost < 0:
            raise ValueError("Unit cost cannot be negative.")
        if unit_weight_kg <= 0:
            raise ValueError("Weight must be greater than zero.")

    def upsert_product(self, code: str, sku: str, name: str, unit_cost: float, unit_weight_kg: float) -> Product:
        code = code.strip().upper()
        sku = sku.strip().upper()
        name = name.strip()
        unit_cost = float(unit_cost)
        unit_weight_kg = float(unit_weight_kg)
        self._validate_product_inputs(code, sku, name, unit_cost, unit_weight_kg)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO products (code, sku, name, unit_cost, unit_weight_kg, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(code) DO UPDATE SET
                    sku = excluded.sku,
                    name = excluded.name,
                    unit_cost = excluded.unit_cost,
                    unit_weight_kg = excluded.unit_weight_kg,
                    updated_at = excluded.updated_at
                """,
                (code, sku, name, unit_cost, unit_weight_kg, now, now),
            )

        return Product(code=code, sku=sku, name=name, unit_cost=unit_cost, unit_weight_kg=unit_weight_kg)

    def get_products(self) -> list[Product]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT code, sku, name, unit_cost, unit_weight_kg
                FROM products
                ORDER BY code ASC
                """
            ).fetchall()
        return [
            Product(
                code=row["code"],
                sku=row["sku"],
                name=row["name"],
                unit_cost=float(row["unit_cost"]),
                unit_weight_kg=float(row["unit_weight_kg"]),
            )
            for row in rows
        ]

    def get_product_by_code_or_sku(self, identifier: str) -> Product | None:
        normalized = identifier.strip().upper()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT code, sku, name, unit_cost, unit_weight_kg
                FROM products
                WHERE code = ? OR sku = ?
                LIMIT 1
                """,
                (normalized, normalized),
            ).fetchone()
        if not row:
            return None
        return Product(
            code=row["code"],
            sku=row["sku"],
            name=row["name"],
            unit_cost=float(row["unit_cost"]),
            unit_weight_kg=float(row["unit_weight_kg"]),
        )

    def create_order(
        self,
        customer_name: str,
        address: str,
        code_or_sku: str,
        quantity: int,
        unit_price: float,
    ) -> dict[str, Any]:
        customer_name = customer_name.strip()
        address = address.strip()
        if not customer_name:
            raise ValueError("Customer name is required.")
        if not address:
            raise ValueError("Address is required.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        product = self.get_product_by_code_or_sku(code_or_sku)
        if product is None:
            raise ValueError(f"Unknown product code/SKU: {code_or_sku}")

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        total_weight_kg = product.unit_weight_kg * quantity
        total_cost = product.unit_cost * quantity
        total_revenue = unit_price * quantity
        profit = total_revenue - total_cost

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO orders (
                    order_date, customer_name, address, product_code, sku, product_name, quantity,
                    unit_weight_kg, total_weight_kg, unit_cost, total_cost, unit_price, total_revenue, profit
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order_date,
                    customer_name,
                    address,
                    product.code,
                    product.sku,
                    product.name,
                    quantity,
                    round(product.unit_weight_kg, 3),
                    round(total_weight_kg, 3),
                    round(product.unit_cost, 2),
                    round(total_cost, 2),
                    round(unit_price, 2),
                    round(total_revenue, 2),
                    round(profit, 2),
                ),
            )

        return {
            "date": order_date,
            "name": customer_name,
            "address": address,
            "code": product.code,
            "sku": product.sku,
            "product": product.name,
            "qty": quantity,
            "unit_weight_kg": round(product.unit_weight_kg, 3),
            "total_weight_kg": round(total_weight_kg, 3),
            "cost": round(total_cost, 2),
            "revenue": round(total_revenue, 2),
            "profit": round(profit, 2),
        }

    def list_recent_orders(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT order_date, customer_name, address, product_code, sku, product_name, quantity,
                       unit_weight_kg, total_weight_kg, total_cost, total_revenue, profit
                FROM orders
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def weekly_totals(self, days: int = 7) -> dict[str, Any]:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS order_count,
                       COALESCE(SUM(total_revenue), 0) AS total_revenue,
                       COALESCE(SUM(profit), 0) AS total_profit
                FROM orders
                WHERE order_date >= ?
                """,
                (since,),
            ).fetchone()
        return {
            "order_count": int(row["order_count"]),
            "total_revenue": float(row["total_revenue"]),
            "total_profit": float(row["total_profit"]),
        }

    def export_orders_csv(self, csv_path: str = "ledger_data.csv") -> str:
        target = Path(csv_path)
        orders = self.list_recent_orders(limit=1_000_000)
        with target.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
            for row in reversed(orders):
                writer.writerow(
                    [
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
                    ]
                )
        return str(target.resolve())
