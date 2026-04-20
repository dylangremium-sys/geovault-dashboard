import re
from dataclasses import dataclass


@dataclass(slots=True)
class ParsedOrderInput:
    customer_name: str
    address: str
    code_or_sku: str
    quantity: int
    unit_price: float


def parse_money(value: str) -> float:
    cleaned = value.strip().upper().replace(",", "")
    cleaned = re.sub(r"(EUR|GBP|USD|€|\$|£)$", "", cleaned).strip()
    return float(cleaned)


def _normalize_lines(raw_data: str) -> list[str]:
    return [line.strip() for line in raw_data.splitlines() if line.strip()]


def parse_order_text(raw_data: str) -> ParsedOrderInput:
    lines = _normalize_lines(raw_data)
    if not lines:
        raise ValueError("No input provided.")

    if len(lines) == 1 and lines[0].count(",") >= 4:
        parts = [part.strip() for part in lines[0].split(",")]
        if len(parts) != 5:
            raise ValueError("Single-line format must be: Name, Address, Code/SKU, Qty, Price")
        name, address, identifier, qty_raw, unit_price_raw = parts
        qty = int(qty_raw)
        unit_price = parse_money(unit_price_raw)
        return ParsedOrderInput(
            customer_name=name,
            address=address,
            code_or_sku=identifier.upper(),
            quantity=qty,
            unit_price=unit_price,
        )

    trailing_line = lines[-1]
    trailing_parts = [part.strip() for part in trailing_line.split(",")]
    if len(trailing_parts) != 3:
        raise ValueError(
            "Multi-line format must end with: Code/SKU, Qty, Price (example: MUS1001, 5, 250EUR)"
        )

    identifier, qty_raw, unit_price_raw = trailing_parts
    qty = int(qty_raw)
    unit_price = parse_money(unit_price_raw)
    if len(lines) < 2:
        raise ValueError("Multi-line format requires a name line before code/qty/price.")

    name = lines[0]
    address = " ".join(lines[1:-1]).strip()
    if not address:
        raise ValueError("Address is required.")

    return ParsedOrderInput(
        customer_name=name,
        address=address,
        code_or_sku=identifier.upper(),
        quantity=qty,
        unit_price=unit_price,
    )
