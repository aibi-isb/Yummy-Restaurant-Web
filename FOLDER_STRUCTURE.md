# FOLDER_STRUCTURE.md

# YUMMY Restaurant Web Application
## Project Folder Structure Guide

> **Architecture:** Feature-Based Modular Django Architecture
>
> **Framework:** Django
>
> **Enforcement Level:** STRICT
>
> Every file and folder must have a single responsibility.

---

# 1. Project Structure

```text
yummy_restaurant/

│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── config/
│
├── apps/
│   ├── authentication/
│   ├── customers/
│   ├── menu/
│   ├── orders/
│   ├── payments/
│   ├── notifications/
│   ├── dashboard/
│   └── core/
│
├── templates/
│
├── static/
│
├── media/
│
├── fixtures/
│
├── docs/
│
├── tests/
│
└── scripts/
```

---

# 2. Root Directory

Contains project-wide files.

```text
manage.py
```

Project management entry point.

---

```text
requirements.txt
```

Python dependencies.

---

```text
README.md
```

Project overview and setup instructions.

---

```text
.env
```

Environment variables.

Never commit to Git.

---

# 3. config/

Contains project configuration.

```text
config/

settings/
urls.py
asgi.py
wsgi.py
```

Responsibilities

- Django settings
- URL configuration
- Deployment configuration

Must NOT contain

- Business logic
- Models
- Templates

---

# 4. apps/

Each business feature lives inside its own Django app.

```text
apps/

authentication/
customers/
menu/
orders/
payments/
notifications/
dashboard/
core/
```

Each app should be independent.

---

# 5. Standard App Structure

Every Django app should follow this layout.

```text
app_name/

admin.py

apps.py

forms.py

models.py

services.py

signals.py

urls.py

views.py

tests.py

migrations/

templates/

static/

templatetags/

management/

fixtures/
```

---

# 6. authentication/

Responsibilities

- Registration
- Login
- Logout
- Password management

Owns

- Authentication forms
- Authentication templates
- User validation

Should NOT manage

- Orders
- Food
- Payments

---

# 7. customers/

Responsibilities

- Customer profile
- Dashboard
- Addresses
- Customer information

Owns

- Customer model
- Profile views

---

# 8. menu/

Responsibilities

- Food categories
- Food items
- Menu browsing
- Search
- Food details

Owns

- Food models
- Menu templates
- Search logic

---

# 9. orders/

Responsibilities

- Shopping cart
- Checkout
- Orders
- Order items
- Order tracking

Owns

- Order models
- Checkout views

---

# 10. payments/

Responsibilities

- Dummy payment
- Payment verification
- Payment history

Owns

- Payment model
- Payment forms

---

# 11. notifications/

Responsibilities

- User notifications
- Django messages
- Notification history

Owns

- Notification model

---

# 12. dashboard/

Administrator interface.

Responsibilities

- Statistics
- Management pages
- Reports

Should only coordinate other apps.

---

# 13. core/

Contains shared project functionality.

Examples

```text
constants.py

choices.py

helpers.py

validators.py

permissions.py

context_processors.py

mixins.py

decorators.py

utils.py
```

Everything here must be reusable.

---

# 14. templates/

Contains shared templates.

```text
templates/

base/

components/

errors/

emails/
```

---

## base/

```text
base.html

public_base.html

dashboard_base.html
```

---

## components/

Reusable UI.

```text
navbar.html

sidebar.html

footer.html

alerts.html

breadcrumbs.html

pagination.html

modal.html

search.html

empty_state.html
```

---

## errors/

```text
403.html

404.html

500.html
```

---

# 15. static/

Project assets.

```text
static/

css/

js/

images/

icons/

fonts/

vendors/
```

---

## css/

```text
base.css

layout.css

components.css

utilities.css

pages/
```

---

## js/

```text
main.js

dashboard.js

search.js

checkout.js
```

---

## images/

```text
logo/

foods/

banners/

avatars/
```

---

## vendors/

Third-party libraries only.

Examples

- Bootstrap
- Bootstrap Icons
- AOS
- Swiper
- GLightbox
- PureCounter

Never edit vendor files.

---

# 16. media/

Uploaded content.

```text
media/

foods/

profiles/
```

Never store uploaded files inside static/.

---

# 17. fixtures/

Database seed data.

```text
food_categories.json

foods.json

admin.json
```

Used for development and testing.

---

# 18. docs/

Project documentation.

```text
ASSIGNMENT_REQUIREMENTS.md

PROJECT_ARCHITECTURE.md

FOLDER_STRUCTURE.md

NAMING_CONVENTIONS.md

CODING_STANDARDS.md

DATABASE_GUIDE.md

DESIGN_SYSTEM.md

FRONTEND_ARCHITECTURE.md

AI_AGENT_RULES.md
```

---

# 19. tests/

Automated tests.

```text
unit/

integration/

functional/
```

---

# 20. scripts/

Utility scripts.

Examples

- Seed database
- Backup database
- Reset development environment

---

# 21. Import Rules

Always import from the lowest dependency possible.

Example

```text
Views
    ↓
Services
    ↓
Models
```

Avoid

```text
Templates
    ↓
Models
```

Templates must never query the database directly.

---

# 22. File Ownership Rules

Each feature owns:

- Models
- Forms
- Views
- Templates
- Static assets
- Tests

Shared code belongs only in:

- core/
- templates/components/
- static/

---

# 23. Where Code Belongs

Business logic

→ services.py

Validation

→ forms.py

Database

→ models.py

Routing

→ urls.py

Presentation

→ templates/

Reusable utilities

→ core/

Configuration

→ config/

---

# 24. Folder Naming Rules

Use lowercase.

Use snake_case.

Examples

```text
food_categories

customer_profile

payment_history
```

Avoid

```text
FoodCategories

Food-Categories

foodCategories
```

---

# 25. File Naming Rules

Examples

```text
food_service.py

order_views.py

payment_forms.py

notification_utils.py
```

---

# 26. Architecture Rules

- One responsibility per folder.
- One feature per Django app.
- No duplicated templates.
- No duplicated CSS.
- No duplicated JavaScript.
- Shared components must live in common directories.
- Keep reusable code in `core/`.
- Keep uploaded media outside static files.
- Keep documentation under `docs/`.
- Organize by feature rather than page.
- Follow Django conventions consistently.
```