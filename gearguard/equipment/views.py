from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Equipment
from .forms import EquipmentForm


@login_required
def equipment_list(request):
	items = Equipment.objects.all()
	return render(request, 'equipment/list.html', {'equipment_list': items})


@login_required
def equipment_detail(request, pk):
	obj = get_object_or_404(Equipment, pk=pk)
	return render(request, 'equipment/detail.html', {'equipment': obj})


@login_required
def equipment_create(request):
	"""View to create a new equipment."""
	if request.method == 'POST':
		form = EquipmentForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Equipment created successfully.')
			return redirect('equipment:equipment_list')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{field}: {error}')
	else:
		form = EquipmentForm()
	return render(request, 'equipment/equipment_form.html', {'form': form, 'title': 'New Equipment'})


@login_required
def equipment_edit(request, pk):
	"""View to edit an existing equipment."""
	equipment = get_object_or_404(Equipment, pk=pk)
	if request.method == 'POST':
		form = EquipmentForm(request.POST, instance=equipment)
		if form.is_valid():
			form.save()
			messages.success(request, 'Equipment updated successfully.')
			return redirect('equipment:equipment_list')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{field}: {error}')
	else:
		form = EquipmentForm(instance=equipment)
	return render(request, 'equipment/equipment_form.html', {'form': form, 'title': 'Edit Equipment'})
	
@login_required
def equipment_scrap(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    equipment.status = 'scrapped'   # must exist in model choices
    equipment.save()

    messages.warning(request, 'Equipment marked as scrapped.')
    return redirect('equipment:equipment_detail', pk=pk)
