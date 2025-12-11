# ERP System - Django Assessment Project

A full-featured Enterprise Resource Planning (ERP) system built with Django, implementing authentication, product management, customer management, sales orders, and inventory tracking with role-based access control.

## 📋 Project Overview

This is a technical assessment project demonstrating Django development capabilities for an interview process. The system manages the core business operations of a retail/jewelry business including product inventory, customer relationships, and sales order processing.

## ✨ Features Implemented

### 1. Authentication & Permissions ✅

**Status: FULLY IMPLEMENTED**

- Custom User model with role-based authentication
- Two user roles with distinct permissions:
  - **Admin**: Full CRUD access to all modules
  - **Sales User**: Limited access (view products, create orders/customers)
- Django's built-in authentication system with custom role validation
- Login/logout functionality with session management
- Custom decorators (`@admin_required`, `@sales_required`) for view-level protection
- Permission classes for API extensibility (`IsAdmin`, `IsSalesUser`, `AdminOrReadOnly`)

**Files**: 
- [accounts/models.py](accounts/models.py) - Custom User model with roles
- [accounts/decorators.py](accounts/decorators.py) - Role-based decorators
- [accounts/permissions.py](accounts/permissions.py) - DRF permission classes
- [accounts/templates/accounts/login.html](accounts/templates/accounts/login.html) - Login page

---

### 2. Product Module ✅

**Status: FULLY IMPLEMENTED**

**Model Fields**:
- `sku` - CharField (unique) ✅
- `name` - CharField ✅
- `category` - CharField ✅
- `cost_price` - DecimalField with validation ✅
- `selling_price` - DecimalField with validation ✅
- `stock_quantity` - PositiveIntegerField ✅

**Features**:
- ✅ Admin can create/update/delete products (protected by `@admin_required`)
- ✅ Sales users can view only (read-only access enforced)
- ✅ Automatic stock reduction when sales orders are confirmed
- ✅ Stock restoration when orders are cancelled
- ✅ Input validation (non-negative prices and quantities)
- ✅ Pagination (10 products per page)
- ✅ Bootstrap-based UI with CRUD forms

**Files**: 
- [products/models.py](products/models.py) - Product model
- [products/views.py](products/views.py) - CRUD operations
- [products/templates/products/](products/templates/products/) - UI templates

---

### 3. Customer Module ✅

**Status: FULLY IMPLEMENTED**

**Model Fields**:
- `customer_id` - Customer code (unique) ✅
- `name` - CharField ✅
- `phone` - CharField ✅
- `address` - TextField ✅
- `opening_balance` - DecimalField ✅
- `email` - EmailField (additional field) ✅

**Features**:
- ✅ Admin has full CRUD operations
- ✅ Sales users can add customers (create access)
- ✅ Sales users **cannot delete** customers (enforced by `@admin_required`)
- ✅ Email validation
- ✅ Pagination (10 customers per page)
- ✅ Bootstrap forms with validation

**Files**: 
- [customers/models.py](customers/models.py) - Customer model
- [customers/views.py](customers/views.py) - CRUD operations
- [customers/templates/customers/](customers/templates/customers/) - UI templates

---

### 4. Sales Orders ✅

**Status: FULLY IMPLEMENTED**

**Model Fields**:
- `order_number` - Auto-generated with pattern `SO-YYYYMMDD-####` ✅
- `customer` - ForeignKey to Customer ✅
- `order_date` - DateField (auto_now_add) ✅
- `created_by` - ForeignKey to User ✅
- `status` - Choices (pending/confirmed/canceled) ✅
- `total_amount` - DecimalField (calculated) ✅

**Order Items**:
- `product` - ForeignKey to Product ✅
- `quantity` - PositiveIntegerField ✅
- `unit_price` - DecimalField ✅
- `total_price` - DecimalField (auto-calculated: quantity × price) ✅

**Business Logic** (Signal-based implementation):
- ✅ **Order Confirmation**: When status changes from "pending" to "confirmed"
  - Stock quantity is reduced for each product
  - Stock movements are logged automatically
  - Pre-validation ensures sufficient stock before confirmation
