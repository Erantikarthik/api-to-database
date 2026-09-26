# API-to-Database Data Pipeline

## Project Overview

This project implements an end-to-end data ingestion pipeline that extracts e-commerce data from REST APIs, transforms and loads the data into PostgreSQL, and generates business reports using SQL JOIN queries.

The project demonstrates practical Data Engineering concepts including API extraction, data ingestion, relational database design, PostgreSQL, Python, SQL JOINs, and business reporting.

---

## Architecture

REST APIs
   ↓
Python API Extraction
   ↓
Data Transformation
   ↓
PostgreSQL Database
   ↓
SQL JOIN Queries
   ↓
Business Reports

---

## Technologies Used

- Python
- REST APIs
- PostgreSQL
- SQL
- psycopg2
- Requests
- pgAdmin 4
- Git
- GitHub
- VS Code

---

## Data Sources

The project uses DummyJSON REST APIs:

- Users API
- Products API
- Carts API

The APIs provide sample e-commerce customer, product, order, and order-item data.

---

## Database Design

The PostgreSQL database is named:

`ecommerce_db`

### Tables

#### 1. customers

Stores customer information.

Columns:

- customer_id
- first_name
- last_name
- email
- city
- state

#### 2. products

Stores product information.

Columns:

- product_id
- title
- category
- price
- stock

#### 3. orders

Stores customer order information.

Columns:

- order_id
- customer_id

#### 4. order_items

Stores individual products included in each order.

Columns:

- order_item_id
- order_id
- product_id
- quantity
- price

---

## Data Pipeline Process

### Step 1 — Extract

Python sends HTTP requests to the REST APIs and retrieves:

- Customers
- Products
- Orders
- Order Items

### Step 2 — Transform

The API JSON responses are parsed and converted into relational records.

### Step 3 — Load

The transformed data is loaded into PostgreSQL tables.

### Step 4 — Reporting

SQL JOIN queries combine the relational tables to generate business reports.

---

## Business Reports

### Customer Order Report

The customer report uses JOIN operations between:

- customers
- orders
- order_items

It calculates:

- Total Orders
- Total Items
- Total Order Amount

### Product Sales Report

The product report uses JOIN operations between:

- products
- order_items

It calculates:

- Units Sold
- Revenue

---

## SQL Concepts Demonstrated

- SELECT
- WHERE
- JOIN
- GROUP BY
- ORDER BY
- COUNT
- SUM
- ROUND
- Aggregate Functions
- Foreign Keys
- Primary Keys

---

## Project Structure

```text
api-to-database/
│
├── main.py
├── business_reports.sql
├── README.md
├── requirements.txt
├── .gitignore
└── venv/