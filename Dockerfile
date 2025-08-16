FROM python:3.13-alpine

# Configuración máquina
RUN apk update && apk add --no-cache \
    build-base \
    libpq \
    pkgconfig \
    mysql-dev \
    mariadb-connector-c-dev \
    python3-dev \
    curl 

# Instalación Poetry
RUN pip install --upgrade pip
RUN pip install poetry

RUN mkdir /app

# Directorio de trabajo
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY pyproject.toml poetry.lock README.md /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "python", "api_devtest/manage.py", "runserver", "0.0.0.0:8000"]