- ✅ **Order Cancellation**: When status changes to "cancelled" from "confirmed"
  - Stock is automatically restored
  - Reverse stock movements are logged
- ✅ **Stock Validation**: Orders cannot be confirmed if insufficient stock
- ✅ **Automatic Order Number Generation**: Format `SO-YYYYMMDD-####`
- ✅ **Total Amount Calculation**: Automatically summed from order items

**Files**: 
- [orders/models.py](orders/models.py) - SalesOrder and SalesOrderItem models
- [orders/signals.py](orders/signals.py) - Stock movement automation
- [orders/views.py](orders/views.py) - Order management
- [orders/templates/orders/](orders/templates/orders/) - UI templates

---

### 5. Stock Movement Log ✅

**Status: FULLY IMPLEMENTED**

**Fields**:
- `product` - ForeignKey to Product ✅
- `quantity` - IntegerField (negative for reductions) ✅
- `created_by` - ForeignKey to User ✅
- `timestamp` - DateTimeField (auto_now_add) ✅

**Features**:
- ✅ Automatic logging via Django signals
- ✅ Logs created when orders are confirmed (negative quantities)
- ✅ Logs created when orders are cancelled (positive quantities)
- ✅ View/list functionality for stock movement history
- ✅ Timestamp tracking for audit trail

