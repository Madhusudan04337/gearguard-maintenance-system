from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm

@login_required
def maintenance_list(request):
    """View to list all maintenance requests."""
    items = MaintenanceRequest.objects.all().order_by('-request_date')
    return render(request, 'maintenance/list.html', {'requests': items})

@login_required
def maintenance_create(request):
    """View to create a new maintenance request."""
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.created_by = request.user
            maintenance_request.save()
            messages.success(request, 'Maintenance request created successfully.')
            return redirect('maintenance_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/form.html', {'form': form, 'title': 'New Maintenance Request'})

@login_required
def maintenance_edit(request, pk):
    """View to edit an existing maintenance request."""
    obj = get_object_or_404(MaintenanceRequest, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance request updated.')
            return redirect('maintenance_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = MaintenanceRequestForm(instance=obj)
    return render(request, 'maintenance/form.html', {'form': form, 'title': 'Edit Request'})
