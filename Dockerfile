FROM python:latest
MAINTAINER Dave Davis
WORKDIR /feed-flipper
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]