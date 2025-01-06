from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Func
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Promotion
from .forms import PromotionForm

class Unaccent(Func):
    function = 'unaccent'
    template = '%(function)s(%(expressions)s)'

@login_required
def promotion_list(request):
    query = request.GET.get('q', '')
    active_filter = request.GET.get('active', '')
    
    promotions = Promotion.objects.all()
    if query:
        promotions = promotions.annotate(
            unaccented_title=Unaccent('title'),
        ).filter(
            Q(unaccented_title__icontains=query)
        )
    if active_filter:
        promotions = promotions.filter(active=(active_filter == 'true'))
        
    paginator = Paginator(promotions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'promotions/promotion_list.html', {'page_obj': page_obj, 'query': query, 'active_filter': active_filter})

@login_required
def create_promotion(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promotion_list')
    else:
        form = PromotionForm()
    return render(request, 'promotions/create_promotion.html', {'form': form})

@login_required
def edit_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    if request.method == 'POST':
        form = PromotionForm(request.POST, instance=promotion, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('promotion_list')
    else:
        form = PromotionForm(instance=promotion, user=request.user)
    return render(request, 'promotions/edit_promotion.html', {'form': form, 'promotion': promotion})

@login_required
def delete_promotion(request, promotion_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You do not have permission to delete promotions.")
    
    promotion = get_object_or_404(Promotion, id=promotion_id)
    if request.method == 'POST':
        promotion.delete()
        return redirect('promotion_list')
    return render(request, 'promotions/delete_promotion.html', {'promotion': promotion})