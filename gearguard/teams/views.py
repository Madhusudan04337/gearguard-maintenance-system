from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team, WorkCenter


@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/list.html', {'teams': teams})


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/detail.html', {'team': team})

@login_required
def workcenter_list(request):
    """View to list all work centers."""
    items = WorkCenter.objects.all()
    return render(request, 'teams/workcenter_list.html', {'workcenters': items})

@login_required
def workcenter_detail(request, pk):
    """View to see details of a specific work center."""
    obj = get_object_or_404(WorkCenter, pk=pk)
    return render(request, 'teams/workcenter_detail.html', {'workcenter': obj})
