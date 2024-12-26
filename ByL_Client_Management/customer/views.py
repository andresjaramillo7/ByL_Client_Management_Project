from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import customer
from .forms import CustomerForm

# Create your views here.
def customer_list(request):
    customers = customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/create_customer.html', {'form': form})