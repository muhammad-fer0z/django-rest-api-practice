from django.db import models
from authentication.models import User


# Create your models here.
class Income(models.Model):
    source_income = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('OTHER', 'OTHER'),
    ]
    source = models.CharField(max_length=100, choices=source_income)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner) + 's income.'
