from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Func
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Customer
from .forms import CustomerForm

class Unaccent(Func):
    function = 'unaccent'
    template = '%(function)s(%(expressions)s)'

@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    active_filter = request.GET.get('active', '')
    
    customers = Customer.objects.all().order_by('created_at')
    
    if query:
        customers = customers.annotate(
            unaccented_name=Unaccent('name'),
            unaccented_email=Unaccent('email'),
        ).filter(
            Q(unaccented_name__icontains=query) |
            Q(unaccented_email__icontains=query) |
            Q(phone__icontains=query)
        )
    if active_filter:
        customers = customers.filter(active=(active_filter == 'true'))
        
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'customers/customer_list.html', {'page_obj': page_obj, 'query': query, 'active_filter': active_filter})

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/create_customer.html', {'form': form})

@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer, user=request.user)
    return render(request, 'customers/edit_customer.html', {'form': form, 'customer': customer})

@login_required
def delete_customer(request, customer_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You do not have permission to delete customers.")
    
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/delete_customer.html', {'customer': customer})