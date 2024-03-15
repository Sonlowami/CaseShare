FROM python:3.13.0a4-alpine

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN python3 -m venv case_env
RUN source case_env/bin/activate
RUN pip install -r requirements.txt

COPY ./static /app
COPY ./templates /app
COPY ./app.py /app

CMD [ "python3", './app.py' ]