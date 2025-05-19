FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir --default-timeout=100

COPY . .

CMD sh -c "python manage.py migrate --noinput && \
           gunicorn service.wsgi:application --bind 0:8000"