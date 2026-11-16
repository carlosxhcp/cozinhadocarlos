import os
import subprocess
import sys

# Usa a conexão direta do Neon durante as migrações.
database_url = os.environ.get("DATABASE_URL_UNPOOLED")

if not database_url:
    raise RuntimeError(
        "A variável DATABASE_URL_UNPOOLED não foi configurada na Vercel."
    )

os.environ["DATABASE_URL"] = database_url

# Executa as migrações do Django.
subprocess.run(
    [sys.executable, "manage.py", "migrate", "--noinput"],
    check=True,
)

print("Migrações executadas com sucesso!")
