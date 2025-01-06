from django.db import models
from promotions.models import Promotion

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True, blank=False, null=False)
    address = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    promotions = models.ManyToManyField(Promotion, related_name='customers')

    def __str__(self):
        return self.name