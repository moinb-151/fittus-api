# 🧾 Fittus - A Splitwise Backend Clone

A Django REST Framework based backend system that replicates the core financial engine of Splitwise — including expense splitting, balance tracking, settlements, and debt simplification.

---

## 🚀 Features

### 👤 Authentication
- Email/password authentication
- Secure login & registration
- Profile management

### 🤝 Friend System
- Send/accept/reject friend requests
- Only friends can be added to groups

### 👥 Groups
- Multiple group types (Trip, Home, Couple, Other)
- Group member management
- Role-based permissions (admin/member)

### 💸 Expenses
- Group & individual expenses
- Multiple split types:
  - Equal
  - Exact
  - Percentage
  - Shares
- Atomic transaction-safe creation
- Automatic balance updates

### ⚖️ Balance Engine
- Normalized debtor–creditor model
- Reverse netting logic
- Derived state tracking
- Optimized queries using `select_related`

### 💰 Settlements
- Partial & full settlement support
- Debt reduction logic
- Historical settlement tracking

### 🔁 Debt Simplification (Greedy Algorithm)
- Computes minimal number of transactions
- Group-level debt optimization
- Non-destructive suggestion API

---

## 🏗 Architecture Overview

```
apps/
├── users/
├── friendships/
├── groups/
├── expenses/
├── balances/
│   ├── models.py
│   └── services/
│       ├── add_debt.py
│       ├── reduce_debt.py
│       └── simplification.py
└── settlements/
```

---

## 🧠 Balance System Design

Balances are stored in normalized form:

```
from_user → owes → to_user → amount
```

This ensures:
- No duplicate bidirectional rows
- Minimal storage
- Easy settlement application
- Efficient simplification

---

## 🛠 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (recommended)
- SQLite (development)
- Docker (planned)
- Docker Compose (planned)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd splitwise-backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Start Server

```bash
python manage.py runserver
```

---

## 🔌 Core API Endpoints

### Authentication
```
POST /users/register/
POST /users/login/
```

### Groups
```
POST /groups/create/
POST /groups/{id}/add-members/
```

### Expenses
```
POST /expenses/create/
```

### Balances
```
GET /balances/
```

### Settlements
```
POST /settlements/create/
GET  /settlements/
GET  /settlements/{user_id}/
```

### Simplification
```
GET /groups/{group_id}/simplify/
```

---

## 🧪 Testing (Planned)

- Expense creation test
- Balance update test
- Settlement test
- Simplification logic test

---

## 📦 Deployment (Upcoming)

- Dockerized application
- Docker Compose for multi-container setup
- Production-ready settings configuration

---

## 👨‍💻 Author

Moin Bagban