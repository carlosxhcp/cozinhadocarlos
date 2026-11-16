import os
import subprocess
import sys
import django

# Utiliza a conexão direta do Neon
database_url = os.environ.get("DATABASE_URL_UNPOOLED")

if not database_url:
    raise RuntimeError("DATABASE_URL_UNPOOLED não configurada.")

os.environ["DATABASE_URL"] = database_url
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Executa as migrações
subprocess.run(
    [sys.executable, "manage.py", "migrate", "--noinput"],
    check=True,
)

print("Migrações executadas com sucesso!")

# Cria o primeiro administrador somente quando solicitado
if os.environ.get("CREATE_SUPERUSER") == "1":
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.environ["DJANGO_SUPERUSER_USERNAME"]
    email = os.environ["DJANGO_SUPERUSER_EMAIL"]
    password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        print("Superusuário criado com sucesso!")
    else:
        print("Esse administrador já existe.")
