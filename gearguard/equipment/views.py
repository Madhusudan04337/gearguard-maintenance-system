from django.shortcuts import render, get_object_or_404
from .models import Equipment


def equipment_list(request):
	items = Equipment.objects.all()
	return render(request, 'equipment/list.html', {'equipment_list': items})


def equipment_detail(request, pk):
	obj = get_object_or_404(Equipment, pk=pk)
	return render(request, 'equipment/detail.html', {'equipment': obj})
