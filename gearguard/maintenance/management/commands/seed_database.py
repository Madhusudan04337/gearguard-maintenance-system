from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json
import os
from equipment.models import Equipment, EquipmentCategory
from teams.models import Team, WorkCenter
from maintenance.models import MaintenanceRequest
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed the database with initial data from JSON file'

    def handle(self, *args, **options):
        json_path = os.path.join(os.path.dirname(__file__), '../../data/seed_data.json')
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return

        # Create users
        self.stdout.write('Creating users...')
        users_dict = {}
        for user_data in data.get('users', []):
            try:
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        'email': user_data['email'],
                        'password': make_password(user_data['password']),
                        'first_name': user_data.get('first_name', ''),
                        'last_name': user_data.get('last_name', ''),
                        'is_staff': user_data.get('is_staff', False),
                        'is_superuser': user_data.get('is_superuser', False),
                    }
                )
                users_dict[user_data['username']] = user
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created user: {user.username}'))
                else:
                    self.stdout.write(f'  - User already exists: {user.username}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating user: {str(e)}'))

        # Create work centers
        self.stdout.write('\nCreating work centers...')
        workcenters_dict = {}
        for wc_data in data.get('work_centers', []):
            try:
                wc, created = WorkCenter.objects.get_or_create(
                    code=wc_data['code'],
                    defaults={
                        'name': wc_data['name'],
                        'tag': wc_data.get('tag', ''),
                        'cost_per_hour': wc_data.get('cost_per_hour', 0),
                        'capacity_efficiency': wc_data.get('capacity_efficiency', 100),
                        'oee_target': wc_data.get('oee_target', 90),
                    }
                )
                workcenters_dict[wc_data['name']] = wc
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created work center: {wc.name}'))
                else:
                    self.stdout.write(f'  - Work center already exists: {wc.name}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating work center: {str(e)}'))

        # Create equipment categories
        self.stdout.write('\nCreating equipment categories...')
        categories_dict = {}
        for cat_data in data.get('equipment_categories', []):
            try:
                responsible = users_dict.get(cat_data.get('responsible'))
                cat, created = EquipmentCategory.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={'responsible': responsible}
                )
                categories_dict[cat_data['name']] = cat
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {cat.name}'))
                else:
                    self.stdout.write(f'  - Category already exists: {cat.name}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating category: {str(e)}'))

        # Create teams
        self.stdout.write('\nCreating teams...')
        teams_dict = {}
        for team_data in data.get('teams', []):
            try:
                wc = workcenters_dict.get(team_data.get('work_center'))
                team, created = Team.objects.get_or_create(
                    name=team_data['name'],
                    defaults={
                        'description': team_data.get('description', ''),
                        'work_center': wc,
                    }
                )
                teams_dict[team_data['name']] = team
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created team: {team.name}'))
                else:
                    self.stdout.write(f'  - Team already exists: {team.name}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating team: {str(e)}'))

        # Create equipment
        self.stdout.write('\nCreating equipment...')
        equipment_dict = {}
        for eq_data in data.get('equipment', []):
            try:
                category = categories_dict.get(eq_data.get('category'))
                employee = users_dict.get(eq_data.get('employee'))
                maintenance_team = teams_dict.get(eq_data.get('maintenance_team'))
                work_center = workcenters_dict.get(eq_data.get('work_center'))
                
                equipment, created = Equipment.objects.get_or_create(
                    serial_number=eq_data['serial_number'],
                    defaults={
                        'name': eq_data['name'],
                        'category': category,
                        'description': eq_data.get('description', ''),
                        'employee': employee,
                        'maintenance_team': maintenance_team,
                        'work_center': work_center,
                        'status': eq_data.get('status', 'active'),
                    }
                )
                equipment_dict[eq_data['name']] = equipment
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created equipment: {equipment.name}'))
                else:
                    self.stdout.write(f'  - Equipment already exists: {equipment.name}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating equipment: {str(e)}'))

        # Create maintenance requests
        self.stdout.write('\nCreating maintenance requests...')
        for mr_data in data.get('maintenance_requests', []):
            try:
                created_by = users_dict.get(mr_data.get('created_by'))
                technician = users_dict.get(mr_data.get('technician'))
                equipment = equipment_dict.get(mr_data.get('equipment'))
                work_center = workcenters_dict.get(mr_data.get('work_center'))
                team = teams_dict.get(mr_data.get('team'))
                
                # Parse scheduled_date
                scheduled_date = None
                if mr_data.get('scheduled_date'):
                    try:
                        scheduled_date = datetime.fromisoformat(mr_data['scheduled_date'].replace('Z', '+00:00'))
                    except:
                        pass
                
                # Parse duration
                from datetime import timedelta
                duration = None
                if mr_data.get('duration'):
                    try:
                        parts = mr_data['duration'].split(':')
                        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
                        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    except:
                        pass
                
                request, created = MaintenanceRequest.objects.get_or_create(
                    subject=mr_data['subject'],
                    created_by=created_by,
                    defaults={
                        'maintenance_for': mr_data.get('maintenance_for', 'equipment'),
                        'equipment': equipment,
                        'work_center': work_center,
                        'technician': technician,
                        'team': team,
                        'scheduled_date': scheduled_date,
                        'duration': duration,
                        'maintenance_type': mr_data.get('maintenance_type', 'corrective'),
                        'priority': mr_data.get('priority', 2),
                        'stage': mr_data.get('stage', 'new'),
                        'notes': mr_data.get('notes', ''),
                        'instructions': mr_data.get('instructions', ''),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created maintenance request: {request.subject}'))
                else:
                    self.stdout.write(f'  - Request already exists: {request.subject}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating maintenance request: {str(e)}'))

        self.stdout.write('\n' + self.style.SUCCESS('✓ Database seeding completed successfully!'))
