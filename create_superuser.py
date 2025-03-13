import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Substitua pelo nome do seu projeto
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Pegando as credenciais do superusuário das variáveis de ambiente
DJANGO_SU_NAME = os.getenv('DJANGO_SUPERUSER_NAME', 'admin')
DJANGO_SU_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
DJANGO_SU_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Verifica se já existe um superusuário com o mesmo e-mail
if not User.objects.filter(username=DJANGO_SU_NAME).exists():
    User.objects.create_superuser(DJANGO_SU_NAME, DJANGO_SU_EMAIL, DJANGO_SU_PASSWORD)
    print("Superusuário criado com sucesso!")
else:
    print("Superusuário já existe. Nenhuma ação necessária.")
