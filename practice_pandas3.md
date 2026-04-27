practice 1: Use pandas to aggregate, pivot, and label

Given two pandas DataFrames, write code to: (1) merge and aggregate revenue; (2) produce a 2x2 pivot; (3) compute per-state counts with value_counts, nunique/size; (4) add a binary flag via np.where. Reuse the merged DataFrame across parts (assume it persists between steps).

Data (toy, representative) users user_id | is_member | state | age 101 | 1 | CA | 29 102 | 0 | NY | 41 103 | 1 | CA | 35 104 | 0 | TX | 50

orders order_id | user_id | channel | amount | status 7001 | 101 | SMS | 12.00 | delivered 7002 | 102 | Email | 5.00 | delivered 7003 | 103 | SMS | 7.00 | delivered 7004 | 103 | Email | 4.00 | delivered 7005 | 101 | Organic | 3.50 | delivered 7006 | 104 | SMS | 6.00 | undelivered

Tasks

Step 1: Merge orders with users on user_id (left join). Compute two outputs: (a) total delivered revenue by channel; (b) delivered revenue by channel restricted to members (is_member==1). Show groupby(...).sum() results as DataFrames.
Step 2: Create a 2x2 pivot of delivered revenue with index=is_member (0/1) and columns=channel in ['SMS','Email'] only, values=amount, aggfunc='sum', fill missing cells with 0. Use pivot_table with aggfunc='sum'.
Step 3: From the merged DataFrame, compute per-state: total orders (size) and unique purchasers (nunique of user_id). Return the top-2 states by total orders using sort_values.
Step 4: Add column high_value_flag = 1 if (user's lifetime delivered amount >= 15) OR (number of delivered SMS orders per user >= 2), else 0. Use np.where and prior groupby aggregations to avoid SettingWithCopy warnings. Show the final head with relevant columns.

practice 2: Calculate annual percentages and YoY by cohorts

Answer both SQL and Python parts. Be precise about deduping and denominator choices.

SQL schema (sample rows): orders order_id | user_id | order_date 1 | 101 | 2023-01-10 2 | 102 | 2023-05-03 3 | 101 | 2024-02-12 4 | 103 | 2024-11-20 5 | 104 | 2024-12-28

order_items order_id | product_id | qty 1 | 10 | 1 1 | 11 | 2 2 | 11 | 1 3 | 12 | 1 4 | 10 | 1 5 | 13 | 1

products product_id | name | category 10 | Widget Pro | Subscription 11 | Widget | Standard 12 | Gadget Pro | Subscription 13 | Service | Standard

users user_id | age | location 101 | 27 | NY 102 | 42 | CA 103 | 35 | NY 104 | 23 | TX

A) Three-table percentage (CTE/subquery/case-when allowed): For calendar year 2024, compute the percentage of distinct orders that contained at least one product with category = 'Subscription'. Count each order at most once even if it has multiple subscription items. Output a single row with pct_subscription_2024 rounded to two decimals.

B) YoY change by location and age group: Define age_group buckets as [18–29], [30–44], [45+]. For each (location, age_group) present in users, compute distinct-order counts in 2023 and 2024 and the YoY percent change = (orders_2024 - orders_2023) / NULLIF(orders_2023, 0). Return columns: location, age_group, orders_2023, orders_2024, yoy_pct_change. If orders_2023 = 0, return NULL for yoy_pct_change (avoid divide-by-zero). Assume an order belongs to the age/location of its user at order time. You may use window functions or conditional aggregation.

Python part (use pandas): You are given two DataFrames with the same data as above: df_orders(order_id, user_id, order_date), df_products(product_id, name, category), df_users(user_id, age, location). For year Y = 2024, compute the number of unique users who purchased any product whose name contains the substring 'Pro' (case-insensitive). Return a DataFrame with columns [location, age_group, unique_users] where age_group uses the same bins as in part B, sorted by unique_users descending, then location ascending. You must use merge, str.contains, groupby, and an aggregation (nunique), and ensure stable sorting for ties.

practice 3: Create and query an e-commerce schema

