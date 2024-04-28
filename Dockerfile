FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py makemigrations pedido
RUN python manage.py makemigrations usuario
RUN python manage.py makemigrations producto
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
