FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY python/pyproject.toml ./python/pyproject.toml
COPY python/README.md ./python/README.md
COPY python/src ./python/src
RUN python -m pip install --no-cache-dir ./python
ENTRYPOINT ["vyonetix-calc"]
