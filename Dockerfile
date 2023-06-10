FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /Firststep

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 4000

CMD ["python", "manage.py", "runserver"]