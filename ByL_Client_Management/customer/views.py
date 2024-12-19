from django.shortcuts import render
from django.http import HttpResponse
from .models import customer

# Create your views here.
def customer_list(request):
    customers = customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})