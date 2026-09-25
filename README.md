# API to Database Data Pipeline

## Project Overview

This project implements an API-to-database data ingestion pipeline using Python.

The solution extracts customer, product, and order data from REST APIs, transforms the data, loads it into a relational database, and generates business reports using SQL JOIN operations.

## Architecture

REST APIs
↓
Python API Extraction
↓
Data Transformation
↓
SQLite Database
↓
Customers + Products + Orders + Order Items
↓
SQL JOIN Queries
↓
Business Reports

## Technologies

- Python
- REST API
- Requests
- SQLite
- SQL
- Git
- GitHub

## APIs Used

- Users API
- Products API
- Carts API

## Database Tables

### Customers
Stores customer information.

### Products
Stores product information.

### Orders
Stores order information and customer relationships.

### Order Items
Stores products, quantities, and prices associated with orders.

## Data Pipeline

1. Extract data from REST APIs.
2. Parse JSON responses.
3. Transform API data into relational structures.
4. Create database tables.
5. Load data into the database.
6. Execute SQL JOIN queries.
7. Generate customer and product business reports.

## Business Reports

### Customer Order Report

Provides:

- Customer name
- City
- Number of orders
- Total items purchased
- Total purchase amount

### Product Sales Report

Provides:

- Product
- Category
- Units sold
- Revenue

## How to Run

Create a virtual environment:

```bash
python -m venv venv
