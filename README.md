# Stock Management System (Gestion Stock)

A comprehensive stock management application with role-based access control, inventory tracking, supplier management, and reporting features.

## Features

- **Role-Based Access Control**: Admin, Stock Manager, and Employee roles
- **Inventory Management**: Track stock levels, movements, and alerts
- **Supplier Management**: Manage supplier information and relationships
- **Reporting & Analytics**: Generate reports with charts and PDF export
- **Modern UI/UX**: Dark green theme with responsive design
- **Dashboard**: Real-time stock overview and analytics

## Prerequisites

Before installing this application, ensure you have the following installed on your system:

- **PHP** (version 7.4 or higher)
- **MySQL** or **PostgreSQL** database
- **Web Server** (Apache/Nginx) or PHP built-in server
- **Composer** (PHP dependency manager)
- **Git** (for version control)

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/cenchy1234/gestionstock.git
cd gestionstock
```

### Step 2: Install Dependencies

```bash
composer install
```

### Step 3: Database Setup

1. Create a new database for the application:
   ```sql
   CREATE DATABASE gestion_stock;
   ```

2. Configure database connection:
   - Copy `.env.example` to `.env`
   - Update database credentials in `.env` file:
   ```
   DB_HOST=localhost
   DB_DATABASE=gestion_stock
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   ```

3. Run database migrations:
   ```bash
   php artisan migrate
   ```

4. Seed the database with initial data:
   ```bash
   php artisan db:seed
   ```

### Step 4: Configure Application

1. Generate application key:
   ```bash
   php artisan key:generate
   ```

2. Set up file permissions (Linux/Mac):
   ```bash
   chmod -R 755 storage
   chmod -R 755 bootstrap/cache
   ```

### Step 5: Start the Application

#### Option A: Using PHP Built-in Server (Development)
```bash
php artisan serve
```
The application will be available at `http://localhost:8000`

#### Option B: Using Apache/Nginx (Production)
Configure your web server to point to the `public` directory of the application.

## Default Login Credentials

After installation, you can log in with these default accounts:

- **Admin**: 
  - Email: `admin@gestionstock.com`
  - Password: `admin123`

- **Stock Manager**: 
  - Email: `manager@gestionstock.com`
  - Password: `manager123`

- **Employee**: 
  - Email: `employee@gestionstock.com`
  - Password: `employee123`

## User Roles & Permissions

- **Admin**: Full system access, user management, system configuration
- **Stock Manager**: Add/modify/view stock, manage inventory, generate reports
- **Employee**: View stock, make requests, limited access

## Git Setup for New Repository

If you're setting up this project as a new repository, follow these commands:

```bash
echo "# gestionstock" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/cenchy1234/gestionstock.git
git push -u origin main
```

## Development Workflow

### Adding New Features
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Commit changes: `git commit -m "Add your feature description"`
4. Push branch: `git push origin feature/your-feature-name`
5. Create a pull request

### Running Tests
```bash
php artisan test
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify database credentials in `.env` file
   - Ensure database server is running
   - Check if database exists

2. **Permission Errors**
   - Set proper file permissions for `storage` and `bootstrap/cache`
   - Ensure web server has write access to these directories

3. **Composer Dependencies**
   - Run `composer install` if vendor folder is missing
   - Clear composer cache: `composer clear-cache`

4. **Application Cache Issues**
   - Clear application cache: `php artisan cache:clear`
   - Clear config cache: `php artisan config:clear`
   - Clear view cache: `php artisan view:clear`

## Support

For support and questions, please create an issue in the GitHub repository or contact the development team.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