PostgreSQL only. 1) Create these tables with appropriate types and constraints (choose minimal correct types): products(product_id PK, name NOT NULL, category NOT NULL, price DECIMAL(10,2) CHECK (price > 0)); customers(customer_id PK, email UNIQUE NOT NULL, created_at DATE NOT NULL); orders(order_id PK, customer_id FK->customers, order_date DATE NOT NULL, status CHECK (status IN ('paid','refunded','cancelled')) NOT NULL, coupon_code TEXT NULL); order_items(order_id FK->orders ON DELETE CASCADE, product_id FK->products, qty INT CHECK (qty > 0) NOT NULL, unit_price DECIMAL(10,2) CHECK (unit_price > 0) NOT NULL, PRIMARY KEY(order_id, product_id)). 2) Insert rows so the tables exactly match the ASCII samples below. 3) Query A: Return per-customer gross revenue from orders with status = 'paid' whose order_date is between '2025-08-01' and '2025-08-31' inclusive. Revenue is SUM(qty * unit_price). Include customers with zero revenue as 0; output columns (customer_id, email, revenue_aug2025). Sort by revenue DESC, then customer_id ASC. 4) Query B: Using "today" = '2025-09-01', list products ordered in the last 7 days [window: '2025-08-26'..'2025-09-01'] from orders whose status NOT IN ('refunded','cancelled'). Output (product_id, name, first_order_date_in_window). 5) DML: Write one UPDATE that sets coupon_code = 'NONE' for orders with status = 'paid', order_date in August 2025, and coupon_code IS NULL; then a SELECT that verifies how many such rows exist after the update. ASCII samples to insert: customers: | customer_id | email | created_at | |------------|---------------------|------------| | 1 | alice@example.com | 2025-08-20 | | 2 | bob@example.com | 2025-08-28 | | 3 | charlie@example.com | 2025-08-30 | products: | product_id | name | category | price | |------------|---------|----------|-------| | 10 | Widget | hardware | 25.00 | | 11 | Gizmo | hardware | 40.00 | | 12 | Course | digital | 199.00| orders: | order_id | customer_id | order_date | status | coupon_code | |----------|-------------|------------|-----------|-------------| | 100 | 1 | 2025-08-29 | paid | NULL | | 101 | 1 | 2025-09-01 | refunded | NULL | | 102 | 2 | 2025-08-31 | paid | SUMMER10 | | 103 | 3 | 2025-09-01 | cancelled | NULL | | 104 | 1 | 2025-08-25 | paid | NULL | order_items: | order_id | product_id | qty | unit_price | |----------|------------|-----|------------| | 100 | 10 | 2 | 25.00 | | 100 | 11 | 1 | 40.00 | | 101 | 12 | 1 | 199.00 | | 102 | 10 | 1 | 25.00 | | 103 | 11 | 2 | 40.00 | | 104 | 10 | 1 | 25.00 | | 104 | 11 | 1 | 40.00 |

---

# PRACTICE INSTRUCTIONS

## Setup

Run `python generate_practice3_data.py` to generate all CSV files into `./data/`.

---

## Practice 1 — Pandas: Aggregate, Pivot, and Label

**Data files:** `data/p1_users.csv`, `data/p1_orders.csv`

**Schema:**

| Table  | Columns |
|--------|---------|
| users  | user_id (int), is_member (0/1), state (str), age (int) |
| orders | order_id (int), user_id (int), channel (str: SMS/Email/Organic), amount (float), status (str: delivered/undelivered) |

**Sample data — users:**

| user_id | is_member | state | age |
|---------|-----------|-------|-----|
| 101     | 1         | CA    | 29  |
| 102     | 0         | NY    | 41  |
| 103     | 1         | CA    | 35  |
| 104     | 0         | TX    | 50  |

**Sample data — orders:**

| order_id | user_id | channel | amount | status      |
|----------|---------|---------|--------|-------------|
| 7001     | 101     | SMS     | 12.00  | delivered   |
| 7002     | 102     | Email   |  5.00  | delivered   |
| 7003     | 103     | SMS     |  7.00  | delivered   |
| 7004     | 103     | Email   |  4.00  | delivered   |
| 7005     | 101     | Organic |  3.50  | delivered   |
| 7006     | 104     | SMS     |  6.00  | undelivered |

**Instructions:**

Load the two CSVs. Merge orders into users on `user_id` (left join from orders side). Keep this merged DataFrame in memory — all steps reuse it.

**Step 1 — Revenue by channel (groupby + sum):**
- (a) Total delivered revenue by channel (all users).
- (b) Delivered revenue by channel for members only (`is_member == 1`).
- Use `groupby('channel')['amount'].sum()`. Show both as DataFrames.