**Files**: 
- [inventory/models.py](inventory/models.py) - StockMovement model
- [orders/signals.py](orders/signals.py#L36-L45) - Auto-logging implementation
- [inventory/templates/inventory/stock_movement_log_list.html](inventory/templates/inventory/stock_movement_log_list.html)

---

### 6. UI Implementation ✅

**Status: DJANGO TEMPLATES (Option A) - FULLY IMPLEMENTED**

- ✅ Bootstrap 5 for responsive design
- ✅ Base template with consistent navigation
- ✅ Role-based menu display (navbar changes per user role)
- ✅ CRUD forms for all modules
- ✅ Table listings with pagination
- ✅ Flash messages for user feedback
- ✅ Clean, professional interface

**Templates**:
- [core/templates/base.html](core/templates/base.html) - Base layout with Bootstrap
- [core/templates/includes/navbar.html](core/templates/includes/navbar.html) - Role-based navigation
- [core/templates/includes/messages.html](core/templates/includes/messages.html) - Flash messages
- [core/templates/includes/pagination.html](core/templates/includes/pagination.html) - Reusable pagination
- Module-specific templates in each app's `templates/` directory

---

### 7. Bonus Features ✅

**Dashboard** ✅ (Implemented)
- Total customers count
- Total sales orders today
- Low stock products alert (< 10 units)
- Displayed on homepage after login

**Pagination** ✅ (Implemented)
- All list views (products, customers, orders) paginated
- 10 items per page
- Reusable pagination component

**Role-Based Menu Display** ✅ (Implemented)
- Dynamic navbar based on user role
- Admin sees all management options
- Sales users see limited menu items

**Input Validation** ✅ (Implemented)
- Backend validation for all forms
- Non-negative price validation
- Email format validation
- Stock quantity validation
- Error messages displayed to users

**Management Commands** ✅ (Implemented)
- `create_user` - Create users with roles via CLI
- `load_jewelry_data` - Seed database with sample jewelry products

**Files**:
- [core/views.py](core/views.py) - Dashboard implementation
- [accounts/management/commands/create_user.py](accounts/management/commands/create_user.py)
- [core/management/commands/load_jewelry_data.py](core/management/commands/load_jewelry_data.py)

---

## 🏗️ Technical Architecture

### Project Structure

```
erp_system/
├── accounts/           # Authentication & user management
├── products/          # Product catalog management
├── customers/         # Customer relationship management
├── orders/            # Sales order processing
├── inventory/         # Stock movement tracking
├── core/              # Dashboard & shared functionality
└── erp_system/        # Project settings & configuration
```

### Key Design Decisions

1. **Custom User Model**: Extended `AbstractUser` with role field for flexible authentication
2. **Signal-Based Stock Management**: Used Django signals (`pre_save`) to automatically handle stock changes on order status updates
3. **Decorator Pattern**: Custom decorators for role-based view protection
4. **Validation at Multiple Layers**: Model validators + view-level validation for data integrity
5. **Auto-Generated Order Numbers**: Implemented in model's `save()` method with date-based sequence
6. **Related Name Usage**: Proper use of `related_name` for reverse relationships (e.g., `order.items.all()`)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd erp_system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Generate a secure secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   
   Create a `.env` file in the project root and paste the generated key:
   ```env
   DJANGO_SECRET_KEY=your-generated-secret-key-here
   DEBUG=True
   ```
   
   **Example**: If the command outputs `django-insecure-abc123xyz789...`, your `.env` should look like:
   ```env
   DJANGO_SECRET_KEY=django-insecure-abc123xyz789...
   DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create admin user**
   ```bash
    python manage.py create_user admin_user --email admin@company.com --role ADMIN --password password123
    # Follow the prompts to create an admin user
   ```

7. **(Optional) Create sales user**
   ```bash
    python manage.py create_user john_doe --email john@example.com --role SALES --password password123
    # Follow the prompts to create a sales user
   ```

7. **(Optional) Load sample data**
   ```bash
   python manage.py load_jewelry_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - URL: http://127.0.0.1:8000/
   - Login with the credentials you created

---

## 📖 Usage Guide

### User Roles & Permissions

| Feature | Admin | Sales User |
|---------|-------|------------|
| View Products | ✅ | ✅ |
| Create/Edit/Delete Products | ✅ | ❌ |
| View Customers | ✅ | ✅ |
| Create Customers | ✅ | ✅ |
| Edit/Delete Customers | ✅ | ❌ |
| Create Sales Orders | ✅ | ✅ |
| Confirm/Cancel Orders | ✅ | ✅ |
| View Stock Movements | ✅ | ✅ |
| Dashboard Access | ✅ | ✅ |

### Typical Workflows

**Creating a Sales Order:**
1. Navigate to Orders → Create Order
2. Select customer
3. Add product line items (product + quantity)
4. System auto-calculates totals
5. Save as "pending"
6. Confirm order → Stock automatically reduces

**Cancelling an Order:**
1. Open order detail
2. Change status to "cancelled"
3. Stock automatically restored
4. Stock movement logged

---

## 🗄️ Database Schema

**Key Relationships:**
- `User` → `SalesOrder` (created_by)
- `Customer` → `SalesOrder` (one-to-many)
- `SalesOrder` → `SalesOrderItem` (one-to-many)
- `Product` → `SalesOrderItem` (many-to-one)
- `Product` → `StockMovement` (one-to-many)
- `User` → `StockMovement` (created_by)

---

## 📝 API Readiness

While the current implementation uses Django templates, the project is structured for easy API extension:

- Permission classes already defined in `accounts/permissions.py`
- Models use proper serialization-friendly fields
- Business logic separated in signals and model methods
- Can be extended with Django REST Framework by:
  - Creating serializers for each model
  - Adding ViewSets
  - Configuring token/JWT authentication

---

## 📊 Assessment Compliance

| Requirement | Status | Notes |
|------------|--------|-------|
| Authentication with 2 roles | ✅ Complete | Admin & Sales User implemented |
| Product module with all fields | ✅ Complete | All required fields + validation |
| Stock auto-decrease on order | ✅ Complete | Signal-based automation |
| Customer module with CRUD | ✅ Complete | Role-based restrictions |
| Sales orders with items | ✅ Complete | Auto order numbers, status tracking |
| Stock movement logging | ✅ Complete | Automatic via signals |
| UI with Bootstrap | ✅ Complete | Professional, responsive design |
| Pagination | ✅ Complete | All list views |
| Dashboard | ✅ Complete | Key metrics displayed |
| Role-based menu | ✅ Complete | Dynamic navbar |

---

## 🎯 Future Enhancements (Not in Scope)

- REST API with DRF
- Excel export functionality
- Product image uploads
- Advanced search & filtering
- Email notifications
- Reporting module
- Multiple warehouses support

---
