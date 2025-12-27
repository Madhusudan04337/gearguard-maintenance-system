from django.db import models


class WorkCenter(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    capacity_efficiency = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    oee_target = models.DecimalField(max_digits=5, decimal_places=2, default=90.00)

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    work_center = models.ForeignKey(WorkCenter, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
