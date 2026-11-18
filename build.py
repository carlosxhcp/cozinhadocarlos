import os
import subprocess
import sys

# ==========================================================
# CONFIGURAÇÃO DO BANCO
# ==========================================================

database_url = os.environ.get("DATABASE_URL_UNPOOLED")

if not database_url:
    raise RuntimeError("DATABASE_URL_UNPOOLED não configurada na Vercel.")

os.environ["DATABASE_URL"] = database_url

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"
)

# ==========================================================
# MIGRAÇÕES
# ==========================================================

print("Verificando configuração do banco de dados...")

subprocess.run(
    [sys.executable, "manage.py", "check"],
    check=True,
)

subprocess.run(
    [sys.executable, "manage.py", "migrate", "--noinput"],
    check=True,
)

print("Migrações executadas com sucesso!")

# ==========================================================
# ARQUIVOS ESTÁTICOS
# ==========================================================

subprocess.run(
    [sys.executable, "manage.py", "collectstatic", "--noinput"],
    check=True,
)

print("Arquivos estáticos coletados com sucesso!")