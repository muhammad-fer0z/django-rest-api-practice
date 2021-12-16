from django.db import models
from authentication.models import User


# Create your models here.

class Expense(models.Model):
    category_options = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('OTHERS', 'OTHERS')
    ]

    category = models.CharField(choices=category_options, max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner) + 's expense.'