**Step 2 — Pivot table (2×2):**
- Filter to delivered orders, channels SMS and Email only.
- Create a pivot table: `index=is_member`, `columns=channel`, `values=amount`, `aggfunc='sum'`, `fill_value=0`.
- Expected shape: 2 rows × 2 columns.

**Step 3 — Per-state order counts and unique purchasers:**
- From the merged DataFrame, group by `state`.
- Compute: `total_orders` = `.size()`, `unique_users` = `.nunique()` on `user_id`.
- Return top-2 states by `total_orders` using `sort_values`.

**Step 4 — High-value flag with `np.where`:**
- Define `lifetime_revenue` per user = sum of delivered `amount`.
- Define `sms_order_count` per user = count of delivered SMS orders.
- Add column `high_value_flag` = 1 if `lifetime_revenue >= 15` OR `sms_order_count >= 2`, else 0.
- Join these aggregations back to the merged DataFrame (avoid `SettingWithCopyWarning`).
- Show final `.head()` with columns: `user_id`, `channel`, `amount`, `lifetime_revenue`, `sms_order_count`, `high_value_flag`.

---

## Practice 2 — SQL + Pandas: Annual Percentages and YoY by Cohort

**Data files:** `data/p2_orders.csv`, `data/p2_order_items.csv`, `data/p2_products.csv`, `data/p2_users.csv`

**Schema:**

| Table       | Columns |
|-------------|---------|
| orders      | order_id (int), user_id (int), order_date (date) |
| order_items | order_id (int), product_id (int), qty (int) |
| products    | product_id (int), name (str), category (str: Subscription/Standard) |
| users       | user_id (int), age (int), location (str) |

**Sample data — orders:**

| order_id | user_id | order_date |
|----------|---------|------------|
| 1        | 101     | 2023-01-10 |
| 2        | 102     | 2023-05-03 |
| 3        | 101     | 2024-02-12 |
| 4        | 103     | 2024-11-20 |
| 5        | 104     | 2024-12-28 |

**Sample data — order_items:**

| order_id | product_id | qty |
|----------|------------|-----|
| 1        | 10         | 1   |
| 1        | 11         | 2   |
| 2        | 11         | 1   |
| 3        | 12         | 1   |
| 4        | 10         | 1   |
| 5        | 13         | 1   |

**Sample data — products:**

| product_id | name       | category     |
|------------|------------|--------------|
| 10         | Widget Pro | Subscription |
| 11         | Widget     | Standard     |
| 12         | Gadget Pro | Subscription |
| 13         | Service    | Standard     |

**Sample data — users:**

| user_id | age | location |
|---------|-----|----------|
| 101     | 27  | NY       |
| 102     | 42  | CA       |
| 103     | 35  | NY       |
| 104     | 23  | TX       |

**Age group buckets:** [18–29], [30–44], [45+]

---

### Part A — SQL: Subscription order percentage in 2024

Write a SQL query against the `orders`, `order_items`, and `products` tables.

**Task:** For calendar year 2024, compute the percentage of **distinct orders** that contained at least one product with `category = 'Subscription'`. Count each qualifying order at most once even if it has multiple subscription items.

**Output:** A single row with one column: `pct_subscription_2024` (rounded to 2 decimal places).

**Hints:** Use a CTE or subquery to flag orders that have a subscription item, then divide by total 2024 orders. Use `NULLIF` or `CASE` to guard against divide-by-zero.

---

### Part B — SQL: YoY change by location and age group

Write a SQL query against the `orders` and `users` tables.

**Task:** For each `(location, age_group)` combination present in `users`, compute:
- `orders_2023`: count of distinct orders placed by users in that group in 2023.
- `orders_2024`: count of distinct orders placed by users in that group in 2024.
- `yoy_pct_change` = `(orders_2024 - orders_2023) / NULLIF(orders_2023, 0)`. Return NULL if `orders_2023 = 0`.

**Output columns:** `location`, `age_group`, `orders_2023`, `orders_2024`, `yoy_pct_change`

**Hints:** Use `CASE WHEN age BETWEEN 18 AND 29 THEN '[18-29]' ...` for buckets. Use conditional aggregation (`SUM(CASE WHEN YEAR = 2023 THEN 1 ELSE 0 END)`) or two CTEs joined together. Include all `(location, age_group)` combos even if order counts are 0.

---

### Part C — Python: Unique "Pro" product purchasers by location and age group in 2024

