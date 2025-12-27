from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, WorkCenter
from .forms import TeamForm


@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/list.html', {'teams': teams})


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/detail.html', {'team': team})


@login_required
def team_create(request):
    """View to create a new team."""
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team created successfully.')
            return redirect('teams:team_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html', {'form': form, 'title': 'New Team'})


@login_required
def team_edit(request, pk):
    """View to edit an existing team."""
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully.')
            return redirect('teams:team_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TeamForm(instance=team)
    return render(request, 'teams/team_form.html', {'form': form, 'title': 'Edit Team'})

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
