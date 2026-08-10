# ASSIGNMENT_REQUIREMENTS.md

# YUMMY Restaurant Web Application
## Assignment Requirements & Implementation Guide

> **Project:** Web Technology and Programming I Assignment
>
> **Framework:** Django
>
> **Database:** SQLite
>
> **Frontend Template:** YUMMY Restaurant
>
> **Admin Template:** AdminHMD
>
> **Status:** Project Requirements Specification
>
> **Enforcement Level:** STRICT

---

# 1. Project Overview

The YUMMY Restaurant Web Application is a full-stack Django-based restaurant ordering system that enables customers to browse meals, place orders, make dummy payments, and track their orders.

Administrators manage food items, customers, payments, orders, and notifications through a dedicated dashboard.

The project demonstrates practical use of Django Models, Views, Templates, Authentication, CRUD operations, Forms, Database Relationships, Search, and Dashboard development.

---

# 2. Technology Stack

## Backend

- Django Framework

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)

## Database

- SQLite

## CSS Framework

- Bootstrap 5

## Templates

Frontend
- YUMMY Restaurant Template

Dashboard
- AdminHMD Dashboard

---

# 3. Project Objectives

The completed system must demonstrate the ability to:

- Build a complete Django web application.
- Integrate frontend templates into Django.
- Implement authentication.
- Perform CRUD operations.
- Design relational databases.
- Handle forms and validation.
- Implement searching.
- Simulate payment processing.
- Build an administrative dashboard.
- Generate user notifications.

---

# 4. User Roles

## Customer

Can:

- Register
- Login
- Browse meals
- Search meals
- View meal details
- Place orders
- Make dummy payments
- Track orders
- Receive notifications
- Manage profile

---

## Administrator

Can:

- Login
- Manage food items
- Manage customers
- Manage orders
- Verify payments
- Update order status
- Send notifications

---

# 5. Functional Requirements

---

## Module 1 — User Registration

Customers must provide:

- Full Name
- Address
- Phone Number
- Username
- Password

### Validation Rules

- Username must be unique.
- Password minimum 8 characters.
- Phone number required.

### Expected Features

- Registration form
- Validation
- Duplicate username checking
- Success message

---

## Module 2 — User Login

Users login using:

- Username
- Password

After successful login:

- Redirect to customer dashboard.

Include:

- Authentication
- Logout
- Session management

---

## Module 3 — Food Menu

Display all available food.

Each item contains:

- Image
- Name
- Category
- Description
- Price
- Availability

Features:

- Pagination
- Categories
- Featured meals
- Responsive cards

---

## Module 4 — Search

Users can search by:

- Food Name
- Category

Expected:

- Instant filtering (optional)
- Server-side search
- Empty-state handling

---

## Module 5 — Food Details

Display:

- Large image
- Description
- Ingredients (optional)
- Price
- Availability
- Quantity selector
- Add to Cart / Order button

---

## Module 6 — Place Order

Customer selects:

- Food
- Quantity
- Delivery Address

System calculates:

Total = Quantity × Price

Order created with:

- Pending status

---

## Module 7 — Dummy Payment

Supported methods:

### Mobile Money

Fields

- Mobile Number
- Network
- Amount

### Dummy Card

Fields

- Card Holder
- Card Number
- Expiry
- CVV
- Amount

Requirements

- No real payment gateway
- Store payment in database
- Await administrator approval

---

## Module 8 — Order Tracking

Customer views:

- Order Number
- Meal
- Quantity
- Amount
- Payment Status
- Order Status

Supported statuses:

- Pending
- Payment Received
- Preparing
- Ready
- Delivered

---

## Module 9 — Notifications

Customer receives notifications when:

- Payment approved
- Order confirmed
- Order preparing
- Order ready
- Order delivered

Display as:

- Dashboard notifications
- Django messages

---

## Module 10 — Food Management

Administrator can:

- Add food
- Edit food
- Delete food
- Change availability

Fields:

- Name
- Category
- Description
- Price
- Image
- Availability

---

## Module 11 — Customer Management

Administrator can:

- View customers
- Search customers