**Task:** Using the four DataFrames loaded from the CSV files, for year 2024, compute the number of **unique users** who purchased any product whose `name` contains the substring `'Pro'` (case-insensitive).

**Output:** A DataFrame with columns `[location, age_group, unique_users]` where:
- `age_group` uses the same bins as Parts A & B: `[18-29]`, `[30-44]`, `[45+]`.
- Sorted by `unique_users` descending, then `location` ascending (stable sort for ties).

**Required methods:** `merge`, `str.contains`, `pd.cut` or `np.select` for age bins, `groupby`, `nunique`.

---

## Practice 3 — PostgreSQL: Create and Query an E-commerce Schema


**Schema to create:**

```sql
products    (product_id  INT PRIMARY KEY,
             name        TEXT NOT NULL,
             category    TEXT NOT NULL,
             price       DECIMAL(10,2) CHECK (price > 0))

customers   (customer_id INT PRIMARY KEY,
             email       TEXT UNIQUE NOT NULL,
             created_at  DATE NOT NULL)

orders      (order_id    INT PRIMARY KEY,
             customer_id INT REFERENCES customers,
             order_date  DATE NOT NULL,
             status      TEXT CHECK (status IN ('paid','refunded','cancelled')) NOT NULL,
             coupon_code TEXT NULL)

order_items (order_id    INT REFERENCES orders ON DELETE CASCADE,
             product_id  INT REFERENCES products,
             qty         INT CHECK (qty > 0) NOT NULL,
             unit_price  DECIMAL(10,2) CHECK (unit_price > 0) NOT NULL,
             PRIMARY KEY (order_id, product_id))
```

**Data to insert:**

customers:

| customer_id | email               | created_at |
|-------------|---------------------|------------|
| 1           | alice@example.com   | 2025-08-20 |
| 2           | bob@example.com     | 2025-08-28 |
| 3           | charlie@example.com | 2025-08-30 |

products:

| product_id | name   | category | price  |
|------------|--------|----------|--------|
| 10         | Widget | hardware | 25.00  |
| 11         | Gizmo  | hardware | 40.00  |
| 12         | Course | digital  | 199.00 |

orders:

| order_id | customer_id | order_date | status    | coupon_code |
|----------|-------------|------------|-----------|-------------|
| 100      | 1           | 2025-08-29 | paid      | NULL        |
| 101      | 1           | 2025-09-01 | refunded  | NULL        |
| 102      | 2           | 2025-08-31 | paid      | SUMMER10    |
| 103      | 3           | 2025-09-01 | cancelled | NULL        |
| 104      | 1           | 2025-08-25 | paid      | NULL        |

order_items:

| order_id | product_id | qty | unit_price |
|----------|------------|-----|------------|
| 100      | 10         | 2   | 25.00      |
| 100      | 11         | 1   | 40.00      |
| 101      | 12         | 1   | 199.00     |
| 102      | 10         | 1   | 25.00      |
| 103      | 11         | 2   | 40.00      |
| 104      | 10         | 1   | 25.00      |
| 104      | 11         | 1   | 40.00      |

---



### Step 1 — DDL: Create all four tables

Write `CREATE TABLE` statements in dependency order (customers and products before orders, orders before order_items). Include all constraints listed in the schema above.

```sql

create table customers (
    customer_id int PRIMARY KEY,
    email text NOT NULL,
    created_at date NOT NULL
)
```

---

### Step 2 — DML: Insert all rows

Write `INSERT INTO` statements matching the sample data exactly.

```sql
insert into customers (customer_id, email, created_at) 
values (1, 'alice@example.com', '2025-08-20')
```

---

### Step 3 — Query A: Per-customer August 2025 revenue

**Task:** For each customer, compute gross revenue from `paid` orders with `order_date` between `'2025-08-01'` and `'2025-08-31'` inclusive. Revenue = `SUM(qty * unit_price)`. Customers with no qualifying orders should appear with revenue = 0.

