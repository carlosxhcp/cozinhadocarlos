import os
import subprocess
import sys

# ==========================================================
# CONFIGURAÇÃO DO BANCO
# ==========================================================

database_url = os.environ.get("DATABASE_URL_UNPOOLED")

if not database_url:
    raise RuntimeError("DATABASE_URL_UNPOOLED não configurada.")

os.environ["DATABASE_URL"] = database_url
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

# ==========================================================
# DIAGNÓSTICO
# ==========================================================

import django
django.setup()

from django.conf import settings
from django.db import connections

print("\n========== DIAGNÓSTICO ==========")

print("Settings:", settings.SETTINGS_MODULE)
print("Banco configurado:", settings.DATABASES)
print("Engine:", settings.DATABASES["default"].get("ENGINE"))

db = connections["default"]

print("Engine da conexão:", db.settings_dict.get("ENGINE"))
print("Backend:", db.__class__.__module__)

print("================================\n")

# ==========================================================
# MIGRAÇÕES
# ==========================================================

subprocess.run(
    [sys.executable, "manage.py", "migrate", "--noinput"],
    check=True,
)

# ==========================================================
# ARQUIVOS ESTÁTICOS
# ==========================================================

subprocess.run(
    [sys.executable, "manage.py", "collectstatic", "--noinput"],
    check=True,
)

print("Build concluído com sucesso!")