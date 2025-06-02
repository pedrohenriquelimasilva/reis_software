# Usando imagem oficial do Python 3.12 (multi-arquitetura, suporta ARM64)
FROM python:3.12-slim

# Desabilita as prompts interativas no apt-get e configura o fuso horário
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

# Atualiza repositórios e instala pacotes necessários
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  tzdata \
  postgresql-server-dev-all \
  libpq-dev \
  gcc \
  # Caso seu projeto precise compilar extensões em C, python3-dev ajuda
  python3-dev \
  # Após instalar, removemos o cache de pacotes para deixar a imagem menor
  && rm -rf /var/lib/apt/lists/*

# Instalamos o Poetry
RUN pip install --no-cache-dir poetry

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências do Poetry
COPY pyproject.toml poetry.lock* /app/

# Se você quiser que o Poetry crie o ambiente virtual *dentro* do container,
# mas sem venv isolado, use:
RUN poetry config virtualenvs.create false

# Instala dependências do Poetry (sem reinstalar o "root package")
RUN poetry install --no-root --no-interaction

# Copia o restante do seu código para /app
COPY . /app

# Expõe a porta 8000 (onde rodará o Uvicorn/FastAPI)
EXPOSE 8000

# Por fim, comando de execução:
CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
