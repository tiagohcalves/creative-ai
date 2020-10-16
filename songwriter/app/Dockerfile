FROM python:3.8-slim

RUN apt update && \
    apt install -y python3-dev gcc

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD data /opt/song-space/data
ADD src /opt/song-space/src

#EXPOSE 5000
WORKDIR /opt/song-space/src

# Start the server
CMD python app.py
