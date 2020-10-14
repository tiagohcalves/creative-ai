FROM python:3.8-slim

RUN apt update && \
    apt install -y python3-dev gcc

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD models /opt/quest-generator/models
ADD src /opt/quest-generator/src

#EXPOSE 5000
WORKDIR /opt/quest-generator

# Start the server
CMD python src/app.py