```sql
-- sum revenue 
-- from `paid` orders 
-- from `order_date` between `'2025-08-01'` and `'2025-08-31'` 

-- all customer_id
-- join table below

-- orders and order_items for only dates
-- join customers table 

with t1 as (
    select o2.customer_id as customer_id, c.email as email, sum(o1.qty*o1.unit_price) as revenue_aug2025
    from order_items as o1
    inner join orders as o2
    on o1.order_id=o2.order_id
        and o2.order_date<='2025-08-31'
        and o2.order_date>='2025-08-01'
        and o2.status='paid'
    left join customers as c
    on c.customer_id=o2.customer_id
    group by 1,2
)


select c1.customer_id, c1.email, coalesce(revenue_aug2025,0) as revenue_aug2025
from customers as c1
left join t1 
on t1.customer_id=c1.customer_id
ORDER BY revenue_aug2025 DESC, c1.customer_id ASC;
```

`drop(columns=)` `drop_duplicates(subset=)`,`dropna(subset=)`, `sort_values(by=)`

```python

agg0=(
    order_items
    .merge(orders,on='order_id', how='left')
    .merge(customers, on='customer_id', how='left')
    .query('status=="paid"')
    .loc[lambda df_: df_.order_date.between('2025-08-01','2025-08-31'),:]
    .assign(rev=lambda df_: df_.qty *df_.unit_price)
    .groupby('customer_id_x', as_index=False)
    .agg(revenue_aug2025=('rev','sum'))
)

(
    customers
    .merge(agg0, left_on='customer_id', right_on='customer_id_x', how='left')
    .assign(revenue_aug2025=lambda df_: df_.revenue_aug2025.fillna(0))
    [['customer_id', 'email', 'revenue_aug2025']]
)

```

**Output columns:** `customer_id`, `email`, `revenue_aug2025`

**Sort:** `revenue_aug2025` DESC, then `customer_id` ASC.

**Hint:** Use a `LEFT JOIN` from customers through orders (filtered to paid + August 2025) to order_items. Use `COALESCE(SUM(...), 0)` to handle zero-revenue customers.

---

### Step 4 — Query B: Products ordered in the last 7 days

**"Today" = `'2025-09-01'`.** List products that appear in at least one order with `order_date BETWEEN '2025-08-26' AND '2025-09-01'` and `status NOT IN ('refunded', 'cancelled')`.


```sql
with t as (    
    select p.product_id as product_id, p.name as name, 
        o2.order_date as order_date,
        row_number() over(partition by p.product_id order by  o2.order_date ) as rank
    from order_items o1
    inner join orders o2
    on o1.order_id=o2.order_id
        and o2.status not in ('refunded', 'cancelled')
        and o2.order_date BETWEEN '2025-08-26' AND '2025-09-01'
    left join products as p
    on o1.product_id=p.product_id)

select product_id, name, order_date as first_order_date_in_window
from t
where rank=1

```

```sql
-- group by and use min date
SELECT p.product_id, p.name, MIN(o2.order_date) AS first_order_date_in_window
FROM order_items o1
INNER JOIN orders o2
    ON o1.order_id = o2.order_id
    AND o2.status NOT IN ('refunded', 'cancelled')
    AND o2.order_date BETWEEN '2025-08-26' AND '2025-09-01'
INNER JOIN products p ON o1.product_id = p.product_id
GROUP BY p.product_id, p.name;
```

```python
list1=['refunded','cancelled']
(
    order_items
    .merge(orders
            .assign(order_date=pd.to_datetime(orders['order_date']).order_date.astype('datetime'))
            .loc[orders.order_date.between('2025-08-26', '2025-09-01'),:]
            .query('~status.isin(@list1)'),
        on='order_id',
        suffixes=('_x','_y'),
        how='inner')
    .merge(products, on='product_id', how='inner')
    .groupby(['product_id', 'name'], as_index=False)
    .agg(first_order_date_in_window=('order_date', 'min'))

)
```



**Output columns:** `product_id`, `name`, `first_order_date_in_window` (= `MIN(order_date)` within the window).

**Hint:** Join `order_items` → `orders` → `products`. Filter on date range and status. Group by product.

---



### Step 5 — DML: Backfill coupon_code and verify

Write a single `UPDATE` statement that sets `coupon_code = 'NONE'` for all orders where:
- `status = 'paid'`
- `order_date` is in August 2025 (`BETWEEN '2025-08-01' AND '2025-08-31'`)
- `coupon_code IS NULL`

```sql

update orders
set coupon_code='NONE'
where status='paid' 
    and  order_date BETWEEN '2025-08-01' AND '2025-08-31'
    and coupon_code is Null

```

Then write a `SELECT COUNT(*)` that returns the number of rows where `coupon_code = 'NONE'` and `order_date` is in August 2025, to verify the update.

