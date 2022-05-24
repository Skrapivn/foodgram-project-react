FROM python:3.7-slim

WORKDIR /app

COPY ./ ./

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]

LABEL author='skrapivn' version='1.0' description='API foodgram'