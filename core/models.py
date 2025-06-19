from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.Model):
    name = models.CharField("Nom", max_length=100, unique=True)
    description = models.TextField("Description", blank=True)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Date de modification", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="Utilisateur", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, verbose_name="Rôle", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField("Actif", default=True)
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Date de modification", auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name if self.role else 'Sans rôle'}"

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

class Purchase(models.Model):
    CATEGORY_CHOICES = [
        ('raw_material', 'Matière première'),
        ('equipment', 'Équipement'),
        ('other', 'Autre'),
    ]

    name = models.CharField("Nom", max_length=200)
    category = models.CharField("Catégorie", max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.DecimalField("Quantité", max_digits=10, decimal_places=2)
    unit_price = models.DecimalField("Prix unitaire", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("Prix total", max_digits=10, decimal_places=2)
    supplier = models.CharField("Fournisseur", max_length=200)
    purchase_date = models.DateField("Date d'achat")
    created_by = models.ForeignKey(User, verbose_name="Créé par", on_delete=models.CASCADE)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Date de modification", auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"
