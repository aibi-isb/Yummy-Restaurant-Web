# CODING_STANDARDS.md

# YUMMY Restaurant Web Application
## Coding Standards Guide

> **Framework:** Django
>
> **Architecture:** Feature-Based Modular Architecture
>
> **Frontend:** Bootstrap 5 + YUMMY Template
>
> **Language:** Python, HTML, CSS, JavaScript
>
> **Enforcement Level:** STRICT

---

# 1. Purpose

This document defines the coding standards for the YUMMY Restaurant Web Application.

Every developer and AI agent must follow these standards to ensure the codebase remains:

- Clean
- Consistent
- Maintainable
- Reusable
- Scalable
- Easy to review

---

# 2. General Principles

Always write code that is:

- Simple
- Readable
- Modular
- Reusable
- Well-structured
- Self-documenting

Follow the **DRY (Don't Repeat Yourself)** principle.

Avoid unnecessary complexity.

---

# 3. Python Standards

Follow **PEP 8**.

Use:

- Four spaces for indentation
- Maximum line length of 88–100 characters
- Blank lines between logical sections
- Meaningful variable names

Example

```python
def calculate_total(quantity, price):
    return quantity * price
```

Avoid

```python
def calc(q,p): return q*p
```

---

# 4. Docstrings

Every public module, class, and function should include a docstring.

Example

```python
def approve_payment(payment):
    """
    Approve a customer's payment and update the order.
    """
```

---

# 5. Type Hints

Use type hints where practical.

Example

```python
def calculate_total(quantity: int, price: float) -> float:
    return quantity * price
```

---

# 6. Function Design

Functions should:

- Perform one task
- Be easy to understand
- Be reusable
- Return predictable values

Avoid deeply nested logic.

---

# 7. Business Logic

Business logic belongs in:

- `services.py`
- Model methods (when appropriate)

Do **not** place business logic inside:

- Views
- Templates
- JavaScript
- HTML

---

# 8. Django Views

Views should remain thin.

Responsibilities:

- Receive requests
- Check permissions
- Validate forms
- Call services
- Render templates
- Redirect users

Avoid:

- Long calculations
- Complex database operations
- Duplicate code

---

# 9. Models

Models are responsible for:

- Database relationships
- Constraints
- Query methods
- Simple domain logic

Do not place presentation logic inside models.

---

# 10. Forms

Always use Django Forms for:

- Registration
- Login
- Checkout
- Payment
- Food management

Validation belongs inside forms—not templates.

---

# 11. Templates

Templates are for presentation only.

Allowed:

- Loops
- Conditions
- Includes
- Template inheritance
- Filters

Avoid:

- Database queries
- Business logic
- Complex calculations

---

# 12. Template Inheritance

Use a shared base layout.

Example

```text
base.html

public_base.html

dashboard_base.html
```

Avoid duplicated HTML.

---

# 13. Reusable Components

Create reusable partials for:

- Navbar
- Footer
- Sidebar
- Alerts
- Cards
- Pagination
- Breadcrumbs
- Search forms
- Empty states
- Modals

Never duplicate markup.

---

# 14. HTML Standards

Use semantic HTML5.

Prefer:

```html
<header>
<nav>
<main>
<section>
<article>
<footer>
```

Avoid excessive `<div>` elements.

---

# 15. Accessibility

Always:

- Use labels for forms
- Add alt text to images
- Maintain heading hierarchy
- Ensure keyboard accessibility
- Use sufficient color contrast

---

# 16. CSS Standards

Use:

- Mobile-first design
- CSS variables
- Reusable utility classes
- BEM naming convention

Avoid:

- Inline styles
- Duplicated CSS
- `!important` unless absolutely necessary

---

# 17. Bootstrap Usage

Use Bootstrap components before creating custom ones.

Prefer:

- Grid system
- Utilities
- Cards
- Forms
- Alerts
- Buttons
- Tables

Customize only when necessary.

---

# 18. JavaScript Standards

Use modern ES6+ syntax.

Prefer:

- `const`
- `let`
- Arrow functions (where appropriate)
- Modules
- Event delegation

Avoid:

- Inline JavaScript
- Global variables
- Duplicated logic

---

# 19. Static Assets

Organize assets clearly.

```text
static/

css/

js/

images/

icons/

fonts/

vendors/
```

Never edit third-party vendor files directly.

---

# 20. Database Standards

Use proper relationships.

Prefer:

- ForeignKey
- OneToOneField
- ManyToManyField

Avoid storing duplicated data.

---

# 21. Constants

Do not hardcode repeated values.

Store reusable constants in:

```text
core/constants.py
```

Examples

- Order statuses
- Payment statuses
- User roles
- Notification types

---

# 22. Error Handling

Handle errors gracefully.

Provide:

- Validation messages
- User-friendly feedback
- Custom 403, 404, and 500 pages

Never expose stack traces to users.

---

# 23. Security

Always:

- Enable CSRF protection
- Validate all user input
- Escape template output
- Restrict admin pages
- Use Django authentication
- Store secrets in `.env`

Never:

- Commit secrets
- Trust client-side validation alone
- Expose sensitive information

---

# 24. Performance

Optimize by:

- Reusing queries
- Using `select_related()` and `prefetch_related()` where appropriate
- Paginating large datasets
- Optimizing images
- Lazy-loading media when possible

---

# 25. Logging

Use Django's logging system.

Log:

- Errors
- Warnings
- Important application events

Avoid excessive debug logging in production.

---

# 26. Testing

Write tests for:

- Models
- Forms
- Views
- Services
- Permissions

Use Django's testing framework.

---

# 27. Documentation

Every new feature should include:

- Clear comments (only when necessary)
- Updated documentation
- Updated architecture if applicable

Code should be self-explanatory whenever possible.

---

# 28. Git Standards

Branch naming

```text
feature/<feature-name>

bugfix/<bug-name>

docs/<document-name>

refactor/<module-name>
```

Commit messages

```text
feat: add food search

fix: correct payment validation

docs: update architecture guide

refactor: simplify order service

test: add checkout tests
```

---

# 29. Code Review Checklist

Before merging, ensure:

- [ ] Code follows PEP 8
- [ ] Naming conventions are followed
- [ ] No duplicated code
- [ ] No hardcoded values
- [ ] Business logic is in services
- [ ] Templates contain presentation only
- [ ] Forms handle validation
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Security reviewed

---

# 30. AI Agent Rules

When generating code, AI agents must:

- Follow the project architecture.
- Respect folder ownership.
- Reuse existing components.
- Never create duplicate functionality.
- Prefer extension over modification.
- Follow the design system.
- Use centralized constants.
- Keep views thin.
- Place business logic in services.
- Generate clean, readable, production-ready code.

---

# 31. Definition of Clean Code

Clean code is:

- Easy to read
- Easy to maintain
- Easy to test
- Easy to extend
- Consistent
- Modular
- Well-documented where necessary
- Free from duplication
- Aligned with Django best practices

---

# 32. Enforcement Rules (STRICT)

- One responsibility per function.
- One responsibility per class.
- One responsibility per module.
- Never duplicate logic.
- Never hardcode business values.
- Always use reusable components.
- Always validate user input.
- Always use named URLs.
- Always use template inheritance.
- Follow the design system consistently.
- Follow Django conventions before introducing custom patterns.
- Every contribution must comply with this guide before it is accepted.