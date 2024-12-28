FROM python:3.12.8-bullseye

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy plik z zależnościami
COPY requirements.txt /app/

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy pozostałe pliki aplikacji
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
