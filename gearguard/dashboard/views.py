from django.shortcuts import render
from equipment.models import Equipment
from maintenance.models import MaintenanceRequest
from teams.models import Team


def home(request):
    """Render the dashboard home page with metrics."""
    equipment_count = Equipment.objects.count()
    open_requests = MaintenanceRequest.objects.exclude(stage__in=['repaired', 'scrapped']).count()
    teams_count = Team.objects.count()
    
    context = {
        'equipment_count': equipment_count,
        'open_requests': open_requests,
        'teams_count': teams_count,
    }
    return render(request, 'dashboard/home.html', context)
