from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import StyledUserCreationForm
from .models import UserProfile


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


@login_required(login_url='accounts:login')
def profile(request):
	"""Display user profile with all details."""
	try:
		user_profile = request.user.userprofile
	except UserProfile.DoesNotExist:
		user_profile = UserProfile.objects.create(user=request.user)
	
	context = {
		'user_profile': user_profile
	}
	return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def profile_edit(request):
	"""Edit user profile information."""
	try:
		user_profile = request.user.userprofile
	except UserProfile.DoesNotExist:
		user_profile = UserProfile.objects.create(user=request.user)
	
	if request.method == 'POST':
		user_profile.full_name = request.POST.get('full_name', user_profile.full_name)
		user_profile.phone = request.POST.get('phone', user_profile.phone)
		user_profile.role = request.POST.get('role', user_profile.role)
		
		if 'avatar' in request.FILES:
			user_profile.avatar = request.FILES['avatar']
		
		user_profile.save()
		messages.success(request, 'Profile updated successfully!')
		return redirect('accounts:profile')
	
	# Pre-calculate role choices to avoid template comparison syntax errors
	role_options = []
	for value, label in UserProfile.ROLE_CHOICES:
		role_options.append({
			'value': value,
			'label': label,
			'selected': (value == user_profile.role)
		})

	context = {
		'user_profile': user_profile,
		'role_options': role_options
	}
	return render(request, 'accounts/profile_edit_v2.html', context)
