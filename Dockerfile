FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1

COPY ./app /code/app

CMD ["uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "80"]