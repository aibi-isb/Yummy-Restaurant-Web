# NAMING_CONVENTIONS.md

# YUMMY Restaurant Web Application
## Naming Conventions Guide

> **Architecture:** Feature-Based Modular Django Architecture
>
> **Framework:** Django
>
> **Enforcement Level:** STRICT
>
> Consistent naming improves readability, maintainability, and collaboration. Every developer and AI agent must follow these conventions.

---

# 1. General Rules

- Use meaningful names.
- Prefer clarity over brevity.
- Avoid abbreviations unless universally understood.
- Keep names consistent throughout the project.
- Use English only.

Good

```text
customer_order
food_category
payment_status
```

Bad

```text
cust
fc
temp1
data2
```

---

# 2. Folder Naming

Use:

- lowercase
- snake_case
- singular when representing a feature

Examples

```text
authentication
customers
menu
orders
payments
notifications
dashboard
core
templates
static
media
fixtures
```

Avoid

```text
FoodItems
Food-Items
foodItems
Food_Items
```

---

# 3. Python File Naming

Use **snake_case.py**

Examples

```text
models.py
views.py
urls.py
forms.py
admin.py
services.py
validators.py
permissions.py
helpers.py
constants.py
```

Feature-specific files

```text
food_service.py
payment_service.py
order_validator.py
notification_helper.py
```

Avoid

```text
FoodService.py
Food-Service.py
foodService.py
```

---

# 4. Class Naming

Use **PascalCase**

Examples

```python
Food
FoodCategory
Order
OrderItem
Payment
Notification
CustomerProfile
RegisterForm
PaymentService
```

Avoid

```python
food
food_category
payment_service
```

---

# 5. Function Naming

Use **snake_case**

Examples

```python
calculate_total()

approve_payment()

send_notification()

create_order()

search_food()

update_order_status()
```

Avoid

```python
CalculateTotal()

calculateTotal()

CalcTotal()
```

---

# 6. Variable Naming

Use **snake_case**

Examples

```python
food_item

customer_name

total_amount

payment_status

delivery_address
```

Avoid

```python
FoodItem

foodItem

TOTAL
```

---

# 7. Constant Naming

Use **UPPER_CASE**

Examples

```python
ORDER_PENDING

ORDER_PREPARING

PAYMENT_APPROVED

MAX_CART_ITEMS

DEFAULT_PAGE_SIZE
```

Store constants inside

```text
core/constants.py
```

Never hardcode repeated values.

---

# 8. Boolean Variables

Begin with words that imply true/false.

Examples

```python
is_available

is_paid

is_admin

has_permission

can_checkout

should_notify
```

Avoid

```python
available

paid

admin
```

---

# 9. Django Model Naming

Models use singular PascalCase.

Examples

```python
Food

Order

Payment

Notification

CustomerProfile
```

Avoid plural model names.

---

# 10. Database Table Naming

Let Django generate table names unless customization is required.

Example

```text
menu_food
orders_order
payments_payment
```

---

# 11. Field Naming

Use snake_case.

Examples

```python
full_name

phone_number

delivery_address

created_at

updated_at

total_amount

payment_method
```

Avoid

```python
FullName

PhoneNo

Address1
```

---

# 12. URL Naming

Use lowercase.

Use hyphens where appropriate.

Examples

```text
/

login/

register/

menu/

menu/<id>/

cart/

checkout/

orders/

notifications/

dashboard/
```

Named URLs

```python
menu:list

menu:detail

orders:create

orders:history

payments:checkout
```

---

# 13. Template Naming

Use snake_case.

Examples

```text
base.html

home.html

food_list.html

food_detail.html

cart.html

checkout.html

dashboard.html

payment_history.html

notification_list.html
```

Reusable partials

```text
navbar.html

footer.html

sidebar.html

pagination.html

alerts.html

modal.html
```

---

# 14. Static File Naming

CSS

```text
base.css

layout.css

utilities.css

menu.css

dashboard.css
```

JavaScript

```text
main.js

checkout.js

dashboard.js

search.js
```

Images

```text
logo.png

hero_banner.jpg

food_placeholder.png
```

---

# 15. CSS Class Naming

Follow **BEM (Block Element Modifier)**.

Examples

```css
.menu-card

.menu-card__image

.menu-card__title

.menu-card__price

.menu-card--featured

.order-table

.order-table__row

.order-table--completed
```

Avoid

```css
.box1

.redText

.div3
```

---

# 16. JavaScript Naming

Functions

```javascript
loadMenu()

calculateTotal()

initializeCart()

showNotification()

submitPayment()
```

Variables

```javascript
cartItems

selectedFood

paymentMethod

searchQuery
```

Constants

```javascript
MAX_ITEMS

API_TIMEOUT

DEFAULT_PAGE_SIZE
```

---

# 17. Form Naming

Forms use PascalCase.

Examples

```python
RegisterForm

LoginForm

CheckoutForm

PaymentForm

FoodForm
```

---

# 18. Service Naming

Use PascalCase for classes.

Examples

```python
OrderService

PaymentService

NotificationService

SearchService
```

Files

```text
services.py

payment_service.py

order_service.py
```

---

# 19. Test Naming

Files

```text
test_models.py

test_views.py

test_forms.py

test_services.py
```

Functions

```python
test_customer_can_register()

test_payment_is_saved()

test_order_total_calculation()

test_admin_can_update_order()
```

---

# 20. Git Branch Naming

Feature

```text
feature/user-registration

feature/payment-system

feature/order-management
```

Bug Fix

```text
bugfix/payment-validation

bugfix/login-error
```

Documentation

```text
docs/project-architecture

docs/coding-standards
```

---

# 21. Commit Message Convention

Format

```text
type: short description
```

Examples

```text
feat: implement customer registration

fix: resolve checkout calculation bug

refactor: simplify payment service

docs: update architecture guide

style: improve dashboard layout

test: add payment unit tests
```

---

# 22. Naming Rules Summary

| Item | Convention |
|-------|------------|
| Folders | lowercase |
| Python files | snake_case.py |
| Classes | PascalCase |
| Functions | snake_case |
| Variables | snake_case |
| Constants | UPPER_CASE |
| Models | Singular PascalCase |
| Forms | PascalCase |
| Services | PascalCase |
| Templates | snake_case.html |
| URLs | lowercase with hyphens |
| CSS Classes | BEM |
| JavaScript Variables | camelCase |
| JavaScript Functions | camelCase |
| Git Branches | feature/, bugfix/, docs/ |
| Commits | Conventional Commits |

---

# 23. Enforcement Rules

- Use descriptive names.
- Never abbreviate business entities.
- Never mix naming styles.
- Follow Django naming conventions.
- Use BEM for CSS.
- Use Conventional Commits for Git.
- Store reusable constants in `core/constants.py`.
- Keep naming consistent across backend, frontend, templates, database, and documentation.
- AI agents and contributors must follow this guide for all new code.