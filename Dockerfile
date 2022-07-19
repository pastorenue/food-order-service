FROM python:3.8
ENV PYTHONUNBUFFERED 1


WORKDIR /backend_api

COPY ./requirements.txt ./requirements.txt
RUN pip install install -Ur ./requirements.txt

COPY . .

EXPOSE 8005
