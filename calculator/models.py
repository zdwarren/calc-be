from django.db import models

class CalculationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    SUCCESS = 'success', 'Success'
    ERROR = 'error', 'Error'

class Calculation(models.Model):
    expression = models.TextField()
    result = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=CalculationStatus.choices,
        default=CalculationStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)  # Nullable as it starts as null
    finished_at = models.DateTimeField(null=True, blank=True)  # Nullable for the same reason
