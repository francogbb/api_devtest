# api_devtest

**Proyecto de prueba para desarrollo y especialización con Django + Poetry**

Este repositorio contiene una aplicación Django estructurada con entorno virtual gestionado por [Poetry].

---

## 📁 Estructura del proyecto
´´´
    📦api_devtest
    ┣ 📂api_devtest 
    ┃ ┣ 📂apps (apps de Django)
    ┃ ┣ 📂config (configuraciones de Django)
    ┃ ┃ ┣ 📂django
    ┃ ┃ ┃ ┣ 📜base.py
    ┃ ┃ ┃ ┣ 📜local.py
    ┃ ┃ ┃ ┗ 📜production.py
    ┃ ┃ ┣ 📂settings (configuraciones de dependencias externas ej: AWS S3)
    ┃ ┃ ┣ 📜asgi.py
    ┃ ┃ ┣ 📜env.py
    ┃ ┃ ┣ 📜urls.py
    ┃ ┃ ┗ 📜wsgi.py
    ┃ ┣ 📂static (archivos estáticos)
    ┃ ┃ ┣ 📂css
    ┃ ┃ ┣ 📂img
    ┃ ┃ ┗ 📂js
    ┃ ┣ 📜manage.py
    ┃ ┗ 📜__init__.py
    ┣ 📜.env.dist
    ┗ 📜CHANGELOG.md
    ┣ 📜poetry.lock
    ┣ 📜pyproject.toml
    ┗ 📜README.md
´´´