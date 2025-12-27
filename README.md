# GearGuard - Equipment Maintenance Management System

A comprehensive Django-based web application for managing equipment maintenance, teams, and work centers across multiple companies. Built with professional styling and robust validation for industrial maintenance operations.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database](#database)
- [API Endpoints](#api-endpoints)
- [Features Details](#features-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

### Equipment Management
- **Equipment Registry**: Track all equipment with serial numbers, categories, and status
- **Multi-Company Support**: Manage equipment across different companies
- **Equipment Categories**: Organize equipment by type (CNC Machines, Hydraulic Systems, etc.)
- **Status Tracking**: Monitor equipment status (active, under maintenance, scrapped)
- **Equipment Details**: Store comprehensive information including description and maintenance history

### Team Management
- **Team Creation & Management**: Create maintenance teams and assign them to work centers
- **Company Assignment**: Link teams to specific companies
- **Team Composition**: Assign technicians to teams with detailed member information
- **Maintenance Planning**: Schedule team-based maintenance activities

### Maintenance Request Management
- **Request Creation**: Create maintenance requests for equipment or work centers
- **Scheduled Date Validation**: Ensure scheduled dates are in the future with proper validation
- **Duration Validation**: Support for HH:MM:SS duration format with validation
- **Priority Levels**: Set maintenance priority (1-3 scale)
- **Maintenance Types**: Support for preventive and corrective maintenance
- **Status Tracking**: Track requests through stages (new, in_progress, completed)

### Work Centers
- **Work Center Management**: Create and manage production work centers
- **Efficiency Metrics**: Track capacity efficiency and OEE (Overall Equipment Effectiveness)
- **Cost Tracking**: Monitor cost per hour for each work center
- **Team Assignment**: Assign maintenance teams to specific work centers

### User Management
- **Role-Based Access**: Support for admin, supervisor, and technician roles
- **Secure Authentication**: Password hashing with Argon2 and PBKDF2
- **Session Management**: Secure session handling with HTTP-only cookies
- **User Profiles**: Manage user information and roles

### Dashboard
- **Overview**: Quick view of maintenance status and team information
- **Statistics**: Display key metrics and maintenance summaries
- **Quick Actions**: Quick links to common operations

## Tech Stack

### Backend
- **Framework**: Django 6.0
- **Database**: SQLite3 (development) / PostgreSQL (production ready)
- **Authentication**: Django Auth with custom validation
- **Password Security**: Argon2 hashing with custom validators

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Tailwind CSS
- **Icons**: Integrated icon system
- **Responsive Design**: Mobile-first approach

### Development
- **Python 3.10+**
- **pip** for package management
- **Git** for version control

## Project Structure

```
gearguard/
├── accounts/              # User authentication and management
│   ├── models.py         # User-related models
│   ├── views.py          # Authentication views
│   ├── forms.py          # Registration/login forms
│   └── urls.py           # Auth URL routes
├── teams/                # Team management
│   ├── models.py         # Team model with company field
│   ├── views.py          # Team CRUD views
│   ├── forms.py          # Team creation/edit forms
│   └── urls.py           # Team routes
├── equipment/            # Equipment management
│   ├── models.py         # Equipment model with company field
│   ├── views.py          # Equipment CRUD views
│   ├── forms.py          # Equipment forms
│   └── urls.py           # Equipment routes
├── maintenance/          # Maintenance request management
│   ├── models.py         # Maintenance request models
│   ├── views.py          # Request handling views
│   ├── forms.py          # Request forms with validation
│   └── urls.py           # Maintenance routes
├── dashboard/            # Dashboard and statistics
│   ├── views.py          # Dashboard views
│   └── urls.py           # Dashboard routes
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── dashboard/        # Dashboard templates
│   ├── teams/            # Team templates
│   ├── equipment/        # Equipment templates
│   └── accounts/         # Auth templates
├── static/               # Static files (CSS, JS, images)
├── data/                 # Seed data
│   └── seed_data.json    # Sample data for initial setup
├── management/           # Custom management commands
│   └── commands/
│       └── seed_database.py  # Database seeding command
├── scripts/              # Utility scripts
│   ├── seed_database.py  # Alternative seeding script
│   └── duplicate_data.py # Data duplication utility
├── gearguard/            # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── validators.py     # Custom password validators
└── manage.py             # Django management script
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. **Clone the Repository**
```bash
git clone <repository-url>
cd gearguard
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply Migrations**
```bash
python manage.py migrate
```

5. **Load Seed Data**
```bash
python manage.py seed_database
```

6. **Create Superuser** (if not created by seed)
```bash
python manage.py createsuperuser
```

7. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

8. **Run Development Server**
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## Configuration

### Environment Variables (Development)
Currently uses SQLite with DEBUG=True. For production:

1. Create `.env` file in project root
2. Set required variables:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost:5432/gearguard
```

### Security Settings
- Password hashing: Argon2 (primary) with PBKDF2 fallback
- Session timeout: 1 hour
- CSRF protection enabled
- XSS filtering enabled
- Secure cookie settings in production

## Usage

### Access Points

**Admin Panel**
- URL: `/admin`
- Default credentials: admin@gearguard.com / Admin@123456

**Dashboard**
- URL: `/`
- Requires authentication

**Teams Management**
- List: `/teams/`
- Create: `/teams/create/`
- Detail: `/teams/<id>/`
- Edit: `/teams/<id>/edit/`

**Equipment Management**
- List: `/equipment/`
- Create: `/equipment/create/`
- Detail: `/equipment/<id>/`

**Maintenance Requests**
- List: `/maintenance/`
- Create: `/maintenance/create/`
- Detail: `/maintenance/<id>/`

### Sample Credentials

After loading seed data, use these test accounts:

| Role | Username | Email | Password |
|------|----------|-------|----------|
| Admin | admin | admin@gearguard.com | Admin@123456 |
| Supervisor | supervisor | supervisor@gearguard.com | Super@123456 |
| Technician 1 | technician1 | tech1@gearguard.com | Tech@123456 |
| Technician 2 | technician2 | tech2@gearguard.com | Tech@123456 |

## Database

### Models

**Team**
- `name`: Team name
- `description`: Team description
- `company`: Associated company
- `work_center`: Assigned work center
- Created/updated timestamps

**Equipment**
- `name`: Equipment name
- `category`: Equipment category
- `serial_number`: Unique serial number
- `description`: Equipment details
- `company`: Company ownership
- `status`: Current status (active, under_maintenance, scrapped)
- `work_center`: Assigned work center
- `maintenance_team`: Assigned team

**MaintenanceRequest**
- `subject`: Request subject
- `maintenance_for`: Target (equipment or work_center)
- `equipment`: Related equipment
- `scheduled_date`: Future-dated maintenance date
- `duration`: Maintenance duration (HH:MM:SS)
- `maintenance_type`: Type (preventive/corrective)
- `priority`: Priority level (1-3)
- `stage`: Current stage (new/in_progress/completed)
- `team`: Assigned team
- `notes`: Additional notes
- `instructions`: Maintenance instructions

### Seed Data

Sample data includes:
- 3 Companies (TechCorp Manufacturing, Precision Industries Ltd, Global Engineering Solutions)
- 4 Users with different roles
- 4 Work Centers with efficiency metrics
- 5 Equipment Categories
- 4 Maintenance Teams with company assignments
- 10 Equipment items
- 5 Maintenance Requests

**Load seed data:**
```bash
python manage.py seed_database
```

### Data Duplication

Duplicate existing data for testing:
```bash
python manage.py shell < scripts/duplicate_data.py
```

## API Endpoints

### Teams
```
GET    /teams/                    - List all teams
POST   /teams/create/             - Create new team
GET    /teams/<id>/               - Team details
POST   /teams/<id>/edit/          - Edit team
```

### Equipment
```
GET    /equipment/                - List all equipment
POST   /equipment/create/         - Create new equipment
GET    /equipment/<id>/           - Equipment details
```

### Maintenance
```
GET    /maintenance/              - List requests
POST   /maintenance/create/       - Create request
GET    /maintenance/<id>/         - Request details
```

## Features Details

### Validation Features

**Scheduled Date Validation**
- Ensures all scheduled maintenance dates are in the future
- Prevents backdated maintenance requests
- Provides clear error messages

**Duration Validation**
- Accepts HH:MM:SS format
- Validates time format on form submission
- Converts to Django timedelta for storage
- Example: `01:30:00` = 1 hour 30 minutes

**Company Field**
- Teams and equipment can be assigned to specific companies
- Display company information in list views with badge styling
- Filter and organize resources by company

### Professional Styling
- Modern card-based layouts
- Responsive tables with color-coded status indicators
- Badge components for company and status display
- Consistent spacing and typography
- Hover effects and visual feedback
- Mobile-first responsive design

## Troubleshooting

### Database Issues

**"No tables found" after migration**
```bash
python manage.py migrate --run-syncdb
python manage.py seed_database
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --force-reinstall
```

## Security Notes

- Store `SECRET_KEY` securely in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regularly update dependencies
- Use strong passwords (min 8 chars with complexity requirements)
- Keep Django and Python updated

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request

## License

Proprietary - GearGuard Equipment Maintenance System

## Support

For issues or questions:
1. Check troubleshooting section
2. Review project documentation
3. Contact development team

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Status**: Production Ready
