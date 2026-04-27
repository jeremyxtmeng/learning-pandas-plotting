"""
Generate and save CSV data for Practice 1 and Practice 2.
Run: python generate_practice3_data.py
Outputs saved to ./data/
"""

import pandas as pd
import os

os.makedirs("data", exist_ok=True)

# ── Practice 1 ──────────────────────────────────────────────────────────────
users_p1 = pd.DataFrame({
    "user_id":   [101, 102, 103, 104],
    "is_member": [1,   0,   1,   0],
    "state":     ["CA","NY","CA","TX"],
    "age":       [29,  41,  35,  50],
})

orders_p1 = pd.DataFrame({
    "order_id": [7001, 7002, 7003, 7004, 7005, 7006],
    "user_id":  [101,  102,  103,  103,  101,  104],
    "channel":  ["SMS","Email","SMS","Email","Organic","SMS"],
    "amount":   [12.00, 5.00, 7.00, 4.00, 3.50, 6.00],
    "status":   ["delivered","delivered","delivered","delivered","delivered","undelivered"],
})

users_p1.to_csv("data/p1_users.csv", index=False)
orders_p1.to_csv("data/p1_orders.csv", index=False)
print("Practice 1 data saved: data/p1_users.csv, data/p1_orders.csv")

# ── Practice 2 ──────────────────────────────────────────────────────────────
orders_p2 = pd.DataFrame({
    "order_id":   [1,   2,   3,   4,   5],
    "user_id":    [101, 102, 101, 103, 104],
    "order_date": pd.to_datetime(["2023-01-10","2023-05-03","2024-02-12","2024-11-20","2024-12-28"]),
})

order_items_p2 = pd.DataFrame({
    "order_id":   [1, 1, 2, 3, 4, 5],
    "product_id": [10,11,11,12,10,13],
    "qty":        [1, 2, 1, 1, 1, 1],
})

products_p2 = pd.DataFrame({
    "product_id": [10, 11, 12, 13],
    "name":       ["Widget Pro","Widget","Gadget Pro","Service"],
    "category":   ["Subscription","Standard","Subscription","Standard"],
})

users_p2 = pd.DataFrame({
    "user_id":  [101, 102, 103, 104],
    "age":      [27,  42,  35,  23],
    "location": ["NY","CA","NY","TX"],
})

orders_p2.to_csv("data/p2_orders.csv", index=False)
order_items_p2.to_csv("data/p2_order_items.csv", index=False)
products_p2.to_csv("data/p2_products.csv", index=False)
users_p2.to_csv("data/p2_users.csv", index=False)
print("Practice 2 data saved: data/p2_orders.csv, data/p2_order_items.csv, data/p2_products.csv, data/p2_users.csv")
