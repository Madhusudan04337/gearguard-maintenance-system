"""
Django script to seed the database with sample data from seed_data.json.
Usage: python manage.py shell < scripts/seed_database.py
OR: from scripts.seed_database import seed_database; seed_database()
"""

import json
from datetime import datetime
from django.contrib.auth.models import User
from equipment.models import Equipment, EquipmentCategory
from teams.models import Team, WorkCenter
from maintenance.models import MaintenanceRequest

def seed_database():
    """Load seed data from JSON file and populate database."""
    
    # Load JSON data
    with open('seed_data.json', 'r') as f:
        data = json.load(f)
    
    print("[Seeding] Starting database seeding...")
    
    # Create Users
    print("[Users] Creating users...")
    users = {}
    for user_data in data['users']:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            }
        )
        users[user_data['username']] = user
        status = "created" if created else "already exists"
        print(f"  - {user_data['username']}: {status}")
    
    # Create Equipment Categories
    print("[Categories] Creating equipment categories...")
    categories = {}
    for cat_data in data['equipment_categories']:
        responsible = users.get(cat_data['responsible_username'])
        category, created = EquipmentCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'responsible': responsible}
        )
        categories[cat_data['name']] = category
        status = "created" if created else "already exists"
        print(f"  - {cat_data['name']}: {status}")
    
    # Create Work Centers
    print("[WorkCenters] Creating work centers...")
    work_centers = {}
    for wc_data in data['work_centers']:
        work_center, created = WorkCenter.objects.get_or_create(
            code=wc_data['code'],
            defaults={
                'name': wc_data['name'],
                'tag': wc_data['tag'],
                'cost_per_hour': wc_data['cost_per_hour'],
                'capacity_efficiency': wc_data['capacity_efficiency'],
                'oee_target': wc_data['oee_target'],
            }
        )
        work_centers[wc_data['code']] = work_center
        status = "created" if created else "already exists"
        print(f"  - {wc_data['name']} ({wc_data['code']}): {status}")
    
    # Create Teams
    print("[Teams] Creating teams...")
    teams = {}
    for team_data in data['teams']:
        work_center = work_centers.get(team_data['work_center_code'])
        team, created = Team.objects.get_or_create(
            name=team_data['name'],
            defaults={
                'description': team_data['description'],
                'work_center': work_center,
            }
        )
        teams[team_data['name']] = team
        status = "created" if created else "already exists"
        print(f"  - {team_data['name']}: {status}")
    
    # Create Equipment
    print("[Equipment] Creating equipment...")
    equipment_map = {}
    for eq_data in data['equipment']:
        category = categories.get(eq_data['category_name'])
        employee = users.get(eq_data['employee_username'])
        maintenance_team = teams.get(eq_data['maintenance_team_name'])
        work_center = work_centers.get(eq_data['work_center_code'])
        
        equipment, created = Equipment.objects.get_or_create(
            serial_number=eq_data['serial_number'],
            defaults={
                'name': eq_data['name'],
                'category': category,
                'description': eq_data['description'],
                'employee': employee,
                'maintenance_team': maintenance_team,
                'work_center': work_center,
                'assigned_date': eq_data['assigned_date'],
                'status': eq_data['status'],
            }
        )
        equipment_map[eq_data['serial_number']] = equipment
        status = "created" if created else "already exists"
        print(f"  - {eq_data['name']}: {status}")
    
    # Create Maintenance Requests
    print("[Requests] Creating maintenance requests...")
    for req_data in data['maintenance_requests']:
        # Parse duration from HH:MM:SS format
        duration_parts = req_data['duration'].split(':')
        from datetime import timedelta
        duration = timedelta(
            hours=int(duration_parts[0]),
            minutes=int(duration_parts[1]),
            seconds=int(duration_parts[2])
        )
        
        equipment = equipment_map.get(req_data.get('equipment_serial'))
        created_by = users.get(req_data['created_by_username'])
        technician = users.get(req_data.get('technician_username'))
        team = teams.get(req_data.get('team_name'))
        
        request_obj, created = MaintenanceRequest.objects.get_or_create(
            subject=req_data['subject'],
            created_by=created_by,
            defaults={
                'maintenance_for': req_data['maintenance_for'],
                'equipment': equipment,
                'maintenance_type': req_data['maintenance_type'],
                'priority': req_data['priority'],
                'stage': req_data['stage'],
                'scheduled_date': datetime.fromisoformat(req_data['scheduled_date']),
                'duration': duration,
                'notes': req_data['notes'],
                'instructions': req_data['instructions'],
                'technician': technician,
                'team': team,
            }
        )
        status = "created" if created else "already exists"
        print(f"  - {req_data['subject']}: {status}")
    
    print("[Complete] Database seeding completed successfully!")

# Run the seed function
if __name__ == '__main__':
    seed_database()
