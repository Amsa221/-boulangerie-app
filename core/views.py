from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Role, UserProfile, Purchase
from .forms import UserRegistrationForm, UserUpdateForm, RoleForm, PurchaseForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

# @login_required
def dashboard(request):
    # Statistiques pour le tableau de bord
    total_users = User.objects.count()
    active_users = UserProfile.objects.filter(is_active=True).count()
    total_purchases = Purchase.objects.count()
    total_purchase_amount = Purchase.objects.aggregate(total=Sum('total_price'))['total'] or 0
    
    # Achats des 30 derniers jours
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_purchases = Purchase.objects.filter(purchase_date__gte=thirty_days_ago)
    recent_purchase_amount = recent_purchases.aggregate(total=Sum('total_price'))['total'] or 0
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_purchases': total_purchases,
        'total_purchase_amount': total_purchase_amount,
        'recent_purchase_amount': recent_purchase_amount,
        'recent_purchases': recent_purchases[:5],
    }
    return render(request, 'core/dashboard.html', context)

# @login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'core/user_list.html', {'users': users})

# @login_required
def user_create(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Utilisateur créé avec succès.')
        return redirect('user_list')
    return render(request, 'core/user_form.html', {'form': form, 'title': 'Créer un utilisateur'})

# @login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserUpdateForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Utilisateur mis à jour avec succès.')
        return redirect('user_list')
    return render(request, 'core/user_form.html', {'form': form, 'title': 'Modifier un utilisateur'})

# @login_required
def role_list(request):
    roles = Role.objects.all()
    return render(request, 'core/role_list.html', {'roles': roles})

# @login_required
def role_create(request):
    form = RoleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Rôle créé avec succès.')
        return redirect('role_list')
    return render(request, 'core/role_form.html', {'form': form, 'title': 'Créer un rôle'})

# @login_required
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=role)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Rôle mis à jour avec succès.')
        return redirect('role_list')
    return render(request, 'core/role_form.html', {'form': form, 'title': 'Modifier un rôle'})

# @login_required
def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'core/purchase_list.html', {'purchases': purchases})

# @login_required
def purchase_create(request):
    form = PurchaseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        purchase = form.save(commit=False)
        purchase.created_by = request.user if request.user.is_authenticated else None
        purchase.save()
        messages.success(request, 'Achat enregistré avec succès.')
        return redirect('purchase_list')
    return render(request, 'core/purchase_form.html', {'form': form, 'title': 'Enregistrer un achat'})

# @login_required
def purchase_update(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    form = PurchaseForm(request.POST or None, instance=purchase)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Achat mis à jour avec succès.')
        return redirect('purchase_list')
    return render(request, 'core/purchase_form.html', {'form': form, 'title': 'Modifier un achat'})

# Désactiver la vue register (inscription)
# def register(request):
#     ...
