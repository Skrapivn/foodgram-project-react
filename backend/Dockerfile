FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ ./

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]

LABEL author='skrapivn' version='1.1' description='API foodgram'