from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .sentry_init import init_sentry


init_sentry()

app = FastAPI(title="Auto-Scribe Target Service", version="0.1.0")

WAREHOUSES = {
    1: "west-coast-fulfillment",
    2: "east-coast-fulfillment",
}

ORDERS = {
    "SAFE-001": {"id": "SAFE-001", "warehouse_id": 1},
    "POISON-001": {"id": "POISON-001", "warehouse_id": 999},
}


class CheckoutRequest(BaseModel):
    order_id: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/orders")
async def orders() -> dict[str, dict[str, int | str]]:
    return ORDERS


@app.post("/checkout")
async def checkout(payload: CheckoutRequest) -> dict[str, str]:
    order = ORDERS.get(payload.order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")

    warehouse_id = int(order["warehouse_id"])
    warehouse_name = WAREHOUSES[warehouse_id]
    return {
        "orderId": payload.order_id,
        "warehouseName": warehouse_name,
    }

# Intentional CWE-89 fixture: only dummy records in an in-memory database.
@app.get("/users")
async def users(name: str) -> list[dict[str, str]]:
    import sqlite3

    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE TABLE users (name TEXT, role TEXT)")
        connection.executemany(
            "INSERT INTO users VALUES (?, ?)",
            [("alice", "user"), ("bob", "admin")],
        )
        rows = connection.execute(
            f"SELECT name, role FROM users WHERE name = '{name}'"
        ).fetchall()
    return [{"name": row[0], "role": row[1]} for row in rows]
