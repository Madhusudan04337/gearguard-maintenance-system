from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
	ROLE_CHOICES = [
		('admin', 'Admin'),
		('manager', 'Manager'),
		('technician', 'Technician'),
	]

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=200, blank=True)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True)
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	team = models.ForeignKey('teams.Team', null=True, blank=True, on_delete=models.SET_NULL)
	work_center = models.ForeignKey('teams.WorkCenter', null=True, blank=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.full_name or getattr(self.user, 'username', str(self.user))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance, email=getattr(instance, 'email', ''))
	else:
		try:
			profile = instance.userprofile
			if profile.email != getattr(instance, 'email', ''):
				profile.email = getattr(instance, 'email', '')
				profile.save()
		except UserProfile.DoesNotExist:
			UserProfile.objects.create(user=instance, email=getattr(instance, 'email', ''))
