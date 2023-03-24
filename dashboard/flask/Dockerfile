FROM python:3.9

WORKDIR /app

ADD requirements.txt /app
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt
ENV ANSIBLE_HOST_KEY_CHECKING=False

ADD . /app

CMD ["uwsgi", "app.ini"]
