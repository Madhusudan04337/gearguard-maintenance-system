from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import StyledUserCreationForm


def logout_view(request):
	"""Log out the user and redirect to the login page with a message."""
	logout(request)
	messages.success(request, 'You have been logged out.')
	return redirect('accounts:login')


def register(request):
	if request.method == 'POST':
		form = StyledUserCreationForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			messages.success(request, 'Account created — you can now log in.')
			return redirect('accounts:login')
	else:
		form = StyledUserCreationForm()
	return render(request, 'accounts/register.html', {'form': form})
