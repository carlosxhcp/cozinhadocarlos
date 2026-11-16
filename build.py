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

# Coleta os arquivos estáticos para produção.
subprocess.run(
    [sys.executable, "manage.py", "collectstatic", "--noinput"],
    check=True,
)

print("Arquivos estáticos coletados com sucesso!")