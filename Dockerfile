FROM python:3.7.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /app