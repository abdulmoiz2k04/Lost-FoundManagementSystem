# Database Schema for Lost and Found Management System

This document outlines the SQL database structure used in this project.

## Overview

- **Database Used:** MySQL
- **Total Tables:** 3
- **Purpose:** To manage users, items reported as lost/found, and item claims.

---

## 1. Users Table (`users`)

| Column Name | Data Type | Description           |
|-------------|-----------|-----------------------|
| user_id     | INT (PK)  | Unique user ID        |
| name        | VARCHAR   | Full name             |
| email       | VARCHAR   | User's email (unique) |
| password    | VARCHAR   | Hashed password       |

---

## 2. Items Table (`items`)

| Column Name | Data Type | Description                          |
|-------------|-----------|--------------------------------------|
| item_id     | INT (PK)  | Unique ID for each item              |
| title       | VARCHAR   | Title/label of the item              |
| description | TEXT      | Description of the item              |
| status      | ENUM      | 'lost' or 'found'                    |
| category    | VARCHAR   | Type/category of item                |
| location    | VARCHAR   | Where it was lost/found             |
| contact     | VARCHAR   | Contact number for more info         |
| user_id     | INT (FK)  | Linked user who reported the item    |
| claimed     | BOOLEAN   | Whether the item is claimed or not   |

- **Relationship:** `user_id` references `users(user_id)`

---

## 3. Claims Table (`claims`)

| Column Name | Data Type | Description                          |
|-------------|-----------|--------------------------------------|
| claim_id    | INT (PK)  | Unique ID for each claim             |
| item_id     | INT (FK)  | Item being claimed                   |
| user_id     | INT (FK)  | User claiming the item               |
| claim_date  | DATETIME  | When the claim was made              |

- **Relationships:**
  - `item_id` references `items(item_id)`
  - `user_id` references `users(user_id)`

---

## Relationships Summary

- A **user** can report multiple **items**
- A **user** can claim multiple **items**
- An **item** can be claimed by only one **user**

---

## Notes

- Proper foreign key constraints are used to ensure relational integrity.
- Claim logic is managed using the `claims` table and the `claimed` field in `items`.