Display:

- Name
- Address
- Phone
- Username
- Registration Date

---

## Module 12 — Order Management

Administrator can:

- View orders
- Search orders
- Confirm orders
- Update status

Display:

- Customer
- Meal
- Quantity
- Amount
- Payment Method
- Date

---

## Module 13 — Payment Verification

Administrator can:

View:

- Payment Method
- Amount
- Date

Actions:

- Approve
- Reject

Approving payment should generate a notification.

---

## Module 14 — Notification Management

System automatically creates notifications when:

- Payment approved
- Order confirmed
- Order status updated

Administrator can:

- View notifications
- Delete notifications (optional)

---

# 6. Core Entities

The project should include at minimum:

- User
- Customer Profile
- Food Category
- Food
- Order
- Order Item
- Payment
- Notification

---

# 7. Required Relationships

Examples:

Customer

→ Many Orders

Order

→ Many Order Items

Food Category

→ Many Foods

Order

→ One Payment

Customer

→ Many Notifications

---

# 8. Non-Functional Requirements

The system must be:

- Responsive
- Secure
- User friendly
- Modular
- Maintainable
- Reusable
- Scalable
- Backend-driven

---

# 9. UI Requirements

Frontend

- YUMMY Restaurant theme

Dashboard

- AdminHMD

Must include:

- Responsive layouts
- Bootstrap components
- Alerts
- Forms
- Tables
- Cards
- Pagination
- Navigation

---

# 10. Django Requirements

Use:

- Models
- Views
- Templates
- Forms
- Authentication
- Messages Framework
- Static Files
- Media Files
- URL Namespaces
- Template Inheritance

Avoid:

- Business logic in templates
- Hardcoded URLs
- Hardcoded constants

---

# 11. Project Architecture Requirements

The implementation must follow:

- Modular architecture
- Feature-based organization
- Shared reusable components
- Centralized constants
- Reusable templates
- Shared partials
- Template inheritance
- Backend-driven rendering

---

# 12. Coding Requirements

Must follow:

- PEP 8
- Django best practices
- Semantic HTML
- Mobile-first design
- Reusable CSS
- Modular JavaScript

---

# 13. Deliverables

The final submission must include:

- Complete Django project
- SQLite database
- Project report (10–15 pages)
- System screenshots
- ER Diagram
- Use Case Diagram
- Presentation slides (10–15)

---

# 14. Suggested Development Order

Phase 1

- Project setup
- Folder structure
- Architecture

Phase 2

- Authentication

Phase 3

- Food management

Phase 4

- Customer interface

Phase 5

- Ordering

Phase 6

- Payments

Phase 7

- Notifications

Phase 8

- Dashboard

Phase 9

- Testing

Phase 10

- Documentation

---

# 15. Definition of Done

The project is considered complete when:

- All 14 modules are implemented.
- Customer workflows function correctly.
- Administrator workflows function correctly.
- CRUD operations are complete.
- Authentication is secure.
- Payments are stored.
- Notifications are generated.
- Database relationships are correct.
- UI is responsive.
- No hardcoded data remains.
- Documentation is complete.
- Deliverables required by the assignment are ready for submission.

---

# 16. Out of Scope

The following are **NOT** required:

- Real payment gateways
- Email integration
- SMS integration
- Online banking
- Third-party authentication
- REST APIs
- Mobile application
- Multi-restaurant support
- Inventory management
- Delivery driver management

---

# 17. Acceptance Checklist

- [ ] User Registration
- [ ] User Login
- [ ] Food Menu
- [ ] Search
- [ ] Food Details
- [ ] Place Order
- [ ] Dummy Payment
- [ ] Order Tracking
- [ ] Notifications
- [ ] Food Management
- [ ] Customer Management
- [ ] Order Management
- [ ] Payment Verification
- [ ] Notification Management
- [ ] Responsive UI
- [ ] SQLite Database
- [ ] Django Authentication
- [ ] CRUD Operations
- [ ] ER Diagram
- [ ] Use Case Diagram
- [ ] Project Report
- [ ] Presentation Slides
- [ ] Final Testing