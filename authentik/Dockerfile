FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=your_project.settings

CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
