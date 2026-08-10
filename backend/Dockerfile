FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY --chown=app:app . .

RUN mkdir -p /app/media /app/staticfiles && chown -R app:app /app/media /app/staticfiles

USER app

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]

CMD ["sh", "-c", "exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --threads ${GUNICORN_THREADS:-2} --timeout ${GUNICORN_TIMEOUT:-60} --control-socket ${GUNICORN_CONTROL_SOCKET:-/tmp/gunicorn.ctl} --access-logfile - --error-logfile -"]
