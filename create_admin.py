from django.contrib.auth import get_user_model

User = get_user_model()
username = "Admin"
password = "MotDePasseUltraSecurise123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superutilisateur créé !")
else:
    print("Le superutilisateur existe déjà.")