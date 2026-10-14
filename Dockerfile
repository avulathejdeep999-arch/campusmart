FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_listings ${SEED_ARGS} && gunicorn campusmart.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]
