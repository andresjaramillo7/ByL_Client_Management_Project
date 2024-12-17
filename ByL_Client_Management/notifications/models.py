from django.db import models

class communication_history(models.Model):
    customer = models.ForeignKey('customer.customer', on_delete=models.CASCADE)
    promotion = models.ForeignKey('promotions.promotion', on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Sent') # Values: Sent, Failed, Read
    
    def __str__(self):
        return f'{self.customer.name} - {self.promotion.title}'