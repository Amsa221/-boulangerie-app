from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Role, UserProfile, Purchase

class XOFInput(forms.NumberInput):
    def format_value(self, value):
        if value is None:
            return ''
        return f"{value:.0f}".replace('.', ',')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Adresse e-mail", required=True)
    first_name = forms.CharField(label="Prénom", max_length=30, required=True)
    last_name = forms.CharField(label="Nom", max_length=30, required=True)
    phone = forms.CharField(label="Téléphone", max_length=20, required=False)
    role = forms.ModelChoiceField(label="Rôle", queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': "Nom d'utilisateur",
            'password1': "Mot de passe",
            'password2': "Confirmation du mot de passe",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone']
            )
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse e-mail", required=True)
    first_name = forms.CharField(label="Prénom", max_length=30, required=True)
    last_name = forms.CharField(label="Nom", max_length=30, required=True)
    phone = forms.CharField(label="Téléphone", max_length=20, required=False)
    role = forms.ModelChoiceField(label="Rôle", queryset=Role.objects.all(), required=True)
    is_active = forms.BooleanField(label="Actif", required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                profile = self.instance.userprofile
                self.fields['phone'].initial = profile.phone
                self.fields['role'].initial = profile.role
                self.fields['is_active'].initial = profile.is_active
            except UserProfile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['phone']
            profile.role = self.cleaned_data['role']
            profile.is_active = self.cleaned_data['is_active']
            profile.save()
        return user

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('name', 'description')
        labels = {
            'name': "Nom",
            'description': "Description",
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('name', 'category', 'quantity', 'unit_price', 'supplier', 'purchase_date')
        labels = {
            'name': "Nom",
            'category': "Catégorie",
            'quantity': "Quantité",
            'unit_price': "Prix unitaire (FCFA)",
            'supplier': "Fournisseur",
            'purchase_date': "Date d'achat",
        }
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'unit_price': XOFInput(attrs={'step': '1', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        }

    def clean_unit_price(self):
        price = self.cleaned_data['unit_price']
        if price < 0:
            raise forms.ValidationError("Le prix ne peut pas être négatif")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError("La quantité ne peut pas être négative")
        return quantity 