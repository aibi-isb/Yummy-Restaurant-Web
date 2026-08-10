# PROJECT_ARCHITECTURE.md

# YUMMY Restaurant Web Application
## Project Architecture Guide

> **Architecture Style:** Feature-Based Modular Architecture
>
> **Framework:** Django (MVT)
>
> **Frontend:** Bootstrap 5 (YUMMY Template)
>
> **Admin Dashboard:** AdminHMD
>
> **Database:** SQLite
>
> **Enforcement Level:** STRICT

---

# 1. Architecture Principles

The project follows a **feature-based modular architecture** built on Django's Model-View-Template (MVT) pattern. Each feature is self-contained, reusable, and loosely coupled, making the system easier to maintain, extend, and test.

Core principles:

- Separation of concerns
- Feature-based organization
- Reusable components
- Backend-driven rendering
- DRY (Don't Repeat Yourself)
- Convention over configuration
- Scalable project structure
- Minimal hardcoding

---

# 2. High-Level Architecture

```text
                Browser
                   │
                   ▼
               URL Router
                   │
                   ▼
                Django Views
                   │
          ┌────────┴────────┐
          ▼                 ▼
      Services          Django Forms
          │                 │
          └────────┬────────┘
                   ▼
                Models
                   │
                   ▼
               SQLite Database
                   │
                   ▼
              Django Templates
                   │
                   ▼
         Shared Components/Layout
                   │
                   ▼
             HTML/CSS/JavaScript
```

---

# 3. Architecture Layers

## Presentation Layer

Responsible for user interaction.

Includes:

- Templates
- Bootstrap UI
- Shared Components
- Layouts
- Static Assets
- JavaScript
- CSS

Responsibilities:

- Display data
- Collect user input
- Show messages
- Responsive UI

---

## Routing Layer

Responsible for mapping URLs to views.

Responsibilities:

- URL namespaces
- Named routes
- Authentication guards
- Clean URL design

Example

```text
/menu/
/menu/15/
/cart/
/checkout/
/orders/
/dashboard/
```

---

## View Layer

Views coordinate requests.

Responsibilities

- Receive requests
- Validate permissions
- Call services
- Render templates
- Redirect users

Views should remain **thin**.

Avoid:

- Complex calculations
- Business logic
- Database-heavy operations

---

## Service Layer

Contains business logic.

Examples

- OrderService
- PaymentService
- NotificationService
- SearchService

Responsibilities

- Order calculations
- Status transitions
- Notification generation
- Payment processing
- Search filtering

---

## Form Layer

Handles validation.

Responsibilities

- Validate input
- Display form errors
- Clean data
- Protect against invalid submissions

Use Django Forms for:

- Registration
- Login
- Checkout
- Payment
- Food Management

---

## Model Layer

Responsible for database interaction.

Entities

- User
- CustomerProfile
- FoodCategory
- Food
- Order
- OrderItem
- Payment
- Notification

Responsibilities

- Relationships
- Constraints
- Database queries
- Model methods

---

## Data Layer

SQLite database.

Stores

- Users
- Foods
- Orders
- Payments
- Notifications
- Categories

---

# 4. Application Architecture

Recommended Django apps:

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

Each app owns:

- models.py
- views.py
- forms.py
- urls.py
- admin.py
- services.py
- templates/
- static/
- tests.py

Apps should not directly depend on each other's internal implementation.

---

# 5. Template Architecture

Use Django template inheritance.

```text
base.html
│
├── public_base.html
│     ├── home.html
│     ├── about.html
│     ├── contact.html
│
└── dashboard_base.html
      ├── dashboard.html
      ├── orders.html
      ├── payments.html
      └── profile.html
```

Shared partials:

- Header
- Navigation
- Sidebar
- Footer
- Breadcrumb
- Alerts
- Pagination
- Modals

---

# 6. Static File Architecture

```text
static/

css/
js/
images/
icons/
fonts/
vendors/
```

Vendor libraries include:

- Bootstrap
- Bootstrap Icons
- AOS
- Swiper
- GLightbox
- PureCounter

Never modify vendor files directly.

---

# 7. Media Architecture

```text
media/

foods/
profiles/
```

Used for:

- Food images
- User profile photos (optional)

Media must be separated from static files.

---

# 8. URL Architecture

Use namespaces.

Example:

```text
/

accounts/
accounts/login/
accounts/register/

menu/
menu/<id>/

cart/

checkout/

orders/

payments/

dashboard/
```

Always reference URLs using Django's `{% url %}` tag.

---

# 9. Navigation Flow

## Public

```text
Home
 ├── About
 ├── Menu
 ├── Gallery
 ├── Contact
 └── Login/Register
```

## Customer

```text
Dashboard
 ├── Menu
 ├── Food Details
 ├── Cart
 ├── Checkout
 ├── Payment
 ├── Orders
 ├── Notifications
 └── Profile
```

## Administrator

```text
Dashboard
 ├── Food Management
 ├── Customers
 ├── Orders
 ├── Payments
 └── Notifications
```

---

# 10. Request Lifecycle

```text
User Request
      │
      ▼
URL Router
      │
      ▼
View
      │
      ▼
Form Validation
      │
      ▼
Service Layer
      │
      ▼
Model
      │
      ▼
Database
      │
      ▼
Template
      │
      ▼
Browser Response
```

---

# 11. Business Logic Rules

Business rules belong in:

- Services
- Model methods (when appropriate)

Never place business logic in:

- Templates
- JavaScript
- HTML

---

# 12. Shared Components

Reusable UI components include:

- Navbar
- Footer
- Hero
- Cards
- Buttons
- Forms
- Alerts
- Tables
- Search bar
- Pagination
- Breadcrumbs
- Empty states
- Loading indicators
- Modals

These components should be shared across multiple pages.

---

# 13. Design System Integration

The UI must follow the project design system.

Key rules:

- Use CSS variables for colors.
- Use Bootstrap utility classes where possible.
- Maintain consistent spacing and typography.
- Reuse component styles.
- Avoid inline styles.

---

# 14. Centralized Constants

Avoid hardcoded values.

Create centralized constants for:

- Order statuses
- Payment statuses
- Food categories
- Notification types
- User roles
- Application settings

---

# 15. Seed Data

Use fixtures or management commands to populate:

- Food categories
- Sample foods
- Administrator account
- Sample customers

Never hardcode sample data into templates.

---

# 16. Error Handling

Provide dedicated pages for:

- 403 Forbidden
- 404 Not Found
- 500 Server Error

Display user-friendly messages and navigation back to the application.

---

# 17. Security Guidelines

- Use Django Authentication.
- Enable CSRF protection.
- Validate all forms.
- Escape template output.
- Protect dashboard routes with authentication.
- Restrict administrator-only pages using permissions.

---

# 18. Scalability

The architecture should support future enhancements without major restructuring, including:

- REST API integration
- Mobile application
- PostgreSQL migration
- Real payment gateways
- Email notifications
- Inventory management
- Delivery tracking

---

# 19. Architecture Rules (STRICT)

- One responsibility per app.
- Keep views thin.
- Place business logic in services.
- Use reusable templates and components.
- Avoid duplicated code.
- Never hardcode URLs or constants.
- Follow Django conventions.
- Reuse layouts through template inheritance.
- Organize code by feature, not by page.
- Build with backend-driven rendering in mind.
```